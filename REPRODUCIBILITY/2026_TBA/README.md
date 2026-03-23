# Compositional Verification of Neuro-Symbolic Behavior Trees (NSBTs)

This directory contains the compositional verification pipeline for NSBTs, extending
the monolithic BehaVerify approach with Assume-Guarantee (A/G) contracts verified via
alpha-beta-CROWN.

Current focus: 1-NN grid world example (7x7 grid, 18 obstacles, 38 contracts).

---

## Repository Layout

```
2026_TBA/
├── examples/grid_world/
│   ├── networks/               # ONNX neural network files
│   ├── contracts/              # Pre-computed A/G contracts (JSON)
│   ├── tree/                   # .tree DSL files (monolithic, all encodings)
│   ├── smv/                    # Generated SMV files (gitignored, see below)
│   ├── results/                # Verification outputs (gitignored)
│   ├── counter_template.tree   # Template for auto-generating counter trees
│   ├── run_compositional_pipeline.py  # End-to-end compositional pipeline
│   ├── verify_contracts.py     # A/G contract verification via CROWN
│   ├── verify_contracts.yaml   # Config for verify_contracts.py
│   ├── make_smv.sh             # Generate monolithic SMV files
│   ├── time_make_smv.sh        # Generate monolithic SMVs with timing
│   ├── run_smv.sh              # Run nuXmv on monolithic SMVs
│   └── run_smv_all.sh          # Batch run all encodings
├── metamodel/                  # BehaVerify TextX grammar
├── scripts/nuxmv_commands/     # nuXmv command files
├── src/                        # BehaVerify source (local copy)
└── nuXmv_DL/bin/nuXmv          # nuXmv binary (not committed, see below)
```

---

## Prerequisites

### 1. BehaVerify

Install from the repository root:

```bash
pip install -e .
```

Or with dev dependencies:

```bash
pip install -e .[dev]
```

### 2. nuXmv 2.1.0

nuXmv cannot be redistributed. Download and place the binary at
`REPRODUCIBILITY/2026_TBA/nuXmv_DL/bin/nuXmv`:

```bash
wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz -O nuXmv_DL.tar.xz
tar -xf nuXmv_DL.tar.xz --one-top-level=nuXmv_DL --strip-components 1
# Move the binary to the expected location:
mkdir -p REPRODUCIBILITY/2026_TBA/nuXmv_DL/bin
mv nuXmv_DL/bin/nuXmv REPRODUCIBILITY/2026_TBA/nuXmv_DL/bin/nuXmv
chmod +x REPRODUCIBILITY/2026_TBA/nuXmv_DL/bin/nuXmv
```

### 3. alpha-beta-CROWN (only needed to re-verify contracts)

The pre-computed contracts are already committed in `contracts/`. You only need
CROWN if you want to re-run contract verification from scratch.

Clone CROWN as a subdirectory:

```bash
cd REPRODUCIBILITY/2026_TBA
git clone https://github.com/Verified-Intelligence/alpha-beta-CROWN alpha-beta-CROWN
pip install -r alpha-beta-CROWN/complete_verifier/requirements/requirements.txt
```

---

## Running the Compositional Pipeline

All commands below assume you are in:

```bash
cd REPRODUCIBILITY/2026_TBA/examples/grid_world
```

**This is required.** Both `run_compositional_pipeline.py` and `dsl_to_nuxmv.py`
resolve paths relative to the current working directory. Running from any other
directory will produce path errors.

### Quick Start (using pre-computed contracts)

The `contracts/` directory contains pre-computed A/G contracts for all tested
networks. Use `--skip-contracts` to bypass the CROWN step entirely.

```bash
# Test 1: Unsafe network (0995, ~99.5% accuracy) -- expect INVAR=false
python run_compositional_pipeline.py \
    --onnx networks/0995__6_18_0__200_1.onnx \
    --output results/compositional/0995 \
    --skip-contracts \
    --contracts contracts/0995__6_18_0__200_1.json

# Test 2: Safe network, 100 neurons -- expect INVAR=true (if all contracts SAT)
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/1000__0100 \
    --skip-contracts \
    --contracts contracts/1000__6_18_0__0100_1.json

# Test 3: Safe network, 300 neurons -- expect INVAR=true (if all contracts SAT)
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0300_1.onnx \
    --output results/compositional/1000__0300 \
    --skip-contracts \
    --contracts contracts/1000__6_18_0__0300_1.json
```

