# ACAS Xu Discrete Contract Implementation and Results Report

**Date:** 2026-04-13

**Scope:** Implementation of discrete verification mode (`--discrete`) for the
ACAS Xu closed-loop A/G contract pipeline, modeled on the analogous GRID-05
discrete mode in `grid_world/verify_grid_world_contracts.py`. This report
documents the design, the differences from continuous mode, and the relevant
scripts.

---

## Background: Continuous vs. Discrete Verification

### Continuous mode

In continuous mode, all dangerous `(x_mag, y_mag)` states that share a
`(heading_own_var, x_sign, y_sign, forbidden_advisory)` group are aggregated
into a single bounding box over their NN inputs:

```
lower[i] = min(nn_input_i over all states in group) - eps
upper[i] = max(nn_input_i over all states in group) + eps
```

with `eps = 1e-4`. CROWN then makes **one verification call per contract**
and checks the property:

> ∀ x ∈ [lower, upper] : ∃ j ≠ forbidden_idx such that y[j] > y[forbidden_idx]

If CROWN returns SAT, the NN never selects the forbidden advisory for **any**
real-valued input point in the entire bounding box — including non-integer
states between the discrete grid points. This is a sound over-approximation:
it proves more than just the integer states.

The eps margin ensures states on the exact boundary are covered and provides
a small numerical buffer for CROWN's internal precision.

Contracts and their bounding boxes are pre-computed by `generate_acas_contracts.py`
and stored in `contracts/continuous_goals/contract_specs_eps1e4.json`. There are
**490 contracts** (across all 5 NNs, roughly 98 per NN).

### Discrete mode

Discrete mode verifies the same set of dangerous states, but checks each one
**individually**. For each `(x_mag, y_mag)` pair in a contract's
`dangerous_xy` list, the exact NN inputs are computed and passed to CROWN
with:

```
lower = upper = exact_nn_inputs   (EPS = 0.0)
```

This means each CROWN call is a **point query** — the input region is a
single point in NN input space, not a bounding box. CROWN determines whether
the NN selects the forbidden advisory at that exact point.

Contracts short-circuit on the first UNSAT found: if any dangerous state
causes a violation, the entire contract is immediately UNSAT without
checking the remaining states.

This approach bridges directly to the 2025_NEUS table-based evaluation, where
the NN is queried at exact integer coordinates. Discrete SAT results are
therefore a stronger claim for the integer grid specifically, but do not cover
the continuous space between grid points (unlike continuous mode).

---

## Comparison Table

| Property | Continuous | Discrete |
|---|---|---|
| Input region per contract | Bounding box over all dangerous states | One exact point per dangerous state |
| EPS | `1e-4` | `0.0` |
| CROWN calls per contract | 1 | ≤ `n_states_covered` (short-circuits on UNSAT) |
| Property proved | NN safe for all real inputs in box | NN safe at each exact integer state |
| Strength of claim | Over-approximation (sound for continuous space) | Exact for integer grid only |
| Per-call timeout | `verification.timeout_sec` (30s default) | `verification.discrete_timeout_sec` (5s default) |
| Short-circuit on UNSAT | N/A (single call) | Yes — remaining states skipped |
| Output subdirectory | `contracts/continuous_goals/` | `contracts/discrete_goals/` |

---

## CROWN Call Count

Because each contract covers a variable number of dangerous states, the total
CROWN call count in discrete mode is:

```
total_calls = sum(contract["n_states_covered"] for all contracts for this NN)
```

In the worst case (no UNSATs, no timeouts), every dangerous state in every
contract is checked. In practice, if a contract is UNSAT, the remaining states
in that contract are skipped — but UNSATs are not expected for a correctly
trained network.

Contrast with continuous mode, where the total call count equals the number
of contracts (≈ 98 per NN regardless of how many states each contract covers).

---

## Design Inspiration: GRID-05

The discrete mode was modeled directly on **GRID-05** in
`grid_world/verify_grid_world_contracts.py`. Key parallels:

