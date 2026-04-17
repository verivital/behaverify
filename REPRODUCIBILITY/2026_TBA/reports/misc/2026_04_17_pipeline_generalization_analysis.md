# Pipeline Generalization Analysis: Grid World vs. ACAS Xu

**Date:** 2026-04-17

**Scope:** Structural comparison of the two existing compositional verification
pipelines to identify what can be lifted into a shared `2026_TBA/pipeline/` layer
and what must remain example-specific.

---

## Overview

Both examples implement the same conceptual pipeline:

```
contract generation → NN verification (CROWN) → SMV construction → nuXmv → report
```

However, the two implementations diverged significantly in how they were built.
Grid world has a clean `pipeline/` subfolder that already approximates a general
module; ACAS Xu embeds most pipeline logic inline in a single orchestrator script.

---

## Stage-by-Stage Comparison

### Stage 1 — Contract Generation

Both examples have a dedicated `generate_*_contracts.py` script that produces a
contract spec JSON. The output schema differs between examples but shares the same
outer structure: `{"contracts": [{id, status, ...}]}`.

| | Grid World | ACAS Xu |
|---|---|---|
| Script | `generate_grid_world_contracts.py` | `generate_acas_contracts.py` |
| Method | Enumerate obstacle-direction pairs | Physics simulation + dangerous-pair grouping |
| Output | Per-contract dict with source, obstacle, forbidden direction | Per-contract dict with heading, signs, bounding box, `dangerous_xy` |
| Pre-computed? | No — generated at run time | Yes — stored in `contract_specs_eps1e4.json` |

**Verdict: Fully example-specific.** The physics and domain knowledge differ too
much for a shared generator.

---

### Stage 2 — NN Verification (CROWN)

Both examples call alpha-beta-CROWN for each contract. The contract spec drives
what region CROWN receives; the CROWN invocation pattern itself is identical.

| | Grid World | ACAS Xu |
|---|---|---|
| Script | `verify_grid_world_contracts.py` | `verify_acas_contracts.py` |
| Continuous mode | Bounding box over ownship × goal range | Bounding box over `(x_mag, y_mag)` dangerous pairs |
| Discrete mode | 49 integer goal points per contract | One exact point per `dangerous_xy` state |
| Short-circuit | N/A | Yes — UNSAT exits inner loop immediately |
| Retry support | No | Yes — `--retry-from` flag |
| Output schema | `{contracts: [{status, wall_sec, ...}]}` | `{contracts: [{status, wall_sec, ...}]}` |

**Verdict: Example-specific verification scripts, but a shared CROWN invocation
helper is extractable.** The logic that builds `lower`/`upper` arrays and calls
`run_crown_verification()` is essentially the same; only the input-space
construction differs.

---

### Stage 3 — SMV Construction

This is the most significant structural divergence between the two pipelines.

**Grid World — direct injection:**
`pipeline/convert_contracts_to_smv.py` calls `dsl_with_contracts_to_nuxmv()`,
which generates the SMV and injects INVAR constraints in a single pass. The SMV
variable names are passed as parameters (`neural_var`, `pos_x`, `pos_y`, `domain`).

**ACAS Xu — base SMV + post-hoc patch:**
`run_acas_compositional_pipeline.py` uses a three-substep approach:
1. Generate `acas_360.smv` from the tree (full NN lookup tables included)
2. Strip the 5 NN lookup-table DEFINE blocks via regex
3. Inject INVAR constraints after the `SPECIFICATIONS` marker

The ACAS patch step hardcodes 7 SMV variable names directly in the script:

```python
SMV_COMMAND_PREV  = "command_stage_0"
SMV_COMMAND_FINAL = "command_stage_5"
SMV_X_VAR         = "x_var_stage_0"
SMV_Y_VAR         = "y_var_stage_0"
SMV_X_MULT        = "x_mult_stage_0"
SMV_Y_MULT        = "y_mult_stage_0"
SMV_HEADING       = "heading_own_var_stage_0"
```

It also hardcodes two DSL marker strings used to locate insertion points in the
raw SMV text, and hardcodes the 5-advisory domain and the `range(1, 6)` loop over
NNs.

**Verdict: The SMV construction step cannot be shared as-is.** The two approaches
are architecturally different (single-pass generation vs. base + patch). The ACAS
approach should eventually move its hardcoded variable names and domain into a
config file, but this does not need to happen before the generalization refactor.

---

