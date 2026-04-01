# 2026_TBA/examples Refactoring Report

**Goal:** `2026_TBA/examples` should contain only compositional verification
artifacts. Monolithic verification (full NN lookup tables, direct nuXmv runs) belongs
in `2025_NEUS`. This report lists every tracked file in `grid_world/` and
`AcasXu_closed_loop/` with a KEEP / DELETE / BORDERLINE verdict and rationale.

**Dependency check:** No compositional script (`verify_contracts.py`,
`run_compositional_pipeline.py`, `run_acas_pipeline.py`, `generate_acas_contracts.py`)
imports or shell-invokes any of the monolithic scripts listed for deletion. The one
apparent reference (`draw_network.py CODES` in `verify_contracts.py`) is a comment,
not an import.

---

## `examples/grid_world/`

### KEEP — Compositional pipeline

| File / Directory | Reason |
|---|---|
| `verify_contracts.py` | CROWN contract verification script (core compositional tool) |
| `verify_contracts.yaml` | CROWN config: grid bounds, EPS, timeout, ONNX path |
| `run_pgd_1000_contracts.sh` | Batch script for PGD runs across all 5 x 100%-accurate NNs |
| `run_compositional_pipeline.py` | End-to-end: SMV generation → contract injection → nuXmv |
| `template.tree` | Source template for tree generation; required by pipeline |
| `obstacles_6_18_0.txt` | Obstacle positions; read by contract generation logic |
| `networks/` (7 ONNX files) | Networks used by CROWN: 0995, 0996, 0100, 0150, 0200, 0250, 0300 |
| `contracts/disabled_pgd/` (4 JSONs) | BaB-only baseline results; reference for PGD comparison |
| `contracts/enabled_pgd/` (5 JSONs) | PGD results for all five 100%-accurate NNs |
| `results/` | Timing results and compositional pipeline outputs |
| `inspect_onnx.py` | Utility for inspecting NN architecture; not imported but useful |

### DELETE — Monolithic verification

| File / Directory | Reason |
|---|---|
| `command.sh` | Generates monolithic SMVs via `make_smv.sh`; pure monolithic |
| `make_smv.sh` | Calls `dsl_to_nuxmv.py` on all tree files; monolithic |
| `make_tree.sh` | Generates tree files used by `make_smv.sh`; only serves monolithic |
| `run_smv.sh` | Runs nuXmv directly on monolithic SMVs |
| `run_smv_all.sh` | Batch version of `run_smv.sh` |
| `time_make_smv.sh` | Times monolithic SMV generation |
| `smv/` (21 SMV files) | All `fixed_100_35_*`, `fixed_140_48_*`, `float_140_*`, `table_*` SMVs; monolithic generated artifacts |
| `tree/` (30 tree files) | Generated tree files for all NN variants; intermediate artifacts not needed for compositional |
| `networks_all/` (25 ONNX files) | Extended NN set not used by the compositional scripts; `networks/` (7 files) covers what's needed |
| `networks_pth/` (25 PTH files) | PyTorch checkpoint files; CROWN uses ONNX only, these serve no compositional purpose |
| `counter_1.smv`, `counter_2.smv` | Counter-example SMVs; unrelated to grid world compositional pipeline |
| `counter_template.tree` | Template for counter examples; same |
| `ctl_counter.txt`, `invar_counter.txt` | Counter verification results |
| `sim_small_20.txt` | Simulation trace; monolithic artifact |
| `images/` (6 PNGs) | Network visualizations; useful visually but not needed for pipeline |
| `Example.tree` | Scratch example tree; not used anywhere |

---

## `examples/AcasXu_closed_loop/`

### KEEP — Compositional pipeline

| File / Directory | Reason |
|---|---|
| `generate_acas_contracts.py` | Generates range-based A/G contracts from physics simulation |
| `verify_acas_contracts.py` | CROWN contract verification (PGD-enabled) |
| `verify_acas_contracts.yaml` | CROWN config: network index, timeout, paths |
| `verify_acas_parallel.py` | Parallel CROWN runner for HPC use |
| `run_acas_pipeline.py` | End-to-end: tree → SMV → contract injection → nuXmv |
| `handle_360.py` | Generates `acasxu_360.tree` from `acasxu_template_360.tree` |
| `acasxu_template_360.tree` | Primary template for the 5-NN 360° closed-loop model |
| `tree/acasxu_360.tree` | Pre-generated tree (committed for `--skip-tree` convenience) |
| `contracts/acas_contract_specs.json` | Pre-computed range-based contract specs (490 contracts) |
| `contracts/acas_verified_nn1.json` | CROWN results for NN_1: 269 SAT, 221 UNSAT (PGD) |
| `networks/` (5 ONNX files) | All five ACAS Xu NNs required by CROWN and `run_acas_pipeline.py` |
| `README.md` | Pipeline documentation |
| `results/pgd_unsat_report.md` | Analysis of the 221 TIMEOUT → UNSAT PGD breakthrough |

