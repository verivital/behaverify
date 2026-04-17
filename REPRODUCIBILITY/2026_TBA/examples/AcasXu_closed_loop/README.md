# ACAS Xu Closed-Loop Compositional Verification

This directory contains the compositional verification pipeline for a closed-loop,
5-NN ACAS Xu (Airborne Collision Avoidance System X) Neuro-Symbolic Behavior Tree (NSBT).

The ownship selects one of five neural networks based on the previous advisory
(`a_prev`), then applies the chosen advisory to update its heading. The safety
invariant is `distance >= 200` (the aircraft never come within 200 raw units of
each other).

For background, see the NeuS 2025 paper:
> *Neuro-Symbolic Behavior Trees and Their Verification*, Serbinowska et al., 2025.

---

## Quick start — interactive contract explorer

Before running any verification, explore the pre-computed A/G contracts
interactively with the Gradio app. No CROWN or nuXmv needed.

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
pip install gradio          # one-time, if not already installed
python3 figures/image_scripts/acas_contract_explorer.py
# → open http://localhost:7860
```

The app shows a 2×2 dashboard for any selected contract:

| | Left | Right |
|---|---|---|
| **Top** | Original physical state space (signed coordinates, heading arrow, quadrant highlight) | Normalized physical state space (ownship at origin) |
| **Bottom** | NN input space — toggle **Continuous**, **Discrete**, or **Both** modes; drag **eps** slider to grow/shrink the bounding box live | Contract details table (id, heading, quadrant, forbidden advisory, bounding box bounds) |

This is the fastest way to build intuition for what continuous vs. discrete
contract verification actually checks before reading any of the pipeline scripts.
See [`figures/README.md`](figures/README.md) for full app documentation.

---

## Directory Layout

```
AcasXu_closed_loop/
├── networks/                               # 5 ONNX files (see networks/README.md)
├── contracts/
│   └── crown/
│       ├── continuous_goals/
│       │   ├── contract_specs_eps1e4.json        # Pre-computed A/G contract specs (eps=1e-4)
│       │   ├── enabled_pgd/
│       │   │   └── aprev_*_crown_results.json    # CROWN results per NN (PGD-enabled)
│       │   └── disabled_pgd/                     # (empty — future runs)
│       └── discrete_goals/
│           └── aprev_*_crown_results.json        # Discrete CROWN results (eps=0, per NN)
├── results/
│   ├── monolithic/                         # nuXmv output and report for the monolithic run
│   └── compositional/
│       ├── continuous_goals/
│       │   └── enabled_pgd/
│       │       └── aprev_*/                # Pipeline output per NN
│       └── discrete_goals/
│           └── all_nns/                    # Discrete compositional pipeline output (all 5 NNs)
├── symbolic/
│   └── smv/                               # Generated base SMV (reused via --skip-smv)
├── figures/                                # Visualization scripts and outputs
│   ├── image_scripts/
│   │   ├── acas_contract_explorer.py       # Interactive Gradio demo (start here)
│   │   ├── acas_discrete_vs_continuous.py  # Static 3-panel comparison figure
│   │   ├── acas_input_region.py            # Single-contract static figure
│   │   └── acas_output_property.py         # NN output bar charts
│   └── figures/README.md                   # Figure documentation
├── tree/                                   # Generated tree file (reused via --skip-tree)
├── acas_template_360.tree                  # Template for the closed-loop model
├── generate_acas_tree.py                   # Fills in template → tree/acas_360.tree
├── generate_acas_contracts.py              # Enumerate dangerous states → contract specs
├── verify_acas_contracts.py                # Verify contract specs via CROWN (serial)
├── verify_acas_contracts_parallel.py       # Parallel retry wrapper for TIMEOUT contracts
├── verify_acas_contracts_config.yaml       # Config for verify_acas_contracts.py
├── run_acas_compositional_pipeline.py      # End-to-end compositional pipeline (single NN)
├── run_all_continuous_pipelines.sh         # Batch: run compositional pipeline for all NNs
├── run_acas_monolithic_pipelines.sh        # Monolithic vs. discrete compositional benchmark
├── verify_all_continuous_contracts.sh      # Batch: run CROWN for all 5 NNs (continuous)
├── verify_all_discrete_contracts.sh        # Batch: run CROWN for all 5 NNs (discrete)
└── retry_all_discrete.sh                   # Retry TIMEOUT discrete contracts via PGD
```

---

## Prerequisites

### 1. BehaVerify + extra dependencies

Install from the repository root, then add the extras for this pipeline:

```bash
pip install -e .
pip install -r REPRODUCIBILITY/2026_TBA/requirements.txt
```

The extras file currently adds only `gradio` (for the interactive contract explorer).
Everything else (`matplotlib`, `numpy`, `pandas`, `onnxruntime`, `PyYAML`) is already
pulled in by the base `behaverify` install.

### 2. nuXmv 2.1.0

nuXmv cannot be redistributed. Download and extract into `REPRODUCIBILITY/2026_TBA/`:

```bash
wget "https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz" \
    -O nuXmv_DL.tar.xz