### Stage 4 — nuXmv Invocation

Nearly identical in both examples.

| | Grid World | ACAS Xu |
|---|---|---|
| Module | `pipeline/run_nuxmv_verification.py` | Inline in `run_acas_compositional_pipeline.py` |
| Subprocess call | `[nuXmv, -source, cmd_file, smv_path]` | Same |
| Verdict parsing | Regex: `-- invariant .+ is (true|false)` | Same regex |
| CTL support | Yes (`-- specification .+ is (true|false)`) | No |
| Returns | `{wall_sec, peak_rss_kb, returncode, invarspec, ctlspec}` | `{wall_sec, peak_rss_kb, returncode, invarspec}` |

**Verdict: `pipeline/run_nuxmv_verification.py` is already general-purpose.**
ACAS Xu could use it as-is (CTL fields would just be `None`).

---

### Stage 5 — Report Writing

| | Grid World | ACAS Xu |
|---|---|---|
| Module | `pipeline/write_pipeline_report.py` | Inline in `run_acas_compositional_pipeline.py` |
| Output format | `{network, onnx_path, timestamp, steps, total_wall_sec, verdict}` | `{timestamp, contracts_path, steps, total_wall_sec, verdict}` |
| Console output | Formatted via `_print_summary()` | Inline print statements |

**Verdict: `pipeline/write_pipeline_report.py` is fully general-purpose.**
It takes an arbitrary `steps` dict and writes structured JSON. The ACAS inline
version is a strict subset of its functionality.

---

## Configuration Structure

Grid world externalizes both example config (`grid_world_config.yaml`) and pipeline
config (`pipeline_config.yaml`). ACAS Xu has `verify_acas_contracts_config.yaml`
for CROWN verification but no pipeline config — paths and SMV variable names are
hardcoded in the orchestrator.

A generalized `pipeline/` layer should standardize on a pipeline config schema
that covers: nuXmv binary path, command file path, metamodel path, and a
checker-agnostic output spec (INVAR only vs. INVAR + CTL).

---

## Generalizability Verdict

| Module | Location | General-purpose? | Action |
|---|---|---|---|
| `resolve_pipeline_paths.py` | `grid_world/pipeline/` | Yes | Move to `pipeline/` as-is |
| `run_nuxmv_verification.py` | `grid_world/pipeline/` | Yes | Move to `pipeline/` as-is |
| `write_pipeline_report.py` | `grid_world/pipeline/` | Yes | Move to `pipeline/` as-is |
| `__init__.py` | `grid_world/pipeline/` | Yes | Move to `pipeline/` |
| `convert_contracts_to_smv.py` | `grid_world/pipeline/` | No — calls grid-specific `dsl_with_contracts_to_nuxmv()` params | Keep in `grid_world/`, refactor interface |
| CROWN invocation helper | Both `verify_*.py` files | Partially | Extract to `pipeline/neuro/alpha-beta-CROWN/` |
| SMV patching logic | `run_acas_compositional_pipeline.py` | No — hardcoded variable names | Keep in `AcasXu_closed_loop/`, move config to YAML |
| Contract generation | Both `generate_*.py` files | No | Keep in example folders |

---

## Recommended `2026_TBA/pipeline/` Structure

```
2026_TBA/pipeline/
├── __init__.py
├── write_pipeline_report.py          # lifted from grid_world/pipeline/ as-is
├── resolve_pipeline_paths.py         # lifted from grid_world/pipeline/ as-is
├── crown/                            # alpha-beta-CROWN verifier (shortened from alpha-beta-CROWN)
│   └── crown_verification.py         # shared CROWN invocation helper (lower/upper construction, timeout handling, result schema)
├── nnv/                              # placeholder for NNV verifier
└── symbolic/                         # one subdirectory per symbolic checker
    ├── nuxmv/
    │   └── run_nuxmv_verification.py # lifted from grid_world/pipeline/ as-is
    └── uclid5/                       # placeholder for UCLID5
```

NN verifier directories (`crown/`, `nnv/`) and symbolic checker directories
(`symbolic/nuxmv/`, `symbolic/uclid5/`) are kept at separate levels because the
two stages are orthogonal — any NN verifier can pair with any symbolic checker.
A config toggle (`nn_verifier: crown`, `symbolic_checker: nuxmv`) selects the
active modules at runtime.

Tool names are lowercased and hyphen-free to avoid quoting in shell scripts.

---

