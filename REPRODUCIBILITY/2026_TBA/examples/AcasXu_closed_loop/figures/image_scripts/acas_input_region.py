"""
acas_input_region.py

Visualizes a single A/G contract's input region in two views:
  Left  — Physical state space (x_mag, y_mag) showing dangerous states and the
           safety boundary (distance = 200 ft).
  Right — Normalized NN input space (dim 1: distance, dim 2: relative angle)
           showing the dangerous state points and the CROWN bounding box.

The selected contract is printed to stdout for reference.

Usage:
    python3 figures/image_scripts/acas_input_region.py
    python3 figures/image_scripts/acas_input_region.py --contract-id 42

Defaults:
    --specs        ../../contracts/continuous_goals/contract_specs_eps1e4.json
    --output       ../acas_input_region.png
    --contract-id  (auto: first contract with n_states_covered >= 5)
"""

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------------------------
# Constants (must match generate_acas_contracts.py)
# ---------------------------------------------------------------------------

DISTANCE_MODIFIER = 100
MAX_DIST_VAR      = 10
SAFETY_THRESHOLD  = 200           # feet
DEGREE_MULTIPLIER = 9             # degrees per heading step

DISTANCE_MEAN  = 19791.091
DISTANCE_RANGE = 60261.0

ADVISORY_LABELS = {
    "clear":        "Clear (CoC)",
    "weak_left":    "Weak Left",
    "weak_right":   "Weak Right",
    "strong_left":  "Strong Left",
    "strong_right": "Strong Right",
}

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_contracts(specs_path: Path) -> list[dict]:
    with open(specs_path) as f:
        data = json.load(f)
    return data["contracts"]


def select_contract(contracts: list[dict], contract_id: int | None) -> dict:
    """Return the requested contract, or auto-select the first with >= 5 states."""
    if contract_id is not None:
        matches = [c for c in contracts if c["id"] == contract_id]
        if not matches:
            raise ValueError(f"No contract found with id={contract_id}")
        return matches[0]

    # Auto-select: pick first with n_states_covered >= 5 for a nice visual
    for c in contracts:
        if c["n_states_covered"] >= 5:
            return c
    return contracts[0]  # fallback


def compute_safe_cells() -> set[tuple[int, int]]:
    """All (x_mag, y_mag) with distance >= SAFETY_THRESHOLD."""
    safe = set()
    for x in range(MAX_DIST_VAR + 1):
        for y in range(MAX_DIST_VAR + 1):
            dist = round(math.sqrt(x * x + y * y)) * DISTANCE_MODIFIER
            if dist >= SAFETY_THRESHOLD:
                safe.add((x, y))
    return safe


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_physical_space(ax: plt.Axes, contract: dict, safe_cells: set) -> None:
    """Left panel: (x_mag, y_mag) physical state space."""
    x_sign = contract["x_sign"]
    y_sign = contract["y_sign"]
    heading_var = contract["heading_own_var"]
    heading_deg = heading_var * DEGREE_MULTIPLIER
    advisory     = contract["forbidden_advisory"]
    dangerous_xy = contract["dangerous_xy"]   # list of [x_mag, y_mag]

    # Grid background: green = safe, salmon = already unsafe
    for xv in range(MAX_DIST_VAR + 1):
        for yv in range(MAX_DIST_VAR + 1):
            color = "#d4edda" if (xv, yv) in safe_cells else "#f8d7da"
            rect = mpatches.FancyBboxPatch(
                (xv - 0.5, yv - 0.5), 1.0, 1.0,
                boxstyle="square,pad=0",
                linewidth=0,
                facecolor=color,
                zorder=0,
            )
            ax.add_patch(rect)

    # Grid lines
    for i in range(MAX_DIST_VAR + 2):
        ax.axhline(i - 0.5, color="white", linewidth=0.6, zorder=1)
        ax.axvline(i - 0.5, color="white", linewidth=0.6, zorder=1)

    # Safety boundary circle (radius where round(r)*100 = 200 → r ≈ 1.5 in grid units)
    theta = np.linspace(0, 2 * math.pi, 300)
    radius = 1.5  # 150 ft / 100 ft-per-unit = 1.5 grid units
    ax.plot(
        radius * np.cos(theta), radius * np.sin(theta),
        color="#c0392b", linewidth=1.5, linestyle="--", zorder=3,
        label=f"Safety boundary (~{SAFETY_THRESHOLD} ft)",
    )

    # Dangerous state dots
    dx = [s[0] for s in dangerous_xy]
    dy = [s[1] for s in dangerous_xy]
    ax.scatter(dx, dy, s=70, color="#c0392b", zorder=5, label="Dangerous states")

    # Ownship marker at origin (relative coordinate frame)
    ax.scatter(0, 0, s=120, color="#2471a3", marker="^", zorder=6, label="Ownship (origin)")

    sign_x = "+" if x_sign == 1 else "−"
    sign_y = "+" if y_sign == 1 else "−"
    ax.set_xlim(-0.5, MAX_DIST_VAR + 0.5)
    ax.set_ylim(-0.5, MAX_DIST_VAR + 0.5)
    ax.set_xlabel("x_mag  (× 100 ft)", fontsize=10)
    ax.set_ylabel("y_mag  (× 100 ft)", fontsize=10)
    ax.set_title(
        f"Physical state space\n"
        f"heading={heading_deg}°, quadrant=({sign_x},{sign_y}), "
        f"forbidden: {ADVISORY_LABELS[advisory]}",
        fontsize=10,
    )
    ax.set_aspect("equal")
    ax.legend(fontsize=8, loc="upper right")


