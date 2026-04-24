Verification Strategies
=======================

.. rst-class:: lead

   BehaVerify supports three complementary strategies today: symbolic
   model checking, simulation, and runtime monitoring.

.. mermaid::

   flowchart LR
     A[.tree model] --> B[BehaVerify core]
     B --> C[SMV] --> M[nuXmv<br/>model checking]
     B --> P[py_trees] --> S[simulation]
     B --> R[monitor] --> O[runtime enforcement]
     %% Reserved future edge (uncomment when re-introducing):
     %% B -.-> X[planned:<br/>probabilistic]
     %% style X stroke-dasharray: 4 3, fill:#eee

1. Symbolic model checking (``nuxmv`` mode)
-------------------------------------------

SMV model + ``specifications { ... }`` block → nuXmv decides
``INVARSPEC`` / ``CTLSPEC`` / ``LTLSPEC`` queries. Fully symbolic and
sound; the fast-forwarding encoding pushes the practical limit to
thousands of BT nodes.

Strengths:

- Exhaustive --- no missed counter-examples.
- Handles integer, enum, and boolean blackboards natively.
- Supports neural-leaf encoding for ACAS-Xu-style problems.

Limitations:

- Requires a nuXmv binary (licence forbids redistribution).
- Treats stochasticity as non-determinism → worst-case bounds only.

2. Simulation (``python`` mode)
-------------------------------

A ``py_trees`` implementation runs for ``--max_iter`` ticks, printing
blackboard state and (optionally) per-node local variables. Simulation
is *not* exhaustive but is useful for:

- Rapid debugging of ``.tree`` logic before invoking nuXmv.
- Generating empirical success / failure rates over random seeds.
- Running against a real sensor/actuator stack via custom readers.

3. Runtime monitoring (``monitor`` / contingency blocks)
--------------------------------------------------------

The ``monitors { ... }`` block compiles an LTL formula into a
stateful monitor that runs alongside the BT and fires a configured
``trigger_action`` when the monitor observes a violation. Suitable for
on-robot deployment where exhaustive verification is either
infeasible or complemented by runtime safety nets.

..
   Reserved placeholder for a future probabilistic strategy.
   Uncomment the block below (remove the outer ``..`` marker and
   de-indent) when the PCTL / DTMC back-end lands.
..
   4. Probabilistic verification *(reserved)*
   ------------------------------------------

   .. note::

      This section is a **placeholder**. It marks the extension point for
      strategies that answer quantitative questions like
      :math:`\Pr[F\,\mathrm{goal}] \ge 0.9` or
      :math:`\Pr[G\,\neg\mathrm{unsafe}] \le 0.01`.

   A probabilistic strategy would:

   - Accept the same ``.tree`` input (with an explicit stochastic-leaf
     extension to the DSL).
   - Emit a DTMC / MDP / PRISM / Storm model from the internal IR.
   - Discharge PCTL queries rather than CTL/LTL.

   The core pipeline (parser → validator → IR) is fully reusable; only a
   new back-end analogous to ``dsl_to_nuxmv`` / ``dsl_to_python`` would be
   needed.

Summary
-------

.. list-table::
   :header-rows: 1

   * - Strategy
     - Soundness
     - Scales to
     - Handles stochasticity
   * - Model checking (nuXmv)
     - exact
     - 2,000+ nodes
     - as non-determinism
   * - Simulation
     - approximate
     - any size
     - yes, per seed
   * - Runtime monitors
     - per trace
     - any size
     - yes, per trace

.. Reserved row for future probabilistic strategy; uncomment to restore:
..
   * - Probabilistic *(reserved)*
     - exact
     - tbd
     - yes, natively
