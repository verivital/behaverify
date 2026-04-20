Testing
=======

.. code-block:: bash

   pytest -q                    # whole suite
   pytest -q tests/test_regression.py
   pytest -q --cov=behaverify

The suite covers:

- ``tests/test_behaverify.py`` -- shared utilities.
- ``tests/test_regression.py`` -- known-good / known-bad ``.tree``
  files from ``test_examples/``.
- ``tests/test_all_modes.py`` -- smoke-tests every generation mode.
- ``tests/test_e2e_python_generation.py`` -- generated Python code
  compiles and ticks.
- ``tests/test_programmatic_api.py`` -- in-process invocation.
- ``tests/test_full_coverage.py`` / ``tests/test_additional_coverage.py``
  -- edge cases and error handling.

Tests tagged ``needs_nuxmv`` are auto-skipped unless the environment
variable ``NUXMV_BIN`` points to a nuXmv binary. Likewise ONNX-gated
tests are skipped if ``onnxruntime`` is unavailable.

Regression examples
-------------------

- ``test_examples/working/`` -- expected to parse and generate.
- ``test_examples/intentionally_broken/`` -- expected to fail with a
  specific error message.

When modifying the parser or validator, also run the tutorial suite
under ``tutorial_examples/`` to catch wording-level regressions.
