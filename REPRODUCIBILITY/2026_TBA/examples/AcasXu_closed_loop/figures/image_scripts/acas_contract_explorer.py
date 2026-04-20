"""
acas_contract_explorer.py

Interactive Gradio app for exploring ACAS Xu A/G contracts.

Lets you filter and select contracts, toggle between continuous / discrete /
both verification modes, and drag an eps slider to see how the bounding box
grows around the exact dangerous state points.

Panel layout (2×2):
  1 — Original physical space      2 — NN input space
  3 — Verification result bar      4 — Contract metadata

The verification result bar chart (panel 3) is only shown when eps matches a
pre-computed CROWN result set:
  eps = 0      → discrete results  (one CROWN call per dangerous state)
  eps = 1e-4   → continuous+PGD results  (one CROWN call per bounding box)
Any other eps value shows a disclaimer instead.

Usage (from AcasXu_closed_loop/):
    python3 figures/image_scripts/acas_contract_explorer.py

    # Custom specs path or port:
    python3 figures/image_scripts/acas_contract_explorer.py --specs path/to/specs.json
    python3 figures/image_scripts/acas_contract_explorer.py --port 7861
"""

import argparse
import json
import math
import sys
from pathlib import Path

import gradio as gr
import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import yaml

try:
    import onnxruntime as ort
except ImportError as e:
    raise SystemExit(
        "onnxruntime is required: pip install onnxruntime"
    ) from e

# ---------------------------------------------------------------------------
# Reach generate_acas_contracts.py (3 hops up from this script's location)
# ---------------------------------------------------------------------------

_ROOT = Path(__file__).parent.parent.parent   # AcasXu_closed_loop/
sys.path.insert(0, str(_ROOT))
from generate_acas_contracts import compute_nn_inputs  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))         # figures/image_scripts/
from acas_output_property import (                      # noqa: E402
    plot_output_panel, run_onnx, centroid, find_unsat_witness,
)

# ---------------------------------------------------------------------------
# Model parameters
# ---------------------------------------------------------------------------

def _load_params() -> dict:
    with open(_ROOT / "acas_model_params.yaml", encoding="utf-8") as f:
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

QUADRANT_LABELS = {
    "(+,+)": (1,  1),
    "(+,−)": (1, -1),
    "(−,+)": (-1,  1),
    "(−,−)": (-1, -1),
}

# Hover tooltip text shown in the contract details HTML table.
_FIELD_TOOLTIPS: dict[str, str] = {
    "Contract id":
        "Unique identifier for this A/G contract in the pre-computed spec file.",
    "heading_own_var":
        "Integer index (0–39) encoding the ownship's current heading. "
        "Multiply by 9° to get degrees. Fixed across all states in this contract.",
    "Quadrant":
        "Sign of the (x, y) relative coordinates — which of the four spatial "
        "quadrants the intruder occupies relative to the ownship.",
    "Forbidden advisory":
        "The ACAS Xu advisory the NN must NOT output for any dangerous state "
        "in this contract. CROWN verifies this holds over the entire bounding box.",
    "n_states_covered":
        "Number of dangerous (x_mag, y_mag) integer grid states grouped into "
        "this contract. Continuous mode: 1 CROWN call covers all of them. "
        "Discrete mode: 1 CROWN call per state (short-circuits on first UNSAT).",
    "Bounding box dim 1":
        "Range of NN input 1 (normalized distance) across all dangerous states, "
        "with the eps margin added to each side.",
    "Bounding box dim 2":
        "Range of NN input 2 (normalized relative angle to intruder) across all "
        "dangerous states, with the eps margin added to each side.",
    "NN input 3 (intsc °)":
        "NN input 3: normalized intruder heading angle (intersection angle). "
        "Constant for all states in this contract — fixed by heading_own_var and quadrant.",
    "NN input 4 (v_own)":
        "NN input 4: normalized ownship speed. Constant across all contracts "
        "(ownship speed is fixed at 20 raw units).",
    "NN input 5 (v_int)":
        "NN input 5: normalized intruder speed. Constant across all contracts "
        "(intruder speed is fixed at 30 raw units).",
}


