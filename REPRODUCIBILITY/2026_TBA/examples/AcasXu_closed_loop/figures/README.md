# ACAS Xu Closed Loop Figures

Generated figures and interactive demos for the ACAS Xu compositional
verification example.

All scripts live in `image_scripts/` and write output directly to this
directory. Run all commands from `AcasXu_closed_loop/` (one level up).

---

## Quick start — interactive demo

If you want to understand this example before reading anything else, run
the Gradio contract explorer app:

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
pip install gradio          # one-time, if not already installed
python3 figures/image_scripts/acas_contract_explorer.py
# → open http://localhost:7860 in your browser
```

The app opens a 2×2 interactive dashboard — no CROWN or nuXmv needed.
See [the app section below](#acas_contract_explorerpyinteractive-app) for full details.

---

## Layout

```
figures/
├── image_scripts/
│   ├── acas_contract_explorer.py     # Interactive Gradio demo app  ← start here
│   ├── acas_discrete_vs_continuous.py  # Static 3-panel comparison figure
│   ├── acas_input_region.py          # Physical + NN input space for one contract
│   └── acas_output_property.py       # Output scores for SAT and UNSAT contracts
├── acas_discrete_vs_continuous.png   # Generated output
├── acas_input_region.png             # Generated output
└── acas_output_property.png          # Generated output
```

---

## `acas_contract_explorer.py` — Interactive app

An interactive Gradio dashboard that lets you explore every A/G contract in
the pre-computed spec file without running any verification. Designed as the
fastest way to build intuition for how the compositional pipeline works.

### What it shows

The UI is a 2×2 grid:

| | Left | Right |
|---|---|---|
| **Top** | Original physical state space | Normalized physical state space |
| **Bottom** | NN input space (continuous / discrete / both) | Contract details table |

**Original physical space (top-left):** The full signed `(x, y)` plane as the
intruder sees it. The active quadrant is highlighted in yellow; safe integer
states appear as small green dots; dangerous states are large red dots. A
heading arrow from the origin shows the ownship's current heading.

**Normalized physical space (top-right):** The canonical relative-coordinate
view: ownship always at origin, axes in magnitude units (× 100 ft). Unsafe
safety circle (< 200 ft radius) shown in red.

**NN input space (bottom-left):** The CROWN verification region drawn over
NN inputs 1 (normalized distance) and 2 (normalized relative angle):
- **Continuous mode** — filled blue bounding box; one CROWN call covers the
  entire shaded region including non-integer states between grid points.
- **Discrete mode** — faint ghost box for reference; individual labeled red
  dots, one per exact integer dangerous state (each requires its own CROWN call).
- **Both** — overlay of continuous box and discrete points simultaneously.

Dragging the **eps** slider grows or shrinks the bounding box margin live, so
you can see exactly how eps affects the over-approximation.

**Contract details (bottom-right):** A Gradio table listing the contract id,
heading, quadrant, forbidden advisory, state count, and all five NN input
bounds for the selected contract.

### Controls

| Control | Description |
|---|---|
| **Heading (var)** slider | Filter by `heading_own_var` (0–39; multiply by 9° for degrees) |
| **Quadrant** dropdown | Filter by `(x_sign, y_sign)` quadrant |
| **Forbidden advisory** dropdown | Filter by which advisory is forbidden |
| **Min states covered** slider | Show only contracts covering ≥ N dangerous states |
| **Select contract** dropdown | Choose among matching contracts |
| **Verification mode** radio | Continuous / Discrete / Both |
| **eps** slider | Bounding box margin (0 = exact hull, 1e-4 = contract default) |
| **Show state index labels** checkbox | Number each discrete point (CROWN call order) |

### Launch

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
python3 figures/image_scripts/acas_contract_explorer.py
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--specs` | `contracts/continuous_goals/contract_specs_eps1e4.json` | Contract spec JSON |
| `--port` | `7860` | Gradio server port |
| `--no-browser` | *(flag)* | Do not auto-open browser tab |

**Requirements:** `gradio`, `matplotlib`, `numpy`, `yaml` (no CROWN or nuXmv needed).

---

## `acas_discrete_vs_continuous.py` — Static comparison figure

Three-panel figure contrasting continuous and discrete contract verification
for a single representative contract.

- **Left — Physical state space:** Dangerous intruder positions and safety boundary.
- **Middle — Continuous NN input space:** One CROWN call covers the entire bounding
  box, including non-integer states between the grid points.
- **Right — Discrete NN input space:** One CROWN call per exact integer dangerous
  state; a faint ghost box shows how much space the discrete checks leave uncovered
  relative to the continuous over-approximation.

Panels 2 and 3 share identical axis ranges for direct visual comparison.

**Generate:**

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
python3 figures/image_scripts/acas_discrete_vs_continuous.py
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--specs` | `contracts/continuous_goals/contract_specs_eps1e4.json` | Contract spec JSON |
| `--output` | `figures/acas_discrete_vs_continuous.png` | Output image path |
| `--contract-id` | *(auto: first with ≥ 5 states)* | Specific contract id to visualize |

---

## `acas_input_region.py` — Single-contract static figure

Two-panel visualization of a single A/G contract:

- **Left — Physical state space:** 10×10 (x\_var, y\_var) grid. Green cells are safe
  (distance ≥ 200 ft), red cells are already-unsafe states. Red dots mark the
  dangerous states covered by the contract; the dashed circle marks the 200 ft
  safety boundary. The ownship sits at the origin.

- **Right — Normalized NN input space:** The CROWN bounding box is drawn as a blue
  rectangle over inputs 1 (normalized distance) and 2 (normalized relative angle).
  Inputs 3–5 are constants for this contract and are listed in the annotation box.

**Generate:**

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
python3 figures/image_scripts/acas_input_region.py
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--specs` | `contracts/continuous_goals/contract_specs_eps1e4.json` | Contract spec JSON |
| `--output` | `figures/acas_input_region.png` | Output image path |
| `--contract-id` | *(auto: first with ≥ 5 states)* | Specific contract id to visualize |

---

## `acas_output_property.py` — NN output scores figure

Two-panel bar chart showing the NN output scores for a **SAT** and an **UNSAT**
contract, illustrating concretely what CROWN is verifying.

- **Left (SAT):** Evaluates the centroid of a SAT contract's bounding box. The
  forbidden advisory (red bar) is never the argmax — the safety property holds.
- **Right (UNSAT):** Samples 500 random inputs from an UNSAT contract's bounding
  box and picks the one where the forbidden advisory scores highest. Shows a
  concrete witness where the NN would choose the forbidden advisory.

Requires `onnxruntime` (`pip install onnxruntime`).

**Generate:**

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
python3 figures/image_scripts/acas_output_property.py
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--results` | `contracts/continuous_goals/enabled_pgd/aprev_clear_crown_results.json` | CROWN results JSON for NN_1 |
| `--specs` | `contracts/continuous_goals/contract_specs_eps1e4.json` | Contract spec JSON (for bounding boxes) |
| `--output` | `figures/acas_output_property.png` | Output image path |
| `--seed` | `42` | RNG seed for reproducible UNSAT sampling |
| `--n-samples` | `500` | Random inputs sampled when searching for UNSAT witness |
