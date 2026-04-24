Neuro-Symbolic Behavior Trees
=============================

.. rst-class:: lead

   BehaVerify verifies behavior trees whose *leaves* are trained
   neural networks, not just hand-written checks and actions. This
   page summarises the encoding introduced by Serbinowska, Manzanas
   Lopez, Nguyen & Johnson (NeuS 2025).

The leaf interface
------------------

A neural leaf is an action whose update is determined by a forward
pass of an ONNX model :math:`\mathcal{N}` over declared
read-variables. Two modes are supported:

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Mode
     - Semantics
   * - classification
     - :math:`\mathcal{N}(x) \in \mathbb{R}^c`; the leaf writes the
       argmax category drawn from a user-declared domain.
   * - regression
     - :math:`\mathcal{N}(x) \in \mathbb{R}^m`; the leaf writes the
       :math:`m` outputs directly.

The leaf interface is *purely functional*: tick :math:`\mapsto`
blackboard update. The BT semantics is unchanged; only the compile
path for actions differs.

The encoding problem
--------------------

For formal verification we cannot execute :math:`\mathcal{N}` inside
nuXmv: the model checker has no notion of floating-point GEMM. We
need a **symbolic encoding**

.. math::

   \mathcal{E}(\mathcal{N}) :
     \Sigma_{\text{int}} \to \Sigma_{\text{int}}

that is *equivalent* to :math:`\mathcal{N}` under some discretisation
of the inputs and weights, and whose semantics are expressible in the
finite-state, integer-valued fragment of SMV.

BehaVerify's strategy: *small-domain quantisation* plus
*layer-by-layer symbolic propagation*.

Small-domain quantisation
-------------------------

The inputs to the network are blackboard variables with finite
integer domains (e.g., ``pos_x`` in ``[0, 24]``). This is the key
constraint: the enumerated inputs span a *finite* set :math:`X \subset
\mathbb{Z}^n`. For every :math:`x \in X`, the output
:math:`\mathcal{N}(x)` is computable at compile time in a reference
Python interpreter (``onnxruntime``) and cached into a lookup table.

The ``model_as NEURAL`` configuration block further selects whether
weights are kept as floats (``float``) or quantised to a fixed-point
representation with configurable ``total`` / ``int_part`` /
``float_part`` widths. Fixed-point weights make the arithmetic exact
under SMV's integer semantics.

SMV emission
------------

For a classification leaf with :math:`|X|` enumerable inputs and
:math:`c` output classes, BehaVerify emits an SMV ``DEFINE`` block
whose value is the argmax class for the input. The shape is:

.. code-block:: text

   DEFINE
     nn_out :=
       case
         (input = x_1) : class_{\mathcal{N}(x_1)};
         (input = x_2) : class_{\mathcal{N}(x_2)};
         ...
       esac;

For regression leaves, the output is a lookup table over
:math:`|X|` entries, one per quantised input.

A single-class argmax is a total function; no default case is needed
when :math:`X` enumerates the entire reachable input set. If
reachability trimming (see :doc:`bt-to-smv`) cannot prove that
:math:`X` is closed under the BT's transition relation, the emitted
``case`` table includes a safe default that returns the class of the
nearest enumerated point.

Layer-by-layer propagation
--------------------------

When the input domain is too large for complete enumeration, NeuS
2025 uses a layer-wise propagation: each layer's reachable
activation set is computed symbolically with a box / zonotope
abstraction, then intersected with the next layer's piecewise-linear
operator (typically ReLU). The final layer produces a reachable
set over output classes. This is the same idea used in standalone
NN-verification tools (auto_LiRPA, CROWN, DeepPoly), lifted into
BehaVerify's compile pipeline.

The paper reports verified trees with **6.25M input states** using
this layer-wise strategy.

Soundness claim
---------------

For a *quantised* neural leaf, the following theorem holds:

**Theorem (NeuS 2025, informal).**
For every reachable input :math:`x \in X`, the quantised symbolic
encoding :math:`\mathcal{E}(\mathcal{N})` returns the same class as
the ground-truth ONNX forward pass, *provided* the quantisation is
applied consistently at both compile time and runtime.

Consequence: the soundness chain of :doc:`soundness` extends to
neuro-symbolic BTs, as long as the runtime interpretation of the
leaf matches the encoding (i.e., fixed-point weights at runtime if
fixed-point was used at compile time).

ACAS-Xu and beyond
------------------

The NeuS 2025 paper validates the approach on the ACAS-Xu advisory
cascade (five separate ONNX networks totalling 42 output advisories)
and on a 5×5 grid-world navigation task. Both examples are bundled
under ``examples/AcasXu*`` and ``examples/Simple-Robot-With-NN/``.

.. admonition:: Current coverage

   BehaVerify's ONNX encoding supports Linear + ReLU stacks with
   optional max-pooling. Softmax attention, layer-norm, and other
   transformer-era operators are not supported at the time of
   writing; the upstream TODO list tracks the expansion.

References
----------

- Serbinowska, Manzanas Lopez, Nguyen, Johnson. Neuro-Symbolic
  Behavior Trees and Their Verification. *NeuS* 2025.
  https://proceedings.mlr.press/v288/serbinowska25a.html
- Julian, Kochenderfer. Policy Compression for Aircraft Collision
  Avoidance Systems. *DASC* 2016 (ACAS-Xu background).
