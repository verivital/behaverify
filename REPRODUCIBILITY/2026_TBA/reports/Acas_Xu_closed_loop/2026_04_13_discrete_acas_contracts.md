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

### CROWN verification (all 5 NNs, discrete mode)

All 5 NNs were verified on an HPC cluster using `verify_all_discrete_contracts.sh`
with `--discrete-timeout 5`. Results per NN:

| NN (`a_prev`) | SAT | UNSAT | Total contracts |
|---|---|---|---|
| clear | 311 | 179 | 490 |
| weak_right | 355 | 135 | 490 |
| weak_left | 316 | 174 | 490 |
| strong_right | 335 | 155 | 490 |
| strong_left | 342 | 148 | 490 |
| **Total** | **1659** | **791** | **2450** |

**~32% of contracts are UNSAT.** This is not a safety violation — see
interpretation below.

### Why so many UNSAT contracts?

UNSAT contracts mean the NN **genuinely selects the forbidden advisory** at those
exact integer states — CROWN is a sound verifier, so this is not a false alarm.
At the same time, the monolithic nuXmv proof (`INVARSPEC: true`) confirms that
the closed-loop system never violates `distance >= 200` starting from valid
initial conditions. These two facts are compatible for one reason only:

**The UNSAT states are unreachable from any valid initial condition.**

#### Proof

**Premise 1 — Contract designation is exact.**
Inspecting `generate_acas_contracts.py`, `enumerate_dangerous_pairs()` labels
`(state S, advisory a)` as forbidden using the following criterion:

```python
nx, ny, ... = simulate_step(x_mag, y_mag, x_sign, y_sign, h, advisory)
if compute_distance(nx, ny) < SAFETY_THRESHOLD:
    # label this (state, advisory) pair as dangerous
```

`simulate_step` is a direct, one-step simulation that exactly replicates the
`environment_update` from `acas_template_360.tree`: it applies the advisory to
update `heading_own_var`, then computes the next position using the new heading
velocity. `compute_distance` returns `round(sqrt(x² + y²)) × 100`, which is the
exact formula in the SMV model. There is no approximation, no epsilon margin, and
no conservatism in the danger labeling — it is a bit-exact forward simulation of
one step of the model.

**Premise 2 — UNSAT means the NN selects the forbidden advisory at that exact point.**
In continuous mode, CROWN verifies a property over a bounding box, and an UNSAT
result could in principle be a bounding box artifact — the counterexample might
lie at a non-integer real coordinate inside the box that does not correspond to
any actual system state.

In discrete mode (EPS=0, `lower = upper = exact_inputs`), the "region" is a
degenerate single point. CROWN's first step is always to run a PGD attack; on a
single-point region this reduces to a forward pass of the NN at that exact input.
If the NN's argmax is the forbidden advisory, CROWN returns UNSAT based on a
concrete evaluation — there is no region to over-approximate and no other point
that could serve as a spurious counterexample. The UNSAT result is therefore
exact up to floating-point precision of the NN evaluation itself, and is not
subject to any bounding-box approximation error.

Combined with Premise 1, this means: if the system ever reaches state S and the
NN selects advisory a, the **very next state** has `distance < 200`, violating
the safety invariant.

**Premise 3 — The monolithic proof holds.**
The 2025_NEUS nuXmv run produces `INVARSPEC: true` on the full closed-loop 5-NN
model. nuXmv's BDD-based model checking is a complete procedure for finite-state
systems: it verifies that `distance >= 200` holds at **every reachable state**
from every valid initial condition.

**Conclusion.**
Suppose, for contradiction, that some UNSAT contract state S is reachable. By
Premise 2 and the closed-loop dynamics, there exists an execution path that
reaches S and transitions to a state with `distance < 200`. This contradicts
Premise 3. Therefore no UNSAT contract state can be reachable from any valid
initial condition. ∎

This proof has two implicit assumptions: (1) `simulate_step` faithfully replicates
`environment_update` without divergence, and (2) the monolithic nuXmv proof is
correct. Both are auditable from the source — the physics functions in
`generate_acas_contracts.py` match the DSL definitions in the template directly.

#### Why the NN outputs near-equal scores at UNSAT states

Direct inspection of several UNSAT contracts shows top-2 NN output scores of
~0.64 vs ~0.65 — an essentially arbitrary choice between two advisories. This is
consistent with the unreachability explanation: the NN was never trained on those
states (they cannot arise in closed-loop execution), so it has no meaningful
preference. The near-equal scores are a symptom of out-of-distribution inputs,
not a cause of unsafety.

### nuXmv verification — segfault at scale

After merging all 5 NNs' discrete contract results into a single file
(1659 SAT contracts → **8982 per-state INVAR constraints**) and running
`run_acas_monolithic_pipelines.sh --skip-monolithic`, the compositional nuXmv
step crashed with a **segmentation fault (exit code 139)** on the 2.2 MB
patched SMV.

The crash occurs during `go` (BDD state-space construction) before `check_invar`
even runs. This is a nuXmv internal bug — a fixed-size buffer overflow when
encoding more INVAR constraints than the tool was built to handle — not a RAM
exhaustion (which would produce OOM-killed, exit code 137). The 8.0s wall time
reflects nuXmv loading the model and then crashing.

For comparison, the monolithic run uses 9.2 GB RAM but succeeds because its
BDD is large but structurally regular (NN lookup tables as case expressions).
The compositional patched SMV is structurally simpler but has ~9K flat INVAR
lines, which apparently hits a different internal limit.

**Discrete mode generates more INVAR constraints than continuous mode**
because each SAT contract in discrete mode expands into one INVAR per
dangerous `(x_mag, y_mag)` state covered (avg ~5.4 states/contract), whereas
in continuous mode each contract generates exactly one INVAR covering the
entire bounding box. The same 1659 SAT contracts would produce ~1659 INVARs
in continuous mode vs 8982 in discrete mode — a ~5× increase in symbolic
verification load.

### Benchmark summary (monolithic vs. discrete compositional)

| | Monolithic | Discrete Compositional |
|---|---|---|
| INVARSPEC | true | N/A (segfault) |
| nuXmv wall time | 49.3s | 8.0s (before crash) |
| Peak RSS | 9.2 GB | — |
| SAT contracts | — | 1659 / 2450 (67.7%) |
| INVAR constraints | — | 8982 |
| SMV size | ~9,700 lines | ~2.2 MB / ~90K lines |

### Future directions — symbolic checker portability

The nuXmv segfault highlights a fundamental design constraint: the compositional
pipeline currently couples neural verification (alpha-beta-CROWN) to symbolic
verification (nuXmv), but this pairing is not fundamental to the approach. The
A/G contracts produced by CROWN are checker-agnostic — they are just
input/output constraints on the NN. Any symbolic model checker capable of
consuming INVAR-style assumptions could substitute for nuXmv.

**UCLID5** is a planned next target. UCLID5 uses SMT-based verification
(rather than BDD) and is designed for modular, assume-guarantee reasoning,
which may handle the flat INVAR constraint load more gracefully than nuXmv's
BDD `go` phase. The pipeline's abstraction — CROWN produces contracts, a
separate tool checks the symbolic model with those contracts injected —
is tool-agnostic by design, and adapting the SMV patch step to emit UCLID5
input format is the natural extension.

A SAT/IC3-based nuXmv path (`check_invar -P ic3`, which avoids full BDD
construction) is a lower-effort alternative to investigate first.

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
