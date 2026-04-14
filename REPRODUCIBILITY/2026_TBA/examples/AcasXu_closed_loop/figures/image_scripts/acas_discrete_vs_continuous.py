"""
acas_discrete_vs_continuous.py

Three-panel figure contrasting continuous and discrete A/G contract verification
for a single ACAS Xu contract:

  Left   — Physical state space: dangerous intruder positions and safety boundary.
  Middle — Continuous NN input space: one CROWN call covers the entire bounding box
           (including non-integer states between the grid points).
  Right  — Discrete NN input space: one CROWN call per exact dangerous state point;
           the faint ghost box shows how much space the discrete checks leave
           uncovered relative to the continuous over-approximation.

Panels 2 and 3 share identical axis ranges for direct visual comparison.

Usage:
    python3 figures/image_scripts/acas_discrete_vs_continuous.py
    python3 figures/image_scripts/acas_discrete_vs_continuous.py --contract-id 42

Defaults:
    --specs        ../../contracts/continuous_goals/contract_specs_eps1e4.json
    --output       ../acas_discrete_vs_continuous.png
    --contract-id  (auto: first contract with n_states_covered >= 5)
"""

import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import yaml

# ---------------------------------------------------------------------------
# Reach generate_acas_contracts.py (3 hops up from this script's location)
# ---------------------------------------------------------------------------

_ROOT = Path(__file__).parent.parent.parent   # AcasXu_closed_loop/
sys.path.insert(0, str(_ROOT))
from generate_acas_contracts import compute_nn_inputs  # noqa: E402

# ---------------------------------------------------------------------------
# Model parameters (single source of truth: acas_model_params.yaml)
# ---------------------------------------------------------------------------

def _load_params() -> dict:
    path = _ROOT / "acas_model_params.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

_P = _load_params()

DISTANCE_MODIFIER = _P["physics"]["distance_modifier"]
MAX_DIST_VAR      = _P["physics"]["max_dist"] // _P["physics"]["distance_modifier"]
SAFETY_THRESHOLD  = _P["physics"]["safety_threshold"]
DEGREE_MULTIPLIER = _P["physics"]["degree_multiplier"]

ADVISORY_LABELS = {
    "clear":        "Clear (CoC)",
    "weak_left":    "Weak Left",
    "weak_right":   "Weak Right",
    "strong_left":  "Strong Left",
    "strong_right": "Strong Right",
}

# ---------------------------------------------------------------------------
# Contract loading / selection (mirrors acas_input_region.py)
# ---------------------------------------------------------------------------

def load_contracts(specs_path: Path) -> list[dict]:
    with open(specs_path) as f:
        data = json.load(f)
    return data["contracts"]


def select_contract(contracts: list[dict], contract_id: int | None) -> dict:
    if contract_id is not None:
        matches = [c for c in contracts if c["id"] == contract_id]
        if not matches:
            raise ValueError(f"No contract found with id={contract_id}")
        return matches[0]
    for c in contracts:
        if c["n_states_covered"] >= 5:
            return c
    return contracts[0]

# ---------------------------------------------------------------------------
# Panel 1 — Physical state space
# ---------------------------------------------------------------------------

def plot_physical(ax: plt.Axes, contract: dict) -> None:
    heading_var = contract["heading_own_var"]
    heading_deg = heading_var * DEGREE_MULTIPLIER
    x_sign      = contract["x_sign"]
    y_sign      = contract["y_sign"]
    advisory    = contract["forbidden_advisory"]
    dangerous   = contract["dangerous_xy"]

    ax.set_facecolor("#d4edda")

    # Safety circle (distance < 200 ft → radius < 1.5 grid units after rounding)
    theta  = np.linspace(0, 2 * math.pi, 300)
    radius = 1.5
    ax.fill(radius * np.cos(theta), radius * np.sin(theta),
            color="#c0392b", alpha=0.35, zorder=1,
            label=f"Unsafe (< {SAFETY_THRESHOLD} ft)")
    ax.plot(radius * np.cos(theta), radius * np.sin(theta),
            color="#c0392b", linewidth=1.5, zorder=2)

    # Dangerous intruder positions
    dx = [s[0] for s in dangerous]
    dy = [s[1] for s in dangerous]
    ax.scatter(dx, dy, s=70, color="#c0392b", zorder=5,
               label="Dangerous intruder positions")

    # Ownship at origin
    ax.scatter(0, 0, s=120, color="#2471a3", marker="^", zorder=6,
               label="Ownship (origin)")

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

# ---------------------------------------------------------------------------
# Shared NN input computation
# ---------------------------------------------------------------------------

def _nn_points(contract: dict) -> list[tuple[float, float]]:
    """Return (nn_input_1, nn_input_2) for each dangerous state."""
    x_sign      = contract["x_sign"]
    y_sign      = contract["y_sign"]
    heading_var = contract["heading_own_var"]
    return [
        (compute_nn_inputs(xm, ym, x_sign, y_sign, heading_var)[0],
         compute_nn_inputs(xm, ym, x_sign, y_sign, heading_var)[1])
        for xm, ym in contract["dangerous_xy"]
    ]


