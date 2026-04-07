"""
direction_bias.py

Analyzes and plots UNSAT A/G contract rates broken down by forbidden direction
(West, East, North, South) across all 100%-accurate networks (1000-series).

A higher UNSAT rate for a direction means the NN more frequently produces that
forbidden move for some continuous goal input in [0, 6]².

Usage:
    python3 direction_bias.py [--contracts-dir PATH] [--output PATH]

Defaults:
    --contracts-dir  ../../contracts/enabled_pgd/
    --output         ../direction_bias.png
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


DIRECTION_LABELS = {
    "We": "West",
    "Ea": "East",
    "No": "North",
    "So": "South",
}
DIRECTION_ORDER = ["We", "Ea", "No", "So"]


def load_direction_stats(
    contracts_dir: Path,
) -> tuple[dict[str, int], dict[str, int], dict[str, dict[str, int]], dict[str, dict[str, int]]]:
    """
    Returns:
        dir_total   -- {dir: total contract count across all networks}
        dir_unsat   -- {dir: UNSAT count across all networks}
        per_net_total  -- {network_name: {dir: total}}
        per_net_unsat  -- {network_name: {dir: unsat}}
    """
    json_files = sorted(
        f for f in contracts_dir.glob("*.json")
        if f.name.startswith("1000")
    )
    if not json_files:
        raise FileNotFoundError(f"No 1000-series JSON files found in {contracts_dir}")

    dir_total: dict[str, int] = defaultdict(int)
    dir_unsat: dict[str, int] = defaultdict(int)
    per_net_total: dict[str, dict] = {}
    per_net_unsat: dict[str, dict] = {}

    for path in json_files:
        name = path.stem
        with open(path) as f:
            data = json.load(f)

        net_total: dict[str, int] = defaultdict(int)
        net_unsat: dict[str, int] = defaultdict(int)

        for contract in data["contracts"]:
            d = contract["forbidden_dir"]
            dir_total[d] += 1
            net_total[d] += 1
            if contract["status"] == "UNSAT":
                dir_unsat[d] += 1
                net_unsat[d] += 1

        per_net_total[name] = dict(net_total)
        per_net_unsat[name] = dict(net_unsat)

    return dict(dir_total), dict(dir_unsat), per_net_total, per_net_unsat


def plot_direction_bias(
    dir_total: dict[str, int],
    dir_unsat: dict[str, int],
    per_net_total: dict[str, dict],
    per_net_unsat: dict[str, dict],
    output_path: Path,
) -> None:
    dirs = DIRECTION_ORDER
    labels = [DIRECTION_LABELS[d] for d in dirs]
    rates = [100 * dir_unsat.get(d, 0) / dir_total[d] for d in dirs]
    counts = [dir_unsat.get(d, 0) for d in dirs]
    totals = [dir_total[d] for d in dirs]

    # Color bars by UNSAT rate (low = blue, high = red)
    norm = plt.Normalize(min(rates), max(rates))
    cmap = plt.cm.coolwarm
    colors = [cmap(norm(r)) for r in rates]

    fig, ax = plt.subplots(figsize=(6, 4))

    bars = ax.bar(labels, rates, color=colors, edgecolor="black", linewidth=0.8, zorder=3)

    # Annotate each bar with count/total
    for bar, count, total, rate in zip(bars, counts, totals, rates):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            f"{count}/{total}",
            ha="center", va="bottom",
            fontsize=10, fontweight="bold",
        )

    # Per-network scatter overlay
    network_names = sorted(per_net_total.keys())
    jitter = np.linspace(-0.15, 0.15, len(network_names))
    for i, name in enumerate(network_names):
        x_positions = []
        y_positions = []
        for j, d in enumerate(dirs):
            t = per_net_total[name].get(d, 0)
            u = per_net_unsat[name].get(d, 0)
            if t > 0:
                x_positions.append(j + jitter[i])
                y_positions.append(100 * u / t)
        ax.scatter(
            x_positions, y_positions,
            s=30, color="black", alpha=0.45, zorder=4,
        )

    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.set_ylabel("UNSAT rate", fontsize=11)
    ax.set_xlabel("Forbidden direction", fontsize=11)
    ax.set_title(
        "UNSAT contract rate by forbidden direction\n"
        "(100%-accurate networks, enabled PGD, dots = per-network)",
        fontsize=11,
    )
    ax.axhline(50, color="gray", linestyle="--", linewidth=0.8, zorder=2, label="50% reference")
    ax.legend(fontsize=9)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=0)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {output_path}")
    plt.close()

    # Print summary table
    print("\nDirection  Total  UNSAT  Rate")
    print("-" * 34)
    for d in dirs:
        t = dir_total[d]
        u = dir_unsat.get(d, 0)
        print(f"  {DIRECTION_LABELS[d]:<8}  {t:>5}  {u:>5}  {100*u/t:>5.1f}%")


def main() -> None:
    here = Path(__file__).parent

    parser = argparse.ArgumentParser(description="Plot UNSAT rate by forbidden direction.")
    parser.add_argument(
        "--contracts-dir",
        type=Path,
        default=here / "../../contracts/enabled_pgd",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=here / "../direction_bias.png",
    )
    args = parser.parse_args()

    contracts_dir = args.contracts_dir.resolve()
    output_path = args.output.resolve()

    print(f"Loading contracts from: {contracts_dir}")
    dir_total, dir_unsat, per_net_total, per_net_unsat = load_direction_stats(contracts_dir)
    plot_direction_bias(dir_total, dir_unsat, per_net_total, per_net_unsat, output_path)


if __name__ == "__main__":
    main()
