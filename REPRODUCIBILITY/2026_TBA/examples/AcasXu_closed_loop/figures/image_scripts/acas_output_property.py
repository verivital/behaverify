"""
acas_output_property.py

Visualizes the CROWN output safety property for an ACAS Xu A/G contract using
concrete NN evaluations, for both a SAT and an UNSAT contract from NN_1
(aprev_clear.onnx).

For each panel:
  - Loads a contract's bounding box (nn_input_lower / nn_input_upper)
  - Chooses a concrete NN input:
      SAT   → centroid of bounding box
      UNSAT → sample --n-samples random inputs, pick the one where the forbidden
               advisory score is highest relative to all others (CROWN proved such
               an input exists; random sampling finds a near-worst-case witness)
  - Runs the ONNX model on that input via onnxruntime
  - Plots the 5 output scores as a bar chart, with the forbidden advisory in red

Output: a single two-panel figure (SAT left, UNSAT right).

Usage:
    python3 figures/image_scripts/acas_output_property.py

Defaults:
    --results    ../../contracts/continuous_goals/enabled_pgd/aprev_clear_crown_results.json
    --specs      ../../contracts/continuous_goals/contract_specs_eps1e4.json
    --output     ../acas_output_property.png
    --seed       42
    --n-samples  500

Requires: onnxruntime  (pip install onnxruntime)
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

try:
    import onnxruntime as ort
except ImportError as e:
    raise SystemExit(
        "onnxruntime is required: pip install onnxruntime"
    ) from e

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ADVISORY_NAMES = ["clear", "weak_left", "weak_right", "strong_left", "strong_right"]
ADVISORY_DISPLAY = {
    "clear":        "Clear",
    "weak_left":    "Weak\nLeft",
    "weak_right":   "Weak\nRight",
    "strong_left":  "Strong\nLeft",
    "strong_right": "Strong\nRight",
}
COLOR_FORBIDDEN = "#c0392b"   # red
COLOR_NORMAL    = "#aaaaaa"   # gray
COLOR_WINNER    = "#2e86c1"   # blue (for the actual argmax bar)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_results(results_path: Path) -> tuple[str, list[dict]]:
    """Returns (onnx_path, contracts_with_status)."""
    with open(results_path) as f:
        data = json.load(f)
    return data["onnx_path"], data["contracts"]


def load_specs(specs_path: Path) -> dict[int, dict]:
    """Returns {id: contract_spec} with nn_input_lower / nn_input_upper."""
    with open(specs_path) as f:
        data = json.load(f)
    return {c["id"]: c for c in data["contracts"]}


def pick_contract(results: list[dict], status: str) -> dict:
    """Return the first result contract with the given status."""
    for r in results:
        if r["status"] == status:
            return r
    raise ValueError(f"No contract with status={status} found in results.")


# ---------------------------------------------------------------------------
# NN evaluation
# ---------------------------------------------------------------------------

def run_onnx(session: "ort.InferenceSession", inputs: np.ndarray) -> np.ndarray:
    """
    Run ONNX session on a (5,) float32 input vector.
    Returns (5,) float32 output scores.

    The ACAS Xu ONNX files use shape [1, 1, 1, 5] for the input (legacy conv wrapper).
    """
    x = inputs.astype(np.float32).reshape(1, 1, 1, -1)
    input_name = session.get_inputs()[0].name
    return session.run(None, {input_name: x})[0][0]


def centroid(lower: list[float], upper: list[float]) -> np.ndarray:
    return (np.array(lower) + np.array(upper)) / 2.0


def find_unsat_witness(
    session: "ort.InferenceSession",
    lower: list[float],
    upper: list[float],
    forbidden_idx: int,
    n_samples: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Sample n_samples uniform inputs from [lower, upper].
    Return (best_input, best_scores) where forbidden score is highest relative to
    max(others) — the closest we can find to the CROWN counterexample via sampling.
    """
    lo = np.array(lower)
    hi = np.array(upper)
    samples = rng.uniform(lo, hi, size=(n_samples, len(lower)))

    best_input  = samples[0]
    best_scores = run_onnx(session, samples[0])
    best_margin = best_scores[forbidden_idx] - np.max(
        np.delete(best_scores, forbidden_idx)
    )

    for i in range(1, n_samples):
        scores = run_onnx(session, samples[i])
        margin = scores[forbidden_idx] - np.max(np.delete(scores, forbidden_idx))
        if margin > best_margin:
            best_margin = margin
            best_input  = samples[i]
            best_scores = scores

    return best_input, best_scores


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def _denorm_distance(d_norm: float) -> float:
    """Reverse the distance normalization to get approximate feet."""
    return d_norm * 60261.0 + 19791.091


def _denorm_angle(a_norm: float) -> float:
    """Reverse angle normalization to get approximate degrees."""
    return a_norm * 360.0