def _contract_html_table(rows: list[tuple[str, str]]) -> str:
    """Build an HTML table with hover tooltips on field-name cells."""
    th_style = (
        "padding:6px 10px; text-align:left; background:#f0f0f0; "
        "font-weight:bold; border-bottom:2px solid #ccc;"
    )
    td_field_style = (
        "padding:5px 10px; border-bottom:1px solid #e0e0e0; "
        "font-family:monospace; cursor:help; white-space:nowrap;"
    )
    td_val_style = (
        "padding:5px 10px; border-bottom:1px solid #e0e0e0; "
        "font-family:monospace;"
    )
    rows_html = "".join(
        f'<tr>'
        f'<td style="{td_field_style}" title="{_FIELD_TOOLTIPS.get(field, "")}">'
        f'{field} <span style="color:#999;font-size:0.8em;">ⓘ</span></td>'
        f'<td style="{td_val_style}">{value}</td>'
        f'</tr>'
        for field, value in rows
    )
    return (
        f'<table style="width:100%;border-collapse:collapse;font-size:13px;">'
        f'<thead><tr>'
        f'<th style="{th_style}">Field</th>'
        f'<th style="{th_style}">Value</th>'
        f'</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table>'
    )

# ---------------------------------------------------------------------------
# Contract data (loaded once at startup)
# ---------------------------------------------------------------------------

_ALL_CONTRACTS: list[dict] = []
_SPECS_PATH: Path = (
    _ROOT / "contracts/crown/continuous_goals/contract_specs_eps1e4.json"
)

_RESULTS_DISCRETE: dict[int, dict] = {}     # contract id → result entry (eps=0)
_RESULTS_CONTINUOUS: dict[int, dict] = {}   # contract id → result entry (eps=1e-4)
_ONNX_SESSION = None                        # ort.InferenceSession, set in main()
_RNG = np.random.default_rng(42)            # seeded for reproducible UNSAT witnesses


def load_contracts(path: Path) -> list[dict]:
    with open(path) as f:
        return json.load(f)["contracts"]


def load_results_dict(path: Path) -> dict[int, dict]:
    """Load a CROWN results JSON and return {contract_id: result_entry}."""
    with open(path) as f:
        data = json.load(f)
    return {c["id"]: c for c in data["contracts"]}


def _nn_pts(contract: dict) -> list[tuple[float, float]]:
    """Return (nn_input_1, nn_input_2) for each dangerous state."""
    xs, ys = contract["x_sign"], contract["y_sign"]
    hv = contract["heading_own_var"]
    result = []
    for xm, ym in contract["dangerous_xy"]:
        inp = compute_nn_inputs(xm, ym, xs, ys, hv)
        result.append((inp[0], inp[1]))
    return result


# ---------------------------------------------------------------------------
# Filter helpers
# ---------------------------------------------------------------------------

def _advisory_choices() -> list[str]:
    advs = sorted({c["forbidden_advisory"] for c in _ALL_CONTRACTS})
    return ["All"] + [ADVISORY_LABELS[a] for a in advs]


def _label_to_advisory(label: str) -> str | None:
    if label == "All":
        return None
    return next(k for k, v in ADVISORY_LABELS.items() if v == label)


def filter_and_list(
    heading_var: int,
    quadrant_label: str,
    advisory_label: str,
    min_states: int,
) -> tuple[list[str], str]:
    """Return filtered contract dropdown choices and a default selection."""
    q   = QUADRANT_LABELS.get(quadrant_label)
    adv = _label_to_advisory(advisory_label)

    filtered = [
        c for c in _ALL_CONTRACTS
        if c["heading_own_var"] == int(heading_var)
        and (q  is None or (c["x_sign"] == q[0] and c["y_sign"] == q[1]))
        and (adv is None or c["forbidden_advisory"] == adv)
        and c["n_states_covered"] >= min_states
    ]

    if not filtered:
        return gr.update(choices=[], value=None), "No contracts match the current filters."

    choices = [
        f"id={c['id']}  head={c['heading_own_var']}  "
        f"quad=({'+' if c['x_sign']==1 else '−'},{'+'  if c['y_sign']==1 else '−'})  "
        f"forbid={c['forbidden_advisory']}  n={c['n_states_covered']}"
        for c in filtered
    ]
    return gr.update(choices=choices, value=choices[0]), ""


