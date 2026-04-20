# Grid World UCLID5 Integration and Initial Results

**Date:** 2026-04-20
**Features:** GRID-08 (UCLID5 integration)

---

## 1. Overview

This report documents the initial integration of UCLID5 as a second symbolic model checker in the compositional NSBT verification pipeline, alongside the existing nuXmv backend. The results for the grid-world example are presented and compared.

---

## 2. Modularity of the Framework

The compositional pipeline separates neuro verification (CROWN) from symbolic verification (nuXmv or UCLID5) at a clean interface: a contracts JSON file. CROWN produces A/G contracts of the form "the NN will not output action _a_ from position _(x, y)_," and the symbolic checker consumes them as assumptions. Adding UCLID5 required no changes to the CROWN verification step or the BehaVerify DSL — only a new translator and runner were needed.

The pipeline entry point is now:

```bash
# CROWN + nuXmv
./run_all_compositional_pipelines.sh contracts/crown/<goals>/ --symbolic nuXmv

# CROWN + UCLID5
./run_all_compositional_pipelines.sh contracts/crown/<goals>/ --symbolic uclid5 --bmc-steps 50
```

Output is separated by checker under `results/compositional/<goals>/crown_nuXmv/` and `results/compositional/<goals>/crown_uclid5/` respectively. This means CROWN-nuXmv and CROWN-UCLID5 results can coexist and be compared directly.

### Implementation Approach

Rather than writing a new BehaVerify code generator from scratch, `dsl_with_contracts_to_uclid5.py` reuses the existing `dsl_to_nuxmv` backend as a first step, then translates the generated SMV to UCLID5 format. The key translation steps are:

- nuXmv `VAR x : {left, right, ...}` → UCLID5 `type enum_t = enum { left, right, ... }; var x : enum_t;`
- nuXmv `INVAR cond` / `INVARSPEC prop` → UCLID5 `assume name : cond;` / `invariant name : prop;`
- nuXmv `ASSIGN next(x) := case ...` → UCLID5 `next { if (...) { x' = ...; } else { ... } }` with `havoc` for non-deterministic assignments
- The BehaVerify behavior tree module hierarchy (selectors, sequences, check nodes) is inlined as closed-form boolean expressions directly into the UCLID5 `next` block, since UCLID5 does not share nuXmv's hierarchical module system
- A/G contracts → module-level `assume name : (pos == ...) ==> (network != action);`

---

## 3. nuXmv vs. UCLID5: Key Differences

Both nuXmv and UCLID5 are symbolic model checkers, but they differ meaningfully in input format, verification algorithms, and expressivity.

| Dimension | nuXmv | UCLID5 |
|---|---|---|
| Input format | `.smv` (nuXmv SMV) | `.ucl` (UCLID5 UCL) |
| Module system | Hierarchical (BehaVerify generates nested modules) | Flat (hierarchy must be inlined) |
| A/G contract encoding | `INVAR cond` (state invariant) | `assume name : cond;` (module-level assumption) |
| Safety property encoding | `INVARSPEC prop` | `invariant name : prop;` in `control` block |
| Default verification algorithm | IC3 / k-induction (complete for finite-state systems) | BMC — bounded up to N steps |
| CTL / LTL support | Yes (`CTLSPEC`, `LTLSPEC`) | Limited (LTL via `ltl` property; no CTL) |
| Backend solver | Native (MiniSat / IC3 engine) | Z3 (via Java bindings) |
| Non-det assignment | `{v1, v2, ..., vN}` in `ASSIGN next` | `havoc x; assume (cond);` |

The most practically significant difference is the verification algorithm. nuXmv's IC3/k-induction is a **complete** method: a `true` result guarantees the invariant holds for all reachable states, not just states reachable within N steps. UCLID5's BMC (as currently configured) only checks up to a fixed bound; a `true` result means no counterexample was found within 50 steps, not that none exists.

---

## 4. Results: CROWN-nuXmv vs. CROWN-UCLID5 (Discrete Goals)

Results for `contracts/crown/discrete_goals/`. The crown_uclid5 results are under gitignore and must be reproduced locally by running:

```bash
./run_all_compositional_pipelines.sh contracts/crown/discrete_goals/ --symbolic uclid5 --bmc-steps 50
```

### INVAR Verdicts

