Theory
======

.. rst-class:: lead

   What behavior trees are, how BehaVerify translates them into SMV,
   how nuXmv discharges the resulting specifications, and why the
   end-to-end result is trustworthy.

All content on these pages is grounded in the four BehaVerify papers
(see :doc:`/reference/publications`) and in the code under
``src/behaverify/``.

----

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: Behavior trees
      :link: behavior-trees
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      Node taxonomy, operational semantics, and the tick relation.

   .. grid-item-card:: Specifications & logics
      :link: specifications-and-logics
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      Invariants, LTL, CTL --- syntax, semantics, and expressiveness.

   .. grid-item-card:: BT $\to$ SMV translation
      :link: bt-to-smv
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      The fast-forwarding encoding and its variable-staging scheme.

   .. grid-item-card:: Model checking with nuXmv
      :link: model-checking
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      BDDs, bounded model checking, IC3 / PDR; what each algorithm
      decides.

   .. grid-item-card:: Soundness
      :link: soundness
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      End-to-end argument: why a verified property on the SMV
      model implies the same property on the BT.

   .. grid-item-card:: Neuro-symbolic BTs
      :link: neuro-symbolic
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      How ONNX leaves are compiled into SMV without changing the
      tick semantics.

   .. grid-item-card:: Stateful BTs
      :link: stateful-trees
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      Node-local state that persists across ticks (FMAS 2024).

   .. grid-item-card:: Contingency monitors
      :link: monitors
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm
      :text-align: center

      LTL safety monitors with trigger actions (FMAS 2024).

.. toctree::
   :maxdepth: 1
   :hidden:

   behavior-trees
   specifications-and-logics
   bt-to-smv
   model-checking
   soundness
   neuro-symbolic
   stateful-trees
   monitors