def _contract_from_choice(choice: str) -> dict | None:
    if not choice:
        return None
    cid = int(choice.split("id=")[1].split()[0])
    matches = [c for c in _ALL_CONTRACTS if c["id"] == cid]
    return matches[0] if matches else None

# ---------------------------------------------------------------------------
# Panel drawing
# ---------------------------------------------------------------------------

def _draw_physical_original(ax: plt.Axes, contract: dict) -> None:
    """
    Panel 1 — Original physical space.

    Shows the ownship at the origin with a heading arrow pointing in its true
    direction, and the intruder at its actual signed (x, y) position using the
    contract's x_sign / y_sign.  All four quadrants are visible.

    The contract's quadrant (x_sign, y_sign) is shaded to show which region
    gets folded into the normalized panel.  Safe integer grid states in that
    quadrant are plotted as small green dots for context; dangerous states are
    larger red dots.

    Heading convention (matches the BehaVerify DSL):
      0° = East (+x), angles increase counter-clockwise.
    """
    heading_deg = contract["heading_own_var"] * DEGREE_MULTIPLIER
    heading_rad = math.radians(heading_deg)
    x_sign      = contract["x_sign"]
    y_sign      = contract["y_sign"]
    advisory    = contract["forbidden_advisory"]
    lim         = MAX_DIST_VAR + 0.5

    ax.set_facecolor("#eaf4fb")

    # Axis lines through origin
    ax.axhline(0, color="#aaaaaa", linewidth=0.8, zorder=0)
    ax.axvline(0, color="#aaaaaa", linewidth=0.8, zorder=0)

    # Highlight the contract quadrant (the region that gets normalized)
    qx0 = 0.0       if x_sign ==  1 else -lim
    qy0 = 0.0       if y_sign ==  1 else -lim
    qw  = lim       # always MAX_DIST_VAR + 0.5 wide
    qh  = lim
    ax.add_patch(mpatches.Rectangle(
        (qx0, qy0), qw, qh,
        facecolor="#fff9c4", alpha=0.55, zorder=1,
        edgecolor="#f39c12", linewidth=1.5,
        label="Contract quadrant",
    ))

    # Safety circle (drawn above quadrant highlight)
    theta  = np.linspace(0, 2 * math.pi, 300)
    radius = 1.5
    ax.fill(radius * np.cos(theta), radius * np.sin(theta),
            color="#c0392b", alpha=0.35, zorder=2,
            label=f"Invariant (< {SAFETY_THRESHOLD} ft)")
    ax.plot(radius * np.cos(theta), radius * np.sin(theta),
            color="#c0392b", linewidth=1.5, zorder=3)

    # Safe integer grid states in the contract quadrant (non-dangerous)
    dangerous_set = {(s[0], s[1]) for s in contract["dangerous_xy"]}
    safe_pts = [
        (x_sign * xm, y_sign * ym)
        for xm in range(MAX_DIST_VAR + 1)
        for ym in range(MAX_DIST_VAR + 1)
        if (xm, ym) not in dangerous_set
    ]
    if safe_pts:
        sx, sy = zip(*safe_pts)
        ax.scatter(sx, sy, s=12, color="#27ae60", alpha=0.55, zorder=4,
                   label=f"Safe states ({len(safe_pts)})")

    # Dangerous intruder positions
    real_dx = [x_sign * s[0] for s in contract["dangerous_xy"]]
    real_dy = [y_sign * s[1] for s in contract["dangerous_xy"]]
    ax.scatter(real_dx, real_dy, s=70, color="#c0392b", zorder=5,
               label=f"Dangerous states ({contract['n_states_covered']})")

    # Ownship at origin
    ax.scatter(0, 0, s=70, color="#2471a3", zorder=6,
               label="Ownship (origin)")

    # Heading arrow — shows true facing direction of ownship
    arrow_len = MAX_DIST_VAR * 0.22
    adx = math.cos(heading_rad) * arrow_len
    ady = math.sin(heading_rad) * arrow_len
    ax.annotate(
        "", xy=(adx, ady), xytext=(0, 0),
        arrowprops=dict(arrowstyle="-|>", color="#2471a3", lw=4.0),
        zorder=7,
    )
    ax.text(adx * 1.12, ady * 1.12, f"{heading_deg}°",
            color="#2471a3", fontsize=15, ha="center", va="center")

    sign_x = "+" if x_sign == 1 else "−"
    sign_y = "+" if y_sign == 1 else "−"
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel("x  (× 100 ft, signed)", fontsize=9)
    ax.set_ylabel("y  (× 100 ft, signed)", fontsize=9)
    ax.set_title(
        f"Original physical space\n"
        f"ownship heading={heading_deg}°  quad=({sign_x},{sign_y})\n"
        f"forbidden: {ADVISORY_LABELS[advisory]}",
        fontsize=9,
    )
    ax.set_aspect("equal")
    ax.legend(fontsize=7, loc="upper right")


