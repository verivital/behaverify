Developer Guide
===============

.. rst-class:: lead

   Internal architecture, how to add a new generation mode or node
   type, and the conventions the maintainers follow.

----

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Architecture
      :link: architecture
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      Parser, validator, IR, and the per-backend layout.

   .. grid-item-card:: Adding a generation mode
      :link: adding-a-mode
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      Plug a new ``dsl_to_<mode>.py`` into the CLI.

   .. grid-item-card:: Adding a check or action type
      :link: adding-a-check
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      Grammar, ``node_creator``, ``check_grammar``, and tests.

   .. grid-item-card:: Testing
      :link: testing
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      ``pytest``, test-examples structure, nuXmv-gated tests.

   .. grid-item-card:: Contributing
      :link: contributing
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      Workflow, code style, PR process.

.. toctree::
   :maxdepth: 1
   :hidden:

   architecture
   adding-a-mode
   adding-a-check
   testing
   contributing
