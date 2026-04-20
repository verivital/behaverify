User Guide
==========

.. rst-class:: lead

   What BehaVerify accepts as input, what it produces as output, and
   how each piece of the DSL is handled across the six generation
   modes.

----

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Tree DSL reference
      :link: tree-dsl
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      The ``.tree`` grammar: blocks, types, expressions, temporal
      operators.

   .. grid-item-card:: Components
      :link: components
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      Composite / decorator / leaf node catalog with memory,
      parallel policies, and sub-tree reuse.

   .. grid-item-card:: Generation modes
      :link: modes
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      ``nuxmv``, ``python``, ``cpp``, ``haskell``, ``latex``,
      ``trace``, ``grid``.

   .. grid-item-card:: Specifications
      :link: specifications
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      INVAR, CTL, LTL templates; contingency monitors; temporal
      operators.

   .. grid-item-card:: Neural networks
      :link: neural-networks
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      Embedding ONNX classifiers / regressors as action leaves.

   .. grid-item-card:: Encodings
      :link: encodings
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      Fast-forwarding vs naive; staging of blackboard variables.

   .. grid-item-card:: Verification strategies
      :link: verification-strategies
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      Model checking, simulation, and runtime monitors.

.. toctree::
   :maxdepth: 1
   :hidden:

   tree-dsl
   components
   modes
   specifications
   neural-networks
   encodings
   verification-strategies
