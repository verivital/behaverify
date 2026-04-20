The ``.tree`` DSL
=================

.. rst-class:: lead

   BehaVerify reads a TextX-based DSL. This page is a compact reference
   to every block, every expression family, and the type system.

Top-level structure
-------------------

Every ``.tree`` file contains the following named blocks in order. All
blocks must appear; empty blocks are permitted.

.. code-block:: text

   configuration { }        # hypersafety / use_reals / neural flags
   enumerations  { }        # user-defined enums
   constants     { }        # named numeric / enum constants
   variables     { }        # blackboard / environment / local vars
   environment_update { }   # how the environment ticks
   monitors      { }        # optional LTL-triggered contingency actions
   checks        { }        # boolean-returning condition leaves
   environment_checks { }   # environment-only conditions
   actions       { }        # state-updating action leaves
   sub_trees     { }        # reusable named subtrees
   tree          { }        # the root tree
   tick_prerequisite { True }
   specifications { }       # INVARSPEC / CTLSPEC / LTLSPEC

The grammar allows ``end_<block>`` in place of a closing ``}`` for
readability; you cannot mix the two styles on the same opener.

Variable scopes and types
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - Scope
     - Tag
     - Meaning
   * - Blackboard
     - ``bl``
     - Shared state across all nodes.
   * - Environment
     - ``env``
     - State only the environment updates.
   * - Local
     - declared inside ``action`` or ``check`` blocks
     - Scoped to a single node.

Types:

- ``BOOLEAN``
- ``INT``
- ``REAL`` (enable via ``configuration { use_reals }``)
- ``[lo, hi]`` -- integer ranges
- enumerations declared in ``enumerations { ... }``
- arrays via the ``array`` modifier

.. code-block:: text

   variable { bl pos   VAR [0, 9]        assign { result {0}   } }
   variable { bl flag  VAR BOOLEAN       assign { result {TRUE}} }
   variable { bl mode  VAR {idle, run}   assign { result {idle}} }
   variable { bl trail array VAR [0, 9]  assign { result {0}   } }

Expression language
-------------------

Every expression is written in **prefix notation**. The table below is
exhaustive for scalar arithmetic and logic; temporal operators only
appear inside the ``specifications`` block.

Arithmetic
^^^^^^^^^^

``(add x y)``, ``(sub x y)``, ``(mult x y)``, ``(idiv x y)``,
``(mod x y)``, ``(neg x)``, ``(abs x)``, ``(min x y)``, ``(max x y)``.

Comparison
^^^^^^^^^^

``(eq x y)``, ``(neq x y)``, ``(lt x y)``, ``(gt x y)``,
``(lte x y)``, ``(gte x y)``.

Boolean
^^^^^^^

``(and a b)``, ``(or a b)``, ``(not a)``, ``(implies a b)``,
``(equivalent a b)``, ``(if cond then else)``.

Array access
^^^^^^^^^^^^

``(index arr i)`` -- dynamic index.
``(index arr (constant_index i))`` -- compile-time index
(significantly tighter in nuXmv output).

Node status
^^^^^^^^^^^

Usable inside specifications only:

``(success node)``, ``(failure node)``, ``(running node)``,
``(active node)``.

Loops and case
^^^^^^^^^^^^^^

``(loop v [lo, hi] such_that cond, body)`` -- constructive summation
over a compile-time range.

``case { cond } result { value } result { default }`` --
``if / else if / else`` chains, permitted in ``result``-producing
positions.

Temporal operators
^^^^^^^^^^^^^^^^^^

Inside LTL specs: ``(next x)``, ``(globally x)``, ``(finally x)``,
``(until x y)``, ``(release x y)``.

Inside CTL specs: ``(always_globally x)``, ``(always_finally x)``,
``(exists_globally x)``, ``(exists_finally x)``.

Inside invariant specs, an auxiliary ``at`` operator accesses a
historical tick (bounded integer). See
:doc:`specifications`.

Meta code vs. code
------------------

- ``code`` -- evaluated at tick-time; may reference variables.
- ``meta_code`` -- must reduce to a compile-time constant; permitted
  in ``loop`` bounds and ``constant_index``.

Loop variables appear in both. Define-kind variables must have
deterministic updates to be evaluable in meta positions.

Next steps
----------

- :doc:`components` -- the node types the DSL assembles into trees.
- :doc:`specifications` -- temporal-logic queries the tool dispatches
  to nuXmv.
- :doc:`neural-networks` -- how an ONNX file plugs into a leaf.
