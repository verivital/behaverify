Adding a Check or Action Type
=============================

..
   The illustrative example ``probabilistic_check`` used here is
   commented out while the probabilistic back-end is parked. Restore
   the original wording when the feature lands.

A new check-node type (e.g. ``timed_check``) needs changes in
four places.

1. Grammar
----------

Edit ``src/behaverify/data/metamodel/behaverify.tx`` to extend the
``check_node`` or ``action_node`` rule. Keep the shape parallel to the
existing alternative so downstream passes do not need redesign.

2. Validation
-------------

Add a sanity check in :mod:`behaverify.check_grammar` that:

- Rejects constructs that can reference runtime-only information.
- Flags duplicate names.
- Validates any per-type numeric bounds (e.g. probabilities in
  :math:`[0, 1]`).

3. IR
-----

:mod:`behaverify.node_creator` walks the TextX model and builds the
internal IR. Add a branch that recognises the new node shape and
builds the corresponding Python object. Prefer composition over
branching -- a new IR class with a minimal interface lets every
backend consume it uniformly.

4. Per-backend codegen
----------------------

Each ``dsl_to_<mode>.py`` must know how to emit the new node. Where
the semantics of a mode doesn't support the construct, raise an
explicit ``BTreeException`` with a friendly message rather than failing
silently.

5. Tests
--------

Add a small ``.tree`` file under ``test_examples/working/`` that
exercises the new construct, and a negative example under
``test_examples/intentionally_broken/``. The regression harness will
pick them up automatically.

6. Documentation
----------------

- Update :doc:`/user-guide/tree-dsl` with the new syntax.
- Add a row in the coverage matrix under :doc:`/user-guide/components`.
- If the node type has formal semantics worth recording, add a theory
  page.