def _axis_limits(contract: dict, eps: float) -> tuple[float, float, float, float]:
    lower = contract["nn_input_lower"]
    upper = contract["nn_input_upper"]
    # Expand by eps on each side (mirrors how bounding box is built)
    bx0, bx1 = lower[0] - eps, upper[0] + eps
    by0, by1 = lower[1] - eps, upper[1] + eps
    pad_x = max((bx1 - bx0) * 0.5, 0.02)
    pad_y = max((by1 - by0) * 0.5, 0.02)
    return bx0 - pad_x, bx1 + pad_x, by0 - pad_y, by1 + pad_y


def _draw_nn_space(
    ax: plt.Axes,
    contract: dict,
    pts: list[tuple[float, float]],
    mode: str,          # "Continuous", "Discrete", "Both"
    eps: float,
    show_labels: bool,
) -> None:
    lower = contract["nn_input_lower"]
    upper = contract["nn_input_upper"]

    # Bounding box with live eps applied
    bx0 = lower[0] - eps
    bx1 = upper[0] + eps
    by0 = lower[1] - eps
    by1 = upper[1] + eps
    box_w, box_h = bx1 - bx0, by1 - by0

    xlim0, xlim1, ylim0, ylim1 = _axis_limits(contract, eps)

    if mode == "Continuous":
        rect = mpatches.FancyBboxPatch(
            (bx0, by0), box_w, box_h,
            boxstyle="square,pad=0",
            linewidth=2.0,
            edgecolor="#2e86c1",
            facecolor="#d6eaf8",
            alpha=0.65,
            zorder=2,
            label=f"CROWN bounding box  (eps={eps:.0e})",
        )
        ax.add_patch(rect)
        ax.scatter([bx0, bx1], [by0, by1], s=25, color="#2e86c1",
                   marker="x", zorder=4, linewidths=1.5)
        # Dangerous points inside the box
        ax.scatter([p[0] for p in pts], [p[1] for p in pts],
                   s=60, color="#c0392b", zorder=5,
                   label=f"Dangerous states ({contract['n_states_covered']})")
        ax.text(0.97, 0.03,
                f"1 CROWN call\neps = {eps:.2e}",
                transform=ax.transAxes, fontsize=8,
                verticalalignment="bottom", horizontalalignment="right",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          alpha=0.85, edgecolor="#aaaaaa"))

    else:  # Discrete
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        n  = contract["n_states_covered"]
        ax.scatter(xs, ys, s=80, color="#c0392b", zorder=5,
                   label=f"Exact state queries ({n})")
        if show_labels:
            for k, (px, py) in enumerate(pts, start=1):
                ax.annotate(str(k), xy=(px, py), xytext=(4, 4),
                            textcoords="offset points", fontsize=7,
                            color="#7b241c")
        ax.text(0.97, 0.03,
                f"{contract['n_states_covered']} CROWN calls\n"
                "one per exact integer state",
                transform=ax.transAxes, fontsize=8,
                verticalalignment="bottom", horizontalalignment="right",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          alpha=0.85, edgecolor="#aaaaaa"))

    ax.set_xlim(xlim0, xlim1)
    ax.set_ylim(ylim0, ylim1)
    ax.set_xlabel("NN input 1: normalized distance", fontsize=9)
    ax.set_ylabel("NN input 2: normalized relative angle", fontsize=9)
    ax.set_title(f"NN input space  [{mode} mode]", fontsize=9)
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(linestyle="--", linewidth=0.4, alpha=0.5)


_EPS_CONTINUOUS = 1e-4
_EPS_TOL        = 1e-6


