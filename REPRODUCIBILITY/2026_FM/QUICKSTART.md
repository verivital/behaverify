# FM 2026 Reproducibility - Quick Start Guide

This guide provides the fastest path to reproducing FM 2026 results.
For detailed explanations, see [README.md](README.md).

---

## Prerequisites

1. **Docker** installed and running (user can run without sudo)
2. **Python 3** with the `docker` package:
   ```bash
   pip install docker
   ```

---

## Two-Step Reproduction

### Step 1: Set Up Docker Environment

```bash
cd REPRODUCIBILITY/2026_FM
python python_script/setup.py
```

This builds the Docker image, creates the container, and downloads nuXmv automatically.

**Alternative options:**
```bash
# Use a local nuXmv binary:
python python_script/setup.py --nuxmv ./nuXmv

# Skip nuXmv (container can still generate .smv files):
python python_script/setup.py --skip-nuxmv
```

### Step 2: Run Experiments & Extract Results

```bash
python python_script/reproduce.py
```

Results will be extracted to `./results/`. This takes **30-60 minutes**.

**Alternative options:**
```bash
# Specify output directory:
python python_script/reproduce.py ./MyOutput

# Extract results without re-running (if tests already ran):
python python_script/reproduce.py --extract-only
```

---

## Directory Structure

```
REPRODUCIBILITY/2026_FM/
├── python_script/          # Python scripts for Docker automation
│   ├── setup.py            # Step 1: Set up Docker environment
│   ├── reproduce.py        # Step 2: Run experiments & extract results
│   ├── run_behaverify.py   # Run BehaVerify on your own .tree files
│   ├── docker_util.py      # Docker utility functions
│   └── ...
├── examples/               # Behavior tree examples (DSL source files)
│   ├── BT2BIP/             # MarsRover, TrainControl examples
│   ├── BT2Fiacre/          # Drone3 examples
│   ├── MoVe4BT/            # Binary tree benchmarks
│   ├── NetworkExample/     # Neural network integration examples
│   └── DrunkenDrone/       # Additional drone example
├── scripts/                # Shell scripts for running tests
│   ├── build_scripts/      # nuXmv file generation scripts
│   ├── encoding_timing_scripts/  # Verification timing scripts
│   └── test_scripts/       # Individual test runners
├── src/                    # BehaVerify source code
├── metamodel/              # DSL grammar (behaverify.tx)
├── requirements/           # Python dependencies
├── MoVe4BT/                # MoVe4BT comparison setup
├── Dockerfile              # Docker build file (GitHub version)
├── Dockerfile.local        # Docker build file (local development)
├── BehaVerify_2026_FM.sh   # Main experiment script
└── README.md               # Full documentation
```

---

## Results Overview

After running, results appear in `results/examples/`:

| Directory | Contents |
|-----------|----------|
| `MoVe4BT/` | Binary tree benchmarks (1-10), timing comparisons |
| `BT2BIP/` | MarsRover & TrainControl verification results |
| `BT2Fiacre/` | Drone3 verification, counterexample traces |
| `NetworkExample/` | Neural network integration verification |

**Key output files:**
- `MoVe4BT/processed_data/2026-FM-MoVe4BT-Timing.png` - Timing comparison graph
- `BT2Fiacre/processed_data/0_*.png` - Counterexample trace visualizations
- `*/results/*.txt` - Verification results (CTL, LTL, INVAR proofs)
- `*/LaTeX/*.tex` - Behavior tree visualizations

---

## Running BehaVerify on Your Own Examples

### From the Host (Recommended)

Use `run_behaverify.py` to run BehaVerify on any `.tree` file from your host machine:

```bash
cd REPRODUCIBILITY/2026_FM

# Generate .smv file only
python python_script/run_behaverify.py path/to/your_tree.tree

# Generate and run nuXmv verification (all specs)
python python_script/run_behaverify.py path/to/your_tree.tree --verify

# Run specific verification types
python python_script/run_behaverify.py path/to/your_tree.tree --verify --ctl
python python_script/run_behaverify.py path/to/your_tree.tree --verify --ltl
python python_script/run_behaverify.py path/to/your_tree.tree --verify --invar

# Custom output directory
python python_script/run_behaverify.py path/to/your_tree.tree -o ./my_results --verify
```

**Example with included MarsRover example:**
```bash
python python_script/run_behaverify.py examples/BT2BIP/MarsRover.tree --verify --invar
```

This will:
1. Copy your `.tree` file into the Docker container
2. Run BehaVerify to generate a nuXmv model (`.smv` file)
3. Run nuXmv verification (if `--verify` specified)
4. Copy all results back to your host machine

**Output files created:**
- `YourTree.smv` - nuXmv model file
- `YourTree_CTL.txt` - CTL verification results (if `--ctl`)
- `YourTree_LTL.txt` - LTL verification results (if `--ltl`)
- `YourTree_INVAR.txt` - INVAR verification results (if `--invar`)

### run_behaverify.py Options

| Option | Description |
|--------|-------------|
| `input_file` | Path to `.tree` DSL file (required) |
| `-o, --output` | Output directory (default: `<input>_output/`) |
| `--verify` | Run nuXmv verification after generating `.smv` |
| `--ctl` | Run CTL specification check |
| `--ltl` | Run LTL specification check |
| `--invar` | Run INVAR specification check |
| `--keep-last-stage` | Keep last stage optimization |
| `--do-not-trim` | Do not trim the model |
| `--behave-only` | Behavior only mode |
| `--recursion-limit` | Python recursion limit for large trees (default: 10000) |

### Inside the Docker Container (Advanced)

For more control, you can work directly inside the container:

```bash
# Start an interactive shell in the container
docker exec -it behaverify_2026_fm bash

# Navigate to the source directory
cd /home/BehaVerify_2026_FM/behaverify/REPRODUCIBILITY/2026_FM/src

# Run BehaVerify directly
/home/BehaVerify_2026_FM/python_venvs/behaverify/bin/python3 dsl_to_nuxmv.py \
    ../metamodel/behaverify.tx \
    ../examples/BT2BIP/MarsRover.tree \
    ./MarsRover.smv

# Run nuXmv on the generated .smv file
../nuXmv ./MarsRover.smv
```

### DSL File Structure

A minimal `.tree` file:
```
configuration {
    use_reals: True
}
variables {
    variable { my_var VAR INT [0, 10] }
}
actions {
    action {
        my_action
        arguments {}
        local_variables {}
        read_variables {}
        write_variables { my_var }
        initial_values { (assign, my_var, 0) }
        update {
            (assign, my_var, (addition, my_var, 1))
            success
        }
    }
}
main_tree {
    composite {
        sequence
        children {
            my_action {}
        }
    }
}
specifications {
    CTLSPEC { (always, (less_than_or_equal, my_var, 10)) }
}
```

See `examples/` for more complete examples and the `metamodel/behaverify.tx` grammar.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker permission denied | Run `sudo usermod -aG docker $USER` and restart |
| nuXmv download fails | Use `--nuxmv ./nuXmv` with manually downloaded binary |
| Tests timeout | Increase Docker memory allocation |
| No PNG files generated | Update Docker version (tested with 20.10.24+) |

For more details, see the [full README](README.md).

---

## Quick Reference

```bash
# Full reproduction (both steps)
cd REPRODUCIBILITY/2026_FM
python python_script/setup.py
python python_script/reproduce.py

# View results
ls results/examples/

# Run BehaVerify on your own .tree file
python python_script/run_behaverify.py my_tree.tree --verify
```