| Concept | Grid world | ACAS Xu |
|---|---|---|
| Discrete items to check | All integer goal positions `{0,...,6}^2` (49 per contract) | All `dangerous_xy` states stored in the contract spec |
| EPS constant | `DISCRETE_GOAL_EPS = 0.0` (in code) | `discrete_state_eps: 0.0` (in YAML) |
| Per-item timeout | `DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC = 5.0` (in code) | `discrete_timeout_sec: 5.0` (in YAML) |
| Short-circuit | First UNSAT exits the inner loop | Same |
| CLI flag | `--discrete`, `--discrete-timeout` | Same |
| Report field | `mode` string in JSON | Same |

**Key implementation difference:** In grid world, the set of integer goal
positions to check is generated at runtime (a fixed 7×7 grid). In ACAS Xu,
the dangerous states are pre-computed by `generate_acas_contracts.py` and
stored in the contract spec as `dangerous_xy`. The discrete verifier simply
iterates over that pre-computed list — no runtime enumeration of a grid is
needed.

**Another difference:** In grid world, the ownship position also carries an
EPS ball around the integer drone cell (`eps` from the continuous config), so
the input region is still a small box even in discrete mode. In ACAS Xu
discrete mode, `lower = upper = exact_inputs` with no EPS on any dimension —
it is a true point query.

---

## Configuration

All discrete verification parameters live in `verify_acas_contracts_config.yaml`
under the `verification` section, following DESIGN-15 (externalize configuration):

```yaml
verification:
  timeout_sec: 30             # Continuous mode: BaB timeout per contract

  discrete_state_eps: 0.0     # EPS around each exact state point (0.0 = point query)
  discrete_timeout_sec: 5.0   # Default per-state BaB timeout for discrete mode
```

`discrete_state_eps` is exposed as a safety valve: if alpha-beta-CROWN crashes
with `inf`/`NaN` due to zero-width bounds in internal division (a known
edge case in `cut_ops.py`), raising it to `1e-5` resolves the issue without
meaningfully changing the semantics of the verification.

---

## Scripts

### Sequential discrete verification (one NN)

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop

python3 verify_acas_contracts.py \
    --network-idx 1 \
    --output contracts/discrete_goals/aprev_clear_crown_results.json \
    --discrete

# Override per-state timeout if needed
python3 verify_acas_contracts.py \
    --network-idx 1 \
    --output contracts/discrete_goals/aprev_clear_crown_results.json \
    --discrete \
    --discrete-timeout 10
```

### Sequential discrete verification (all 5 NNs)

```bash
cd REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop

./verify_all_discrete_contracts.sh

# Pass extra args (e.g. custom per-state timeout) to all 5 runs
./verify_all_discrete_contracts.sh --discrete-timeout 10
```

Output goes to `contracts/discrete_goals/aprev_*_crown_results.json` (one file per NN).

### Parallel retry (discrete mode)

If some contracts time out in the sequential run, the parallel wrapper can
retry them with a longer per-state timeout:

```bash
python3 verify_acas_contracts_parallel.py \
    --retry-from contracts/discrete_goals/aprev_clear_crown_results.json \
    --timeout 3600 \
    --discrete \
    --discrete-timeout 60 \
    --workers 8
```

---

## Results

*TBD — to be filled in after running the scripts above.*

---

## Notes

- The contract specs JSON (`contract_specs_eps1e4.json`) is reused as-is for
  discrete mode. The `nn_input_lower`/`nn_input_upper` bounding box fields are
  ignored in discrete mode; only `dangerous_xy` is used.
- The `mode` field in each results JSON distinguishes discrete from continuous
  runs at a glance:
  - Continuous: `"mode": "continuous"`
  - Discrete: `"mode": "discrete, EPS=0.0, timeout=5.0s per state"`
- Discrete results are written to `contracts/discrete_goals/` to keep them
  separate from continuous results in `contracts/continuous_goals/`.
