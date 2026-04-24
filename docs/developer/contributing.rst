Contributing
============

.. rst-class:: lead

   Issue reports, PRs, and forks welcome. This page is the short
   version of the workflow.

Workflow
--------

1. Fork the repository on GitHub.
2. Create a feature branch: ``git checkout -b feat/my-thing``.
3. Run the tests before you start: ``pytest -q`` --- everything should
   be green on ``main``.
4. Make your change. Keep the diff focused.
5. Add or update tests. Public-facing changes also need a docs update
   (in ``docs/``).
6. Run ``pytest`` and ``make -C docs html`` locally.
7. Open a pull request with a clear problem statement and a
   ``Test plan`` checklist.

Code style
----------

- Python: PEP 8 with ``pylint`` enforcement in CI.
- Prefer explicit imports; avoid wildcard ``from X import *``.
- Error messages should include the offending model line / column
  wherever possible.
- Wrap user-facing errors in :class:`~behaverify.behaverify_common.BTreeException`.

Docs style
----------

- Sphinx sources under ``docs/``. ReST preferred for core pages; MyST
  (Markdown) acceptable for developer notes.
- Cross-reference liberally with ``:doc:`` and ``:ref:``.
- Keep the landing pipeline diagram in sync with any backend or input
  change --- the source lives in
  ``docs/_static/tikz/pipeline.tex``.

Release process
---------------

Tagged releases follow semantic versioning. The maintainer publishes to
PyPI and cuts a GitHub release note; the exact script is in
``scripts/``.

Reporting issues
----------------

Open an issue with:

- Your Python version and OS.
- Whether nuXmv is installed and, if so, the version.
- The ``.tree`` file (minimised) that reproduces the problem.
- The full stack trace or the nuXmv stdout excerpt.