tar -xf nuXmv_DL.tar.xz --one-top-level=nuXmv_DL --strip-components 1
chmod +x nuXmv_DL/bin/nuXmv
```

The pipeline defaults to `../../nuXmv_DL/bin/nuXmv` relative to this directory.

### 3. alpha-beta-CROWN (only needed to re-verify contracts)

Pre-computed contract specs and NN_1 verification results are committed in
`contracts/`. You only need CROWN to re-run or extend contract verification.

```bash
cd REPRODUCIBILITY/2026_TBA
git clone https://github.com/Verified-Intelligence/alpha-beta-CROWN alpha-beta-CROWN
pip install -r alpha-beta-CROWN/complete_verifier/requirements/requirements.txt
```

---

## Model Overview

### State variables

| Variable | Domain | Meaning |
|---|---|---|
| `x_mag`, `y_mag` | integers [0, 10] | Position magnitude (× 100 = raw units) |
| `x_sign`, `y_sign` | {−1, +1} | Position sign (quadrant) |
| `heading_own_var` | integers [0, 39] | Ownship heading index (× 9° = degrees) |
| `command` (a_prev) | 5 advisories | Previous advisory; selects which NN runs |

`heading_int` is fixed at 225° and speeds are fixed at 20 (own) and 30 (intruder).

### NN selection

```
a_prev = clear        → NN_1  (aprev_clear.onnx)
a_prev = weak_right   → NN_2
a_prev = weak_left    → NN_3
a_prev = strong_right → NN_4
a_prev = strong_left  → NN_5
```

### Safety invariant

```
INVARSPEC (distance >= 200)
```

where `distance = round(sqrt(x_mag² + y_mag²)) × 100`.

---

## Monolithic Verification (baseline)

The monolithic result (from a reference run):

```
INVARSPEC: true
User time: ~49 seconds
Peak RSS:  ~9.6 GB
```

To regenerate the monolithic SMV and re-verify (from this directory):

```bash
# 1. Generate tree from template
python generate_acas_tree.py

# 2. Generate base SMV
mkdir -p symbolic/smv
python3 -c "
import sys; sys.path.insert(0, '../../src')
import dsl_to_nuxmv as _dsl
_dsl.dsl_to_nuxmv('../../metamodel/behaverify.tx',
    'tree/acas_360.tree', 'symbolic/smv/acas_360.smv',
    False, False, False, False, 10000, False, True, None)
"

# 3. Verify with nuXmv
../../nuXmv_DL/bin/nuXmv \
    -source ../../commands/nuxmv_commands/command_all_invar \
    ./symbolic/smv/acas_360.smv \
    > results/monolithic/nuxmv_output.txt
```

Or use the all-in-one benchmark script (handles tree/SMV generation, monolithic run, discrete
compositional run, and side-by-side summary):

```bash
./run_acas_monolithic_pipelines.sh
./run_acas_monolithic_pipelines.sh --skip-monolithic   # use 2025_NEUS reference result (~9.6 GB RAM)
```

Use `command_all_invar` (not `command_invar`) to get nuXmv's internal timing.
Report **User time** from the output.

---

## Compositional Verification

### Overview

The compositional pipeline has four stages:

```
generate_acas_contracts.py  →  contract specs JSON
verify_acas_contracts.py    →  CROWN verification results JSON
run_acas_compositional_pipeline.py  →  contract-injected SMV  →  nuXmv verdict
```

All commands below assume you are in this directory:

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
```

---

### Step 1 — Generate contract specs

This enumerates all dangerous (state, advisory) pairs and groups them into
range-based A/G contracts (bounding box over `x_mag`, `y_mag` for fixed
`heading_own_var`, sign quadrant, and forbidden advisory).

```bash
python generate_acas_contracts.py
# Output: contracts/crown/continuous_goals/contract_specs_eps1e4.json
# Expected: ~490 contracts for NN_1 (one per non-empty heading/sign/advisory group)
```

This step is fast (~1 minute) and does not require CROWN. The output is
already committed in `contracts/crown/continuous_goals/contract_specs_eps1e4.json`.

---

### Step 2 — Verify contracts via CROWN

#### Pilot run (sanity check before committing to a full run)

```bash
python verify_acas_contracts.py --limit 5
```

Expected output: a mix of SAT (~0.5s each) and TIMEOUT (30s each).

#### Full run for NN_1

Edit `verify_acas_contracts_config.yaml` if you need to change the timeout or output
path. The default is 30s per contract, NN_1 only.

```bash
nohup python verify_acas_contracts.py > results/verify_nn1.log 2>&1 &
```

Expected: ~269 SAT, ~221 TIMEOUT, ~113 minutes total.

#### Second-pass retry (higher timeout for TIMEOUT contracts)

```bash
nohup python verify_acas_contracts.py \
    --retry-from contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json \
    --timeout 60 \
    > results/verify_nn1_retry.log 2>&1 &
```

