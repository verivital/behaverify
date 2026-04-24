Collatz
=======

The Collatz recurrence :math:`x \mapsto x/2` (even) or
:math:`x \mapsto 3x + 1` (odd) is the smallest non-trivial behavior
tree with genuinely rich dynamics.

Location
--------

``examples/Collatz/collatz.tree``

Features exercised
------------------

- A ``selector`` wrapping a three-child ``sequence``.
- ``loop``-constructed set-valued initial assignment (:math:`x \in
  [1, 254]`).
- Integer clamping via ``(min max_val ...)``.
- ``INVARSPEC`` only --- no temporal operators needed.

Invocation
----------

.. code-block:: bash

   python -m behaverify nuxmv examples/Collatz/collatz.tree ../out/ \
       --generate --invar --nuxmv_path ../nuXmv

Suggested exercise
------------------

- Run with ``--use_encoding naive`` and compare the generated SMV
  against the default ``fastforwarding`` encoding. See
  :doc:`../user-guide/encodings`.
- Render the tree with ``latex`` mode on the small variant
  ``collatz_small.tree``:

  .. code-block:: bash

     python -m behaverify latex examples/Collatz/collatz_small.tree \
         ./collatz.tex
     pdflatex collatz.tex
