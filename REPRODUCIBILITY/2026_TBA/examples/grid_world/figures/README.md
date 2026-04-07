# Grid World Figures

Generated figures for the grid world compositional verification example.

All scripts live in `image_scripts/` and write output directly to this directory.
Run all commands from `grid_world/` (one level up).

---

## Layout

```
figures/
├── image_scripts/                     # Scripts that generate figures
│   ├── heatmap_unsat_contracts.py     # Heatmap of avg UNSAT contracts per obstacle
│   └── direction_bias.py              # Bar chart of UNSAT rate by forbidden direction
├── heatmap_unsat_contracts.png        # Generated output
└── direction_bias.png                 # Generated output
```

---

## Figures

### `heatmap_unsat_contracts.png`

A 7x7 heatmap of the grid world where each obstacle cell is colored by the average
number of UNSAT A/G contracts across all 100%-accurate networks (1000-series only).

- **Dark blue (0.0):** all contracts for this obstacle are SAT — the NN is safe here
- **Yellow (4.0):** all four surrounding contracts are UNSAT — unsafe in every direction

Key finding: obstacles (3,3) and (5,5) score 4.0 across all five 100%-accurate networks,
meaning the NN produces a forbidden move approaching these obstacles from any direction,
for some continuous goal input in [0,6]². This violates the A/G contract despite the
network achieving 100% accuracy on discrete training inputs.

**Generate:**

```bash
cd REPRODUCIBILITY/2026_TBA/examples/grid_world
python3 figures/image_scripts/heatmap_unsat_contracts.py
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--contracts-dir` | `contracts/enabled_pgd/` | Directory of contract JSON files to aggregate |
| `--output` | `figures/heatmap_unsat_contracts.png` | Output image path |

**Example — BaB-only contracts:**

```bash
python3 figures/image_scripts/heatmap_unsat_contracts.py \
    --contracts-dir contracts/disabled_pgd/ \
    --output figures/heatmap_unsat_contracts_bab.png
```

---

### `direction_bias.png`

A bar chart showing the UNSAT contract rate broken down by forbidden direction
(West, East, North, South) across all five 100%-accurate networks. Per-network
rates are overlaid as scatter dots to show consistency across networks.

Key finding: North (58%) and South (60%) show higher UNSAT rates than West (47%)
and East (52%), suggesting the NN's decision boundary is more prone to continuous-
domain failures for vertical movements than horizontal ones.

**Generate:**

```bash
cd REPRODUCIBILITY/2026_TBA/examples/grid_world
python3 figures/image_scripts/direction_bias.py
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--contracts-dir` | `contracts/enabled_pgd/` | Directory of contract JSON files to aggregate |
| `--output` | `figures/direction_bias.png` | Output image path |
