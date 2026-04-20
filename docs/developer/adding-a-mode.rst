Adding a Generation Mode
========================

.. The original example here was "add a PRISM backend that would
   generate a DTMC from a .tree model". Reinstate when the
   probabilistic back-end work resumes.

This page walks through the minimal steps to add a new generation
mode (for example, a back-end that emits Promela for the SPIN model
checker).

1. Create the backend module
----------------------------

.. code-block:: text

   src/behaverify/dsl_to_<mode>.py

Export a top-level function with the conventional signature:

.. code-block:: python

   def dsl_to_mode(
       metamodel_file, model_file, main_name, write_location,
       recursion_limit, no_checks, **options,
   ):
       """Write the back-end's artefact files into ``write_location``."""

2. Register the mode in the CLI
-------------------------------

Open ``src/behaverify/behaverify.py``. Find the mode dispatch (a chain
of ``if args.mode == "...":`` branches) and add a branch for your new
mode name that imports your module and calls its entry point. Add
corresponding CLI arguments (``argparse.add_subparsers`` or manual
branch) for any mode-specific flags.

3. Hook into the test runner
----------------------------

Add a test fixture in ``tests/test_all_modes.py`` that invokes your new
mode on a canonical example (``examples/Collatz/collatz.tree`` is a
good starter). The existing mode tests give the template.

4. Update the docs
------------------

- :doc:`/user-guide/modes` -- CLI reference entry.
- :doc:`/user-guide/components` -- coverage matrix row.
- :doc:`/user-guide/verification-strategies` -- strategy summary.

If the new mode introduces a new DSL construct, extend the grammar
under ``src/behaverify/data/metamodel/behaverify.tx`` and update
:mod:`behaverify.check_grammar` -- see :doc:`adding-a-check`.

5. Follow the existing conventions
----------------------------------

- Emit files under ``<write_location>/<mode>/``.
- Respect ``--overwrite`` -- never clobber by default.
- Accept ``--recursion_limit`` and ``--no_checks`` uniformly.
- Emit deterministic output (no timestamps) so golden-file tests work.

Checklist before PR
-------------------

- ``pytest`` passes.
- ``make -C docs html`` builds without warnings.
- You have added or updated an example demonstrating the new mode.
- The user-guide pages mention the new mode.