def _draw_bar_panel(ax: plt.Axes, contract: dict, eps: float) -> None:
    """
    Panel 3 — CROWN verification result bar chart.

    Shown only when eps matches a pre-computed result set:
      eps ≈ 0      → discrete results  (one CROWN call per dangerous state)
      eps ≈ 1e-4   → continuous+PGD results  (one CROWN call per bounding box)
    Any other eps value renders a disclaimer instead.
    """
    if eps < _EPS_TOL:
        results    = _RESULTS_DISCRETE
        mode_label = "discrete  (eps=0)"
    elif abs(eps - _EPS_CONTINUOUS) < _EPS_TOL:
        results    = _RESULTS_CONTINUOUS
        mode_label = "continuous+PGD  (eps=1e-4)"
    else:
        ax.axis("off")
        ax.text(
            0.5, 0.5,
            "Bar chart only available for\n"
            "eps=0 (discrete) or eps=1e-4 (continuous PGD).\n"
            "Adjust the slider to one of those values.",
            transform=ax.transAxes,
            ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#fff9c4",
                      edgecolor="#f39c12", alpha=0.9),
        )
        return

    result = results.get(contract["id"])
    if result is None:
        ax.axis("off")
        ax.text(
            0.5, 0.5,
            f"No verification result found\nfor contract id={contract['id']}.",
            transform=ax.transAxes,
            ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#fdecea",
                      edgecolor="#c0392b", alpha=0.9),
        )
        return

    status        = result["status"]
    forbidden_idx = result["forbidden_advisory_idx"]
    lower         = contract["nn_input_lower"]
    upper         = contract["nn_input_upper"]
    n_states      = contract["n_states_covered"]

    if status == "SAT":
        input_vec = centroid(lower, upper)
        scores    = run_onnx(_ONNX_SESSION, input_vec)
    else:  # UNSAT
        input_vec, scores = find_unsat_witness(
            _ONNX_SESSION, lower, upper, forbidden_idx, 500, _RNG
        )

    plot_output_panel(
        ax, scores, forbidden_idx,
        contract["forbidden_advisory"], status,
        contract["id"], input_vec, n_states,
    )
    ax.set_title(ax.get_title() + f"\n[{mode_label}]", fontsize=8)

# ---------------------------------------------------------------------------
# Main render function (called by Gradio)
# ---------------------------------------------------------------------------

def _empty_fig(msg: str = "") -> plt.Figure:
    fig = plt.figure(figsize=(5, 4))
    if msg:
        plt.text(0.5, 0.5, msg, ha="center", va="center", fontsize=11)
    plt.axis("off")
    return fig


def render(
    contract_choice: str,
    mode: str,
    eps: float,
    show_labels: bool,
) -> tuple:
    """Return (fig_orig, fig_nn, fig_bar, html) for the four Gradio panels."""
    if mode == "Discrete":
        eps = 0.0
    contract = _contract_from_choice(contract_choice)
    if contract is None:
        plt.close("all")
        empty = _empty_fig("No contract selected.")
        return empty, empty, empty, ""

    pts = _nn_pts(contract)
    heading_deg = contract["heading_own_var"] * DEGREE_MULTIPLIER
    sign_x = "+" if contract["x_sign"] == 1 else "−"
    sign_y = "+" if contract["y_sign"] == 1 else "−"

    plt.close("all")

    # Panel 1 — original physical space
    fig_orig, ax_orig = plt.subplots(1, 1, figsize=(6, 5))
    _draw_physical_original(ax_orig, contract)
    fig_orig.tight_layout()

    # Panel 2 — NN input space
    fig_nn, ax_nn = plt.subplots(1, 1, figsize=(6, 5))
    _draw_nn_space(ax_nn, contract, pts, mode, eps, show_labels)
    fig_nn.tight_layout()

    # Panel 3 — verification result bar chart
    fig_bar, ax_bar = plt.subplots(1, 1, figsize=(6, 5))
    _draw_bar_panel(ax_bar, contract, eps)
    fig_bar.tight_layout()

    # Panel 4 — contract metadata as an HTML table with hover tooltips
    lower = contract["nn_input_lower"]
    upper = contract["nn_input_upper"]
    table_rows = [
        ("Contract id",          str(contract["id"])),
        ("heading_own_var",      f"{contract['heading_own_var']} ({heading_deg}°)"),
        ("Quadrant",             f"({sign_x}, {sign_y})"),
        ("Forbidden advisory",   ADVISORY_LABELS[contract["forbidden_advisory"]]),
        ("n_states_covered",     str(contract["n_states_covered"])),
        ("Bounding box dim 1",   f"[{lower[0]:.4f}, {upper[0]:.4f}]"),
        ("Bounding box dim 2",   f"[{lower[1]:.4f}, {upper[1]:.4f}]"),
        ("NN input 3 (intsc °)", f"[{lower[2]:.4f}, {upper[2]:.4f}]"),
        ("NN input 4 (v_own)",   f"{lower[3]:.4f}"),
        ("NN input 5 (v_int)",   f"{lower[4]:.4f}"),
    ]

    return fig_orig, fig_nn, fig_bar, _contract_html_table(table_rows)

# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

def build_ui() -> gr.Blocks:
    advisory_choices = _advisory_choices()
    quadrant_choices = ["All"] + list(QUADRANT_LABELS.keys())

    # Pick a default heading_var that has at least one contract with >= 5 states
    default_heading = next(
        (c["heading_own_var"] for c in _ALL_CONTRACTS if c["n_states_covered"] >= 5),
        _ALL_CONTRACTS[0]["heading_own_var"] if _ALL_CONTRACTS else 0,
    )
    max_heading = max(c["heading_own_var"] for c in _ALL_CONTRACTS)

    # Build initial contract list for the default heading
    _init_choices, _ = filter_and_list(default_heading, "All", "All", 1)
    init_choices = _init_choices["choices"]
    init_value   = _init_choices["value"]

    with gr.Blocks(title="ACAS Xu Contract Explorer") as demo:
        gr.Markdown(
            "## ACAS Xu A/G Contract Explorer\n"
            "Filter contracts by heading, quadrant, and forbidden advisory. "
            "Select a contract to visualize its input region under continuous "
            "and discrete verification modes. Drag the **eps** slider to see "
            "how the bounding box grows around the exact dangerous state points.\n\n"
            "Set **eps=0** or **eps=1e-4** to load the CROWN verification result "
            "bar chart in panel 3."
        )

        with gr.Row():
            # ── Left column: filters + contract picker ──────────────────────
            with gr.Column(scale=1, min_width=280):
                gr.Markdown("### Filters")
                heading_sl = gr.Slider(
                    minimum=0, maximum=max_heading, step=1,
                    value=default_heading,
                    label="Heading (var)",
                    info=f"heading_own_var × {DEGREE_MULTIPLIER}° = actual heading")
                quadrant_dd = gr.Dropdown(
                    quadrant_choices, value="All", label="Quadrant")
                advisory_dd = gr.Dropdown(
                    advisory_choices, value="All", label="Forbidden advisory")
                min_states_sl = gr.Slider(
                    1, 20, value=1, step=1, label="Min states covered")

                gr.Markdown("### Contract")
                contract_dd = gr.Dropdown(
                    init_choices, value=init_value,
                    label="Select contract", interactive=True)
                filter_status = gr.Markdown("")

                gr.Markdown("### Display")
                mode_radio = gr.Radio(
                    ["Continuous", "Discrete"],
                    value="Continuous", label="Verification mode")
                eps_sl = gr.Slider(
                    minimum=0.0, maximum=0.05, value=1e-4, step=1e-5,
                    label="eps (bounding box margin)",
                    info="0 = tight hull of exact points; 1e-4 = contract default")
                labels_cb = gr.Checkbox(
                    value=True, label="Show state index labels (discrete)")

            # ── Right column: 2×2 grid of separate Gradio components ─────────
            with gr.Column(scale=3):
                with gr.Row():
                    plot_orig = gr.Plot(label="1 — Original physical space")
                    plot_nn   = gr.Plot(label="2 — NN input space")
                with gr.Row():
                    plot_bar  = gr.Plot(label="3 — Contract verification result (SAT / UNSAT)")
                    with gr.Column():
                        gr.Markdown("#### 4 — Contract Details")
                        gr.Markdown(
                            "*Hover over a field name for a description.*",
                            elem_classes=["hint-text"],
                        )
                        info_html = gr.HTML()

        render_outputs = [plot_orig, plot_nn, plot_bar, info_html]

        # ── Wire up filters → contract list ─────────────────────────────────
        filter_inputs = [heading_sl, quadrant_dd, advisory_dd, min_states_sl]
        for ctrl in filter_inputs:
            ctrl.change(
                fn=filter_and_list,
                inputs=filter_inputs,
                outputs=[contract_dd, filter_status],
            )

        # ── Wire up contract/mode/eps/labels → panels ────────────────────────
        render_inputs = [contract_dd, mode_radio, eps_sl, labels_cb]
        for ctrl in render_inputs:
            ctrl.change(
                fn=render,
                inputs=render_inputs,
                outputs=render_outputs,
            )

        # ── Disable eps slider when Discrete is selected (eps is always 0) ──
        def _toggle_eps(mode: str):
            if mode == "Discrete":
                return gr.update(interactive=False, value=0.0)
            return gr.update(interactive=True, value=1e-4)

        mode_radio.change(fn=_toggle_eps, inputs=[mode_radio], outputs=[eps_sl])

        # ── Initial render ───────────────────────────────────────────────────
        demo.load(
            fn=render,
            inputs=render_inputs,
            outputs=render_outputs,
        )

    return demo

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    global _ALL_CONTRACTS, _SPECS_PATH, _RESULTS_DISCRETE, _RESULTS_CONTINUOUS, _ONNX_SESSION

    parser = argparse.ArgumentParser(
        description="Interactive ACAS Xu contract explorer (Gradio)."
    )
    parser.add_argument(
        "--specs", type=Path, default=_SPECS_PATH,
        help="Path to contract specs JSON "
             "(default: contracts/crown/continuous_goals/contract_specs_eps1e4.json)",
    )
    parser.add_argument(
        "--results-discrete", type=Path,
        default=_ROOT / "contracts/crown/discrete_goals/aprev_clear_crown_results.json",
        dest="results_discrete",
        help="CROWN results JSON for discrete mode (eps=0)",
    )
    parser.add_argument(
        "--results-continuous", type=Path,
        default=_ROOT / "contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json",
        dest="results_continuous",
        help="CROWN results JSON for continuous+PGD mode (eps=1e-4)",
    )
    parser.add_argument(
        "--port", type=int, default=7860,
        help="Port to serve the Gradio app on (default: 7860)",
    )
    parser.add_argument(
        "--share", action="store_true",
        help="Create a public shareable Gradio link",
    )
    args = parser.parse_args()

    _SPECS_PATH    = Path(args.specs).resolve()
    _ALL_CONTRACTS = load_contracts(_SPECS_PATH)

    # Keep only one NN's contracts for the explorer (NN_1 / aprev_clear = network_idx 1)
    # All NNs share the same physical state structure; filtering avoids 5× duplicate entries.
    nn1 = [c for c in _ALL_CONTRACTS if c.get("network_idx") == 1]
    if nn1:
        _ALL_CONTRACTS = nn1

    print(f"Loaded {len(_ALL_CONTRACTS)} contracts from {_SPECS_PATH}")

    # Load verification results
    disc_path = Path(args.results_discrete).resolve()
    cont_path = Path(args.results_continuous).resolve()
    _RESULTS_DISCRETE   = load_results_dict(disc_path)
    _RESULTS_CONTINUOUS = load_results_dict(cont_path)
    print(f"Discrete results:   {len(_RESULTS_DISCRETE)} entries from {disc_path}")
    print(f"Continuous results: {len(_RESULTS_CONTINUOUS)} entries from {cont_path}")

    # Load ONNX model — onnx_path in the results JSON is relative to _ROOT
    with open(cont_path) as f:
        cont_data = json.load(f)
    onnx_rel  = cont_data["onnx_path"]
    onnx_path = (_ROOT / onnx_rel).resolve()
    if not onnx_path.exists():
        onnx_path = Path(onnx_rel).resolve()
    print(f"ONNX model: {onnx_path}")
    _ONNX_SESSION = ort.InferenceSession(str(onnx_path))

    print(f"Serving on http://localhost:{args.port}")

    demo = build_ui()
    demo.launch(server_port=args.port, share=args.share)


if __name__ == "__main__":
    main()
