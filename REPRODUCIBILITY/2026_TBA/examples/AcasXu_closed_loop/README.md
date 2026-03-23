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

## Directory Layout

```
AcasXu_closed_loop/
├── networks/
│   ├── ACASXU_run2a_1_1_batch_2000.onnx   # NN_1 (a_prev=clear)
│   ├── ACASXU_run2a_2_1_batch_2000.onnx   # NN_2 (a_prev=weak_right)
│   ├── ACASXU_run2a_3_1_batch_2000.onnx   # NN_3 (a_prev=weak_left)
│   ├── ACASXU_run2a_4_1_batch_2000.onnx   # NN_4 (a_prev=strong_right)
│   └── ACASXU_run2a_5_1_batch_2000.onnx   # NN_5 (a_prev=strong_left)
├── contracts/
│   ├── acas_contract_specs.json            # Pre-computed A/G contract specs
│   └── acas_verified_nn1.json              # CROWN verification results for NN_1
├── tree/                                   # Generated .tree file (gitignored)
├── smv/                                    # Generated base SMV (gitignored)
├── results/                                # Verification outputs (gitignored)
├── acasxu_template_360.tree                # Template for the closed-loop model
├── handle_360.py                           # Fills in template → tree/acasxu_360.tree
├── generate_acas_contracts.py              # Enumerate dangerous states → contract specs
├── verify_acas_contracts.py                # Verify contract specs via CROWN
├── verify_acas_contracts.yaml              # Config for verify_acas_contracts.py
├── run_acas_pipeline.py                    # End-to-end compositional pipeline
├── command.sh                              # Generate monolithic SMV
├── time_command.sh                         # Generate monolithic SMV with timing
└── invar.txt                               # Monolithic nuXmv result (committed)
```

---

## Prerequisites

### 1. BehaVerify

Install from the repository root:

```bash
pip install -e .
```

### 2. nuXmv 2.1.0

nuXmv cannot be redistributed. Download and place the binary at
`REPRODUCIBILITY/2026_TBA/nuXmv/bin/nuXmv` (relative to the repo root):

```bash
wget "https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz" \
    -O nuXmv_DL.tar.xz
tar -xf nuXmv_DL.tar.xz --one-top-level=nuXmv --strip-components 1
chmod +x nuXmv/bin/nuXmv
```

The pipeline defaults to `../../../../nuXmv/bin/nuXmv` relative to this directory.

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
| `x_var`, `y_var` | integers [0, 10] | Position magnitude (× 100 = raw units) |
| `x_mult`, `y_mult` | {−1, +1} | Position sign (quadrant) |
| `heading_own_var` | integers [0, 39] | Ownship heading index (× 9° = degrees) |
| `command` (a_prev) | 5 advisories | Previous advisory; selects which NN runs |

`heading_int` is fixed at 225° and speeds are fixed at 20 (own) and 30 (intruder).

### NN selection

```
a_prev = clear        → NN_1  (ACASXU_run2a_1_1_batch_2000.onnx)
a_prev = weak_right   → NN_2
a_prev = weak_left    → NN_3
a_prev = strong_right → NN_4
a_prev = strong_left  → NN_5
```

### Safety invariant

```
INVARSPEC (distance >= 200)
```

where `distance = round(sqrt(x_var² + y_var²)) × 100`.

---

## Monolithic Verification (baseline)

The committed file `invar.txt` contains the monolithic result:

```
INVARSPEC: true
User time: ~49 seconds
Peak RSS:  ~9.6 GB
```

To regenerate the monolithic SMV and re-verify (from this directory):

```bash
# 1. Generate tree from template
python handle_360.py

# 2. Generate SMV (with timing)
./time_command.sh

# 3. Verify with nuXmv
../../../../nuXmv/bin/nuXmv \
    -source ../../scripts/nuxmv_commands/command_all_invar \
    ./smv/acasxu_360.smv \
    > invar.txt
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
run_acas_pipeline.py        →  contract-injected SMV  →  nuXmv verdict
```

