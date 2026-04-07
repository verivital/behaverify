"""
heatmap_unsat_contracts.py

Generates a heatmap of UNSAT A/G contract counts per obstacle on the 7x7 grid world.

For each obstacle cell, the color represents how many of its associated contracts
are UNSAT on average across all networks in the specified contracts folder.

Usage:
    python3 heatmap_unsat_contracts.py [--contracts-dir PATH] [--output PATH]

Defaults:
    --contracts-dir  ../../contracts/enabled_pgd/
    --output         ../heatmap_unsat_contracts.png
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


GRID_MIN = 0
GRID_MAX = 6
GRID_SIZE = GRID_MAX - GRID_MIN + 1


def load_obstacle_unsat_counts(contracts_dir: Path) -> dict[tuple, list[int]]:
    """
    Returns a dict mapping obstacle (ox, oy) -> list of UNSAT counts,
    one entry per JSON file in contracts_dir.
    """
    json_files = sorted(
        f for f in contracts_dir.glob("*.json")
        if f.name.startswith("1000")
    )
    if not json_files:
        raise FileNotFoundError(f"No 1000-series JSON files found in {contracts_dir}")

    # obstacle -> [unsat_count_per_network]
    per_network: dict[tuple, list[int]] = defaultdict(list)

    for path in json_files:
        with open(path) as f:
            data = json.load(f)

        # Count UNSAT contracts per obstacle for this network
        counts: dict[tuple, int] = defaultdict(int)
        for contract in data["contracts"]:
            obs = tuple(contract["obstacle"])
            if contract["status"] == "UNSAT":
                counts[obs] += 1
            else:
                counts.setdefault(obs, 0)

        for obs, count in counts.items():
            per_network[obs].append(count)

    return per_network


def build_heatmap(per_network: dict[tuple, list[int]]) -> tuple[np.ndarray, set]:
    """
    Returns:
        grid   -- (GRID_SIZE x GRID_SIZE) float array of average UNSAT counts.
                  NaN for non-obstacle cells.
        obstacles -- set of (ox, oy) tuples
    """
    grid = np.full((GRID_SIZE, GRID_SIZE), np.nan)
    obstacles = set(per_network.keys())

    for (ox, oy), counts in per_network.items():
        avg = sum(counts) / len(counts)
        # matplotlib imshow: row 0 = top, so flip y
        row = GRID_SIZE - 1 - oy
        col = ox
        grid[row, col] = avg

    return grid, obstacles


def plot_heatmap(grid: np.ndarray, obstacles: set, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))

    # Background for non-obstacle cells
    bg = np.zeros((GRID_SIZE, GRID_SIZE))
    ax.imshow(bg, cmap="Greys", vmin=0, vmax=1, alpha=0.08)

    # Heatmap over obstacle cells only
    masked = np.ma.masked_invalid(grid)
    max_val = max(1, int(np.nanmax(grid)))
    img = ax.imshow(
        masked,
        cmap="plasma",
        vmin=0,
        vmax=max_val,
        interpolation="nearest",
    )

    # Grid lines
    for x in range(GRID_SIZE + 1):
        ax.axhline(x - 0.5, color="black", linewidth=1.0)
        ax.axvline(x - 0.5, color="black", linewidth=1.0)

    # Annotate obstacle cells with their average UNSAT count
    for (ox, oy) in obstacles:
        row = GRID_SIZE - 1 - oy
        col = ox
        val = grid[row, col]
        ax.text(
            col, row, f"{val:.1f}",
            ha="center", va="center",
            fontsize=9, fontweight="bold",
            color="black" if val >= 3.0 else "white",
        )

    # Axes labels
    ax.set_xticks(range(GRID_SIZE))
    ax.set_xticklabels(range(GRID_SIZE))
    ax.set_yticks(range(GRID_SIZE))
    ax.set_yticklabels(range(GRID_SIZE - 1, -1, -1))
    ax.set_xlabel("Drone x", fontsize=11)
    ax.set_ylabel("Drone y", fontsize=11)
    ax.set_title(
        "Average UNSAT contracts per obstacle\n(100%-accurate networks, enabled PGD)",
        fontsize=12,
    )

    cbar = fig.colorbar(img, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Avg UNSAT contracts", fontsize=10)

    empty_patch = mpatches.Patch(facecolor="whitesmoke", edgecolor="gray", label="Free cell")
    ax.legend(handles=[empty_patch], loc="upper right", fontsize=9)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {output_path}")
    plt.close()


def main() -> None:
    here = Path(__file__).parent

    parser = argparse.ArgumentParser(description="Generate UNSAT contract heatmap.")
    parser.add_argument(
        "--contracts-dir",
        type=Path,
        default=here / "../../contracts/enabled_pgd",
        help="Directory containing contract JSON files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=here / "../heatmap_unsat_contracts.png",
        help="Output image path.",
    )
    args = parser.parse_args()

    contracts_dir = args.contracts_dir.resolve()
    output_path = args.output.resolve()

    print(f"Loading contracts from: {contracts_dir}")
    per_network = load_obstacle_unsat_counts(contracts_dir)
    grid, obstacles = build_heatmap(per_network)

    print(f"Obstacles found: {len(obstacles)}")
    print(f"Grid max value:  {np.nanmax(grid):.2f}")

    plot_heatmap(grid, obstacles, output_path)


if __name__ == "__main__":
    main()
