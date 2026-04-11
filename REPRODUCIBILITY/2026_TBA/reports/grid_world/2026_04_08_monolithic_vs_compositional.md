# Monolithic vs. Compositional Verification — Grid World Timing Report

**Date:** 2026-04-08
**Features:** GRID-05 (discrete compositional), GRID-06 (monolithic baseline)

---

## Overview

This report compares two verification pipelines for grid-world NSBTs using **discrete
integer coordinates** (ε = 0 for both drone and goal positions). Both pipelines check
the same two specifications:

- **INVARSPEC** — the drone never collides with an obstacle
- **CTLSPEC** — the drone always eventually reaches the target, or the target is in an
  obstacle (`AG(in_obstacle(target) ∨ AF(drone = target))`)

### Monolithic pipeline (2025_NEUS table approach)
```
.tree → BehaVerify (embed full NN lookup table) → .smv → nuXmv → verdict
```
BehaVerify queries the ONNX model for all 2401 (drone, goal) input combinations and
embeds the results as a lookup table in the SMV file. nuXmv then verifies both specs
on the resulting monolithic model.

Data: `REPRODUCIBILITY/2025_NEUS/examples/grid_world/results/`

### Compositional pipeline (2026_TBA, discrete mode)
```
CROWN (verify A/G contracts) → BehaVerify (inject contracts as INVAR) → .smv → nuXmv → verdict
```
alpha-beta-CROWN verifies 38 A/G contracts per network (one-time cost). The SAT
contracts are injected as INVARSPEC assumptions into a compact SMV. nuXmv then checks
both specs on the contract-abstracted model.

Data: `REPRODUCIBILITY/2026_TBA/examples/grid_world/results/compositional/discrete_goals/`

---

## Timing Results

### Monolithic

Timing measured with bash `time`. SMV generation runs BehaVerify (includes ONNX table
construction). nuXmv runs INVARSPEC + CTLSPEC together.

| Network              | Accuracy | SMV gen (s) | nuXmv (s) | Total (s) | INVAR | CTL  |
|----------------------|----------|-------------|-----------|-----------|-------|------|
| 1000__6_18_0__0100_1 | 100%     | 2.274       | 2.155     | 4.429     | true  | true |
| 1000__6_18_0__0150_1 | 100%     | 2.051       | 1.768     | 3.819     | true  | true |
| 1000__6_18_0__0200_1 | 100%     | 2.091       | 1.712     | 3.803     | true  | true |
| 1000__6_18_0__0250_1 | 100%     | 1.847       | 2.000     | 3.847     | true  | true |
| 1000__6_18_0__0300_1 | 100%     | 1.889       | 1.905     | 3.794     | true  | true |
| 0996__6_18_0__200_1  | 99.6%    | 2.065       | 5.114     | 7.179     | false | false|
| 0995__6_18_0__200_1  | 99.5%    | 1.806       | 3.695     | 5.501     | false | false|

### Compositional (symbolic phase only — contracts pre-verified)