### DELETE — Monolithic / backup / scratch

| File / Directory | Reason |
|---|---|
| `command.sh` | Generates monolithic `acasxu_360.smv` directly; superseded by `run_acas_pipeline.py` step 2 |
| `time_command.sh` | Times monolithic SMV generation only |
| `translation_time.txt` | Output of `time_command.sh`; monolithic timing artifact |
| `acasxu_template_360_backup.tree` | Backup of template; redundant with git history |
| `acasxu_template_360_FAST.tree` | Alternative template variant; not used in the main pipeline |
| `acasxu_template_720.tree` | 720° variant; not used in any compositional script |
| `handle_360_backup.py` | Backup of `handle_360.py`; redundant with git history |

### BORDERLINE — Discuss before deleting

| File | Case for KEEP | Case for DELETE |
|---|---|---|
| `invar.txt` | Serena's authoritative monolithic baseline (49s, 9.6 GB, INVAR=true on `serenegrace`); the only evidence that monolithic gives a different result than compositional — paper-critical comparison point | Pure monolithic artifact; inconsistent with the "compositional only" rule; lives in `2025_NEUS` more naturally |

**Recommendation:** Keep `invar.txt` with a comment in `README.md` making clear it is
the monolithic reference baseline, not a compositional output. It directly supports the
paper claim that compositional (INVAR=false) and monolithic (INVAR=true) diverge.

---

## `examples/` (top level, outside the two main folders)

### DELETE — Entire `AcasXu/` folder

All files in `examples/AcasXu/` are from the initial single-NN ACAS Xu exploration
phase (`Refactor DESIGN-01` commit, `8217c3103`), predating the closed-loop
compositional pipeline. None are imported or referenced by any current pipeline script.

| Contents | Reason to delete |
|---|---|
| `acasxu_FROZENVAR.tree`, `acasxu_SETPOINT.tree`, `acasxu_SINGLE*.tree` | Single-NN exploration trees; not part of 5-NN closed-loop pipeline |
| `acasxu_SETPOINT.pdf` | Diagram artifact |
| `command.sh`, `time_command.sh` | Monolithic timing scripts |
| `networks/` (5 ONNX files) | Duplicate of `AcasXu_closed_loop/networks/`; same files |
| `timing-*.txt`, `translation_timing.txt` | Monolithic timing results |

### DELETE — Top-level utility scripts

| File | Reason |
|---|---|
| `clean_all.sh` | Cleans generated SMV/tree files; only relevant with monolithic `make_smv.sh` |
| `create_grid.py` | Grid generation utility; not imported by any compositional script |
| `draw_network.py` | Visualization; only a docstring comment reference in `verify_contracts.py`, not imported |
| `draw_output.py` | Visualizes monolithic nuXmv traces |
| `draw_SIMPLE_output.py` | Same |
| `parse_nuxmv_output.py` | Parses monolithic nuXmv output format |
| `parse_SIMPLE_nuxmv_output_stage_FIRST.py` | Monolithic output parsing |
| `parse_SIMPLE_nuxmv_output_stage_LAST.py` | Monolithic output parsing |

---

## Summary Counts

| Category | Files / Dirs | Action |
|---|---|---|
| `grid_world/` keep | 10 entries | — |
| `grid_world/` delete | 15 entries (~120 files including `networks_all/`, `networks_pth/`, `smv/`, `tree/`) | `git rm -r` |
| `AcasXu_closed_loop/` keep | 14 entries | — |
| `AcasXu_closed_loop/` delete | 7 entries | `git rm` |
| `AcasXu_closed_loop/` borderline | 1 (`invar.txt`) | Keep with note |
| `examples/AcasXu/` | Entire folder (~17 files) | `git rm -r` |
| `examples/` top-level scripts | 8 files | `git rm` |

After deletion, `2026_TBA/examples` reduces to two clean folders with no monolithic
artifacts: `grid_world/` (contracts, networks, pipeline) and `AcasXu_closed_loop/`
(contracts, networks, pipeline).
