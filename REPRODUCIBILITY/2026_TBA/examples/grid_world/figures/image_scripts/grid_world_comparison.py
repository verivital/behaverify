"""
grid_world_comparison.py

Stacked-bar timing comparison: monolithic vs compositional (discrete) verification
of grid-world NSBTs, with a verdict table (INVAR / CTL) below.

Monolithic pipeline  (2025_NEUS table approach):
    .tree  →  BehaVerify  →  .smv  →  nuXmv  →  verdict
    Data source: REPRODUCIBILITY/2025_NEUS/examples/grid_world/results/

Compositional pipeline (2026_TBA, discrete mode):
    pre-verified contracts  →  BehaVerify  →  .smv  →  nuXmv  →  verdict
    Data source: REPRODUCIBILITY/2026_TBA/examples/grid_world/results/compositional/discrete_goals/

NOTE: CROWN contract verification (~30–47 min per network) was pre-computed and is
      NOT included in the timing bars. The bars show only the symbolic phase:
      SMV generation + nuXmv.

Usage (from REPRODUCIBILITY/2026_TBA/examples/grid_world/figures/image_scripts/):
    python3 grid_world_comparison.py

Output:
    ../grid_world_comparison.png
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

_HERE    = Path(__file__).parent.resolve()                                            # figures/image_scripts/
_NEUS    = (_HERE / "../../../../../2025_NEUS/examples/grid_world/results").resolve() # REPRODUCIBILITY/2025_NEUS/...
_COMP    = (_HERE / "../../results/compositional/discrete_goals").resolve()            # grid_world/results/...
_OUT_DIR = (_HERE / "..").resolve()                                                    # figures/

# ---------------------------------------------------------------------------
# Networks: (stem, short_label, monolithic_invar, monolithic_ctl)
# short_label is shown on the x-axis
# ---------------------------------------------------------------------------
NETWORKS: list[tuple[str, str, bool, bool]] = [
    ("1000__6_18_0__0100_1", "0100\n(100%)",  True,  True),
    ("1000__6_18_0__0150_1", "0150\n(100%)",  True,  True),
    ("1000__6_18_0__0200_1", "0200\n(100%)",  True,  True),
    ("1000__6_18_0__0250_1", "0250\n(100%)",  True,  True),
    ("1000__6_18_0__0300_1", "0300\n(100%)",  True,  True),
    ("0996__6_18_0__200_1",  "0996\n(99.6%)", False, False),
    ("0995__6_18_0__200_1",  "0995\n(99.5%)", False, False),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_bash_time(s: str) -> float:
    """Parse bash 'time' output line like '1m2.345s' → seconds."""
    m = re.match(r"(\d+)m([\d.]+)s", s.strip())
    if not m:
        raise ValueError(f"Cannot parse time string: {s!r}")
    return float(m.group(1)) * 60.0 + float(m.group(2))


def load_monolithic(stem: str) -> tuple[float, float]:
    """Return (smv_gen_sec, nuxmv_sec) for the monolithic pipeline."""
    timing_lines = (_NEUS / f"timing_table_{stem}.txt").read_text().splitlines()
    nuxmv_lines  = (_NEUS / f"table_{stem}_invar_ctl.txt").read_text().splitlines()

    smv_real   = next(l.split()[1] for l in timing_lines if l.startswith("real"))
    nuxmv_real = next(l.split()[1] for l in reversed(nuxmv_lines) if l.startswith("real"))

    return _parse_bash_time(smv_real), _parse_bash_time(nuxmv_real)


def load_compositional(stem: str) -> tuple[float, float, bool, bool]:
    """Return (smv_gen_sec, nuxmv_sec, invar_passed, ctl_passed)."""
    report = json.loads((_COMP / f"{stem}_discrete" / "pipeline_report.json").read_text())
    smv_sec   = report["steps"]["smv_generation"]["wall_sec"]
    nuxmv_sec = report["steps"]["nuxmv_verification"]["wall_sec"]
    invar     = report["steps"]["nuxmv_verification"]["invarspec"] == "true"
    ctl       = report["steps"]["nuxmv_verification"]["ctlspec"] == "true"
    return smv_sec, nuxmv_sec, invar, ctl


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

mono_smv, mono_nuxmv                    = [], []
comp_smv, comp_nuxmv, comp_invar, comp_ctl = [], [], [], []

for stem, _label, _mi, _mc in NETWORKS:
    ms, mn           = load_monolithic(stem)
    cs, cn, ci, cc   = load_compositional(stem)
    mono_smv.append(ms);   mono_nuxmv.append(mn)
    comp_smv.append(cs);   comp_nuxmv.append(cn)
    comp_invar.append(ci); comp_ctl.append(cc)

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

C_MONO_SMV = "#E07B39"   # warm orange  — monolithic SMV generation
C_MONO_NX  = "#8B2500"   # dark brick   — monolithic nuXmv
C_COMP_SMV = "#5B9BD5"   # steel blue   — compositional SMV generation
C_COMP_NX  = "#1A4E8C"   # dark navy    — compositional nuXmv

fig, (ax_bar, ax_tbl) = plt.subplots(
    2, 1, figsize=(11, 7.5),
    gridspec_kw={"height_ratios": [3, 1]},
)

x     = np.arange(len(NETWORKS))
width = 0.35

# --- Bars ---
ax_bar.bar(x - width / 2, mono_smv,   width, color=C_MONO_SMV, label="Monolithic: SMV generation")
ax_bar.bar(x - width / 2, mono_nuxmv, width, color=C_MONO_NX,  label="Monolithic: nuXmv",
           bottom=mono_smv)

ax_bar.bar(x + width / 2, comp_smv,   width, color=C_COMP_SMV, label="Compositional: SMV generation")
ax_bar.bar(x + width / 2, comp_nuxmv, width, color=C_COMP_NX,  label="Compositional: nuXmv",
           bottom=comp_smv)

ax_bar.set_ylabel("Time (seconds)", fontsize=11)
ax_bar.set_title(
    "Symbolic Verification Time — Monolithic vs. Compositional (Discrete, ε = 0)",
    fontsize=12, fontweight="bold", pad=10,
)
ax_bar.set_xticks(x)
ax_bar.set_xticklabels([lbl for _, lbl, _, _ in NETWORKS], fontsize=9)
ax_bar.set_xlabel("Network (training episodes / accuracy)", fontsize=10, labelpad=6)
ax_bar.legend(loc="upper right", fontsize=9, framealpha=0.85)
ax_bar.grid(axis="y", alpha=0.35, linestyle="--")
ax_bar.set_xlim(-0.6, len(NETWORKS) - 0.4)

max_mono = max(s + n for s, n in zip(mono_smv, mono_nuxmv))
max_comp = max(s + n for s, n in zip(comp_smv, comp_nuxmv))
ax_bar.set_ylim(0, max(max_mono, max_comp) * 1.25)

# Footnote at bottom-left inside plot area
ax_bar.annotate(
    "* CROWN contract verification (~30–47 min per network) was pre-computed;\n"
    "  it is not included in the bars above.",
    xy=(0.01, 0.03), xycoords="axes fraction",
    va="bottom", ha="left", fontsize=7.5, color="#555555",
    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7, ec="#cccccc"),
)

# --- Verdict table ---
ax_tbl.axis("off")

def _v(b: bool) -> str:
    return "true" if b else "false"

col_labels = [lbl.replace("\n", " ") for _, lbl, _, _ in NETWORKS]
row_labels = ["Mono  INVAR", "Mono  CTL", "Comp  INVAR", "Comp  CTL"]

cell_data = [
    [_v(v) for _, _, v, _ in NETWORKS],       # monolithic INVAR
    [_v(v) for _, _, _, v in NETWORKS],        # monolithic CTL
    [_v(v) for v in comp_invar],               # compositional INVAR
    [_v(v) for v in comp_ctl],                 # compositional CTL
]

_GREEN = "#c8e6c9"
_RED   = "#ffcdd2"
cell_colors = [
    [_GREEN if v == "true" else _RED for v in row]
    for row in cell_data
]

tbl = ax_tbl.table(
    cellText=cell_data,
    rowLabels=row_labels,
    colLabels=col_labels,
    cellColours=cell_colors,
    loc="center",
    cellLoc="center",
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1.0, 1.55)

# Bold the row label column
for (row, col), cell in tbl.get_celld().items():
    if col == -1:
        cell.set_text_props(fontweight="bold")

plt.tight_layout(pad=1.5)

out = _OUT_DIR / "grid_world_comparison.png"
plt.savefig(out, bbox_inches="tight", dpi=200)
print(f"Saved: {out}")
