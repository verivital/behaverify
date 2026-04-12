# ACAS Xu Refactoring Plan

**Date:** 2026-04-10

**Goal:** Refactor `REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop/` to match the
`grid_world/` directory structure, then add discrete (EPS=0.0) contract support mirroring
what was done for grid world.

**Status at time of writing:**
- ONNX files in `networks/` have already been renamed (e.g., `ACASXU_run2a_1_1_batch_2000.onnx`
  → `aprev_clear.onnx`). All references updated across scripts, JSONs, tree files, and README.
- `networks/README.md` has been written with the legacy name cross-reference table.
- `results/pgd_unsat_report.md` is a duplicate of
  `reports/Acas_Xu_closed_loop/2026_03_25_pgd_unsat_acas_report.md` and should be deleted
  (see Phase 4).

---

## Current Directory State (before remaining refactor)

```
AcasXu_closed_loop/
├── acasxu_template_360.tree       # Template — handle_360.py reads this
├── handle_360.py                  # Generates tree/acasxu_360.tree from template
├── networks/                      # 5 ONNX files (already renamed)
│   ├── aprev_clear.onnx
│   ├── aprev_weak_right.onnx
│   ├── aprev_weak_left.onnx
│   ├── aprev_strong_right.onnx
│   ├── aprev_strong_left.onnx
│   └── README.md                  # Already written
├── contracts/
│   ├── acas_contract_specs.json   # Spec file (eps=1e-4, continuous) — 2.5MB
│   └── acas_verified_nn1.json     # CROWN results for NN1, PGD-enabled
├── verify_acas_contracts.yaml     # CROWN config (network_idx, timeout, output_path)
├── verify_acas_contracts.py       # Verifies contracts via CROWN (single process)
├── verify_acas_parallel.py        # Parallel wrapper for verify_acas_contracts.py
├── generate_acas_contracts.py     # Generates acas_contract_specs.json (no CROWN)
├── run_acas_pipeline.py           # End-to-end: tree→SMV→patch→nuXmv
├── results/
│   ├── compositional/nn1/         # Pipeline output for NN1
│   │   ├── acasxu_360_contracts.smv
│   │   ├── nuxmv_output.txt
│   │   └── pipeline_report.json
│   └── pgd_unsat_report.md        # DUPLICATE — delete this (canonical copy in reports/)
├── smv/
│   └── acasxu_360.smv             # Generated base SMV (reused via --skip-smv)
├── tree/
│   └── acasxu_360.tree            # Generated tree (reused via --skip-tree)
├── invar.txt                      # Stale nuXmv output from early run — DELETE
└── README.md                      # Exists but needs updating after refactor
```

---

## Phase 1 — `contracts/` reorganization

**Goal:** Mirror grid_world's `continuous_goals/` / `discrete_goals/` split.

The eps is baked into the contract spec JSON at generation time, so continuous and discrete
need separate spec files. `acas_contract_specs.json` was generated with eps=1e-4 (continuous).

**Target structure:**
```
contracts/
├── continuous_goals/
│   ├── acas_contract_specs.json        # MOVE from contracts/ (eps=1e-4)
│   ├── enabled_pgd/
│   │   └── nn1_crown_results.json      # MOVE+RENAME from contracts/acas_verified_nn1.json
│   └── disabled_pgd/                   # empty for now
└── discrete_goals/
    └── acas_contract_specs.json        # TO GENERATE with eps=0.0 (future)
```

**Steps:**
1. `mkdir -p contracts/continuous_goals/enabled_pgd contracts/continuous_goals/disabled_pgd`
2. `mkdir -p contracts/discrete_goals`
3. Move `contracts/acas_contract_specs.json` → `contracts/continuous_goals/acas_contract_specs.json`
4. Move `contracts/acas_verified_nn1.json` → `contracts/continuous_goals/enabled_pgd/nn1_crown_results.json`
5. Update path references in:
   - `verify_acas_contracts.yaml` (`contracts_path` and `output_path` fields)
   - `verify_acas_parallel.py` (hardcoded path in docstring/usage: `contracts/acas_verified_nn1.json`)
   - `run_acas_pipeline.py` (default `--contracts` and `--spec` argument help strings and defaults)
   - `README.md` (all path references)

**IMPORTANT:** `acas_contract_specs.json` has `"onnx"` paths stored per contract (already
updated to new names). The JSON structure is: top-level `contracts` array, each entry has
`"network_idx"`, `"onnx"`, `"nn_input_lower"`, `"nn_input_upper"`, etc.

---

## Phase 2 — `results/` reorganization

**Goal:** Mirror grid_world's mode-organized results structure.

**Target structure:**
```
results/
└── compositional/
    ├── continuous_goals/
    │   └── enabled_pgd/
    │       └── nn1/                # MOVE from results/compositional/nn1/
    │           ├── acasxu_360_contracts.smv
    │           ├── nuxmv_output.txt
    │           └── pipeline_report.json
    └── discrete_goals/             # empty — for upcoming discrete runs
```