| Network | SAT Contracts | CROWN-nuXmv INVAR | CROWN-UCLID5 INVAR | Agreement |
|---|---|---|---|---|
| `0995__6_18_0__200_1` | 35 / 38 | **false** | **false** | ✓ |
| `0996__6_18_0__200_1` | 34 / 38 | **false** | **false** | ✓ |
| `1000__6_18_0__0100_1` | 38 / 38 | **true** | **true** | ✓ |
| `1000__6_18_0__0150_1` | 38 / 38 | **true** | **true** | ✓ |
| `1000__6_18_0__0200_1` | 38 / 38 | **true** | **true** | ✓ |
| `1000__6_18_0__0250_1` | 38 / 38 | **true** | **true** | ✓ |
| `1000__6_18_0__0300_1` | 38 / 38 | **true** | **true** | ✓ |

All 7 networks agree on the INVAR verdict. The two unsafe networks (0995, 0996) are flagged as unsafe by both checkers; the five safe networks (1000-series, all 38/38 contracts SAT) are verified as safe by both.

### Timing Comparison

| Network | nuXmv (total) | nuXmv (verify only) | UCLID5 (total) |
|---|---|---|---|
| `0995__6_18_0__200_1` | 7.3 s | 0.136 s | 153.2 s |
| `0996__6_18_0__200_1` | 5.1 s | 0.104 s | 99.1 s |
| `1000__6_18_0__0100_1` | 5.1 s | 0.094 s | 1142.5 s |
| `1000__6_18_0__0150_1` | 4.9 s | 0.093 s | 806.8 s |
| `1000__6_18_0__0200_1` | 4.9 s | 0.094 s | 817.1 s |
| `1000__6_18_0__0250_1` | 4.9 s | 0.095 s | 805.4 s |
| `1000__6_18_0__0300_1` | 5.1 s | 0.094 s | 812.0 s |

nuXmv verification takes under 0.15 seconds per network; the 5-7 second total is dominated by SMV generation. UCLID5 takes 99–1142 seconds, reflecting the cost of BMC with Z3 over 50 steps on a model with complex inlined BT expressions.

### Observations

- **Verdict agreement is complete** across all seven networks for the discrete-goals setting. This is a strong early signal that the UCLID5 translation is semantically correct.
- **Unsafe networks are found faster.** The 0995 and 0996 networks (INVAR=false) take 99–153 seconds in UCLID5 because counterexamples are found early in the BMC search. Safe networks require checking all 50 steps, producing 51 "verified" invariant checks per run.
- **nuXmv is substantially faster** due to IC3/k-induction vs. explicit-path BMC and its native solver vs. Z3 via JVM.
- The nuXmv pipeline also produces CTL results; UCLID5 currently does not have CTL support configured.
- The results reported here are limited to the discrete-goals setting. Additional testing (continuous goals with PGD-enabled contracts, ACAS Xu) is needed before claiming full equivalence.

---

## 5. Limitations and Future Work

### BMC Bound and Completeness

The UCLID5 pipeline currently uses `bmc(50)` in the `control` block. For the discrete-goals setting, 50 steps appears sufficient to reproduce nuXmv's results, but this has not been formally justified. A counterexample that requires more than 50 steps would be missed, producing a false `true` verdict.

Switching to **k-induction** would eliminate this incompleteness. UCLID5 supports k-induction natively:

```ucl
control {
    k = unroll (50);
    induction;
    check;
    print_results;
}
```

k-induction proves an invariant holds for all reachable states (not just up to a bound) by showing: (1) the invariant holds in the initial state, and (2) if it holds for k consecutive states it holds for the next. This would bring UCLID5 results to the same level of completeness as nuXmv's INVARSPEC checks.

### Further Validation

- Test on `continuous_goals/enabled_pgd` contracts (larger contract sets, continuous goal coordinates)
- Test on the ACAS Xu example (multi-NN, different BT structure) to validate generality of the SMV→UCLID5 translator
- Timing comparison at different BMC bounds to characterize the tradeoff

### CTL Properties

nuXmv also verifies CTL specifications (`CTLSPEC`) that are present in the BehaVerify model. UCLID5 does not currently support CTL; the UCLID5 pipeline silently drops CTL specifications. If CTL verification is required, nuXmv remains the only supported backend.
