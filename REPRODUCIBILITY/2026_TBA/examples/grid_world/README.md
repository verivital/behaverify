# Grid World Compositional Verification

1-NN grid world example: 7x7 grid, 18 obstacles, 38 A/G contracts.
Each contract asserts that the NN never moves the drone into a specific obstacle
from the adjacent cell, for all continuous goal positions in [0, 6]².

For setup (BehaVerify, nuXmv, alpha-beta-CROWN), see the
[root README](../../README.md).

> **Note:** this pipeline imports BehaVerify from `2026_TBA/src/` directly, not
> from the installed pip package. See the root README for details.

---

## Layout

```
grid_world/
├── networks/              # 7 ONNX files — see networks/README.md for naming convention
├── contracts/             # Pre-computed A/G contracts (CROWN output, JSON)
│   └── crown/
│       ├── continuous_goals/
│       │   ├── enabled_pgd/   # PGD-enabled contracts (SAT/UNSAT, zero timeouts)
│       │   └── disabled_pgd/  # BaB-only contracts (baseline comparison, some timeouts)
│       └── discrete_goals/    # Discrete contracts (eps=0, replicates 2025_NEUS integer-point check)
├── results/
│   ├── compositional/     # Pipeline reports (pipeline_report.json per network per mode)
│   │   ├── continuous_goals/enabled_pgd/
│   │   ├── continuous_goals/disabled_pgd/
│   │   └── discrete_goals/
│   └── monolithic/        # nuXmv output from the 2025_NEUS table approach
├── figures/               # Generated figures and scripts — see figures/README.md
├── generate_grid_world_contracts.py   # Generate contract specs from obstacle config (no CROWN)
├── convert_contracts_to_smv.py        # Convert verified contracts → contract-injected SMV
├── verify_grid_world_contracts.py     # Verify contracts via CROWN (called by the shell script below)
├── verify_grid_world_contracts.sh     # Batch: verify all 7 NNs (--mode and --neuro flags)
├── run_compositional_pipeline.py      # Single-network end-to-end compositional pipeline
├── run_all_compositional_pipelines.sh # Batch: run compositional pipeline for all networks in a contracts folder
├── run_all_monolithic_pipelines.sh    # Batch: run monolithic pipeline for all 7 networks
├── grid_world_domain_config.yaml      # Domain config: grid bounds, obstacles, EPS, timeout
├── pipeline_filepaths_config.yaml     # Pipeline config: tool paths, SMV variable names
└── counter_template.tree              # Tree template for run_compositional_pipeline.py
```

> **Shared pipeline modules** live in `2026_TBA/pipeline/` (not inside `grid_world/`).
> `run_compositional_pipeline.py` imports from there via a `sys.path` insert.
> This keeps NN-verifier logic (`pipeline/neuro/crown/`) and symbolic-checker logic
> (`pipeline/symbolic/nuxmv/`) reusable across both the grid-world and ACAS Xu examples.

> **Why compositional has more output folders than monolithic:**
> Monolithic verification has one configuration — BehaVerify embeds a lookup table, nuXmv checks it.
> Compositional verification is configurable: you choose the NN verifier (CROWN with PGD, BaB-only,
> or other tools), the contract mode (continuous goals or discrete), and the symbolic checker (nuXmv
> here, but swappable). Each combination produces its own `contracts/` and `results/` subfolder.
> This is by design: the pipeline separates NN verification from symbolic verification so each step
> can be tuned or replaced independently.

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

Note: `--skip-contracts` bypasses `verify_grid_world_contracts.py` entirely — the pre-computed
JSON is used directly. PGD only matters when re-running contract verification from scratch.

