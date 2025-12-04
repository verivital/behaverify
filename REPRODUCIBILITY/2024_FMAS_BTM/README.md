# BehaVerify FMAS 2024: Behavior Tree Monitors (BTM) Reproducibility

This README provides instructions for reproducing results from the FMAS 2024 paper:

**"Verification of Behavior Trees with Contingency Monitors"**
- arXiv: https://arxiv.org/abs/2411.14162

## About This Artifact

This artifact demonstrates BehaVerify's runtime monitor generation and compares it against:
- **Copilot** - Haskell-based runtime verification
- **Monitorless baseline** - Behavior tree execution without monitoring

The experiments use **drone navigation** scenarios with collision avoidance monitors.

## Paper Figures

| Figure | Description | Generated Files |
|--------|-------------|-----------------|
| Figure 5 | Grid visualizations (10x10, 50x50 with dense/sparse obstacles) | Grid images from draw_output.py |
| Figure 6 | Loop detection examples (potential loop scenarios) | Loop visualization images |
| Figure 8 | Runtime timing & monitor file size comparisons | `images/timing_*.png`, `images/file_sizes_*.png` |
| Figure 9 | Design-time verification timing | `images/timing_design_time.png` |

## Prerequisites

1. **Docker** with ability to run as regular user (see https://docs.docker.com/engine/install/linux-postinstall/)
2. **nuXmv** model checker - Download from https://nuxmv.fbk.eu/
   - Version 2.0.0 or 2.1.0 (Linux 64-bit)
   - Place the binary in this directory as `nuXmv` (no file extension)
3. **Python 3** with `docker` package: `pip install docker`

## Quick Start with Docker

### Install Test (~3 min)
```bash
python3 ./python_script/build_and_run.py ./ ./nuXmv install ./install
```

### Partial Test (~8 min)
```bash
python3 ./python_script/build_and_run.py ./ ./nuXmv partial ./partial
```

### Full Test (~16 min)
```bash
python3 ./python_script/build_and_run.py ./ ./nuXmv full ./full
```

Results will be in `/path/to/output.tar`. Extract and check `example/images/` for generated figures.

## Running Locally (without Docker)

### Installation
```bash
# Install dependencies
sudo apt update && sudo apt upgrade
sudo apt install python3 pip graphviz
pip install py_trees pandas jinja2 textX matplotlib pillow

# Clone repository
git clone https://github.com/verivital/behaverify
cd behaverify/REPRODUCIBILITY/2024_FMAS_BTM

# Enable scripts
chmod -R +x ./*.sh ./example/*.sh

# Place nuXmv binary
# Download from https://nuxmv.fbk.eu/ and place as ./nuXmv
chmod +x ./nuXmv
```

### Run Experiments
```bash
# Install test (2 iterations)
./BehaVerify_2024_FMAS_BTM.sh ./ 2

# Partial test (5 iterations)
./BehaVerify_2024_FMAS_BTM.sh ./ 5

# Full test (9 iterations)
./BehaVerify_2024_FMAS_BTM.sh ./ 9
```

Results will be in `example/images/`.

## Experiments Explained

### 1. Dense Fixed Obstacles
- Grid navigation with densely-packed fixed obstacle patterns
- Grid sizes scale from 9x9 to larger
- Tests collision monitor effectiveness

### 2. Sparse Random Obstacles
- Grid navigation with randomly-placed sparse obstacles
- Same scaling as dense experiments
- Compares monitor overhead with different obstacle densities

### 3. Design-Time Verification
- Model checking of safety properties at design time
- Uses nuXmv for LTL specification verification
- Compares with runtime monitoring approach

## Monitor Types

The experiments use two LTL monitors defined in `template_monitor.tree`:

1. **collision_monitor**: Ensures drone doesn't collide with obstacles
   - LTL: `G(not collision_condition)`

2. **loop_monitor**: Prevents back-and-forth movement
   - LTL: `G(left -> X(not right)) & G(right -> X(not left)) & ...`

## Directory Structure

```
2024_FMAS_BTM/
├── BehaVerify_2024_FMAS_BTM.sh    # Main orchestration script
├── Dockerfile                      # Docker configuration
├── README.md                       # This file
├── example/
│   ├── behaverify/                 # BehaVerify monitor implementation
│   ├── copilot/                    # Copilot comparison
│   ├── monitorless/                # Baseline without monitors
│   ├── extra_files/
│   │   ├── template_monitor.tree   # Monitor template
│   │   ├── draw_output.py          # Grid visualization
│   │   └── ...
│   ├── pipeline_create_*.sh        # Experiment creation scripts
│   ├── pipeline_existing_*.sh      # Execution pipelines
│   ├── graph_*.py                  # Graph generation scripts
│   └── make_graphs.sh              # Graph orchestrator
├── python_script/                  # Docker control scripts
└── src/                            # BehaVerify source (frozen version)
```

## Generated Output

After running experiments, check `example/images/` for:

- `timing_dense_fixed.png` - Runtime timing (dense obstacles)
- `timing_sparse_random.png` - Runtime timing (sparse obstacles)
- `file_sizes_dense_fixed.png` - Monitor file sizes (dense)
- `file_sizes_sparse_random.png` - Monitor file sizes (sparse)
- `timing_design_time.png` - Design-time verification timing

## Troubleshooting

1. **Permission denied**: Run without sudo, or configure Docker for non-root access
2. **Docker build fails**: Try `./clean_docker.sh` to remove old containers/images
3. **No images generated**: Check for OpenBLAS pthread errors; upgrade Docker or run graph scripts manually

## Citation

If you use this artifact, please cite:
```
@inproceedings{behaverify_btm_fmas2024,
  title={Verification of Behavior Trees with Contingency Monitors},
  author={...},
  booktitle={FMAS 2024},
  year={2024}
}
```

## Related Papers

- **FMAS 2024 SBT**: "Formalizing Stateful Behavior Trees" - see `../2024_FMAS_SBT/`
- **SEFM 2022**: "BehaVerify: Verifying Temporal Logic Specifications for Behavior Trees"
