Glossary
========

.. glossary::

   BT
      Behavior tree. A rooted tree whose internal nodes are control
      flow (``sequence``, ``selector``, ``parallel``) and whose leaves
      are conditions and actions.

   BT.CPP
      `BehaviorTree.CPP <https://www.behaviortree.dev/>`_, a widely
      used C++ implementation of behavior trees for ROS 2 and other
      robotics stacks.

   blackboard
      Shared mutable state accessible to every tree node. Declared
      with the ``bl`` scope tag.

   CTL
      Computation Tree Logic. Path-quantified temporal logic.

   fast-forwarding encoding
      BehaVerify's default SMV encoding where one behavior-tree tick
      becomes one SMV transition. See :doc:`/user-guide/encodings`.

   INVARSPEC
      An nuXmv invariant specification: a predicate that must hold in
      every reachable state.

   leaf node
      A behavior-tree node with no children --- either a
      ``check`` or an ``action``.

   LTL
      Linear Temporal Logic.

   monitor
      An LTL formula compiled to a runtime automaton that fires a
      trigger action when violated.

   nuXmv
      `nuXmv <https://nuxmv.fbk.eu/>`_, a symbolic model-checker used
      by BehaVerify for formal verification.

   ONNX
      Open Neural Network Exchange format; the representation
      BehaVerify uses for neural leaves.

..
   Probabilistic-CTL entry is commented out while the probabilistic
   back-end work is parked. Restore when the feature lands.
..
   PCTL
      Probabilistic CTL. Not currently handled by BehaVerify; planned
      under :doc:`/user-guide/verification-strategies`.

   py_trees
      `py_trees <https://py-trees.readthedocs.io/>`_, the Python BT
      library BehaVerify targets.

   SMV
      The modelling language consumed by nuXmv.

   sub-tree
      A named, reusable fragment of a behavior tree; inserted via
      ``insert { name }``.

   tick
      One execution sweep of the tree, from root through all active
      nodes.