This re-verifies only the TIMEOUT contracts and merges results into
`contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json`. Worst case: ~3.7 hours.

> **Why two passes?** Contracts either verify in under 1s (large margin) or
> time out quickly (near the NN's decision boundary). A short initial timeout
> (30s) identifies easy contracts cheaply; a second pass at 60s recovers
> borderline ones without wasting time on genuinely hard contracts.

---

### Step 3 — Run the compositional pipeline

Using pre-computed contracts (skip tree/SMV regeneration):

```bash
python run_acas_compositional_pipeline.py \
    --contracts contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json \
    --output    results/compositional/continuous_goals/enabled_pgd/aprev_clear \
    --skip-tree --skip-smv
```

Full pipeline (regenerate tree and SMV from scratch):

```bash
python run_acas_compositional_pipeline.py \
    --contracts contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json \
    --output    results/compositional/continuous_goals/enabled_pgd/aprev_clear
```

Results are written to `results/compositional/continuous_goals/enabled_pgd/aprev_clear/pipeline_report.json`.

---

## Interpreting Results

| Field | Meaning |
|---|---|
| `steps.smv_patch.sat_contracts` | SAT contracts used to inject constraints |
| `steps.smv_patch.invar_lines` | INVAR constraints injected into the patched SMV |
| `steps.smv_patch.nn_lines_removed` | NN lookup-table lines removed from base SMV |
| `steps.nuxmv.invarspec` | `"true"` = invariant holds, `"false"` = counterexample |
| `total_wall_sec` | End-to-end compositional time |

**INVARSPEC=false with TIMEOUT contracts present is almost certainly spurious.**
nuXmv exploits the unconstrained states (from timed-out contracts) to construct
a fake counterexample. The verdict is only meaningful when all 490 contracts are
SAT. This is the same behavior observed in the grid-world example when fewer than
38/38 contracts were verified.

**INVARSPEC=false with 0 UNSAT contracts** confirms the issue is contract
incompleteness, not a real safety violation. If UNSAT contracts appear, the NN
genuinely violates a contract — investigate those cases first.

The monolithic baseline is `true` in ~49s. A compositional run with
complete contracts should also return `true` in significantly less time (the patched
SMV has ~1,600 lines vs. ~9,700 for the monolithic model).

---

## Timeout Sensitivity Experiment

Running the pipeline at multiple timeout levels and recording the SAT rate and
nuXmv verdict is a meaningful experiment for paper evaluation:

```
Timeout | SAT contracts | nuXmv verdict
--------+---------------+---------------
  5s    | ?             | false (spurious)
 15s    | ?             | ?
 30s    | 269           | false (spurious)
 60s    | ?             | ?
120s    | ?             | true (expected)
```

This demonstrates quantitatively how contract completeness affects the
compositional proof — a property invisible to the monolithic approach.

---

## Common Issues

### INVARSPEC=false despite safe NNs

Contract coverage is incomplete. Some TIMEOUT contracts leave holes in the
abstraction that nuXmv uses to find a spurious path. Run the second-pass retry
with a higher timeout. See the grid-world README for the same pattern.

### `verify_acas_contracts.py` gives wrong results with `--retry-from`

The retry merges results by contract `id`. If `contract_specs_eps1e4.json` was
regenerated after the original verification run (changing contract `id`s), the
merge will be incorrect. Always regenerate verification results from scratch if
the spec file changes.

### `generate_acas_tree.py` fails with `FileNotFoundError`

The `tree/` directory must exist before running:

```bash
mkdir -p tree symbolic/smv
python generate_acas_tree.py
```

### Monolithic SMV takes too long or runs out of memory

The monolithic SMV (`symbolic/smv/acas_360.smv`) is ~9,700 lines and contains 5 full
NN lookup tables. nuXmv peak RSS is ~9.6 GB. Ensure at least 12 GB free RAM.
The compositional patched SMV is ~1,600 lines and uses far less memory.

### `run_acas_compositional_pipeline.py` gives `INVARSPEC=None`

Check `results/compositional/continuous_goals/enabled_pgd/aprev_clear/nuxmv_output.txt` for nuXmv error messages.
Common causes: SMV type errors (see `--skip-smv` flag to reuse a known-good
base SMV), or missing nuXmv binary.

---

## Contract Structure

Contracts are **range-based**: for each non-empty group of
`(heading_own_var, x_sign, y_sign, forbidden_advisory)`, a single CROWN call
verifies the property over the bounding box of all dangerous `(x_mag, y_mag)`
states in that group.

This mirrors the grid-world approach where source position was fixed and goal
position ranged continuously. Here, `(heading_own_var, x_sign, y_sign)` is fixed
(determining NN inputs 3–5 exactly) and `(x_mag, y_mag)` ranges over the dangerous
region (determining NN inputs 1–2).

| Grouping | Max contracts per NN | vs. per-state |
|---|---|---|
| Per state | 2,830 | baseline |
| Per heading+sign+advisory (this approach) | ~490 | ~6× reduction |
| Per sign+advisory only | ~100 | ~28× reduction |
