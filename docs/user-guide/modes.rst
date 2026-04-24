Generation Modes
================

.. rst-class:: lead

   BehaVerify's CLI dispatches to one of seven modes. This page
   summarises each, lists the principal options, and shows a canonical
   invocation.

General form
------------

.. code-block:: bash

   python -m behaverify <mode> <model.tree> <output_dir> [options...]

The mode keyword is case-insensitive.

``nuxmv``
---------

Generate an SMV model and optionally invoke nuXmv to discharge
``specifications``.

.. code-block:: bash

   python -m behaverify nuxmv model.tree ./out \
       --generate --invar --ctl --ltl \
       --simulate 10 --nuxmv_path ../nuXmv

Key options:

- ``--generate`` -- write the ``.smv`` file (required when the input is
  a ``.tree``; omit when feeding an existing ``.smv``).
- ``--invar``, ``--ctl``, ``--ltl`` -- discharge the corresponding
  specifications.
- ``--simulate N`` -- simulate the model for ``N`` steps.
- ``--use_encoding {fastforwarding | naive}`` -- see :doc:`encodings`.
- ``--keep_last_stage`` -- disable the last-stage optimisation
  (debugging).
- ``--do_not_trim`` -- keep unreachable nodes (debugging).

``python``
----------

Generate a ``py_trees`` implementation.

.. code-block:: bash

   python -m behaverify python model.tree ./out --max_iter 500

Key options:

- ``--max_iter N`` -- how many ticks the generated runner loops for.
- ``--serene_print`` -- use the Serene custom printer.
- ``--py_tree_print`` -- use ``py_trees``'s ASCII tree printer.

``cpp``
-------

Generate C++ leaf-node classes compatible with
`BehaviorTree.CPP <https://www.behaviortree.dev/>`_.

.. code-block:: bash

   python -m behaverify cpp model.tree ./out

.. note::

   Current cpp coverage is a subset of the full BT.CPP v4 feature set;
   see the coverage table in :doc:`components` and the upstream
   ``TODO.md`` for tracked gaps.

``haskell``
-----------

Generate a pure-functional Haskell implementation.

.. code-block:: bash

   python -m behaverify haskell model.tree ./out

Uses the templates in ``src/behaverify/data/haskell_files/``.

``latex``
---------

Render the tree as a TikZ diagram.

.. code-block:: bash

   python -m behaverify latex model.tree ./diagram.tex
   pdflatex diagram.tex

Options:

- ``--insert_only`` -- emit only the TikZ block (no preamble).
- ``--on_sides`` -- inline variable annotations on the side.

``trace``
---------

Render a nuXmv counter-example trace as a sequence of images.

.. code-block:: bash

   python -m behaverify nuxmv model.tree ./out --generate --invar \
       --nuxmv_path ../nuXmv
   python -m behaverify trace model.tree \
       ./out/nuxmv/model_output.txt ./out/

``grid``
--------

Specialised rendering for grid-world traces.

.. code-block:: bash

   python -m behaverify grid nuxmv ./trace.txt ./out/ 10 10

The two trailing arguments are the grid's ``x_size`` and ``y_size``.
The ``grid`` mode infers entity positions from variable names and is
intentionally schema-specific -- it pairs well with the Grid-world
example template in ``examples/``.

Shared options
--------------

All modes accept:

- ``--overwrite`` -- replace existing files at the output path.
- ``--recursion_limit N`` -- raise Python's recursion limit (needed for
  very deep trees).
- ``--no_checks`` -- skip grammar / type validation (faster, riskier).
