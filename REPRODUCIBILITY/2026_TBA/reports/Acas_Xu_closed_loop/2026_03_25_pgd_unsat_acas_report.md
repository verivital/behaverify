# ACAS Xu Contract Verification Report: PGD Attack Results

**Date:** 2026-03-31

## Summary

All 221 previously-TIMEOUT contracts for NN_1 (`aprev_clear.onnx`) are
**UNSAT** — the neural network genuinely violates these assume-guarantee contracts.

| Metric | Value |
|--------|-------|
| Network | NN_1 (aprev_clear.onnx) |
| Total contracts | 490 |
| SAT (verified safe) | 269 |
| UNSAT (violated) | 221 |
| TIMEOUT | 0 |
| Total wall time | 17.3 seconds |
| Avg UNSAT time | 0.043s |
| Max UNSAT time | 1.299s |
| Min UNSAT time | 0.008s |
| Timestamp | 2026-03-25T14:11:18 |

## Background

The 490 range-based A/G contracts encode dangerous (state, advisory) combinations:
for each contract, the NN must **not** select a forbidden advisory when given inputs
from a specific region of the normalized input space.

Previous runs with alpha-beta-CROWN's branch-and-bound (BaB) solver produced:
- **30s timeout**: 269 SAT, 221 TIMEOUT
- **60s timeout**: 269 SAT, 221 TIMEOUT (no change)
- **120s timeout**: 269 SAT, 221 TIMEOUT (no change)
- **3600s timeout (CPU)**: 269 SAT, 221 TIMEOUT (no change after 18 contracts)
- **600s timeout (GPU, BaB only)**: 269 SAT, 221 TIMEOUT (no change after 18 contracts)

BaB explored up to 146 million domains per contract on the RTX 5090 without convergence,
because it was attempting to **prove** a property that is actually **false**.

## Resolution: PGD Adversarial Attack

Enabling PGD (Projected Gradient Descent) attack mode in alpha-beta-CROWN
(`attack__pgd_order="before"`, 50 restarts) resolved all 221 contracts instantly.
PGD finds concrete counterexample inputs where the NN selects the forbidden advisory,
confirming each contract is UNSAT.

### Configuration

```yaml
device: cuda (NVIDIA GeForce RTX 5090, 32GB)
attack__pgd_order: before
attack__pgd_restarts: 50
bab__timeout: 600
bab__cut__enabled: true
bab__branching__method: sb
```

## Why BaB Failed

The ACAS Xu network (6 hidden layers x 50 neurons, 300 ReLU nodes) produces output
scores for the forbidden advisory that are extremely close to competing advisories.
The worst lower bounds from CROWN's linear relaxation were approximately -0.037,
meaning the relaxation gap prevented BaB from ever proving or disproving the property.

For UNSAT contracts, BaB must find a counterexample to terminate early, but its
search strategy (domain splitting) is not designed for counterexample search.
PGD, being a gradient-based attack, directly optimizes for violations and finds
them in milliseconds.

## Implications for Compositional Verification

With 221/490 contracts UNSAT, the NN_1 network does not satisfy all assume-guarantee
contracts required for the compositional safety proof. The compositional pipeline
will report `INVAR=false` — this is a **real** safety violation, not a spurious
counterexample from incomplete contract coverage.

The 269 SAT contracts confirm that in those input regions, the NN behaves correctly.
The 221 UNSAT contracts identify specific (heading, quadrant, advisory) combinations
where the NN makes unsafe decisions.

## UNSAT Contract Breakdown by Forbidden Advisory

| Forbidden Advisory | Count |
|-------------------|-------|
| strong_right | 65 |
| weak_left | 47 |
| weak_right | 44 |
| strong_left | 39 |
| clear | 26 |

## Full Results

Detailed per-contract results (ID, heading, quadrant, forbidden advisory, states
covered, wall time, status) are saved in:

```
contracts/acas_verified_nn1.json
```
