Neural-Network Leaves
=====================

.. rst-class:: lead

   BehaVerify embeds ONNX classifiers and regressors directly into
   action leaves. The tool encodes the network into SMV for formal
   verification and uses ``onnxruntime`` at tick-time for the Python
   runtime.

Declaring a neural leaf
-----------------------

A neural leaf is a normal ``action`` block with an additional
``neural_network { ... }`` sub-block. The inputs and outputs are drawn
from the declared read / write variables.

.. code-block:: text

   action { nn_move
       arguments {} local_variables {}
       read_variables  {pos_x, pos_y}
       write_variables {next_move}
       initial_values {}
       neural_network {
           network_file 'path/to/model.onnx'
           model_as NEURAL
           neural_mode classification {
               domain_codes { left, right, up, down, stay }
               inputs { pos_x, pos_y }
           }
           outputs { next_move }
       }
   }

Modes:

- ``classification`` -- ONNX outputs are logits over a user-declared
  domain; BehaVerify emits an argmax that maps to the domain enum.
- ``regression`` -- ONNX outputs are real-valued; specify ``INT`` or
  ``REAL`` and ``num_outputs``.

Quantisation for verification
-----------------------------

Set the encoding at the top of the model:

.. code-block:: text

   configuration { neural }

Optional sub-block tuning the fixed-point representation is available
via:

.. code-block:: text

   configuration {
       neural
       # float | fixed | fixed_direct
       # total / int_part / float_part bit widths
   }

Per the 2025 NeuS paper, BehaVerify has been used to verify behavior
trees with up to **6.25M input states** using classification leaves,
and ACAS-X-style collision-avoidance towers with five ONNX models.

Runtime execution (``python`` mode)
-----------------------------------

The generated Python runtime imports ``onnxruntime`` lazily:

.. code-block:: python

   # Inside the generated leaf:
   session = onnxruntime.InferenceSession(Path(__file__).parent / "model.onnx")
   out = session.run(None, {"input": np.array([pos_x, pos_y], dtype=np.float32)})

Weights are not re-exported; the ``.onnx`` files are referenced by path
relative to the output directory. Bundle them alongside the generated
code when deploying.

Formal verification (``nuxmv`` mode)
------------------------------------

The nuXmv backend inlines the network as a chain of ``DEFINE``
assignments, one per neuron, with ReLU encoded via ``case`` expressions
and matrix multiplications expanded by the meta-compiler. See the
Serbinowska et al. NeuS 2025 paper for the full encoding and the
state-space reductions it enables.

.. admonition:: Scope

   Current ONNX coverage is restricted to Linear + ReLU stacks with
   optional max-pooling. Transformer-style operators (softmax
   attention, LayerNorm) are not yet supported; track the upstream
   TODO list for expansion.

Examples
--------

Reference implementations live under ``examples/``:

- ``examples/Simple-Robot-With-NN/`` -- minimal classification leaf on
  a 5×5 grid.
- ``examples/ANSR_ONNX/`` and ``examples/ANSR_ONNX_2/`` -- A* network
  integration examples.
- ``examples/AcasXu/`` -- ACAS-Xu-style advisory cascade.