Each run produces a `pipeline_report.json` in the output directory with per-step
wall time, peak memory, contract counts, and nuXmv verdict.

### Full Pipeline (re-verifying contracts via CROWN)

To re-run contract verification, edit `verify_contracts.yaml` to point to the
desired network, then run from `grid_world/`:

```bash
python verify_contracts.py
```

Then run the pipeline without `--skip-contracts`:

```bash
python run_compositional_pipeline.py \
    --onnx networks/1000__6_18_0__0100_1.onnx \
    --output results/compositional/1000__0100 \
    --contracts contracts/1000__6_18_0__0100_1.json
```

---

## Running the Monolithic Pipeline (for comparison)

### Generate SMV files

```bash
# With timing (writes results/timing_*.txt per tree):
./time_make_smv.sh python

# Without timing:
./make_smv.sh python
```

This generates `smv/` files for all trees in `tree/`. The `smv/` directory is
gitignored and must be regenerated locally.

### Run nuXmv verification

```bash
# All 1000-family networks, table encoding, with nuXmv internal timing:
./run_smv.sh table \
    "../../nuXmv_DL/bin/nuXmv -source ../../scripts/nuxmv_commands/command_all_invar" \
    timing_table

# 0995 network (not covered by run_smv.sh -- run manually):
../../nuXmv_DL/bin/nuXmv \
    -source ../../scripts/nuxmv_commands/command_all_invar \
    ./smv/table_0995__6_18_0__200_1.smv \
    > ./results/timing_table_0995.txt
```

Results are saved to `results/`. Report **User time** from the nuXmv output for
verification timing.

---

## Interpreting Results

| Field | Meaning |
|---|---|
| `steps.contracts.sat` | Number of A/G contracts verified SAT by CROWN |
| `steps.contracts.timeout` | Contracts that timed out (inconclusive) |
| `steps.smv_generation.wall_sec` | Time to generate contract-injected SMV |
| `steps.nuxmv_verification.invarspec` | `"true"` = invariant holds, `"false"` = counterexample found |
| `verdict` | Combined INVAR + CTL result |

**Important:** If contracts timed out, `invarspec=false` may be a spurious
counterexample caused by an incomplete abstraction, not a real safety violation.
The invariant is only meaningful when all 38 contracts are SAT.

For the monolithic results, `User time` in the nuXmv output (from `command_all_invar`)
is the verification time. SMV generation time is in `results/timing_*.txt` from
`time_make_smv.sh`.

---

## Common Issues

### "Permission denied" when running `make_smv.sh`

The script requires a Python interpreter as its first argument:

```bash
./make_smv.sh python          # uses system python
./make_smv.sh python3         # or explicit python3
```

Running `./make_smv.sh` without arguments leaves `$python` empty, causing bash
to try to execute the `.py` file directly.

### Doubled path in ONNX loading (e.g., `.../results/compositional/0995//home/...`)

Both `dsl_to_nuxmv.py` and CROWN join paths via string concatenation, not
`os.path.join`. Absolute ONNX paths produce doubled slashes. Always use paths
**relative to the current working directory** (`grid_world/`) or relative to the
tree file's parent directory. `run_compositional_pipeline.py` handles this
automatically via `os.path.relpath()`.

### Compositional pipeline gives INVAR=false for a safe network

This means some contracts timed out and the abstraction is too coarse. The SMV
model allows the NN to make moves it wouldn't actually make, giving nuXmv a
spurious counterexample. Re-run `verify_contracts.py` with a higher
`timeout_sec` in `verify_contracts.yaml` to get more SAT contracts.

### `run_smv.sh` only handles the `1000` network family

The script loops over neuron counts `{0100, 0150, 0200, 0250, 0300}` and
hardcodes the `_1000__6_18_0__0` filename pattern. The `0995` network must be
run manually (see above).

### nuXmv output has no timing information

Use `command_all_invar` instead of `command_combo_invar_ctl`. The combo command
does not include nuXmv's internal `time` command between steps.

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
unsafe (the invariant should fail). Networks starting with `1000` achieved 100%
accuracy and are expected to be safe.
