# ACAS Xu YAML Constant Standardization

**Date:** 2026-04-12

**Scope:** Elimination of duplicated physics and NN normalization constants across
`generate_acas_contracts.py`, `generate_acas_tree.py`, and
`figures/image_scripts/acas_input_region.py` in favor of a single YAML source of truth
(`acas_model_params.yaml`), with a companion parser (`extract_acas_constants.py`) that
refreshes the YAML from the authoritative `.tree` template.

---

## Motivation

Prior to this change, the same set of physics and normalization constants was independently
hardcoded in three separate Python files:

| File | Constants duplicated |
|---|---|
| `generate_acas_contracts.py` | 16 constants: all physics, all NN normalization, advisories, network map |
| `generate_acas_tree.py` | 4 constants: `SPEED_OWN`, `SPEED_INT`, `MAX_DIST`, `DISTANCE_MODIFIER` |
| `figures/image_scripts/acas_input_region.py` | 8 constants: `DISTANCE_MODIFIER`, `MAX_DIST_VAR`, `SAFETY_THRESHOLD`, `DEGREE_MULTIPLIER`, `DISTANCE_MEAN`, `DISTANCE_RANGE`, `HEADING_INT` |

All of these values are ultimately sourced from `acas_template_360.tree`'s `constants { }`
block and variable definitions, but had to be manually kept in sync across files. A silent
drift (e.g., changing `degree_multiplier` in the template without updating the Python files)
would produce incorrect contracts or incorrect visualization without any runtime error.

This violates DESIGN-04 (DRY) and DESIGN-15 (Externalize Configuration).

---

## What Changed

### New: `acas_model_params.yaml`

Single source of truth for all model parameters. Organized into four sections:

- **`physics`** — simulation constants (`distance_modifier`, `max_dist`, `speed_own`,
  `speed_int`, `seconds_per_update`, `degree_multiplier`, `heading_int_degrees`,
  `safety_threshold`)
- **`nn_normalization`** — NN input normalization ranges (`distance_mean`, `distance_range`,
  speed mean/range values)
- **`advisories`** — ordered list of advisory names (defines class index mapping)
- **`networks`** — a_prev → `{idx, onnx}` mapping

Two fields in `physics` are **not** present in the `.tree` constants block and are manually
maintained:

- `heading_int_degrees: 225` — the intruder heading is a DEFINE variable in the `.tree`, not
  a named constant.
- `safety_threshold: 200` — the INVARSPEC bound; not stored anywhere in the DSL, only in the
  formal specification.

### New: `extract_acas_constants.py`

Standalone parser that reads `acas_template_360.tree` and refreshes the tree-sourced fields
in `acas_model_params.yaml`, leaving the manually maintained fields untouched.

Fields refreshed from the `.tree` file:

| YAML key | `.tree` source |
|---|---|
| `physics.distance_modifier` | `constants { distance_modifier }` |
| `physics.max_dist` | `constants { max_dist }` |
| `physics.seconds_per_update` | `constants { seconds_per_update }` |
| `physics.degree_multiplier` | `constants { degree_multiplier }` |
| `physics.speed_own` | `variables { env speed_own DEFINE INT assign{result{20}} }` |
| `physics.speed_int` | `variables { env speed_int DEFINE INT assign{result{30}} }` |
| `nn_normalization.*` | `constants { distance_mean, distance_range, speed_*_mean/range }` |

**Note on speed parsing:** The template defines `speed_own` and `speed_int` twice — once
as a formula (`result{(mult, speed_own_var, distance_modifier)}`) and once as a literal
override (`result{20}`). The parser matches only the literal-integer form, which is the
active definition.

Usage:

```bash
python3 extract_acas_constants.py                   # uses defaults
python3 extract_acas_constants.py \
    --tree  acas_template_360.tree \
    --params acas_model_params.yaml
```

### Updated: three Python files

Each file now loads constants from `acas_model_params.yaml` at import time via
`yaml.safe_load`. Derived values (`MAX_DIST_VAR`, `HEADING_INT_VAR`, `ADV_IDX`,
`_NN_INPUT_SPEED_*`, etc.) are still computed in code from the loaded primitives, since YAML
cannot express expressions.

---

## Data Flow After This Change

```
acas_template_360.tree
        │
        │  (run extract_acas_constants.py to refresh)
        ▼
acas_model_params.yaml          ← single source of truth
        │
        ├──► generate_acas_tree.py       (Step 1: fill template → acas_360.tree)
        ├──► generate_acas_contracts.py  (Step 2: enumerate dangerous pairs → contract specs)
        └──► acas_input_region.py        (visualization)
```

`extract_acas_constants.py` is intended as Step 0 in the master reproducibility script,
ensuring the YAML is always consistent with the current template before any downstream
script runs.

---

## What Was Not Changed

- `verify_acas_contracts.py` and `verify_acas_contracts_parallel.py` — these scripts do not
  use the physics constants; they receive pre-computed contract specs as input.
- `acas_config.yaml` — this is operational config for the CROWN verification run
  (timeout, network index, output path) and is distinct from model parameters.
- `heading_int_degrees` and `safety_threshold` in the YAML — manually maintained; no
  automated parser path exists since these values are not in the `.tree` constants block.