**Steps:**
1. `mkdir -p results/compositional/continuous_goals/enabled_pgd`
2. `mkdir -p results/compositional/discrete_goals`
3. Move `results/compositional/nn1/` → `results/compositional/continuous_goals/enabled_pgd/nn1/`
4. Update path references in `README.md`

---

## Phase 3 — Script renaming (DESIGN-02)

**Goal:** Names should be self-explanatory at 2AM without opening the file.

| Current name | New name | Reason |
|---|---|---|
| `run_acas_pipeline.py` | `run_acas_compositional_pipeline.py` | Matches grid_world naming |
| `verify_acas_contracts.yaml` | `acas_config.yaml` | Matches `grid_world_config.yaml` |
| `verify_acas_parallel.py` | `verify_acas_contracts_parallel.py` | Makes relationship to `verify_acas_contracts.py` explicit |

**Steps:**
1. Rename the three files above
2. Update `verify_acas_contracts.py` — it defaults to `"verify_acas_contracts.yaml"` at line ~43:
   ```python
   def load_config(path: str = "verify_acas_contracts.yaml") -> dict[str, Any]:
   ```
   → change default to `"acas_config.yaml"`
3. Update `verify_acas_contracts_parallel.py` — its usage docstring references
   `verify_acas_contracts.yaml` → update to `acas_config.yaml`
4. Update `README.md` — all script name references

---

## Phase 4 — Cleanup, additions, and README update

### Deletions
- **Delete `results/pgd_unsat_report.md`** — duplicate of
  `reports/Acas_Xu_closed_loop/2026_03_25_pgd_unsat_acas_report.md`
- **Delete `invar.txt`** — stale nuXmv output from early exploratory run on machine
  "serenegrace", not part of any pipeline

### Additions
- **Add `run_all_continuous_pipelines.sh`** — batch wrapper that runs
  `run_acas_compositional_pipeline.py` for all 5 NNs using continuous_goals contracts.
  Mirror `run_all_compositional_pipelines.sh` from grid_world. Structure:
  ```bash
  #!/usr/bin/env bash
  # run_all_continuous_pipelines.sh
  # Batch: run compositional pipeline for all 5 ACAS Xu NNs (continuous contracts, PGD-enabled)
  _HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  PYTHON="${PYTHON:-python3}"
  CONTRACTS_DIR="${_HERE}/contracts/continuous_goals/enabled_pgd"
  OUT_DIR="${_HERE}/results/compositional/continuous_goals/enabled_pgd"
  # loop over nn1..nn5
  ```

### README update
After all phases complete, rewrite `README.md` to reflect the new structure. Key sections:
- Updated directory tree (matching new layout)
- Updated all script names
- Updated all contract/result paths
- Add blockquote explaining why compositional has more output folders (same as grid_world)
- Note that `smv/` and `tree/` are intentional intermediate artifact dirs (--skip-smv/--skip-tree)

---

## Phase 5 — Discrete contracts (EPS=0.0)

**This is the new feature, done after the refactor is complete.**

Mirrors `grid_world/contracts/discrete_goals/` which uses `DISCRETE_GOAL_EPS = 0.0`.

In ACAS Xu, "discrete" means EPS=0.0 in `generate_acas_contracts.py --eps 0.0`, producing
tighter bounding boxes (exact convex hull of dangerous state NN inputs, no margin).

**Steps:**
1. Run `python generate_acas_contracts.py --eps 0.0 --output contracts/discrete_goals/acas_contract_specs.json`
2. Verify contracts: add `--mode discrete` flag (or separate config) to `verify_acas_contracts.py`
   so it reads from `contracts/discrete_goals/acas_contract_specs.json`
3. Run pipeline per NN, write results to `results/compositional/discrete_goals/nn{1..5}/`
4. Compare discrete vs continuous SAT/UNSAT counts — expect discrete to have more SAT
   (tighter boxes = easier to verify, potentially fewer violations)
5. Add `run_all_discrete_pipelines.sh` batch script

**Key question to answer:** Does EPS=0.0 resolve the 221 UNSAT contracts for NN1?
In grid_world, discrete mode showed INVAR=true for 100%-accurate NNs. If the same holds
for ACAS Xu NN1, it means the violations are at non-exact-state floating-point inputs
(analogous to non-integer goal positions in grid_world), not at the actual discrete system
states. That would be a meaningful result.

---

## Path reference checklist

When updating paths, grep for these strings to find all occurrences:
- `contracts/acas_contract_specs.json`
- `contracts/acas_verified_nn1.json`
- `results/compositional/nn1`
- `run_acas_pipeline.py`
- `verify_acas_contracts.yaml`
- `verify_acas_parallel.py`

Run after each phase to verify nothing was missed:
```bash
grep -r "acas_verified_nn1\|run_acas_pipeline\|verify_acas_contracts\.yaml\|verify_acas_parallel\b\|compositional/nn1\b\|contracts/acas_contract_specs" \
    REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop/
```