def _axis_limits(contract: dict, pad_factor: float = 0.5) -> tuple[float, float, float, float]:
    """Shared axis limits for panels 2 and 3 (symmetric padding around bounding box)."""
    lower = contract["nn_input_lower"]
    upper = contract["nn_input_upper"]
    box_w = upper[0] - lower[0]
    box_h = upper[1] - lower[1]
    pad_x = max(box_w * pad_factor, 0.01)
    pad_y = max(box_h * pad_factor, 0.01)
    return lower[0] - pad_x, upper[0] + pad_x, lower[1] - pad_y, upper[1] + pad_y

# ---------------------------------------------------------------------------
# Panel 2 — Continuous NN input space
# ---------------------------------------------------------------------------

def plot_continuous(ax: plt.Axes, contract: dict,
                    pts: list[tuple[float, float]],
                    xlim: tuple, ylim: tuple) -> None:
    lower   = contract["nn_input_lower"]
    upper   = contract["nn_input_upper"]
    box_w   = upper[0] - lower[0]
    box_h   = upper[1] - lower[1]
    advisory = contract["forbidden_advisory"]

    # Filled bounding box
    rect = mpatches.FancyBboxPatch(
        (lower[0], lower[1]), box_w, box_h,
        boxstyle="square,pad=0",
        linewidth=2.0,
        edgecolor="#2e86c1",
        facecolor="#d6eaf8",
        alpha=0.6,
        zorder=2,
        label="CROWN bounding box",
    )
    ax.add_patch(rect)
    ax.scatter([lower[0], upper[0]], [lower[1], upper[1]],
               s=30, color="#2e86c1", marker="x", zorder=4, linewidths=1.5)

    # Exact dangerous state points (inside the box)
    ax.scatter([p[0] for p in pts], [p[1] for p in pts],
               s=70, color="#c0392b", zorder=5,
               label=f"Dangerous states ({contract['n_states_covered']})")

    # Annotation
    ax.text(
        0.97, 0.03,
        "1 CROWN call\ncovers entire shaded region\n(incl. non-integer states)",
        transform=ax.transAxes, fontsize=8,
        verticalalignment="bottom", horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  alpha=0.85, edgecolor="#aaaaaa"),
    )

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("NN input 1: normalized distance", fontsize=10)
    ax.set_ylabel("NN input 2: normalized relative angle", fontsize=10)
    ax.set_title(
        f"Continuous mode  (contract id={contract['id']})\n"
        f"forbidden: {ADVISORY_LABELS[advisory]}",
        fontsize=10,
    )
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(linestyle="--", linewidth=0.4, alpha=0.5)

# ---------------------------------------------------------------------------
# Panel 3 — Discrete NN input space
# ---------------------------------------------------------------------------

def plot_discrete(ax: plt.Axes, contract: dict,
                  pts: list[tuple[float, float]],
                  xlim: tuple, ylim: tuple) -> None:
    lower    = contract["nn_input_lower"]
    upper    = contract["nn_input_upper"]
    box_w    = upper[0] - lower[0]
    box_h    = upper[1] - lower[1]
    n_states = contract["n_states_covered"]
    advisory = contract["forbidden_advisory"]

    # Faint ghost bounding box (spatial reference only)
    ghost = mpatches.FancyBboxPatch(
        (lower[0], lower[1]), box_w, box_h,
        boxstyle="square,pad=0",
        linewidth=1.5,
        edgecolor="#2e86c1",
        facecolor="#d6eaf8",
        alpha=0.10,
        linestyle="--",
        zorder=1,
        label="Continuous box (reference)",
    )
    ax.add_patch(ghost)

    # Individual point markers with call-index labels
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.scatter(xs, ys, s=70, color="#c0392b", zorder=5,
               label=f"Exact state queries ({n_states})")

    for k, (px, py) in enumerate(pts, start=1):
        ax.annotate(
            str(k),
            xy=(px, py),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7,
            color="#7b241c",
        )

    # Annotation
    ax.text(
        0.97, 0.03,
        f"{n_states} CROWN calls\none per exact integer state\n(N = n_states_covered)",
        transform=ax.transAxes, fontsize=8,
        verticalalignment="bottom", horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  alpha=0.85, edgecolor="#aaaaaa"),
    )

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("NN input 1: normalized distance", fontsize=10)
    ax.set_ylabel("NN input 2: normalized relative angle", fontsize=10)
    ax.set_title(
        f"Discrete mode  (contract id={contract['id']})\n"
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
        description="Visualize continuous vs. discrete ACAS Xu A/G contract verification."
    )
    parser.add_argument(
        "--specs", type=Path,
        default=here / "../../contracts/continuous_goals/contract_specs_eps1e4.json",
    )
    parser.add_argument(
        "--output", type=Path,
        default=here / "../acas_discrete_vs_continuous.png",
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

    pts  = _nn_points(contract)
    xlim_pair = _axis_limits(contract)[:2]
    ylim_pair = _axis_limits(contract)[2:]

    fig, (ax_phys, ax_cont, ax_disc) = plt.subplots(1, 3, figsize=(15, 5))

    plot_physical(ax_phys, contract)
    plot_continuous(ax_cont, contract, pts, xlim_pair, ylim_pair)
    plot_discrete(ax_disc, contract, pts, xlim_pair, ylim_pair)

    fig.suptitle(
        "ACAS Xu A/G Contract — Continuous vs. Discrete Verification",
        fontsize=12, fontweight="bold", y=1.01,
    )

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
