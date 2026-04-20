ACAS-Xu
=======

ACAS-Xu is a neural-network-based airborne collision-avoidance
advisory system. BehaVerify's ACAS-Xu examples wire up to five ONNX
advisory networks into a single behavior tree and verify
collision-avoidance properties.

Locations
---------

- ``examples/AcasXu/`` -- open-loop advisory cascade.
- ``examples/AcasXu_closed_loop/`` -- closed-loop variant that advances
  the aircraft state at every tick.

Features exercised
------------------

- Multi-model ``neural_network`` blocks, each with its own ONNX file.
- Classification leaves with five output classes (``clear``, ``weak
  left``, ``strong left``, ``weak right``, ``strong right``).
- Integer-ranged blackboard for relative aircraft state.
- CTL specifications quantifying over collision-free paths.

Invocation
----------

.. code-block:: bash

   python -m behaverify nuxmv examples/AcasXu/acasxu.tree ../out/ \
       --generate --ctl --invar --nuxmv_path ../nuXmv \
       --recursion_limit 3000

ACAS-Xu pushes the static analyser harder than most models: the
``--recursion_limit`` bump is not optional.

Published results
-----------------

Serbinowska et al. (NeuS 2025) report verified input spaces of
**6.25 million states** on the closed-loop variant. See the
reproducibility materials under
``REPRODUCIBILITY/2025_NeuS/``.