def plot_input_space(ax: plt.Axes, contract: dict) -> None:
    """Right panel: normalized NN input space (dim 1 vs dim 2)."""
    lower = contract["nn_input_lower"]
    upper = contract["nn_input_upper"]
    dangerous_xy = contract["dangerous_xy"]
    advisory     = contract["forbidden_advisory"]

    # We need to recompute NN inputs for each dangerous state.
    # They're not stored in the spec per-state, but we can back them out
    # from the bounding box extremes plus dots.
    # Instead, the contract has nn_input_lower/upper — we have the bounding box.
    # For the dots, we use the stored dangerous_xy and note the box is tight.
    # We plot the box rectangle and annotate the dangerous states as a cluster.
    # (exact per-state normalized inputs would require re-running compute_nn_inputs)

    # Bounding box rectangle
    box_x = lower[0]
    box_y = lower[1]
    box_w = upper[0] - lower[0]
    box_h = upper[1] - lower[1]

    rect = mpatches.FancyBboxPatch(
        (box_x, box_y), box_w, box_h,
        boxstyle="square,pad=0",
        linewidth=2.0,
        edgecolor="#2e86c1",
        facecolor="#d6eaf8",
        alpha=0.6,
        zorder=2,
        label="CROWN bounding box",
    )
    ax.add_patch(rect)

    # Corner markers for box bounds
    ax.scatter([lower[0], upper[0]], [lower[1], upper[1]], s=30, color="#2e86c1",
               marker="x", zorder=4, linewidths=1.5)

    # Dangerous state cluster — shown schematically since exact per-state normalized
    # inputs are not stored in the spec (only bounding box is stored).
    # Place a red dot at the centroid of the box to indicate coverage.
    cx = (lower[0] + upper[0]) / 2
    cy = (lower[1] + upper[1]) / 2
    ax.scatter(
        [cx], [cy], s=80, color="#c0392b", zorder=5,
        label=f"{contract['n_states_covered']} dangerous state(s)\n(centroid shown)",
    )

    # Constant inputs annotation
    fixed_text = (
        f"Input 3 (intersect angle): {lower[2]:.4f} … {upper[2]:.4f}\n"
        f"Input 4 (v_own, const):   {lower[3]:.4f}\n"
        f"Input 5 (v_int, const):   {lower[4]:.4f}"
    )
    ax.text(
        0.03, 0.03, fixed_text,
        transform=ax.transAxes,
        fontsize=7.5,
        verticalalignment="bottom",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.8, edgecolor="#aaaaaa"),
    )

    # Axis limits with margin
    margin_x = max(0.05, box_w * 0.5)
    margin_y = max(0.05, box_h * 0.5)
    ax.set_xlim(lower[0] - margin_x, upper[0] + margin_x)
    ax.set_ylim(lower[1] - margin_y, upper[1] + margin_y)

    ax.set_xlabel("NN input 1: normalized distance\n(dist − 19791.091) / 60261", fontsize=10)
    ax.set_ylabel("NN input 2: normalized relative angle\nrel_angle_adj / 360", fontsize=10)
    ax.set_title(
        f"CROWN input region  (contract id={contract['id']})\n"
        f"forbidden: {ADVISORY_LABELS[advisory]}",
        fontsize=10,
    )
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(linestyle="--", linewidth=0.4, alpha=0.5)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    here = Path(__file__).parent

    parser = argparse.ArgumentParser(
        description="Visualize a single ACAS Xu A/G contract input region."
    )
    parser.add_argument(
        "--specs", type=Path,
        default=here / "../../contracts/continuous_goals/contract_specs_eps1e4.json",
    )
    parser.add_argument(
        "--output", type=Path,
        default=here / "../acas_input_region.png",
    )
    parser.add_argument(
        "--contract-id", type=int, default=None, dest="contract_id",
        help="Contract id to visualize (default: auto-select first with >= 5 states)",
    )
    args = parser.parse_args()

    specs_path  = args.specs.resolve()
    output_path = args.output.resolve()

    print(f"Loading contracts from: {specs_path}")
    contracts = load_contracts(specs_path)
    contract  = select_contract(contracts, args.contract_id)
    safe_cells = compute_safe_cells()

    print(f"Selected contract id={contract['id']}:")
    print(f"  heading_own_var={contract['heading_own_var']}  "
          f"({contract['heading_own_var'] * DEGREE_MULTIPLIER}°)")
    print(f"  quadrant=({contract['x_sign']:+},{contract['y_sign']:+})")
    print(f"  forbidden={contract['forbidden_advisory']}")
    print(f"  n_states_covered={contract['n_states_covered']}")
    print(f"  nn_input_lower={[f'{v:.4f}' for v in contract['nn_input_lower']]}")
    print(f"  nn_input_upper={[f'{v:.4f}' for v in contract['nn_input_upper']]}")

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11, 5))

    plot_physical_space(ax_left, contract, safe_cells)
    plot_input_space(ax_right, contract)

    fig.suptitle(
        "ACAS Xu A/G Contract — Input Region Visualization",
        fontsize=12, fontweight="bold", y=1.01,
    )

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
