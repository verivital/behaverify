# Grid World: Research Plan and Current Status

**Date:** 2026-04-07
**Project:** Compositional verification of neuro-symbolic behavior trees (NSBTs)
**Example:** `examples/grid_world/` — 7×7 grid, 18 obstacles, 38 A/G contracts, 1 NN

---

## 1. Research Context

The 2025_NEUS paper verified grid world safety using a **lookup table** approach: the NN was
evaluated on all integer inputs and stored in nuXmv as a precomputed table. For the small grid
(7×7), this is fast. For the large grid (50×50, 6,250,000 input combinations), INVAR verified
in ~29 seconds but CTL timed out after one hour.

The 2026_TBA paper proposes a **compositional A/G approach** as the explicitly-stated future
work of 2025_NEUS (Section 5): instead of encoding the NN, verify A/G contracts via CROWN and
inject them as INVAR assumptions into nuXmv. This makes the nuXmv model independent of NN size.

---

## 2. Comparison Framing

The table approach and compositional approach are not competing on speed for small grids.
The table approach wins there. The compositional approach's advantages are:

| Dimension | Table (2025_NEUS) | Compositional (2026_TBA) |
|---|---|---|
| NN encoding in nuXmv | 6.25M lookup entries (large grid) | Fixed set of A/G contracts |
| Safety domain checked | Discrete integer inputs only | Continuous [0, 6]² via CROWN |
| CTL on large grid | Timeout after 1 hour | Open question — model is leaner |
| New findings possible | No | Yes — continuous safety gap |

The core claim: **the compositional approach is more informative and more scalable**, not faster
on small discrete examples.

---

## 3. The Continuous Safety Gap (Key Finding)

Contracts were verified over the full continuous goal domain [0, 6]² rather than over the 49
integer grid points the NN was trained on. Result for all seven networks tested:

- **0995 (99.5% accuracy):** 17 SAT, 21 UNSAT — safety violations exist
- **0996 (99.6% accuracy):** 15 SAT, 23 UNSAT
- **1000__× networks (100% accuracy):** 16–18 SAT, 20–22 UNSAT

All 21 UNSAT contracts for 0995 (confirmed via counterexample extraction, 2026-04-07) show
**non-integer goal coordinates**. The networks are discrete-safe — they never collide at the
49 integer training inputs — but their learned decision boundaries produce unsafe outputs for
continuous goals between integer points.

This gap is invisible to the table approach. It is the primary new finding of 2026_TBA's
grid world experiments.

---

## 4. Planned Experiments

### 4a. PGD-enabled vs. BaB-only comparison (small grid, pending)

**Goal:** Demonstrate that PGD is essential for resolving UNSAT contracts efficiently.

**Design:**
- Same 5 networks (1000 series), same 60s timeout per contract
- One variable: PGD enabled vs. disabled (BaB only)
- Expected: BaB-only → mostly TIMEOUT for UNSAT contracts; PGD → zero timeouts

**Status:** PGD-enabled contracts exist for all 5 networks (`contracts/enabled_pgd/`).
BaB-only contracts are incomplete (`contracts/disabled_pgd/` has 4 of 5). Overnight run
pending:

```bash
cd REPRODUCIBILITY/2026_TBA/examples/grid_world
./run_continuous_bab_1000_contracts.sh
```

After run, execute full pipeline comparison:

```bash
./run_all_compositional_pipelines.sh contracts/continuous_goals/disabled_pgd/
```

### 4b. Discrete goal verification (small grid, not yet started)

**Goal:** Bridge to 2025_NEUS. Confirm that all 100%-accurate networks are discrete-safe by
checking contracts with integer-only goal inputs (eps-ball around each of 49 integer goals).

**Design:** Run CROWN with goal constrained to eps-ball around each integer point (cx, cy)
rather than [0, 6]². Expected result: all 38 contracts SAT for 100%-accurate networks,
consistent with the table approach.

**Why this matters:** It separates two claims cleanly:
- Claim A: The NN is safe on integer inputs (agrees with 2025_NEUS, discrete-safe)
- Claim B: The NN is NOT safe on continuous inputs (new finding, 2026_TBA)

**Status:** Not yet implemented. Requires modifying verification to loop over 49 integer
goals per contract. See §5 for prioritization.

### 4c. Large grid CTL attempt (`grid_world_big`, stretch goal)

**Goal:** Attempt CTL verification on the 50×50 grid where 2025_NEUS explicitly timed out.

**Motivation:** The compositional approach replaces a 6.25M-entry lookup table with a compact
set of A/G contract assumptions. The nuXmv model is dramatically leaner regardless of grid
size, which may enable CTL to succeed where the table approach failed.

**Risks:**
- `grid_world_big` was deleted from `2026_TBA/` during DESIGN-16; its network, obstacles,
  and tree files would need to be sourced from `2025_NEUS/examples/grid_world_big/`.
- If large-grid networks also have UNSAT continuous contracts, INVAR fails and CTL is moot.
  The UNSAT result would itself be a finding, but a different one.
- Significant setup effort; should not proceed until small-grid story is complete.

**Status:** Deferred. Treat as stretch goal for after §4a and §4b are done.

---

## 5. Priority Order

1. **Run `run_bab_1000_contracts.sh` overnight** (§4a) — low effort, high value, directly
   needed for the PGD comparison table. Can run unattended.

2. **Implement discrete goal verification** (§4b) — medium effort, needed to bridge to
   2025_NEUS and cleanly separate discrete-safe vs. continuous-unsafe claims.

3. **Port pipeline to large grid** (§4c) — high effort, stretch goal. Only attempt after
   the small-grid narrative is solid and the CTL result could be a headline finding.

---

## 6. Open Items

| Item | Status |
|---|---|
| BaB-only contracts for 0150 and 0250 networks | Pending overnight run |
| 0996 network contracts (enabled_pgd) | Generated 2026-04-07; pipeline run pending |
| Counterexample extraction validation | Done (0995, 2026-04-07) — all UNSAT at non-integer goals |
| Discrete goal verification implementation | Not started |
| Large grid CTL attempt | Deferred |
| AcasXu_closed_loop dead code review | Deferred |