```bash
# Unsafe network (0995, ~99.5% accuracy) -- expect INVAR=false
python run_compositional_pipeline.py \
    --onnx networks/0995__6_18_0__200_1.onnx \
    --output results/compositional/continuous_goals/disabled_pgd/0995 \
    --skip-contracts \
    --contracts contracts/crown/continuous_goals/disabled_pgd/0995__6_18_0__200_1.json

# 100%-accurate network, BaB-only contracts -- expect INVAR=false (UNSAT contracts)
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/continuous_goals/disabled_pgd/1000__0100 \
    --skip-contracts \
    --contracts contracts/crown/continuous_goals/disabled_pgd/1000__6_18_0__0100_1.json

# 100%-accurate network, PGD contracts -- expect INVAR=false (genuine UNSAT)
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/continuous_goals/enabled_pgd/1000__0100 \
    --skip-contracts \
    --contracts contracts/crown/continuous_goals/enabled_pgd/1000__6_18_0__0100_1_pgd60.json
```

Each run produces a `pipeline_report.json` in the output directory with per-step
wall time, peak memory, contract counts, and nuXmv verdict.

### Full Pipeline (re-verifying contracts via CROWN)

Re-run contract verification with PGD enabled (recommended):

```bash
python verify_grid_world_contracts.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output contracts/crown/continuous_goals/enabled_pgd/1000__6_18_0__0100_1_pgd60.json
```

> The `_pgd60` suffix reflects `timeout_sec: 60` in `grid_world_domain_config.yaml`.
> `verify_grid_world_contracts.sh` reads this value at runtime, so changing `timeout_sec`
> automatically produces a different suffix (e.g., `_pgd120` for `timeout_sec: 120`).

Then run the pipeline:

```bash
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/continuous_goals/enabled_pgd/1000__0100 \
    --contracts contracts/crown/continuous_goals/enabled_pgd/1000__6_18_0__0100_1_pgd60.json
```

### Batch Verification (all NNs)

All three verification modes (continuous PGD, continuous BaB, discrete) are handled by
the unified `verify_grid_world_contracts.sh` script. The `--neuro` flag sets the NN verifier
name used as the `contracts/<neuro>/` path prefix, making it easy to add future verifiers.

```bash
# PGD-enabled (recommended) → contracts/crown/continuous_goals/enabled_pgd/
./verify_grid_world_contracts.sh

# BaB-only baseline (no PGD) → contracts/crown/continuous_goals/disabled_pgd/
./verify_grid_world_contracts.sh --mode continuous-bab

# Discrete integer-point check → contracts/crown/discrete_goals/
./verify_grid_world_contracts.sh --mode discrete

# Future verifier (nnv) → contracts/nnv/continuous_goals/enabled_pgd/
./verify_grid_world_contracts.sh --neuro nnv
```

---

## PGD Attacks in Contract Verification

**What PGD is:** Projected Gradient Descent (PGD) is an adversarial attack method. Given
a neural network and an input region, PGD repeatedly applies gradient steps to search for
an input in that region that violates the property being checked (e.g., the NN outputs a
forbidden direction). If PGD finds one, the contract is immediately UNSAT — no further
search needed. *(Madry et al., "Towards Deep Learning Models Resistant to Adversarial
Attacks," arXiv:1706.06083, 2017. https://arxiv.org/abs/1706.06083)*

**Why it matters here:** Without PGD, alpha-beta-CROWN falls back entirely to
Branch-and-Bound (BaB), which exhaustively partitions the input space. BaB is complete
(always finds a violation if one exists) but slow — it times out on large or hard
contracts. PGD is fast and incomplete: it may miss violations, but when it succeeds it
produces a concrete counterexample in seconds.

**Practical effect on results:**

| PGD setting | Contract is hard to verify | Result |
|-------------|---------------------------|--------|
| Enabled (`pgd_order=before`) | PGD finds a counterexample | **UNSAT** — genuine violation, fast |
| Enabled (`pgd_order=before`) | PGD finds no counterexample, BaB finishes | **SAT** — verified safe |
| Disabled (BaB only) | BaB times out | **TIMEOUT** — inconclusive |

This is why PGD-enabled runs have zero timeouts for these networks: the contracts that
would time out under BaB-only have genuine counterexamples that PGD finds immediately.
A TIMEOUT is not "safe" — it means verification was inconclusive. Always prefer
PGD-enabled results when reporting safety verdicts.

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
  Re-run with PGD enabled or increase `timeout_sec` in `grid_world_domain_config.yaml`.

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
