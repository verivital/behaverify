Your First Model
================

.. rst-class:: lead

   We'll build a 6-line behavior tree that checks a battery variable
   and either explores or goes home, then we'll verify a safety
   invariant against it.

The DSL in one page
-------------------

A ``.tree`` file has seven named blocks, in this order:

.. code-block:: text

   configuration { }
   enumerations  { }
   constants     { }
   variables     { variable { bl battery VAR [0, 100] assign { result {100} } } }
   environment_update { }
   checks        { ... }
   actions       { ... }
   sub_trees     { }
   tree          { ... }
   tick_prerequisite { True }
   specifications { INVARSPEC { (gte, battery, 0) } }

Every block is required to appear, but many may be empty. See
:doc:`../user-guide/tree-dsl` for the full grammar.

A minimal model
---------------

Save the following as ``battery.tree``:

.. code-block:: text

   configuration { }
   enumerations  { }
   constants     { }

   variables {
       variable { bl battery VAR [0, 100]
           assign { result {100} } }
       variable { bl at_home VAR BOOLEAN
           assign { result {TRUE} } }
   }

   environment_update { }

   checks {
       check { battery_low arguments {} read_variables {battery}
           condition {(lt, battery, 20)} }
       check { home arguments {} read_variables {at_home}
           condition {at_home} }
   }
   environment_checks { }

   actions {
       action { explore arguments {}
           local_variables {} read_variables {battery}
           write_variables {battery, at_home} initial_values {}
           update {
               variable_statement {battery assign {result {(sub, battery, 10)} } }
               variable_statement {at_home assign {result {FALSE} } }
               return_statement { result {success} } } }
       action { return_home arguments {}
           local_variables {} read_variables {}
           write_variables {battery, at_home} initial_values {}
           update {
               variable_statement {battery assign {result {100} } }
               variable_statement {at_home assign {result {TRUE} } }
               return_statement { result {success} } } }
   }

   sub_trees { }

   tree {
       composite { root selector
           children {
               composite { rth sequence
                   children { battery_low {} return_home {} } }
               explore {} } }
   }

   tick_prerequisite { True }

   specifications {
       INVARSPEC { (gte, battery, 0) }
       LTLSPEC { (globally (implies battery_low (finally home))) }
   }

Generate and verify
-------------------

.. code-block:: bash

   python -m behaverify nuxmv battery.tree ./battery_out \
       --generate --invar --ltl --nuxmv_path ../nuXmv

Expected output (trimmed):

.. code-block:: text

   -- specification  G ((battery >= 0))  is true
   -- specification  G (battery_low -> F home)  is true

You have now authored, generated, and formally verified your first
behavior tree. From here:

- Add a decorator: :doc:`../user-guide/components`.
- Plug in a neural leaf: :doc:`../user-guide/neural-networks`.
- Pick a different backend: :doc:`../user-guide/modes`.
