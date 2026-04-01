# Grid World Compositional Verification

1-NN grid world example: 7x7 grid, 18 obstacles, 38 A/G contracts.
Each contract asserts that the NN never moves the drone into a specific obstacle
from the adjacent cell, for all continuous goal positions in [0, 6]².

For setup (BehaVerify, nuXmv, alpha-beta-CROWN), see the
[root README](../../README.md).

---

## Layout

```
grid_world/
├── networks/              # 7 ONNX files (0995, 0996, 1000 x 5 neuron counts)
├── contracts/
│   ├── disabled_pgd/      # BaB-only results (pre-PGD baseline, 4 networks)
│   └── enabled_pgd/       # PGD-enabled results (SAT/UNSAT, zero timeouts, 5 networks)
├── results/               # Pipeline reports and PGD analysis
├── verify_contracts.py    # A/G contract verification via alpha-beta-CROWN
├── verify_contracts.yaml  # Config: grid bounds, EPS, timeout, ONNX path
├── run_pgd_1000_contracts.sh  # Batch PGD runner for five 100%-accurate NNs
├── run_compositional_pipeline.py  # End-to-end compositional pipeline
├── counter_template.tree      # Tree template used by run_compositional_pipeline.py
│                              #   when --tree is not provided (auto-generates a .tree)
└── inspect_onnx.py        # Utility for inspecting NN architecture
```

---

## Running the Compositional Pipeline

All commands below assume you are in `grid_world/`:

```bash
cd REPRODUCIBILITY/2026_TBA/examples/grid_world
source /path/to/behaverify_venv/bin/activate
```

**This is required.** Both `run_compositional_pipeline.py` and `dsl_to_nuxmv.py`
resolve paths relative to the current working directory.

### Quick Start (using pre-computed contracts)

Note: `--skip-contracts` bypasses `verify_contracts.py` entirely — the pre-computed
JSON is used directly. PGD only matters when re-running contract verification from scratch.

```bash
# Unsafe network (0995, ~99.5% accuracy) -- expect INVAR=false
python run_compositional_pipeline.py \
    --onnx networks/0995__6_18_0__200_1.onnx \
    --output results/compositional/0995 \
    --skip-contracts \
    --contracts contracts/disabled_pgd/0995__6_18_0__200_1.json

# 100%-accurate network, BaB-only contracts -- expect INVAR=false (UNSAT contracts)
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/1000__0100_bab \
    --skip-contracts \
    --contracts contracts/disabled_pgd/1000__6_18_0__0100_1.json

# 100%-accurate network, PGD contracts -- expect INVAR=false (genuine UNSAT)
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/1000__0100_pgd \
    --skip-contracts \
    --contracts contracts/enabled_pgd/1000__6_18_0__0100_1_pgd60.json
```

Each run produces a `pipeline_report.json` in the output directory with per-step
wall time, peak memory, contract counts, and nuXmv verdict.

### Full Pipeline (re-verifying contracts via CROWN)

Re-run contract verification with PGD enabled (recommended):

```bash
python verify_contracts.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output contracts/enabled_pgd/1000__6_18_0__0100_1_pgd60.json
```

Then run the pipeline:

```bash
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/1000__0100 \
    --contracts contracts/enabled_pgd/1000__6_18_0__0100_1_pgd60.json
```

### Batch PGD Run (all five 100%-accurate NNs)

```bash
./run_pgd_1000_contracts.sh
```

Results are saved to `contracts/enabled_pgd/<name>_pgd60.json`.

---

## Interpreting Results

| Field | Meaning |
|---|---|
| `steps.contracts.sat` | Number of A/G contracts verified SAT by CROWN |
| `steps.contracts.unsat` | Contracts with genuine safety violations (PGD found counterexample) |
| `steps.contracts.timeout` | Contracts that timed out (inconclusive) |
| `steps.smv_generation.wall_sec` | Time to generate contract-injected SMV |
| `steps.nuxmv_verification.invarspec` | `"true"` = invariant holds, `"false"` = counterexample found |
| `verdict` | Combined INVAR + CTL result |

**Important:** With PGD enabled, UNSAT contracts are genuine safety violations — the
NN moves the drone into an obstacle for some continuous input in the contract region.
The invariant is only meaningful when all 38 contracts are SAT; any UNSAT contract
means the abstraction is unsound and `invarspec=false` reflects a real property failure.

For 100%-accurate NNs, UNSAT contracts arise from continuous goal positions outside
the discrete training distribution — see `results/pgd_unsat_report.md` for analysis.

---

## Common Issues

### Compositional pipeline gives INVAR=false for a 100%-accurate network

Two distinct causes — check `steps.contracts` in `pipeline_report.json`:

- **UNSAT contracts (PGD enabled):** genuine safety violations. The NN produces a
  forbidden move for some real-valued input in the contract region. This is a real
  finding. See `results/pgd_unsat_report.md`.
- **TIMEOUT contracts (PGD disabled or timeout too low):** abstraction is incomplete.
  Re-run with PGD enabled or increase `timeout_sec` in `verify_contracts.yaml`.

### Doubled path in ONNX loading (e.g., `.../results/compositional/0995//home/...`)

Absolute ONNX paths produce doubled slashes in path concatenation. Always use paths
relative to `grid_world/`. `run_compositional_pipeline.py` handles this automatically
via `os.path.relpath()`.

### nuXmv output has no timing information

Use `command_all_invar` instead of `command_combo_invar_ctl`. The combo command does
not include nuXmv's internal `time` command between steps.

---

## Network Naming Convention

```
{accuracy}__{grid_rows}_{obstacles}_{obs_size}__{neuron_count}_{run}.onnx

Example: 1000__6_18_0__0300_1.onnx
  - 1000  = 100.0% training accuracy (1000/1000 correct)
  - 6     = 6x6 grid (7x7 including borders)
  - 18    = 18 obstacles
  - 0     = obstacle size parameter
  - 0300  = 300 neurons in hidden layer
  - 1     = run index
```

Networks starting with `0995` achieved ~99.5% accuracy and are expected to be
unsafe (invariant fails). Networks starting with `1000` achieved 100% accuracy;
they are discrete-safe but have UNSAT contracts for continuous goal inputs.
