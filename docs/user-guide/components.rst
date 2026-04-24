Components
==========

.. rst-class:: lead

   BehaVerify supports the standard modern-BT node taxonomy: composite,
   decorator, and leaf. This page lists the node kinds accepted by the
   DSL, their semantics, and the code each backend emits for them.

Composite nodes
---------------

.. list-table::
   :header-rows: 1
   :widths: 22 23 55

   * - Kind
     - DSL keyword
     - Semantics
   * - Sequence
     - ``sequence``
     - Tick children left-to-right; return ``failure``/``running`` on
       first non-success, else ``success``.
   * - Selector (fallback)
     - ``selector``
     - Tick children left-to-right; return ``success``/``running`` on
       first non-failure, else ``failure``.
   * - Parallel
     - ``parallel policy {success_on_all | success_on_one}``
     - Tick all children; return ``success`` once the policy's quorum is
       met.

Every composite may carry a **memory flag**:

- (no flag) -- no memory: each tick restarts from the first child.
- ``with_partial_memory`` -- on re-tick, resume after the last
  ``running`` child.
- ``with_true_memory`` -- additionally remember ``success``/``failure``
  of already-evaluated children.

Decorator nodes
---------------

.. list-table::
   :header-rows: 1
   :widths: 22 23 55

   * - Kind
     - DSL keyword
     - Semantics
   * - Status overrider
     - ``X_is_Y``
     - Re-map the child's status: ``X`` becomes ``Y``. Classical
       aliases like ``success_is_running`` or ``failure_is_success`` are
       expressible.
   * - Inverter
     - ``inverter``
     - Swap ``success`` ↔ ``failure``; leave ``running`` alone.
   * - Repeat
     - ``repeat N``
     - Tick the child up to ``N`` times; succeed only if every attempt
       succeeds.
   * - One-shot
     - ``one_shot {success_only | success_failure | failure_only}``
     - After the chosen terminal status, freeze the node.

Leaf nodes
----------

.. list-table::
   :header-rows: 1
   :widths: 22 23 55

   * - Kind
     - DSL keyword
     - Semantics
   * - Check
     - ``check``
     - Evaluate a boolean condition over declared read-variables;
       ``success`` iff the condition holds.
   * - Environment check
     - ``environment_check``
     - Same shape but reads only environment-scope variables.
   * - Action
     - ``action``
     - Run a sequence of ``variable_statement`` updates, then a
       ``return_statement`` (``success`` / ``failure`` / ``running``).
   * - Neural action
     - ``action`` block with a ``neural_network { ... }`` sub-block
     - Forward-propagates an ONNX model and writes the output to the
       declared ``write_variables``. See :doc:`neural-networks`.

Sub-trees
---------

A ``sub_tree { name ... }`` declaration introduces a reusable named
tree fragment. Inserting a reference is syntactically separate:

.. code-block:: text

   sub_trees {
       sub_tree { safe_stop
           composite { s sequence
               children { emergency_check {} brake {} } } }
   }

   tree {
       composite { root selector children {
           insert { safe_stop }
           ...
       } }
   }

Backend coverage matrix
-----------------------

The following matrix shows where each feature is supported natively by
the generation backend. A dash (``--``) means the feature is either
unsupported or emitted through a non-native wrapper; the upstream
``TODO.md`` tracks the outstanding items.

.. list-table::
   :header-rows: 1
   :widths: 22 11 11 11 11 11

   * - Feature
     - nuxmv
     - python
     - cpp
     - haskell
     - latex
   * - Sequence / Selector
     - Yes
     - Yes
     - partial
     - Yes
     - Yes
   * - Parallel
     - Yes
     - Yes
     - --
     - Yes
     - Yes
   * - Memory flags
     - Yes
     - Yes
     - --
     - Yes
     - --
   * - ``X_is_Y`` / Inverter
     - Yes
     - Yes
     - --
     - Yes
     - Yes
   * - Repeat / One-shot
     - Yes
     - Yes
     - --
     - Yes
     - Yes
   * - Sub-tree insertion
     - Yes
     - Yes
     - partial
     - Yes
     - Yes
   * - Neural leaf (ONNX)
     - Yes
     - Yes
     - partial
     - Yes
     - --

See :doc:`modes` for the per-backend command-line reference.
