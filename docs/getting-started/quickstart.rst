Quickstart
==========

.. rst-class:: lead

   Five minutes from a fresh clone to a verified CTL property. We use
   the bundled ``examples/DrunkenDrone/DrunkenDrone.tree`` model.

Run the tool
------------

From the repository root, with the virtual environment active:

.. code-block:: bash

   python -m behaverify nuxmv \
       examples/DrunkenDrone/DrunkenDrone.tree \
       ../behaverify_test/ \
       --generate --invar --ctl --ltl --simulate 10 \
       --nuxmv_path ../nuXmv

What this does, step by step:

1. ``--generate`` parses the ``.tree`` file and emits
   ``../behaverify_test/nuxmv/DrunkenDrone.smv``.
2. ``--invar``, ``--ctl``, ``--ltl`` invoke nuXmv on that SMV model to
   discharge invariant / CTL / LTL specifications declared inside the
   ``specifications { ... }`` block of the ``.tree`` file.
3. ``--simulate 10`` produces a 10-step simulation trace.
4. The combined nuXmv stdout is captured in
   ``../behaverify_test/nuxmv/DrunkenDrone_output.txt``.

Read the outputs
----------------

.. code-block:: bash

   cat ../behaverify_test/nuxmv/DrunkenDrone.smv          # the model
   cat ../behaverify_test/nuxmv/DrunkenDrone_output.txt   # nuXmv stdout

The stdout file contains one block per specification, either
``-- specification ...  is true`` (verified) or ``is false`` followed by
a counter-example trace you can render with :doc:`../user-guide/modes`
(``trace`` mode).

Swap to a Python runtime
------------------------

For on-robot use you usually want the same tree as executable Python:

.. code-block:: bash

   python -m behaverify python \
       examples/DrunkenDrone/DrunkenDrone.tree \
       ../behaverify_demo_py/ --max_iter 200

This produces a ``py_trees`` implementation plus a ``runner.py`` that
loops the tick function. Open the runner and adapt it to wire your own
blackboard readers / environment handlers.

Swap to C++
-----------

The ``cpp`` mode generates BT.CPP-compatible leaf-node classes:

.. code-block:: bash

   python -m behaverify cpp \
       examples/DrunkenDrone/DrunkenDrone.tree \
       ../behaverify_demo_cpp/

See :doc:`../user-guide/modes` for the current coverage of BT.CPP v4
features.

Next steps
----------

- Write your own tree: :doc:`first-model`.
- Browse the DSL reference: :doc:`../user-guide/tree-dsl`.
- Compare verification strategies: :doc:`../user-guide/verification-strategies`.
