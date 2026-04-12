# ACAS Xu Contract Architecture Audit

**Date:** 2026-04-11

**Scope:** Audit of `generate_acas_contracts.py` and `verify_acas_contracts.py` against
the NeuS 2025 paper (Serbinowska et al., *Neuro-Symbolic Behavior Trees and Their Verification*)
and the ACAS Xu original source (Julian et al. 2016).

---

## Overall Assessment

The A/G contract approach implemented in `2026_TBA` is the compositional verification framework
proposed as future work in Section 5 of the NeuS 2025 paper. The paper itself uses only the
table-based nuXmv encoding for ACAS Xu; the CROWN-based contract approach here is the extension.
The implementation direction is sound and well-aligned with the paper's intent.

---

## High Confidence

### 1. Input normalization constants

`generate_acas_contracts.py` uses:
```
DISTANCE_MEAN  = 19791.091,  DISTANCE_RANGE  = 60261.0
SPEED_OWN_MEAN =    650.0,   SPEED_OWN_RANGE =  1100.0
SPEED_INT_MEAN =    600.0,   SPEED_INT_RANGE =  1200.0
```

These match the normalization constants from the original ACAS Xu NNET files (Julian et al. 2016).
The NeuS 2025 paper gives the example `(50000 - 19791.091) / 60021 = 0.498` — the denominator
`60021` appears to be a typo for `60261`, and `0.498` is slightly off as a result. The code's
value of `60261` is correct.

The angle inputs (relative_angle_adjusted, intersect_angle_adjusted) are divided by 360 to
normalize to a bounded range. Speed inputs are constants: all states use the same fixed
`speed_own = 20` and `speed_int = 30`, so inputs 4 and 5 are the same for every contract.

### 2. Output constraint formulation

`verify_acas_contracts.py` checks:

```
∀x ∈ [lower, upper]: ∃j ≠ forbidden_idx such that y[j] > y[forbidden_idx]
```

This is the correct safety property: for every input state in the contract's bounding box, the
NN prefers some other advisory over the forbidden one, i.e., the forbidden advisory is never
chosen. CROWN's SAT result means this holds for the entire input region — the A/G guarantee is
sound for all states covered by the contract.

### 3. NN selection by a_prev

The mapping `a_prev → (network_idx, onnx_path)` correctly reflects the closed-loop selector:
τ=0 is fixed for all NNs (N_{γ,1} in the paper's notation), and γ corresponds to the previous
advisory. Five NNs, one per a_prev value. Network indices 1–5 are internal labels only; the
key correctness constraint is that each a_prev maps to exactly one ONNX file.

### 4. Physics model

`simulate_step` applies heading first, then computes position using the updated heading. This
correctly matches the sequential `environment_update` ordering in the BehaVerify DSL, where
`heading_own_var` is assigned before the position variables. Dangerous pair enumeration is
logically sound: a (state, advisory) pair is dangerous iff the current distance is safe
(≥ 200) but the next distance after applying that advisory drops below 200.

### 5. Bounding box construction

For each `(heading_own_var, x_mult, y_mult, forbidden_advisory)` group, a single bounding box
is computed over the NN inputs of all dangerous states in that group. Inputs 3/4/5 are constants
for fixed heading, so only inputs 1 (distance) and 2 (relative angle) vary within a group. The
eps margin (`1e-4` by default) is added symmetrically on each side. This is sound: if CROWN
verifies the property on the enlarged box, it holds on the exact convex hull of dangerous states.

---

## Skeptical / Needs Verification

### 1. Output class index ordering (MEDIUM risk)

`generate_acas_contracts.py` defines:
```python
ADVISORIES = ['clear', 'weak_left', 'weak_right', 'strong_left', 'strong_right']
# → clear=0, weak_left=1, weak_right=2, strong_left=3, strong_right=4
```

The standard ACAS Xu convention from Julian et al. is CoC=0, WL=1, WR=2, SL=3, SR=4, which
matches. However, the `.tree` file's advisory enum may use a different order
(e.g., `{clear, weak_right, weak_left, strong_right, strong_left}`). The `forbidden_advisory_idx`
in the contracts is derived from `ADV_IDX` above — **not** from the DSL enum order — so the
contracts are correct only if the ONNX files' output neurons are actually ordered 0=CoC, 1=WL,
2=WR, 3=SL, 4=SR.

**Recommended check:** Load one ONNX file and run a known input through it; compare the argmax
to the expected advisory from the original ACAS Xu lookup table for that input.

### 2. PGD not wired up despite folder naming (LOW-MEDIUM risk)

`build_crown_config` in `verify_acas_contracts.py` hardcodes `pgd_order="skip"` with no YAML
override path:

```python
def build_crown_config(cfg: dict[str, Any]) -> Any:
    return (
        ConfigBuilder.from_defaults()
        .set(general__device="cpu")
        .set(attack__pgd_order="skip")          # always skipped
        .set(bab__timeout=cfg["verification"]["timeout_sec"])
        ()
    )
```

The existing results live in `contracts/continuous_goals/enabled_pgd/`, implying PGD was enabled
for that run. Either the results predate this code version, or the folder name is wrong. Either
way, when `disabled_pgd/` results are added later, the distinction will be meaningless unless
PGD toggling is wired up through the YAML config (mirroring grid_world's approach).

**Recommended fix:** Add a `pgd_enabled` boolean to the YAML config and have `build_crown_config`
read it to set `pgd_order` to `"before"` or `"skip"` accordingly.

### 3. Angle computation matching the DSL (LOW risk, pre-verified implicitly)

`compute_relative_angle_adjusted` and `compute_intersect_angle_adjusted` claim to match the
DEFINE blocks in `acas_template_360.tree`. This was not independently verified by tracing
through the tree file's case statements side-by-side. The physics simulation was used to generate
the dangerous pairs, so if these angle functions are wrong, the contract bounding boxes cover the
wrong NN inputs — contracts would be formally verified but for states that don't correspond to
the actual dangerous system states.

**Recommended check:** Pick 2–3 concrete (x_var, y_var, x_mult, y_mult, heading_own_var) states,
compute the NN inputs via `generate_acas_contracts.py`'s functions, and compare against what the
BehaVerify-generated Python implementation of the tree computes for those same states.

---

## Summary Table

| Item | Confidence | Note |
|---|---|---|
| Input normalization constants | High | Code is correct; paper has a minor typo |
| Safety property formulation | High | ∃j: y[j] > y[forbidden] for all inputs in box |
| NN selection by a_prev | High | τ=0 fixed, γ=a_prev, correct mapping |
| Physics / dangerous pair enumeration | High | Heading-first update order is correct |
| Bounding box construction + eps | High | Sound over-approximation |
| Output class index ordering | Medium | Matches standard convention; verify against ONNX |
| PGD enabled/disabled wiring | Medium | Hardcoded skip; folder name may be misleading |
| Angle computation vs DSL | Low risk | Not line-by-line verified against template |