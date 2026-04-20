Installation
============

BehaVerify is a pure-Python package with a single external dependency
(`nuXmv <https://nuxmv.fbk.eu/>`_), required only when you actually
invoke the formal-verification mode. Every other generation mode ---
Python, C++, Haskell, LaTeX, runtime monitors --- runs with just Python.

Supported Python versions: **3.10, 3.11, 3.12**. Platforms: Linux,
macOS, Windows.

From source
-----------

.. code-block:: bash

   git clone https://github.com/verivital/behaverify
   cd behaverify
   python3 -m venv ../behaverify_venv
   source ../behaverify_venv/bin/activate      # Linux/macOS
   # .\..\behaverify_venv\Scripts\activate     # Windows PowerShell
   pip install -e ".[dev]"

The ``[dev]`` extra pulls in ``pytest`` and ``pytest-cov`` for the
regression suite.

nuXmv (required for ``nuxmv`` mode)
-----------------------------------

The nuXmv licence forbids redistribution, so BehaVerify cannot bundle
it. Download it from the nuXmv project page:

.. code-block:: bash

   wget "https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz" \
       -O nuXmv_DL.tar.xz
   tar -xf nuXmv_DL.tar.xz --one-top-level=nuXmv_DL --strip-components 1
   mv nuXmv_DL/bin/nuXmv ../nuXmv
   chmod +x ../nuXmv

Windows users should download the Windows build from the same page and
place ``nuXmv.exe`` somewhere on ``PATH``. When invoking BehaVerify,
pass the path via ``--nuxmv_path``:

.. code-block:: bash

   behaverify nuxmv model.tree ./out --generate --ctl --nuxmv_path ../nuXmv

ONNX runtime (required for neural-leaf models)
----------------------------------------------

``onnx`` and ``onnxruntime`` are already declared in ``pyproject.toml``;
they are installed automatically by the command above. No manual step
is needed unless you want to target a GPU build of ``onnxruntime``.

Verify the installation
-----------------------

.. code-block:: bash

   python -m behaverify python examples/Collatz/collatz.tree ./out_collatz

Inspect ``./out_collatz/python/collatz.py`` --- it should be a
``py_trees`` implementation of the Collatz behavior tree. If the
``--generate`` flag also wrote ``./out_collatz/nuxmv/collatz.smv`` you
are ready for the :doc:`quickstart`.

Troubleshooting
---------------

.. admonition:: TextX grammar complaints
   :class: tip

   Grammar errors usually come with a line + column and an expected-
   token list. The most common cause is a missing ``end_*`` keyword;
   BehaVerify accepts both brace-terminated blocks (``}``) and
   ``end_block``-terminated blocks but they cannot be mixed on the same
   opener.

.. admonition:: ``recursion_limit`` errors
   :class: warning

   Very deep trees (>400 nodes) can overflow Python's default recursion
   limit during parsing. Pass ``--recursion_limit 3000`` or similar.

.. admonition:: Windows path quoting
   :class: warning

   Use forward slashes in arguments or wrap paths in double quotes.
   Most build failures on Windows come from shell-split backslashes.