## `contracts/` and `results/` Layout

### `contracts/`

Contracts are the output of NN verification only — there is no symbolic equivalent.
The NN verifier is encoded in the directory name. Within that, the existing
`continuous_goals/` vs `discrete_goals/` and `enabled_pgd/` vs `disabled_pgd/`
hierarchy is preserved.

```
contracts/
├── crown/
│   ├── continuous_goals/
│   │   ├── enabled_pgd/
│   │   │   └── <name>_crown_results.json
│   │   └── disabled_pgd/
│   │       └── <name>_crown_results.json
│   └── discrete_goals/
│       └── <name>_crown_results.json
└── nnv/                              # placeholder
```

### `results/`

Results encode both the NN verifier and the symbolic checker. The experimental
condition (`monolithic` vs `compositional`, `continuous` vs `discrete`, PGD flag)
is captured by the directory path; the tool pair is captured by the report filename.

```
results/
├── monolithic/
│   └── <checker>_report.json         # e.g. nuxmv_report.json
└── compositional/
    ├── continuous_goals/
    │   └── enabled_pgd/
    │       └── crown_nuxmv_report.json     # tool pair in filename
    └── discrete_goals/
        └── crown_nuxmv_report.json
```

**Filename convention:** `<nn_verifier>_<symbolic_checker>_report.json`

Examples:
- `crown_nuxmv_report.json` — current default
- `crown_uclid5_report.json` — future UCLID5 run on same contracts
- `nnv_nuxmv_report.json` — hypothetical NNV + nuXmv run

This allows multiple tool-pair results to coexist in the same directory without
collision, making cross-tool comparisons straightforward.

### Report file content

The report JSON itself should also record the tools used:

```json
{
  "nn_verifier": "crown",
  "symbolic_checker": "nuxmv",
  "mode": "compositional",
  "contract_mode": "continuous",
  "pgd_enabled": true,
  ...
}
```

This makes the file self-describing independent of its path.

---

## Example Folder Layouts (post-refactor)

### `AcasXu_closed_loop/`

```
AcasXu_closed_loop/
├── figures/                          # UNCHANGED — visualizations and figure scripts
├── networks/                         # UNCHANGED — ONNX network files
├── tree/                             # UNCHANGED — generated .tree file
├── symbolic/                         # NEW — replaces smv/; checker-specific intermediate files
│   ├── smv/                          #   nuXmv: base SMV + patched SMV
│   └── ucl/                          #   UCLID5: future .ucl input files
├── contracts/                        # RESTRUCTURED — was contracts/continuous_goals/ etc.
│   └── crown/
│       ├── continuous_goals/
│       │   ├── enabled_pgd/
│       │   └── disabled_pgd/
│       └── discrete_goals/
├── results/                          # RESTRUCTURED — report filenames encode tool pair
│   ├── monolithic/
│   │   └── nuxmv_report.json
│   └── compositional/
│       ├── continuous_goals/
│       │   └── enabled_pgd/
│       │       └── crown_nuxmv_report.json
│       └── discrete_goals/
│           └── crown_nuxmv_report.json
├── generate_acas_contracts.py        # UNCHANGED — ACAS-specific contract enumeration
├── generate_acas_tree.py             # UNCHANGED — ACAS-specific tree generation
├── verify_acas_contracts.py          # REFACTORED — thin wrapper; ACAS input-space construction only; delegates to pipeline/crown/
├── verify_acas_contracts_parallel.py # REFACTORED — same; preserves lazy per-process imports
├── run_acas_compositional_pipeline.py# REFACTORED — ACAS SMV patching only; delegates nuXmv + report to pipeline/symbolic/nuxmv/ and pipeline/
├── run_acas_monolithic_pipelines.sh  # PATHS UPDATED — no logic change
├── verify_all_discrete_contracts.sh  # PATHS UPDATED — no logic change
├── verify_all_continuous_contracts.sh# PATHS UPDATED — no logic change
├── verify_acas_contracts_config.yaml # UPDATED — hardcoded SMV variable names moved here from run_acas_compositional_pipeline.py
└── acas_model_params.yaml            # UNCHANGED — physics constants
```

