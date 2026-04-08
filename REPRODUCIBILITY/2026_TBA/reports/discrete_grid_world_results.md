# Discrete Grid World Verification Results

**Date:** 2026-04-07
**Feature:** GRID-05 — Discrete compositional verification of 1-NN grid world NSBTs

---

## Overview

We applied the compositional A/G verification pipeline to replicate the discrete safety
claim from the 2025_NEUS monolithic table approach. In discrete mode, each contract is
verified against all 49 integer goal points in {0,...,6}², with both drone EPS and goal
EPS set to 0.0 (exact integer coordinates). CROWN proves each contract; nuXmv verifies
the INVAR using the resulting reachable sets.

This tests the same safety property as the 2025_NEUS lookup table approach — does the NN
avoid directing the drone into an obstacle for every integer (drone, goal) pair? — but
compositionally rather than monolithically.

---

## Results Summary

| Network               | Accuracy | SAT | UNSAT | Start    | End      | Elapsed (approx) |
|-----------------------|----------|-----|-------|----------|----------|------------------|
| 1000__6_18_0__0100_1  | 100%     | 38  | 0     | 15:16:50 | 15:52:04 | ~35 min          |
| 1000__6_18_0__0150_1  | 100%     | 38  | 0     | 15:52:19 | 16:26:06 | ~34 min          |
| 1000__6_18_0__0200_1  | 100%     | 38  | 0     | 16:26:18 | 17:00:28 | ~34 min          |
| 1000__6_18_0__0250_1  | 100%     | 38  | 0     | 17:00:40 | 17:42:14 | ~42 min          |
| 1000__6_18_0__0300_1  | 100%     | 38  | 0     | 17:42:30 | 18:21:23 | ~39 min          |
| 0996__6_18_0__200_1   | 99.6%    | 34  | 4     | 18:21:36 | 18:51:38 | ~30 min          |
| 0995__6_18_0__200_1   | 99.5%    | 35  | 3     | 19:04:43 | 19:51:38 | ~47 min          |

Start times from nohup banners; end times from JSON file creation timestamps (local time, CDT).
Future runs will record elapsed_sec directly in the JSON report header.

---

## Key Findings

### 100%-Accurate Networks (1000-series)
All 38 contracts return SAT for all five networks. This replicates the 2025_NEUS result:
the 100%-accurate NSBTs are provably safe for every integer (drone, goal) pair. CROWN
resolved each contract via PGD without invoking branch-and-bound (BaB), so the eps=0
interval did not cause numerical issues in alpha-beta-CROWN.

### 99.6%-Accurate Network (0996)
4 UNSAT contracts found. All four counterexamples are exact integer points, confirmed
by forward pass through the ONNX model:

| Contract | Source | Forbidden | Counterexample (drone_x, drone_y, goal_x, goal_y) |
|----------|--------|-----------|---------------------------------------------------|
| obstacle (3,3) source (3,4) forbid So | (3,4) | So | (3, 4, 3, 3) |
| obstacle (4,1) source (4,0) forbid No | (4,0) | No | (4, 0, 0, 5) |
| obstacle (5,5) source (6,5) forbid We | (6,5) | We | (6, 5, 4, 6) |
| obstacle (5,5) source (5,4) forbid No | (5,4) | No | (5, 4, 4, 5) |

### 99.5%-Accurate Network (0995)
3 UNSAT contracts found. All three counterexamples are exact integer points, confirmed
by forward pass:

| Contract | Source | Forbidden | Counterexample (drone_x, drone_y, goal_x, goal_y) |
|----------|--------|-----------|---------------------------------------------------|
| obstacle (3,3) source (3,4) forbid So | (3,4) | So | (3, 4, 4, 3) |
| obstacle (5,5) source (6,5) forbid We | (6,5) | We | (6, 5, 4, 6) |
| obstacle (5,5) source (5,4) forbid No | (5,4) | No | (5, 4, 4, 5) |

---

## Technical Notes

- **eps=0 safety:** CROWN does not crash at eps=0 for these networks because PGD
  resolves all contracts before BaB is invoked. The unprotected division in
  `cut_ops.py` lines 319–322 is never reached.
- **Coordinate convention:** x increases East, y increases North. Matches 2025_NEUS.
- **Discrete mode implementation:** `verify_one_contract_discrete()` in
  `verify_grid_world_contracts.py` iterates over all 49 integer goals, short-circuiting
  on the first UNSAT. `DISCRETE_GOAL_EPS = 0.0` pins goal to exact integer point.
- **Pipeline generality:** Unlike the 2025_NEUS table approach (bespoke to grid world),
  this pipeline applies to any NSBT with a neural component verifiable by CROWN.

---

## Next Steps

- **GRID-06:** Visualize discrete vs. continuous UNSAT counts per network; generate
  comparison figure for the paper.
- **Large grid CTL:** Port pipeline to a larger grid world and attempt CTL verification
  where the monolithic table approach timed out (stretch goal).
