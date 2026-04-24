Soundness
=========

.. rst-class:: lead

   When nuXmv reports "specification ... is true", that verdict must
   carry back to the original ``.tree`` model. This page is the
   end-to-end soundness argument: five sequential claims, each of
   which the literature or BehaVerify's test suite backs.

The soundness chain
-------------------

Let :math:`T` be a behavior tree, :math:`\varphi` a DSL-level
specification, and :math:`M_T` the SMV model BehaVerify emits for
:math:`T`. We want:

.. math::

   M_T \models_{\text{SMV}} \tau(\varphi)
   \;\Longrightarrow\;
   T \models_{\text{BT}} \varphi.

where :math:`\tau` is BehaVerify's translation of DSL specifications
into SMV ``INVARSPEC`` / ``LTLSPEC`` / ``CTLSPEC`` syntax.

The argument is built around two intermediate representations that
sit between the user-facing ``.tree`` file and the SMV model nuXmv
verifies:

- **AST** (*abstract syntax tree*) --- the tree-shaped parse result
  produced by TextX from the raw DSL string. It records every
  grammatical construct the user wrote, before any semantic
  processing.
- **IR** (*internal representation*) --- BehaVerify's own
  :mod:`behaverify.node_creator` output. It is a typed,
  scope-resolved graph of ``InternalNode`` objects with all
  sub-tree insertions expanded and every variable / expression
  pinned to its declared type and scope. Every generator
  (``dsl_to_nuxmv``, ``dsl_to_python`` …) reads from the same IR.

The chain decomposes as:

.. figure:: /_static/img/soundness-chain.png
   :alt: Soundness chain from .tree to T models phi with five numbered
         claims labelling each preservation step.
   :class: pipeline-hero
   :width: 95%

   The soundness chain.

Each arrow must preserve meaning. We enumerate the five claims below.

Claim 1 --- grammar parsing is injective
----------------------------------------

The TextX parser at
``src/behaverify/data/metamodel/behaverify.tx`` is an injective map
from DSL strings to ASTs up to whitespace, comments, and
block-terminator style (``}`` vs ``end_*``). A DSL string that parses
without error identifies a unique AST.

*Evidence:* TextX's parser is generated from the metamodel; ambiguity
would manifest as a shift/reduce warning at generation time, which
the test suite asserts does not occur
(``tests/test_behaverify.py::test_metamodel_loads``).

Claim 2 --- validation rejects ill-formed trees
-----------------------------------------------

``check_grammar.validate_model`` enforces:

- every variable is declared before use and used in a consistent
  scope (``bl`` / ``env`` / local);
- every expression type-checks against the declared types;
- every node name is unique within its sibling list;
- every reference (to a sub-tree, a variable, a constant, a node
  name in a specification) resolves.

A model passing validation is guaranteed well-typed and
well-referenced. The validator is *conservative*: any warning halts
translation.

*Evidence:* ``test_examples/intentionally_broken/`` contains one
invalid ``.tree`` file per failure mode; the regression suite
asserts each triggers an error.

Claim 3 --- the IR preserves the AST's semantics
------------------------------------------------

:mod:`behaverify.node_creator` walks the AST and builds an
``InternalNode`` tree. The transformation renames certain
constructs for uniformity (e.g., anonymous sub-trees gain synthetic
names) but does not alter the *tick* relation.

*Evidence:* for every test in ``test_examples/working/``, the
Python-mode and nuXmv-mode outputs are regenerated on every commit
and diffed against the checked-in reference
(``tests/test_all_modes.py``). Divergence fails CI.

Claim 4 --- the fast-forwarding encoding is equivalent to the BT tick
---------------------------------------------------------------------

Formalised and proved in Serbinowska & Johnson (SEFM 2022):

**Theorem (Fast-forwarding equivalence).**
For every BT :math:`T` and blackboard-only LTL/CTL/INVAR formula
:math:`\varphi`,

.. math::

   M_T^{\text{FF}} \models \tau(\varphi)
   \;\Longleftrightarrow\;
   M_T^{\text{naive}} \models \tau(\varphi)
   \;\Longleftrightarrow\;
   T \models_{\text{BT}} \varphi.

The proof shows that :math:`M_T^{\text{FF}}` and
:math:`M_T^{\text{naive}}` are **stuttering-equivalent**: they visit
the same blackboard values in the same order, modulo the
internal-BT-step states that LTL/CTL cannot distinguish when atoms
refer only to blackboard variables.

*Evidence:* formal proof in the SEFM 2022 paper plus BehaVerify's
differential-testing harness (``tests/test_all_modes.py``) that runs
the same queries under ``fastforwarding`` and ``naive`` encodings and
asserts identical verdicts.

Claim 5 --- nuXmv's algorithms are sound and complete
-----------------------------------------------------

nuXmv's INVAR, CTL, and LTL checks are sound and complete for finite
Kripke structures. See :doc:`model-checking` for the underlying
algorithms; correctness proofs are in the canonical references
(Baier & Katoen; Clarke, Grumberg & Peled). Where BehaVerify
exposes a choice of algorithm (e.g., IC3 vs. BDD reachability for
invariants), both are sound and complete for the same class of
problems.

*Evidence:* nuXmv's peer-reviewed publications, its long deployment
history, and the accompanying nuXmv regression suite.

Putting the claims together
---------------------------

Composing Claims 1–5:

.. math::

   \text{.tree parses} \;\wedge\; \text{validates} \;\Rightarrow\;
   \text{IR is well-typed}

.. math::

   \text{IR} \xrightarrow{\text{Claim 4}}
   M_T^{\text{FF}} \text{ with } T \models \varphi
   \Leftrightarrow M_T^{\text{FF}} \models \tau(\varphi)

.. math::

   \text{nuXmv returns ``verified''}
   \xrightarrow{\text{Claim 5}}
   M_T^{\text{FF}} \models \tau(\varphi)

.. math::

   \therefore\quad
   \text{nuXmv verdict ``verified''}
   \;\Longrightarrow\;
   T \models_{\text{BT}} \varphi.

Counter-examples
----------------

When nuXmv returns "false", it emits a finite trace through
:math:`M_T` witnessing the violation. BehaVerify's ``trace`` mode
lifts that trace back into a per-tick log at the BT level:

1. Parse the nuXmv stdout and extract the :math:`(s_0, s_1, \ldots,
   s_k)` sequence.
2. Decode each :math:`s_i` into its blackboard valuation and the
   per-tick node-status map.
3. Render an image or log per tick.

Because Claim 4 preserves meaning in *both* directions, the BT-level
trace witnesses the same violation as the SMV-level trace.

Caveats
-------

The soundness chain assumes:

- the SMV semantics implemented by nuXmv matches the textbook
  semantics used in Claim 4's proof;
- the nuXmv binary used is un-patched and un-corrupted;
- floating-point reals (enabled via ``configuration { use_reals }``)
  are interpreted as :math:`\mathbb{R}` by nuXmv --- i.e., with
  infinite-precision arithmetic, not machine floats. Mixing
  ``use_reals`` and runtime ONNX execution (``.py`` mode) can
  therefore produce a verified tree that *fails* at runtime on float
  non-associativity; see :doc:`neuro-symbolic` for the discussion.

Noisy environments modelled as non-determinism give **worst-case**
guarantees. The verifier proves :math:`\varphi` holds against the
adversary, not with any particular probability.

References
----------

- Serbinowska, Johnson. BehaVerify. *SEFM* 2022.
- Baier, Katoen. *Principles of Model Checking.* MIT Press, 2008.
- Cavada et al. The nuXmv Symbolic Model Checker. *CAV* 2014.
