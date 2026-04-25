Behavior Tree → SMV Translation
===============================

.. rst-class:: lead

   BehaVerify's core contribution is a translation from BTs to SMV
   models that exposes exactly the right transitions to nuXmv. This
   page formalises the *fast-forwarding* encoding from Serbinowska &
   Johnson (SEFM 2022) and describes its variable-staging scheme.

Encoding at a glance
--------------------

.. figure:: /_static/img/encoding-naive.png
   :alt: Naive encoding: six SMV transitions encode one BT tick.
   :class: pipeline-hero
   :width: 95%

   Naive encoding. Every internal BT step --- entering the root,
   ticking each child, bubbling statuses up, updating the
   blackboard --- is its own SMV transition.

.. figure:: /_static/img/encoding-ff.png
   :alt: Fast-forwarding encoding: one SMV transition encodes one BT tick.
   :class: pipeline-hero
   :width: 70%

   Fast-forwarding encoding. One SMV transition collapses an entire
   root-to-leaf traversal plus all blackboard updates into a single
   atomic step.

Let :math:`T` be a BT with node set :math:`V` and blackboard variables
:math:`B = \{b_1, \ldots, b_k\}`. Write :math:`\Sigma = \mathrm{dom}(B)`
for the set of blackboard valuations.

Naive encoding
^^^^^^^^^^^^^^

The naive encoding tracks a program counter :math:`\mathrm{pc} \in V
\cup \{\bot\}` that names the node currently being visited. A single
SMV transition corresponds to one atomic step of the BT interpreter:
entering a composite, ticking a child, bubbling up a status. Because
a full tick of a tree with :math:`n` nodes requires
:math:`\Theta(n)` such steps, the induced SMV model grows *linearly*
in the tree size at every "real" tick of the BT.

Fast-forwarding encoding
^^^^^^^^^^^^^^^^^^^^^^^^

The fast-forwarding encoding removes the program counter. Every SMV
transition encodes a *whole tick*: given a blackboard valuation
:math:`\sigma`, the transition :math:`R(\sigma, \sigma')` holds iff
:math:`\sigma'` is the blackboard that results from running one tick
of the BT on :math:`\sigma`. Formally, if :math:`\mathrm{tick}_T :
\Sigma \to \Sigma` is the BT's one-tick blackboard map, then

.. math::

   R_{\text{FF}}(\sigma, \sigma') \;\Leftrightarrow\; \sigma' = \mathrm{tick}_T(\sigma).

Serbinowska & Johnson showed that this encoding is **semantically
equivalent** to the naive one for every INVAR/CTL/LTL formula whose
atoms refer only to blackboard variables and post-tick node
statuses --- the very formulas that BehaVerify's DSL accepts.

Variable staging
----------------

A single tick may read and write the same blackboard slot multiple
times (e.g., a sequence whose children all update ``pos_x``). The
straightforward compilation into SMV would use intermediate variables
for each such read, exploding the state space. BehaVerify instead
**stages** each blackboard variable:

.. math::

   b_i \;\Longrightarrow\; b_i^{(0)},\; b_i^{(1)},\; \ldots,\; b_i^{(n_i)}

where :math:`b_i^{(0)}` is the tick-start value, :math:`b_i^{(n_i)}`
is the tick-end value, and the intermediate stages
:math:`b_i^{(j)}` record writes in the order they occur inside the
tick. The SMV transition relation then closes the loop across ticks
with

.. math::

   \mathrm{next}(b_i^{(0)}) \;=\; b_i^{(n_i)}.

An intermediate stage :math:`b_i^{(j)}` is **dead** if no subsequent
stage reads it; BehaVerify's post-generation pass
(:mod:`behaverify.dsl_to_nuxmv`) removes dead stages, so the final
model carries only live stages.

Node trimming
-------------

A sub-tree whose guard condition (the ``tick_prerequisite`` plus any
ancestor-imposed boolean) is unsatisfiable in every reachable state
cannot fire. The trimming pass in
:mod:`behaverify.dsl_to_nuxmv` identifies such sub-trees (via a
conservative BDD-based reachability argument) and removes them from
the emitted SMV. The ``--do_not_trim`` flag disables this pass.

Trimming is **sound but incomplete**: it never removes a node that
*could* fire, and it may leave in place a node that never fires in
practice.

Non-determinism
---------------

Unknown initial values or environmental noise are encoded as
set-valued SMV assignments:

.. code-block:: text

   init(x) := {1, 2, 3};

nuXmv treats these as **non-deterministic**. Every property is then
implicitly universally quantified over the choices:

.. math::

   M \models \varphi
   \;\Leftrightarrow\;
   \forall \text{resolution of the nondeterminism}.\; M^{\text{resolved}} \models \varphi.

This gives worst-case guarantees, adequate for safety properties but
not for quantitative reasoning.

Putting it together
-------------------

The full BehaVerify $\to$ SMV pipeline is:

1. **Parse.** TextX consumes a ``.tree`` and builds an AST.
2. **Validate.** :mod:`behaverify.check_grammar` rejects
   type/scope/reference errors.
3. **Build IR.** :mod:`behaverify.node_creator` converts the AST to
   the internal node tree.
4. **Meta-compile expressions.** :mod:`behaverify.meta_functions`
   lowers prefix-notation expressions to per-backend expression trees,
   resolving ``constant_index`` and ``loop`` constructs.
5. **Generate SMV.** :mod:`behaverify.dsl_to_nuxmv` walks the IR,
   emits the staging variables, the fast-forwarding transition
   relation, the ``specifications`` block, and (optionally) runs the
   trimming pass.

The resulting ``.smv`` file is self-contained: it can be fed to nuXmv
without the original ``.tree``.

Encoding size
-------------

Serbinowska & Johnson (SEFM 2022) report empirical sizes:

- Naive encoding: state space :math:`\Theta(|V| \cdot 2^{|B|})`.
- Fast-forwarding: state space :math:`\Theta(2^{|B|})`.

The authors verified a binary BT with **2,055 nodes** under
fast-forwarding; naive timed out well below 200. The practical
takeaway: use fast-forwarding (the default) unless you are actively
debugging the compiled transition and want per-step granularity.

References
----------

- Serbinowska, Johnson. BehaVerify: Verifying Temporal Logic
  Specifications for Behavior Trees. *SEFM* 2022, LNCS 13550,
  pp. 307–323.
  https://doi.org/10.1007/978-3-031-17108-6_19
