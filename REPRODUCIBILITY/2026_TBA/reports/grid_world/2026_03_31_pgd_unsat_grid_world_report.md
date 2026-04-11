# Grid World Contract Verification Report: PGD Attack Results

**Date:** 2026-04-07

## Summary

All five 100%-accurate grid-world NNs produce a consistent ~50/50 SAT/UNSAT split
when contracts are verified with PGD attack enabled. Zero timeouts remain — PGD
resolved every contract that BaB-only verification left as TIMEOUT.

| Network | Accuracy | SAT | UNSAT | TIMEOUT | Total |
|---------|----------|-----|-------|---------|-------|
| `1000__6_18_0__0100_1` | 100% | 18 | 20 | 0 | 38 |
| `1000__6_18_0__0150_1` | 100% | 19 | 19 | 0 | 38 |
| `1000__6_18_0__0200_1` | 100% | 16 | 22 | 0 | 38 |
| `1000__6_18_0__0250_1` | 100% | 17 | 21 | 0 | 38 |
| `1000__6_18_0__0300_1` | 100% | 17 | 21 | 0 | 38 |

Configuration: `attack__pgd_order=before`, `pgd_restarts=50`, `bab__timeout=60s`,
`drone EPS=0.001`, `goal=[0,6]²`.
Results in `contracts/pgd/<name>_pgd60.json`.

---

## Background: What Changed from BaB-Only

Previous BaB-only runs (with `attack__pgd_order=skip`) produced TIMEOUT for the same
contracts that PGD now resolves as UNSAT:

| Network | BaB SAT | BaB UNSAT | BaB TIMEOUT | BaB timeout_sec |
|---------|---------|-----------|-------------|-----------------|
| `0100` | 18 | 0 | 20 | 60s |
| `0200` | 16 | 0 | 22 | 10s |
| `0300` | 17 | 0 | 21 | 60s |

The SAT counts are **identical** between BaB-only and PGD runs. BaB correctly proved
the safe contracts; it simply cannot find counterexamples efficiently, so it timed out
on the UNSAT ones. PGD, being a gradient-based attack, finds violations in milliseconds.

---

## Why 100%-Accurate NNs Have UNSAT Contracts

**"100% accuracy" is measured on a discrete test set** of integer goal positions:
49 combinations of {0, 1, ..., 6}² = 49 discrete (goal_x, goal_y) pairs. CROWN checks
contracts over the *continuous* range goal ∈ [0, 6]², including non-integer positions
such as (3.7, 2.3) that the NN was never trained on.

The drone position EPS=0.001 is essentially a point check — violations are not coming
from the drone position dimension. They come from the **continuous goal dimension**:
at some real-valued goal position outside the training distribution, the NN selects the
forbidden direction (the one that moves into an obstacle).

This is the same discrete-vs-continuous gap observed in the ACAS Xu pipeline:
- Monolithic SMV verification (discrete states): **INVAR=true** — the system appears safe
- Continuous CROWN contracts: **UNSAT** — the NN is unsafe for real-valued inputs not
  in the training set

**The contracts are not flawed.** A flawed contract would produce degenerate UNSAT
patterns (e.g., all contracts UNSAT, or violations at physically implausible inputs).
Instead, the UNSAT pattern is geometrically structured (see below), and the SAT/UNSAT
boundary is consistent across five independently trained NNs.

---

## Contract Consistency Across Networks

Checking which contracts are UNSAT in all 5 networks vs. only some:

| Category | Count |
|----------|-------|
| UNSAT in **all 5** networks | 13 |
| UNSAT in **at least 1** network | 28 |
| SAT in **all 5** networks | 10 |

The 13 universally-UNSAT contracts are structurally notable — they include all four
cardinal approaches to obstacle **(3,3)** (the grid center) and all four approaches
to obstacle **(5,5)**, plus isolated cases at (1,4), (2,1), (4,1), (4,2), (6,1):

```
#6:  obstacle (1,4)  source (0,4)  forbid Ea
#12: obstacle (2,1)  source (2,0)  forbid No
#18: obstacle (3,3)  source (4,3)  forbid We
#19: obstacle (3,3)  source (2,3)  forbid Ea
#20: obstacle (3,3)  source (3,2)  forbid No
#21: obstacle (3,3)  source (3,4)  forbid So
#26: obstacle (4,1)  source (4,0)  forbid No
#29: obstacle (4,2)  source (4,3)  forbid So
#30: obstacle (5,5)  source (6,5)  forbid We
#31: obstacle (5,5)  source (4,5)  forbid Ea
#32: obstacle (5,5)  source (5,4)  forbid No
#33: obstacle (5,5)  source (5,6)  forbid So
#35: obstacle (6,1)  source (6,0)  forbid No
```

The central obstacle (3,3) being entirely UNSAT across all networks makes geometric
sense: a goal on the far side of the central obstacle is a common real-valued input,
and all five trained NNs learn to head toward the goal rather than around the obstacle
at some continuous goal position.

The 15 remaining UNSAT contracts (present in some but not all networks) represent
NN-training-variance-dependent brittleness — the exact continuous decision boundary
differs slightly between training runs.

---

## UNSAT Breakdown by Forbidden Direction

Across all 5 networks (190 contracts total: 38 × 5):

| Direction | UNSAT | SAT |
|-----------|-------|-----|
| No (North) | 29 | 21 |
| So (South) | 27 | 18 |
| Ea (East)  | 26 | 24 |
| We (West)  | 21 | 24 |

North and South have slightly higher UNSAT rates. East and West contracts are more
reliably safe across all networks.

---

## Implications for Compositional Verification

With ~50% of contracts UNSAT, the compositional nuXmv pipeline will report
**INVAR=false** for all five 100%-accurate NNs. This is a **real** result, not a
spurious counterexample from incomplete contract coverage:

- The UNSAT contracts identify concrete (drone_pos, goal) input regions where the NN
  genuinely selects a direction that moves into an obstacle
- The 10 universally-SAT contracts provide provable continuous-space safety guarantees
  for those regions
- The monolithic SMV result (INVAR=true) remains correct for the **discrete** model —
  the NN is safe at all 49 integer goal positions — but the compositional approach
  exposes genuine brittleness in the continuous input space

The compositional approach is a **strictly stronger** safety analysis than discrete
monolithic verification. It can detect decision-boundary violations between training
points that a lookup-table-based model checker cannot see.

---

## Recommended Next Steps

1. **Run the 99.5% and 99.6% NNs with PGD** to compare UNSAT rates with the 100%
   networks — if the near-100% NNs have more UNSAT contracts, it validates that
   contract UNSAT correlates with real NN error rate.

2. **Inspect counterexample inputs** from a representative UNSAT contract: confirm
   the violating goal position is a non-integer value (out of training distribution)
   rather than an integer position (which would indicate a genuine discrete failure).

3. **Consider tightening the goal range** in future contract formulations — e.g.,
   restricting goals to a small EPS-ball around integer positions, as done for drone
   position. This would make contracts directly comparable to the discrete SMV model.
   The trade-off is losing the continuous-space coverage guarantee.

4. **Use PGD-enabled verification as the default** for all future contract runs.
   BaB-only verification should not be used for any contract set that may contain
   UNSAT cases, as it will time out instead of finding counterexamples.