All commands below assume you are in this directory:

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
```

---

### Step 1 — Generate contract specs

This enumerates all dangerous (state, advisory) pairs and groups them into
range-based A/G contracts (bounding box over `x_var`, `y_var` for fixed
`heading_own_var`, sign quadrant, and forbidden advisory).

```bash
python generate_acas_contracts.py
# Output: contracts/acas_contract_specs.json
# Expected: ~490 contracts for NN_1 (one per non-empty heading/sign/advisory group)
```

This step is fast (~1 minute) and does not require CROWN. The output is
already committed in `contracts/acas_contract_specs.json`.

---

### Step 2 — Verify contracts via CROWN

#### Pilot run (sanity check before committing to a full run)

```bash
python verify_acas_contracts.py --limit 5
```

Expected output: a mix of SAT (~0.5s each) and TIMEOUT (30s each).

#### Full run for NN_1

Edit `verify_acas_contracts.yaml` if you need to change the timeout or output
path. The default is 30s per contract, NN_1 only.

```bash
nohup python verify_acas_contracts.py > results/verify_nn1.log 2>&1 &
```

Expected: ~269 SAT, ~221 TIMEOUT, ~113 minutes total.

#### Second-pass retry (higher timeout for TIMEOUT contracts)

```bash
nohup python verify_acas_contracts.py \
    --retry-from contracts/acas_verified_nn1.json \
    --timeout 60 \
    > results/verify_nn1_retry.log 2>&1 &
```

This re-verifies only the TIMEOUT contracts and merges results into
`contracts/acas_verified_nn1.json`. Worst case: ~3.7 hours.

> **Why two passes?** Contracts either verify in under 1s (large margin) or
> time out quickly (near the NN's decision boundary). A short initial timeout
> (30s) identifies easy contracts cheaply; a second pass at 60s recovers
> borderline ones without wasting time on genuinely hard contracts.

---

### Step 3 — Run the compositional pipeline

Using pre-computed contracts (skip tree/SMV regeneration):

```bash
python run_acas_pipeline.py \
    --contracts contracts/acas_verified_nn1.json \
    --output    results/compositional/nn1 \
    --skip-tree --skip-smv
```

Full pipeline (regenerate tree and SMV from scratch):

```bash
python run_acas_pipeline.py \
    --contracts contracts/acas_verified_nn1.json \
    --output    results/compositional/nn1
```

Results are written to `results/compositional/nn1/pipeline_report.json`.

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

The monolithic baseline (`invar.txt`) is `true` in ~49s. A compositional run with
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

The retry merges results by contract `id`. If `acas_contract_specs.json` was
regenerated after the original verification run (changing contract `id`s), the
merge will be incorrect. Always regenerate verification results from scratch if
the spec file changes.

### `handle_360.py` fails with `FileNotFoundError`

The `tree/` directory must exist before running:

```bash
mkdir -p tree smv
python handle_360.py
```

### Monolithic SMV takes too long or runs out of memory

The monolithic SMV (`smv/acasxu_360.smv`) is ~9,700 lines and contains 5 full
NN lookup tables. nuXmv peak RSS is ~9.6 GB. Ensure at least 12 GB free RAM.
The compositional patched SMV is ~1,600 lines and uses far less memory.

### `run_acas_pipeline.py` gives `INVARSPEC=None`

Check `results/compositional/nn1/nuxmv_output.txt` for nuXmv error messages.
Common causes: SMV type errors (see `--skip-smv` flag to reuse a known-good
base SMV), or missing nuXmv binary.

---

## Contract Structure

Contracts are **range-based**: for each non-empty group of
`(heading_own_var, x_mult, y_mult, forbidden_advisory)`, a single CROWN call
verifies the property over the bounding box of all dangerous `(x_var, y_var)`
states in that group.

This mirrors the grid-world approach where source position was fixed and goal
position ranged continuously. Here, `(heading_own_var, x_mult, y_mult)` is fixed
(determining NN inputs 3–5 exactly) and `(x_var, y_var)` ranges over the dangerous
region (determining NN inputs 1–2).

| Grouping | Max contracts per NN | vs. per-state |
|---|---|---|
| Per state | 2,830 | baseline |
| Per heading+sign+advisory (this approach) | ~490 | ~6× reduction |
| Per sign+advisory only | ~100 | ~28× reduction |
