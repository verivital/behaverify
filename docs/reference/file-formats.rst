File Formats
============

BehaVerify works with the following on-disk artefacts.

Inputs
------

``.tree``
^^^^^^^^^

The primary input: a behavior tree described in BehaVerify's DSL. See
:doc:`/user-guide/tree-dsl` for the grammar reference.

``.onnx``
^^^^^^^^^

Neural-network weights consumed by ``neural_network`` leaves. See
:doc:`/user-guide/neural-networks`.

``.smv``
^^^^^^^^

An already-existing nuXmv SMV model; can be fed to ``nuxmv`` mode
without ``--generate`` to re-verify without re-emission.

Outputs
-------

``<output>/nuxmv/<name>.smv``
    nuXmv SMV model.

``<output>/nuxmv/<name>_output.txt``
    Captured nuXmv stdout (specifications, simulation traces).

``<output>/python/<name>.py``, ``<output>/python/runner.py``
    Generated ``py_trees`` implementation and an invocation script.

``<output>/cpp/<name>.cpp``, ``<output>/cpp/<name>.h``
    Generated BT.CPP leaf-node classes.

``<output>/haskell/<name>.hs``
    Generated pure Haskell implementation.

``<output>/<name>.tex``
    Generated TikZ diagram (``latex`` mode).

Generated directories respect ``--overwrite``; without that flag the
tool refuses to clobber existing files.

Traces
------

``*_output.txt`` produced by nuXmv follows the standard nuXmv format:
one block per specification with either ``is true`` or ``is false``
followed by a counter-example trace in the ``-> State: ... <-`` notation.
The ``trace`` mode renders these back into labelled node / variable
sequences.
