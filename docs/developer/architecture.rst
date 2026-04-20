Architecture
============

Five passes take a ``.tree`` file to a backend artefact.

1. **Parse** -- TextX applies the grammar in
   ``src/behaverify/data/metamodel/behaverify.tx``.
2. **Validate** -- :mod:`behaverify.check_grammar` performs static
   checks (type / scope / reachability).
3. **Build IR** -- :mod:`behaverify.node_creator` constructs the
   internal node tree.
4. **Meta-compile expressions** -- :mod:`behaverify.meta_functions`
   lowers prefix-notation expressions to per-backend expression trees.
5. **Generate** -- a ``dsl_to_<mode>.py`` module walks the IR and emits
   the artefact.

Module map
----------

.. list-table::
   :header-rows: 1

   * - File
     - Responsibility
   * - ``behaverify.py``
     - CLI entry point; mode dispatch.
   * - ``check_grammar.py``
     - Static validation (types, scope, references).
   * - ``node_creator.py``
     - DSL model → internal node tree.
   * - ``meta_functions.py``
     - Expression IR and meta-compilation.
   * - ``meta_functions_neural.py``
     - ONNX → expression IR.
   * - ``dsl_to_nuxmv.py``
     - SMV generator (fastforwarding + naive encodings).
   * - ``dsl_to_python.py``
     - ``py_trees`` generator.
   * - ``dsl_to_cpp.py``
     - BT.CPP-compatible C++ generator.
   * - ``dsl_to_haskell.py``
     - Pure Haskell generator.
   * - ``dsl_to_latex.py``
     - TikZ diagram generator.
   * - ``counter_trace.py``, ``grid_world_draw/``
     - Trace rendering.

API reference
-------------

The full auto-generated API reference lives under
:doc:`/api/index` (built with ``sphinx-autoapi``).

Dataflow
--------

.. mermaid::

   flowchart TD
     A[.tree file] --> B[TextX parser]
     B --> C[check_grammar.validate_model]
     C --> D[node_creator.build_model]
     D --> E[meta_functions lowering]
     E --> F1[dsl_to_nuxmv]
     E --> F2[dsl_to_python]
     E --> F3[dsl_to_cpp]
     E --> F4[dsl_to_haskell]
     E --> F5[dsl_to_latex]
     F1 --> G1[.smv model]
     F2 --> G2[py_trees .py]
     F3 --> G3[BT.CPP .cpp/.h]
     F4 --> G4[Haskell .hs]
     F5 --> G5[TikZ .tex]

Every backend receives the same IR, so adding a mode does not require
changes to the parser or the IR builder -- see :doc:`adding-a-mode`.
