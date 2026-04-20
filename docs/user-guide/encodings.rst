Encodings
=========

.. rst-class:: lead

   How BehaVerify compresses a full behavior-tree tick into an SMV
   transition. The default encoding is designed for scale.

Fast-forwarding vs naive
------------------------

The ``--use_encoding`` flag selects how a tick is lowered into SMV:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Option
     - How a tick is encoded
     - State-space growth
   * - ``fastforwarding`` *(default)*
     - An entire tick (root-to-leaf traversal + all updates) is a
       single SMV transition.
     - Linear in tree depth / width.
   * - ``naive``
     - Each internal BT step --- entering a composite, ticking a child,
       returning from it --- is one SMV transition.
     - Grows roughly with tree nodes × program counters.

Fast-forwarding is the contribution introduced in Serbinowska &
Johnson (SEFM 2022) and refined in follow-ups. Reported in the tool
paper: **2,055-node trees verified** vs. approximately 200 nodes in
comparable non-fast-forwarding tools.

Variable staging
----------------

Because a tick may read and write the same blackboard slot multiple
times, BehaVerify stages each blackboard variable:

.. code-block:: text

   x_stage_0  # value at tick start
   x_stage_1  # after leaf A
   x_stage_2  # after leaf B
   ...
   x_stage_n  # value at tick end

``next(x_stage_0) := x_stage_n;`` closes the loop across ticks. The
``--keep_last_stage`` flag keeps every stage alive; by default, unused
intermediate stages are eliminated.

Node-trimming
-------------

If nuXmv (or the static analyser) determines a sub-tree cannot run
under the declared ``tick_prerequisite``, BehaVerify removes those
nodes from the generated SMV / Python / C++ code. ``--do_not_trim``
disables this and is useful when you want counter-examples to list
unreachable nodes verbatim.

Non-deterministic choice
------------------------

BehaVerify uses set-valued SMV assignments ``init(x) := {1, 2, 3};`` to
model unknown initial conditions or noisy environments. nuXmv treats
these as *non-deterministic* --- the verifier proves the property
against the adversarial worst case.

..
   Trailing sentence is commented out while the probabilistic
   back-end is parked. Restore when the feature lands.
..
   See :doc:`verification-strategies` for where probabilistic
   semantics would sit instead.
