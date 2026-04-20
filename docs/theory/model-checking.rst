Model Checking with nuXmv
=========================

.. rst-class:: lead

   BehaVerify's verification backend is `nuXmv
   <https://nuxmv.fbk.eu/>`_. This page gives the theory of the
   algorithms nuXmv uses --- BDD-based symbolic reachability, bounded
   model checking, and IC3 / PDR --- and explains which one is
   invoked for each BehaVerify CLI flag.

The model-checking problem
--------------------------

Given a Kripke structure :math:`M = (S, s_0, R, L)` (see
:doc:`specifications-and-logics`) and a temporal formula
:math:`\varphi`, the model-checking problem asks whether

.. math::

   M \models \varphi.

For finite-state models and CTL/LTL this question is **decidable**.
nuXmv's three principal algorithms below all return either
``verified`` or a counter-example trace.

Symbolic representation: BDDs
-----------------------------

A **binary decision diagram** (BDD) is a canonical representation of a
boolean function :math:`f : \{0,1\}^n \to \{0,1\}`. BDDs are:

- **Canonical** under a fixed variable order: two BDDs for the same
  function under the same order are syntactically identical.
- **Compact** on many structured problems: set union / intersection /
  composition are polynomial in BDD size.

nuXmv encodes :math:`M` symbolically: states as bit-vectors, sets of
states as BDDs, and :math:`R` as a BDD over :math:`(s, s')` pairs.
Forward image and backward image are one-step operations on BDDs
(existential quantification followed by substitution).

BDD-based reachability (INVARSPEC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To decide :math:`M \models G\,\varphi` (an INVAR), nuXmv computes the
set of reachable states iteratively:

.. math::

   \mathrm{Reach}_0 &= \{s_0\},\\
   \mathrm{Reach}_{k+1} &= \mathrm{Reach}_k \cup \mathrm{Image}(\mathrm{Reach}_k),\\
   \mathrm{Reach}_\infty &= \bigcup_k \mathrm{Reach}_k.

Termination is guaranteed because :math:`S` is finite and
:math:`\mathrm{Reach}_k` is monotone. The invariant holds iff
:math:`\mathrm{Reach}_\infty \subseteq \{\,s \mid s \models \varphi\,\}`.

For CTL, nuXmv computes the fixpoint of the appropriate
:math:`\mu`-calculus formula (e.g.,
:math:`AF\,\varphi = \mu Z.\; \varphi \lor AX\,Z`).

Bounded model checking (BMC)
----------------------------

Bounded model checking encodes the question "is there a path of
length :math:`\le k` that violates :math:`\varphi`?" as a propositional
SAT instance:

.. math::

   \Phi_k = I(s_0) \wedge \bigwedge_{i=0}^{k-1} R(s_i, s_{i+1})
            \wedge \neg\varphi_k(s_0, \ldots, s_k).

If a modern SAT solver returns **SAT**, the assignment is a
counter-example of length :math:`\le k`. If **UNSAT**, no bug of that
depth exists --- but deeper bugs might.

BMC is **unsound for proving properties** (unless the chosen :math:`k`
exceeds the reachability diameter) but is very effective at *finding*
bugs, because modern SAT solvers scale where BDDs do not. nuXmv runs
BMC when invoked with ``check_ltlspec_bmc`` or when called via
BehaVerify's ``--simulate`` flag.

IC3 / PDR
---------

IC3 (Incremental Construction of Inductive Counterexamples) ---
sometimes called Property-Directed Reachability (PDR) --- is the
default algorithm for invariants in modern nuXmv. It is **sound**
(proofs are genuine) and **complete** (terminates in finite time on
finite-state models).

IC3 maintains a sequence of over-approximations
:math:`F_0, F_1, \ldots, F_k` of the reachable states, each relative
to the property :math:`\varphi`:

.. math::

   F_0 &= I,\\
   F_{i+1} \supseteq \mathrm{Image}(F_i) &\qquad \text{(frame monotonicity)},\\
   F_i &\subseteq \varphi     \qquad \text{(each frame is safe so far)}.

When a frame can be shown inductive (:math:`F_{i+1} = F_i`), the
property is proved. When an unsafe state is found, IC3 tries to
*block* the predecessor chain by learning new clauses; a successful
block strengthens a frame, an unsuccessful block yields a
counter-example.

Compared to BDDs, IC3 scales better on systems with many unconstrained
inputs and is the preferred algorithm for large SMV models generated
by BehaVerify under fast-forwarding.

LTL: automata-theoretic approach
--------------------------------

For an LTL property :math:`\varphi`, nuXmv:

1. Negates the formula: :math:`\psi = \neg\varphi`.
2. Builds a Büchi automaton :math:`\mathcal{A}_\psi` that accepts
   exactly the :math:`\omega`-words satisfying :math:`\psi`.
3. Forms the product :math:`M \times \mathcal{A}_\psi`.
4. Checks **non-emptiness**: does the product contain a reachable
   fair cycle? If yes, any such cycle is a counter-example for
   :math:`\varphi`; if no, :math:`M \models \varphi`.

Non-emptiness is decided by symbolic SCC analysis on the product's
transition relation, again with BDDs.

Simulation
----------

nuXmv's ``--simulate N`` flag produces a random :math:`N`-step path
through the model. BehaVerify exposes this via its own
``--simulate N``. Simulation is useful for:

- sanity-checking the emitted SMV before committing to a full
  verification run;
- producing example traces for a stakeholder;
- exercising the monitor automata.

Simulation is neither sound nor complete --- it just draws one path.

Which algorithm runs when
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 26 28 26

   * - BehaVerify flag
     - nuXmv command
     - Algorithm
     - Soundness
   * - ``--invar``
     - ``check_invar``
     - IC3 / BDD reachability
     - sound, complete
   * - ``--ctl``
     - ``check_ctlspec``
     - symbolic :math:`\mu`-calculus
     - sound, complete
   * - ``--ltl``
     - ``check_ltlspec``
     - Büchi product +
       symbolic SCC
     - sound, complete
   * - ``--simulate N``
     - ``go; pick_state; simulate -k N``
     - random walk
     - neither

Complexity
----------

- CTL / invariants are in **PSPACE** in the size of the SMV formula
  and the number of bits of the state variable. In practice BDD /
  IC3 runs much faster than worst case on structured systems.
- LTL is in **PSPACE** in formula size; the Büchi construction is
  :math:`2^{O(|\varphi|)}` in the worst case.
- BMC depth-:math:`k` check is in **NP** in the unrolling size.

BehaVerify's fast-forwarding encoding (see :doc:`bt-to-smv`) keeps the
state-variable bit-width :math:`O(\log |\Sigma|)` instead of
:math:`O(|V|)`, which is the reason the backend scales to thousands
of tree nodes.

References
----------

- Cavada, Cimatti, Dorigatti, Griggio, Mariotti, Micheli, Mover,
  Roveri, Tonetta. The nuXmv Symbolic Model Checker. *CAV* 2014.
- Bradley. SAT-Based Model Checking without Unrolling. *VMCAI* 2011
  (IC3).
- Biere, Cimatti, Clarke, Zhu. Symbolic Model Checking without
  BDDs. *TACAS* 1999 (BMC).
- Clarke, Grumberg, Peled. *Model Checking.* MIT Press, 1999.
