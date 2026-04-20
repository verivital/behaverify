Simple Robot with NN
====================

A minimal grid-world tree where the locomotion leaf is driven by a
trained ONNX classifier. Useful starting point for your own
neural-symbolic behavior tree.

Location
--------

``examples/Simple-Robot-With-NN/``

Features exercised
------------------

- A 5×5 grid blackboard.
- A single classification ``neural_network`` leaf producing one of
  ``{left, right, up, down, stay}``.
- A selector that guards the NN leaf behind a bounds-check ``check``
  node.

Invocation
----------

Formal verification (requires nuXmv):

.. code-block:: bash

   python -m behaverify nuxmv \
       examples/Simple-Robot-With-NN/model.tree ../out/ \
       --generate --ctl --invar --nuxmv_path ../nuXmv

Simulation (pure Python):

.. code-block:: bash

   python -m behaverify python \
       examples/Simple-Robot-With-NN/model.tree ../out_py/

Then run ``python ../out_py/python/runner.py`` to watch the robot
navigate.