**Key script changes:**
- `verify_acas_contracts.py` and its parallel variant become thin wrappers. All CROWN invocation, config building, status normalization, and result JSON writing move to `pipeline/crown/crown_verification.py`. These scripts retain only ACAS-specific input space construction (`compute_nn_inputs`, `dangerous_xy` iteration).
- `run_acas_compositional_pipeline.py` retains ACAS-specific SMV patching logic (strip NN tables, inject INVARs) but delegates nuXmv invocation to `pipeline/symbolic/nuxmv/run_nuxmv_verification.py` and report writing to `pipeline/write_pipeline_report.py`.
- Hardcoded SMV variable names (`command_stage_0`, `x_var_stage_0`, etc.) move from the Python script into `verify_acas_contracts_config.yaml`.

---

### `grid_world/`

```
grid_world/
├── figures/                          # UNCHANGED — visualizations and figure scripts
├── networks/                         # UNCHANGED — ONNX network files
├── pipeline/                         # DELETED — modules lifted to 2026_TBA/pipeline/
├── contracts/                        # RESTRUCTURED — was contracts/continuous_goals/ etc.
│   └── crown/
│       ├── continuous_goals/
│       │   ├── enabled_pgd/
│       │   └── disabled_pgd/
│       └── discrete_goals/
├── results/                          # RESTRUCTURED — report filenames encode tool pair
│   ├── monolithic/
│   │   └── crown_nuxmv_report.json
│   └── compositional/
│       ├── continuous_goals/
│       │   └── enabled_pgd/
│       │       └── crown_nuxmv_report.json
│       └── discrete_goals/
│           └── crown_nuxmv_report.json
├── generate_grid_world_contracts.py  # UNCHANGED — grid-specific contract enumeration
├── verify_grid_world_contracts.py    # REFACTORED — thin wrapper; grid input-space construction only; delegates to pipeline/crown/
├── run_compositional_pipeline.py     # REFACTORED — delegates SMV generation, nuXmv, report to pipeline/
├── run_all_compositional_pipelines.sh# PATHS UPDATED — no logic change
├── run_all_monolithic_pipelines.sh   # PATHS UPDATED — no logic change
├── verify_continuous_pgd_contracts.sh# PATHS UPDATED — no logic change
├── verify_continuous_bab_contracts.sh# PATHS UPDATED — no logic change
├── verify_discrete_contracts.sh      # PATHS UPDATED — no logic change
├── grid_world_config.yaml            # UNCHANGED — grid bounds, obstacles, verification params
└── pipeline_config.yaml              # UPDATED — paths reflect new structure; nuxmv_cmd points to commands/nuxmv_commands/
```

**Key script changes:**
- `grid_world/pipeline/` is deleted. Its three general-purpose modules (`run_nuxmv_verification.py`, `write_pipeline_report.py`, `resolve_pipeline_paths.py`) move to `2026_TBA/pipeline/symbolic/nuxmv/` and `2026_TBA/pipeline/` respectively. `convert_contracts_to_smv.py` stays in `grid_world/` (grid-specific SMV generation parameters).
- `verify_grid_world_contracts.py` becomes a thin wrapper mirroring the ACAS refactor: grid-specific input space construction only, CROWN invocation delegated to `pipeline/crown/`.
- `run_compositional_pipeline.py` delegates nuXmv and report stages to shared pipeline modules.

---

## Pipeline Module Ownership Summary

| Module | Owner | Delegates to |
|---|---|---|
| Contract enumeration | Example (`generate_*.py`) | — |
| CROWN invocation | `pipeline/crown/crown_verification.py` | called by `verify_*.py` wrappers |
| SMV generation/patching | Example (`run_*_pipeline.py`) | — |
| nuXmv invocation | `pipeline/symbolic/nuxmv/run_nuxmv_verification.py` | called by `run_*_pipeline.py` |
| Report writing | `pipeline/write_pipeline_report.py` | called by `run_*_pipeline.py` |
| Path resolution | `pipeline/resolve_pipeline_paths.py` | called by `run_*_pipeline.py` |

---

## Notes on the ACAS Xu SMV Patching Approach

The ACAS approach (generate base SMV → strip NN tables → inject INVARs) is more
broadly applicable than the grid world approach (contracts injected during
generation) because it works on any pre-existing SMV without requiring a
`dsl_with_contracts_to_nuxmv()` variant. Future examples should adopt it as the
standard patching strategy. Moving the hardcoded SMV variable names to a config
file is a prerequisite for this.

Since the patch step produces a modified `.smv` file, switching from nuXmv to
UCLID5 only requires changing the checker invocation stage — the patched model
can be post-processed into whatever input format the new checker expects.
