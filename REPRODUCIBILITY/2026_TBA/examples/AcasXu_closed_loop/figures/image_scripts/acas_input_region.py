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
import yaml

# ---------------------------------------------------------------------------
# Model parameters (single source of truth: acas_model_params.yaml)
# ---------------------------------------------------------------------------

def _load_params() -> dict:
    path = Path(__file__).parent.parent.parent / "acas_model_params.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

_P = _load_params()

DISTANCE_MODIFIER = _P["physics"]["distance_modifier"]
MAX_DIST_VAR      = _P["physics"]["max_dist"] // _P["physics"]["distance_modifier"]
SAFETY_THRESHOLD  = _P["physics"]["safety_threshold"]
DEGREE_MULTIPLIER = _P["physics"]["degree_multiplier"]
DISTANCE_MEAN     = _P["nn_normalization"]["distance_mean"]
DISTANCE_RANGE    = _P["nn_normalization"]["distance_range"]
HEADING_INT       = _P["physics"]["heading_int_degrees"]

ADVISORY_LABELS = {
    "clear":        "Clear (CoC)",
    "weak_left":    "Weak Left",
    "weak_right":   "Weak Right",
    "strong_left":  "Strong Left",
    "strong_right": "Strong Right",
}

# ---------------------------------------------------------------------------
# NN input computation (mirrors generate_acas_contracts.py)
# ---------------------------------------------------------------------------

def _compute_nn_input1(x_mag: int, y_mag: int) -> float:
    """Normalized distance (NN input 1)."""
    dist = round(math.sqrt(x_mag * x_mag + y_mag * y_mag)) * DISTANCE_MODIFIER
    return (dist - DISTANCE_MEAN) / DISTANCE_RANGE


def _compute_nn_input2(
    x_mag: int, y_mag: int, x_sign: int, y_sign: int, heading_own_var: int
) -> float:
    """Normalized relative angle (NN input 2)."""
    heading_own = heading_own_var * DEGREE_MULTIPLIER

    # arctan_val: atan(y/x) if y_sign=1, atan(x/y) if y_sign=-1
    if y_sign == 1:
        av = 0 if x_mag == 0 else round(math.degrees(math.atan(y_mag / x_mag)))
    else:
        av = 0 if y_mag == 0 else round(math.degrees(math.atan(x_mag / y_mag)))

    # Relative angle cases (matches DSL sequential case order)
    x, y = x_mag * DISTANCE_MODIFIER, y_mag * DISTANCE_MODIFIER
    if x_sign == 1 and y == 0:
        rel = 270 - heading_own
    elif x_sign == -1 and y == 0:
        rel = 90 - heading_own
    elif x == 0 and y_sign == 1:
        rel = 360 - heading_own
    elif x == 0 and y_sign == -1:
        rel = 180 - heading_own
    elif x_sign == 1 and y_sign == 1:
        rel = (270 - heading_own) + av
    elif x_sign == 1 and y_sign == -1:
        rel = (180 - heading_own) + av
    elif x_sign == -1 and y_sign == 1:
        rel = (90 - heading_own) - av
    else:  # x_sign == -1 and y_sign == -1
        rel = (180 - heading_own) - av

    # Normalize to [-180, 180]
    mod = rel % 360
    pos = mod if mod >= 0 else mod + 360
    adj = pos - 360 if pos > 180 else pos
    return adj / 360.0


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



# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_physical_space(ax: plt.Axes, contract: dict) -> None:
    """Left panel: (x_mag, y_mag) physical state space."""
    x_sign = contract["x_sign"]
    y_sign = contract["y_sign"]
    heading_var = contract["heading_own_var"]
    heading_deg = heading_var * DEGREE_MULTIPLIER
    advisory     = contract["forbidden_advisory"]
    dangerous_xy = contract["dangerous_xy"]   # list of [x_mag, y_mag]

    # Green background for the full grid
    ax.set_facecolor("#d4edda")

    # Solid red filled circle = unsafe region (distance < 200 ft)
    # Radius 1.5 grid units is the exact discretization boundary:
    # round(sqrt(x²+y²)) * 100 < 200 iff Euclidean distance < 1.5
    theta = np.linspace(0, 2 * math.pi, 300)
    radius = 1.5
    ax.fill(
        radius * np.cos(theta), radius * np.sin(theta),
        color="#c0392b", alpha=0.35, zorder=1,
        label=f"Unsafe region (< {SAFETY_THRESHOLD} ft)",
    )
    ax.plot(
        radius * np.cos(theta), radius * np.sin(theta),
        color="#c0392b", linewidth=1.5, zorder=2,
    )

    # Dangerous state dots (intruder positions)
    dx = [s[0] for s in dangerous_xy]
    dy = [s[1] for s in dangerous_xy]
    ax.scatter(dx, dy, s=70, color="#c0392b", zorder=5, label="Intruder positions (dangerous)")

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

    x_sign      = contract["x_sign"]
    y_sign      = contract["y_sign"]
    heading_var = contract["heading_own_var"]

    # Compute exact NN inputs 1 & 2 for each dangerous state
    pts = [
        (
            _compute_nn_input1(xm, ym),
            _compute_nn_input2(xm, ym, x_sign, y_sign, heading_var),
        )
        for xm, ym in dangerous_xy
    ]

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

    # Intruder positions: exact NN inputs computed per dangerous state
    ax.scatter(
        [p[0] for p in pts], [p[1] for p in pts],
        s=70, color="#c0392b", zorder=5,
        label=f"Intruder positions ({contract['n_states_covered']} states)",
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

    # Independent proportional padding per axis so the box occupies ~50% of
    # each axis regardless of its aspect ratio. Small floor handles near-zero spans.
    pad_x = max(box_w * 0.5, 0.01)
    pad_y = max(box_h * 0.5, 0.01)
    ax.set_xlim(lower[0] - pad_x, upper[0] + pad_x)
    ax.set_ylim(lower[1] - pad_y, upper[1] + pad_y)

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

    print(f"Selected contract id={contract['id']}:")
    print(f"  heading_own_var={contract['heading_own_var']}  "
          f"({contract['heading_own_var'] * DEGREE_MULTIPLIER}°)")
    print(f"  quadrant=({contract['x_sign']:+},{contract['y_sign']:+})")
    print(f"  forbidden={contract['forbidden_advisory']}")
    print(f"  n_states_covered={contract['n_states_covered']}")
    print(f"  nn_input_lower={[f'{v:.4f}' for v in contract['nn_input_lower']]}")
    print(f"  nn_input_upper={[f'{v:.4f}' for v in contract['nn_input_upper']]}")

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11, 5))

    plot_physical_space(ax_left, contract)
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
