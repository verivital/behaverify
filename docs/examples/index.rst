Examples
========

.. rst-class:: lead

   Worked examples from the ``examples/`` directory. Each entry
   highlights the DSL features it exercises and the verification
   queries it answers.

----

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: DrunkenDrone
      :link: drunken-drone
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      Battery-aware navigation; LTL "eventually returns home".

   .. grid-item-card:: Collatz
      :link: collatz
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      The textbook Collatz recurrence in a 6-node tree.

   .. grid-item-card:: ACAS-Xu
      :link: acas-xu
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      Neural collision-avoidance cascade (five ONNX models).

   .. grid-item-card:: Simple Robot with NN
      :link: simple-robot-nn
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      Grid-world navigation with an ONNX policy leaf.

   .. grid-item-card:: Grid-World (scalability)
      :link: gridworld
      :link-type: doc
      :class-card: sd-border-0 sd-shadow-sm

      49 × 478 obstacle map; BehaVerify's canonical 2,055-node
      scalability benchmark.

.. toctree::
   :maxdepth: 1
   :hidden:

   drunken-drone
   collatz
   acas-xu
   simple-robot-nn
   gridworld
