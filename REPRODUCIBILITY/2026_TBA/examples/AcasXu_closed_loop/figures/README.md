# ACAS Xu Closed Loop Figures

Generated figures for the ACAS Xu compositional verification example.

All scripts live in `image_scripts/` and write output directly to this directory.
Run all commands from `AcasXu_closed_loop/` (one level up).

---

## Layout

```
figures/
├── image_scripts/
│   ├── acas_input_region.py      # Physical + NN input space for one contract
│   └── acas_output_property.py  # Output scores for a SAT and an UNSAT contract
├── acas_input_region.png         # Generated output
└── acas_output_property.png      # Generated output
```

---

## Figures

### `acas_input_region.png`

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
| `--specs` | `contracts/continuous_goals/acas_contract_specs.json` | Contract spec JSON |
| `--output` | `figures/acas_input_region.png` | Output image path |
| `--contract-id` | *(auto: first with ≥ 5 states)* | Specific contract id to visualize |

**Example — specific contract:**

```bash
python3 figures/image_scripts/acas_input_region.py --contract-id 42
```

---

### `acas_output_property.png`

Two-panel bar chart showing the NN output scores for a **SAT** and an **UNSAT** contract,
illustrating concretely what CROWN is verifying.

- **Left (SAT):** Evaluates the centroid of a SAT contract's bounding box. The forbidden
  advisory (red bar) is never the argmax — the safety property holds at this point.
- **Right (UNSAT):** Samples 500 random inputs from an UNSAT contract's bounding box and
  picks the one where the forbidden advisory scores highest relative to all others.
  Shows a concrete witness where the NN would choose the forbidden advisory.

Requires `onnxruntime` (`pip install onnxruntime`).

**Generate:**

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop
python3 figures/image_scripts/acas_output_property.py
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--results` | `contracts/continuous_goals/enabled_pgd/nn1_crown_results.json` | CROWN results JSON for NN_1 |
| `--specs` | `contracts/continuous_goals/acas_contract_specs.json` | Contract spec JSON (for bounding boxes) |
| `--output` | `figures/acas_output_property.png` | Output image path |
| `--seed` | `42` | RNG seed for reproducible UNSAT sampling |
| `--n-samples` | `500` | Random inputs sampled when searching for UNSAT witness |
