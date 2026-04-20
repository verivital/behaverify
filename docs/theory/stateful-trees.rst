Stateful Behavior Trees
=======================

.. rst-class:: lead

   Classical BT semantics is memoryless across ticks: every tick
   restarts at the root. Stateful BTs (Serbinowska, Robinette,
   Potteiger, Karsai & Johnson, FMAS 2024) lift that restriction by
   annotating nodes with a *local state* that persists across ticks.

Motivation
----------

The textbook BT semantics is memoryless: each tick starts afresh at
the root. That is fine for reactive domains but awkward for
multi-step actions (*navigate to waypoint :math:`p`*) that should not
restart on every tick.

Colledanchise & Ögren introduced the ``with_partial_memory`` /
``with_true_memory`` flags (see :doc:`behavior-trees`) to let a
composite remember which children it had finished or started. Those
flags are attached to a single composite, though, and do not capture
richer stateful structures --- e.g. a sub-tree whose root *behaves
differently* the second time it is entered after a success.

Formalisation
-------------

Serbinowska et al. (FMAS 2024) formalise stateful BTs as a tuple

.. math::

   (T, \Lambda, \Delta)

where

- :math:`T` is a classical BT,
- :math:`\Lambda : V \to \mathcal{L}` assigns each node a *local
  state* drawn from a finite lattice :math:`\mathcal{L}`, and
- :math:`\Delta : V \times \mathcal{L} \times \mathcal{S} \to
  \mathcal{L}` updates a node's local state based on its return
  status.

The tick relation is extended to

.. math::

   \mathrm{tick}_{\text{stateful}} :
     V \times \Sigma \times \mathcal{L}^{|V|}
     \to
     \mathcal{S} \times \Sigma \times \mathcal{L}^{|V|},

i.e. the joint state is now the blackboard plus the lattice-valued
label assignment.

Encoding into SMV
-----------------

BehaVerify's fast-forwarding encoding (see :doc:`bt-to-smv`)
generalises to the extended tuple: every local state becomes a staged
SMV variable just like blackboard variables, and the transition
relation updates both the blackboard *and* the lattice assignment on
each tick. The soundness argument of :doc:`soundness` applies
verbatim --- Claim 4 is stated in terms of the (joint) transition
relation, not specifically over blackboard variables.

Authoring syntax
----------------

A ``memory { ... }`` block may be attached to a composite or
sub-tree. Validation enforces that the lattice type is finite;
infinite lattices would break decidability of the model-checking
problem.

Discipline
----------

Two modelling rules keep stateful BTs tractable:

1. **Finiteness.** Every lattice must be finite. A local-state
   variable ranging over an unbounded counter is rejected by
   :mod:`behaverify.check_grammar`.
2. **Observability.** Local state may be referenced inside
   specifications via ``(state node_name)`` atoms. BehaVerify
   compiles these to boolean predicates over the staged SMV
   variables, so there is no cost to inspecting local state in a
   specification.

References
----------

- Serbinowska, Robinette, Potteiger, Karsai, Johnson. Formalizing
  Stateful Behavior Trees. *FMAS* 2024, EPTCS 411, pp. 201-218.
  https://dx.doi.org/10.4204/EPTCS.411.14