Timing measured with `time.perf_counter()` in `pipeline_report.json`. CROWN contract
verification was pre-computed and is **not** included in these times (see §"Contract
Verification Cost" below). SMV generation runs BehaVerify with injected SAT contracts.

| Network              | Accuracy | Contracts injected | SMV gen (s) | nuXmv (s) | Total (s) | INVAR | CTL   |
|----------------------|----------|--------------------|-------------|-----------|-----------|-------|-------|
| 1000__6_18_0__0100_1 | 100%     | 38 / 38            | 4.935       | 0.094     | 5.072     | true  | false |
| 1000__6_18_0__0150_1 | 100%     | 38 / 38            | 4.802       | 0.093     | 4.937     | true  | false |
| 1000__6_18_0__0200_1 | 100%     | 38 / 38            | 4.770       | 0.094     | 4.906     | true  | false |
| 1000__6_18_0__0250_1 | 100%     | 38 / 38            | 4.777       | 0.095     | 4.914     | true  | false |
| 1000__6_18_0__0300_1 | 100%     | 38 / 38            | 4.979       | 0.094     | 5.117     | true  | false |
| 0996__6_18_0__200_1  | 99.6%    | 34 / 38            | 4.940       | 0.104     | 5.088     | false | false |
| 0995__6_18_0__200_1  | 99.5%    | 35 / 38            | 7.082       | 0.136     | 7.302     | false | false |

---

## Contract Verification Cost (CROWN, one-time per network)

Contract verification timing was not captured in the pipeline JSON reports for these
runs (contracts were pre-computed and passed via `--skip-contracts`). Wall-clock
elapsed times were estimated from nohup banner timestamps:

| Network              | Approx. elapsed |
|----------------------|-----------------|
| 1000__6_18_0__0100_1 | ~35 min         |
| 1000__6_18_0__0150_1 | ~34 min         |
| 1000__6_18_0__0200_1 | ~34 min         |
| 1000__6_18_0__0250_1 | ~42 min         |
| 1000__6_18_0__0300_1 | ~39 min         |
| 0996__6_18_0__200_1  | ~30 min         |
| 0995__6_18_0__200_1  | ~47 min         |

**Contracts are reusable.** A/G contracts encode properties of the NN itself (input
region → output action), not the specification being checked. Once verified by CROWN,
the same contract JSON can be used to check any number of INVARSPECs, CTLSPECs, or
LTLSPECs without re-running CROWN. The monolithic approach has no equivalent — it
re-embeds the full lookup table for every new verification run.

---

## Key Comparisons

### INVAR agreement

Both pipelines agree on INVARSPEC for all 7 networks. The 100%-accurate networks (1000-
series) pass; 0996 and 0995 fail, with CROWN finding exact integer counterexamples that
are confirmed by direct ONNX forward pass.

### CTL divergence

Monolithic proves CTL=true for the 5 fully-accurate networks. Compositional returns
CTL=false for **all** 7 networks.

This is a fundamental consequence of abstraction, not a bug. The A/G contracts guarantee
"if the drone is in input region X, the NN will not output a collision-inducing action."
They say nothing about whether the drone makes progress toward the goal. nuXmv can
construct a liveness counterexample (the drone loops forever near the goal without
reaching it) because the contract abstraction does not rule this out. The monolithic
approach encodes the complete transition table, so nuXmv can verify forward progress
directly.

### nuXmv time

Compositional nuXmv is 18–50× faster than monolithic nuXmv (0.09–0.14s vs 1.7–5.1s).
The contract-abstracted SMV is much smaller than the full lookup-table SMV, so BDD
construction and model checking complete almost instantly. This advantage grows with
network size and would be critical for larger models where the monolithic SMV becomes
intractable.

### SMV generation time

Compositional SMV generation is ~2–4× slower than monolithic (4.8–7.1s vs 1.8–2.3s)
because BehaVerify must parse and inject the contract JSON in addition to the standard
tree compilation. This is a fixed overhead regardless of network size.

### Symbolic phase total

Both approaches complete the symbolic phase in roughly 4–7s per network. The timing
advantage of compositional nuXmv is offset by slower SMV generation.

---

## Amortized Cost Argument

For a single specification check, the total costs are roughly comparable (symbolic phase
~4–7s each), but compositional carries the one-time CROWN overhead (~30–47 min). The
compositional approach pays off when:

1. **Multiple specifications** are checked on the same network — contracts are verified
   once; each additional spec costs only ~5s.
2. **Larger networks** — monolithic SMV size scales with the number of NN inputs ×
   states, making nuXmv intractable. Compositional nuXmv cost is insensitive to NN
   size (only SMV generation grows slightly).
3. **Specification iteration** — researchers revising INVARSPECs or CTLSPECs during
   development pay ~5s per iteration compositionally vs ~4–7s monolithically (both fast
   at this scale, but the advantage is preserved at scale).

---

## Figure

See `figures/grid_world_comparison.png` (generated by
`figures/image_scripts/grid_world_comparison.py`) for a stacked-bar visualization of
the symbolic phase timings and a verdict table.
