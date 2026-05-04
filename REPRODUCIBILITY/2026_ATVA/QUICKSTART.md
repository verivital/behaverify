# ATVA 2026 Reproducibility - Quick Start Guide

This guide provides the fastest path to reproducing ATVA 2026 results.
For detailed explanations, see [README.md](README.md).

---

## Prerequisites

1. **Docker** installed and running (user can run without sudo)
2. **nuXmv 2.1.0** binary placed at `REPRODUCIBILITY/2026_ATVA/nuXmv`
   - Download: https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz
   - Extract the binary from `nuXmv-2.1.0-linux64/nuXmv-2.1.0-Linux/bin/nuXmv` — no file extension

---

## Reproducing Results (Two Commands)

Run from the **repository root** (`behaverify/`):

### Step 1: Build the Docker image

```bash
docker build -f REPRODUCIBILITY/2026_ATVA/Dockerfile.local -t behaverify_2026_atva_img .
```

This installs all dependencies and packages BehaVerify from the frozen local source.
Only needs to be done once (or after code changes).

### Step 2: Run experiments

```bash
docker run -v $(pwd)/REPRODUCIBILITY/2026_ATVA/docker_results:/output behaverify_2026_atva_img
```

This runs `BehaVerify_2026_ATVA.sh` inside the container. Results are written
directly to `REPRODUCIBILITY/2026_ATVA/docker_results/` on your host as the
script runs. Takes **30–60 minutes**.

---

## Directory Structure

```
REPRODUCIBILITY/2026_ATVA/
├── BehaVerify_2026_ATVA.sh      # Main experiment script (runs everything)
├── Dockerfile                   # Docker build file (artifact reviewer path, pulls from GitHub)
├── Dockerfile.local             # Docker build file (local dev path, uses local files)
├── examples/                    # Behavior tree source files
│   ├── BT2BIP/                  # MarsRover, TrainControl examples
│   ├── BT2Fiacre/               # Drone3 examples
│   ├── EncodingComparison/      # FF vs. Naive binary-tree benchmark (Table 2)
│   ├── NetworkExample/          # Neural network integration examples
│   └── DrunkenDrone/            # DrunkenDrone example (Figure 1)
├── scripts/                     # Shell scripts for running experiments
│   ├── build_scripts/           # SMV file generation scripts
│   ├── encoding_timing_scripts/ # Verification timing scripts
│   └── test_scripts/            # Individual nuXmv test runners
├── src/                         # Frozen BehaVerify source snapshot
├── metamodel/                   # DSL grammar (behaverify.tx)
├── requirements/                # Python dependencies
└── README.md                    # Full documentation
```

---

## Results Overview

After running, results appear in `docker_results/`:

| Directory | Contents |
|-----------|----------|
| `EncodingComparison/` | FF vs. Naive ablation results (Table 2), N=1–10 |
| `BT2BIP/` | MarsRover & TrainControl verification results (Section 4.3) |
| `BT2Fiacre/` | Drone3 verification, counterexample traces (Table 3) |
| `NetworkExample/` | NSBT repo example verification results |
| `DrunkenDrone/` | LaTeX source for Figure 1 |

**Key output files:**
- `EncodingComparison/results/*_{FF,NAIVE}_binary_tree_N.txt` — CTL/LTL/STATES timing for Table 2
- `BT2Fiacre/results/INVAR_full_opt_drone3_{0,2,3}.txt` — INVAR results for Table 3 and Section 4.2
- `BT2Fiacre/processed_data/0_*.png` — Counterexample trace images (Section 4.2 footnote)
- `*/LaTeX/*.tex` — Behavior tree TikZ diagrams

---

## Running Locally (Without Docker)

If you have BehaVerify installed locally with nuXmv available:

```bash
cd REPRODUCIBILITY/2026_ATVA

# Enable scripts (first time only)
chmod +x BehaVerify_2026_ATVA.sh
find scripts/ -name "*.sh" -exec chmod +x {} \;

# Run everything
./BehaVerify_2026_ATVA.sh ./
```

Results land in `examples/*/results/` and `examples/*/LaTeX/`.

---

## Reproducing Individual Tables

### Table 2: Fastforwarding vs. Naive ablation

```bash
cd REPRODUCIBILITY/2026_ATVA/scripts/build_scripts
./exp_encoding_comparison_create.sh python3 1 10 1

cd ../encoding_timing_scripts
./exp_encoding_comparison_run.sh 1 10 1 5m
```

Results: `examples/EncodingComparison/results/`

### Table 3: BT2Fiacre drone comparison

```bash
cd REPRODUCIBILITY/2026_ATVA/scripts/build_scripts
./exp_tool_comparisons_2026_ATVA_create.sh python3 1 10 1

cd ../encoding_timing_scripts
./exp_tool_comparisons_2026_ATVA_run.sh 1 10 1
```

Results: `examples/BT2Fiacre/results/`

### Table 3: Results Matching Lookup Table

**Source models used for the table (indices 0 and 3 only):**

| drone3 column | droneNew column |
|---|---|
| `examples/BT2Fiacre/drone3_height.tree` → `tree/drone3_0.tree` | `examples/BT2Fiacre/droneNew_height.tree` → `tree/drone3_3.tree` |

| Table row | Result file | What to extract |
|---|---|---|
| Prep. / drone3 | `results/translation_drone3_0.txt` | `total:` |
| Prep. / droneNew | `results/translation_drone3_3.txt` | `total:` |
| Check Height / drone3 | `results/SILENT_INVAR_full_opt_drone3_0.txt` | second `elapse:` |
| Check Height / droneNew | `results/SILENT_INVAR_full_opt_drone3_3.txt` | second `elapse:` |
| Reach. states / drone3 | `results/STATES_full_opt_drone3_0.txt` | first log₂ in reachable line |
| Total states / drone3 | `results/STATES_full_opt_drone3_0.txt` | second log₂ in reachable line |
| Reach. states / droneNew | `results/STATES_full_opt_drone3_3.txt` | first log₂ |
| Total states / droneNew | `results/STATES_full_opt_drone3_3.txt` | second log₂ |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker permission denied | Run `sudo usermod -aG docker $USER` and restart |
| `nuXmv: not found` inside container | Ensure `nuXmv` binary is at `REPRODUCIBILITY/2026_ATVA/nuXmv` before building |
| Scripts: permission denied | Run `find scripts/ -name "*.sh" -exec chmod +x {} \;` |
| Tests timeout | Increase Docker memory allocation |

For more details, see [README.md](README.md).

---

## Quick Reference

```bash
# From repo root — build once, run anytime
docker build -f REPRODUCIBILITY/2026_ATVA/Dockerfile.local -t behaverify_2026_atva_img .
docker run -v $(pwd)/REPRODUCIBILITY/2026_ATVA/docker_results:/output behaverify_2026_atva_img

# View results
ls REPRODUCIBILITY/2026_ATVA/docker_results/
```