def plot_output_panel(
    ax: plt.Axes,
    scores: np.ndarray,
    forbidden_idx: int,
    forbidden_advisory: str,
    status: str,
    contract_id: int,
    input_vec: np.ndarray,
    n_states: int,
) -> None:
    """Draw one bar-chart panel (SAT or UNSAT)."""
    labels  = [ADVISORY_DISPLAY[a] for a in ADVISORY_NAMES]
    argmax  = int(np.argmax(scores))

    bar_colors = []
    for i, _ in enumerate(ADVISORY_NAMES):
        if i == forbidden_idx:
            bar_colors.append(COLOR_FORBIDDEN)
        elif i == argmax:
            bar_colors.append(COLOR_WINNER)
        else:
            bar_colors.append(COLOR_NORMAL)

    bars = ax.bar(labels, scores, color=bar_colors, edgecolor="black", linewidth=0.7, zorder=3)

    # Dashed reference line at forbidden advisory score
    ax.axhline(
        scores[forbidden_idx], color=COLOR_FORBIDDEN,
        linestyle="--", linewidth=1.2, zorder=2,
        label=f"Forbidden score ({ADVISORY_NAMES[forbidden_idx]})",
    )

    # Annotate bars with score values
    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.003 * (max(scores) - min(scores) + 1e-6),
            f"{score:.3f}",
            ha="center", va="bottom", fontsize=7.5,
        )

    # Status annotation box — placed below the x-axis to avoid overlapping bars
    if status == "SAT":
        verdict_text = "SAT: forbidden advisory never has max score"
        box_color    = "#d4edda"
    else:
        verdict_text = "UNSAT: found input where forbidden advisory wins"
        box_color    = "#f8d7da"

    ax.text(
        0.5, -0.18, verdict_text,
        transform=ax.transAxes,
        fontsize=9, ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=box_color, edgecolor="#aaaaaa"),
        clip_on=False,
    )

    # Input info box — placed below the verdict box
    dist_ft   = _denorm_distance(input_vec[0])
    angle_deg = _denorm_angle(input_vec[1])
    input_text = (
        f"dist ≈ {dist_ft:.0f} ft    rel_angle ≈ {angle_deg:.1f}°    inputs 3–5: constant"
    )
    ax.text(
        0.5, -0.31, input_text,
        transform=ax.transAxes,
        fontsize=7.5, ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#aaaaaa", alpha=0.9),
        clip_on=False,
    )

    ax.set_ylabel("NN output score", fontsize=10)
    ax.set_title(
        f"{status} example  (contract id={contract_id}, {n_states} state(s) covered)\n"
        f"Forbidden: {ADVISORY_NAMES[forbidden_idx]}   "
        f"Argmax: {ADVISORY_NAMES[argmax]}",
        fontsize=10,
    )
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=0)
    ax.legend(fontsize=8)

    # Legend patches for bar colors
    legend_patches = [
        mpatches.Patch(color=COLOR_FORBIDDEN, label="Forbidden advisory"),
        mpatches.Patch(color=COLOR_WINNER,    label="Actual argmax"),
        mpatches.Patch(color=COLOR_NORMAL,    label="Other advisories"),
    ]
    ax.legend(handles=legend_patches, fontsize=8, loc="lower right")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    here = Path(__file__).parent

    parser = argparse.ArgumentParser(
        description="Visualize ACAS Xu A/G contract output property (SAT vs UNSAT)."
    )
    parser.add_argument(
        "--results", type=Path,
        default=here / "../../contracts/continuous_goals/enabled_pgd/aprev_clear_crown_results.json",
    )
    parser.add_argument(
        "--specs", type=Path,
        default=here / "../../contracts/continuous_goals/contract_specs_eps1e4.json",
    )
    parser.add_argument(
        "--output", type=Path,
        default=here / "../acas_output_property.png",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="RNG seed for UNSAT witness sampling (default: 42)",
    )
    parser.add_argument(
        "--n-samples", type=int, default=500, dest="n_samples",
        help="Number of random inputs to sample when searching for UNSAT witness (default: 500)",
    )
    args = parser.parse_args()

    results_path = args.results.resolve()
    specs_path   = args.specs.resolve()
    output_path  = args.output.resolve()
    rng          = np.random.default_rng(args.seed)

    print(f"Loading results from: {results_path}")
    onnx_rel, result_contracts = load_results(results_path)

    # Resolve ONNX path relative to the results file's parent directory
    onnx_path = (results_path.parent.parent.parent / onnx_rel).resolve()
    if not onnx_path.exists():
        # Fallback: try relative to CWD
        onnx_path = Path(onnx_rel).resolve()
    print(f"ONNX model:  {onnx_path}")

    print(f"Loading specs from:   {specs_path}")
    specs_by_id = load_specs(specs_path)

    session = ort.InferenceSession(str(onnx_path))

    # Pick SAT and UNSAT contracts
    sat_result   = pick_contract(result_contracts, "SAT")
    unsat_result = pick_contract(result_contracts, "UNSAT")

    panels = [
        ("SAT",   sat_result),
        ("UNSAT", unsat_result),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    for ax, (status, result) in zip(axes, panels):
        cid  = result["id"]
        spec = specs_by_id[cid]
        lower        = spec["nn_input_lower"]
        upper        = spec["nn_input_upper"]
        forbidden_idx = result["forbidden_advisory_idx"]
        n_states     = result["n_states_covered"]

        if status == "SAT":
            input_vec = centroid(lower, upper)
            scores    = run_onnx(session, input_vec)
            print(
                f"\nSAT contract id={cid}: evaluating centroid "
                f"→ argmax={ADVISORY_NAMES[int(np.argmax(scores))]}"
            )
        else:
            print(f"\nUNSAT contract id={cid}: sampling {args.n_samples} inputs...")
            input_vec, scores = find_unsat_witness(
                session, lower, upper, forbidden_idx, args.n_samples, rng
            )
            margin = scores[forbidden_idx] - np.max(np.delete(scores, forbidden_idx))
            print(
                f"  Best witness margin={margin:+.4f}  "
                f"(forbidden={ADVISORY_NAMES[forbidden_idx]}, "
                f"score={scores[forbidden_idx]:.4f})"
            )

        plot_output_panel(
            ax, scores, forbidden_idx,
            result["forbidden_advisory"], status,
            cid, input_vec, n_states,
        )

    fig.suptitle(
        "ACAS Xu A/G Contract — Output Property Visualization  (NN_1: aprev_clear.onnx)",
        fontsize=12, fontweight="bold", y=1.02,
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.28)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"\nSaved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
