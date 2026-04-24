Command-Line Reference
======================

``behaverify`` is installed as a Python module. Invoke as either:

.. code-block:: bash

   behaverify <mode> <args...>
   # or
   python -m behaverify <mode> <args...>

General form
------------

.. code-block:: text

   behaverify <mode> <model_file> <output_location> [options...]

``<mode>`` is one of ``nuxmv``, ``python``, ``cpp``, ``haskell``,
``latex``, ``trace``, ``grid``. Case-insensitive.

Shared options
--------------

.. option:: --overwrite

   Replace existing files at the output location.

.. option:: --recursion_limit N

   Raise Python's recursion limit to ``N`` (default 1000). Required for
   very deep trees.

.. option:: --no_checks

   Skip static validation. Faster but leaks unhelpful tracebacks on
   malformed models.

.. option:: --record_times PATH

   Write an execution-time report to ``PATH``.

``nuxmv``-mode options
----------------------

.. option:: --generate

   Parse the ``.tree`` input and emit SMV. Required unless feeding an
   existing ``.smv``.

.. option:: --invar, --ctl, --ltl

   Invoke nuXmv on the ``INVARSPEC`` / ``CTLSPEC`` / ``LTLSPEC``
   blocks of the input.

.. option:: --simulate N

   Simulate for ``N`` steps.

.. option:: --nuxmv_path PATH

   Path to the nuXmv executable. Required whenever ``--invar``,
   ``--ctl``, ``--ltl``, or ``--simulate`` is used.

.. option:: --use_encoding {fastforwarding | naive}

   See :doc:`/user-guide/encodings`.

.. option:: --keep_last_stage

   Disable the last-stage optimisation.

.. option:: --do_not_trim

   Retain unreachable nodes in the generated SMV.

``python``-mode options
-----------------------

.. option:: --max_iter N

   Number of ticks for the generated runner (default 100).

.. option:: --no_var_print, --serene_print, --py_tree_print

   Control the per-tick printout.

``latex``-mode options
----------------------

.. option:: --insert_only

   Emit only a TikZ block (no preamble).

.. option:: --on_sides

   Place variable annotations beside nodes instead of below.

Worked examples live under :doc:`/examples/index`.
