Specifications
==============

.. rst-class:: lead

   BehaVerify discharges three families of temporal-logic specifications
   through nuXmv: invariants, LTL, and CTL. Runtime monitors generated
   from LTL formulas additionally support contingency-triggered
   behaviors.

Invariants (``INVARSPEC``)
--------------------------

An ``INVARSPEC`` declares a state predicate that must hold in every
reachable state.

.. code-block:: text

   specifications {
       INVARSPEC { (gte, battery_level, 0) }
       INVARSPEC { (and (gte, pos_x, 0) (lte, pos_x, x_max)) }
   }

Invariants are the cheapest and most widely applicable family: nuXmv
checks them by BDD-based reachability without any LTL/CTL overhead.
Bounded history can be referenced via the ``at`` operator:

.. code-block:: text

   INVARSPEC { (implies (gt, (x at -1), 0) (gte, x, 0)) }

LTL (``LTLSPEC``)
-----------------

An ``LTLSPEC`` quantifies over paths. BehaVerify's prefix-notation
temporal vocabulary:

.. list-table::
   :header-rows: 1

   * - Operator
     - Prefix form
     - Standard notation
   * - next
     - ``(next x)``
     - :math:`X\,\varphi`
   * - globally
     - ``(globally x)``
     - :math:`G\,\varphi`
   * - finally
     - ``(finally x)``
     - :math:`F\,\varphi`
   * - until
     - ``(until x y)``
     - :math:`\varphi \, U \, \psi`
   * - release
     - ``(release x y)``
     - :math:`\varphi \, R \, \psi`

Example: battery monitor eventually triggers return-to-base when low.

.. code-block:: text

   LTLSPEC { (globally (implies (lt, battery_level, 20)
                                (finally at_home))) }

CTL (``CTLSPEC``)
-----------------

Path-quantified temporal logic.

.. list-table::
   :header-rows: 1

   * - Operator
     - Prefix form
     - Standard notation
   * - AG
     - ``(always_globally x)``
     - :math:`A\,G\,\varphi`
   * - AF
     - ``(always_finally x)``
     - :math:`A\,F\,\varphi`
   * - EG
     - ``(exists_globally x)``
     - :math:`E\,G\,\varphi`
   * - EF
     - ``(exists_finally x)``
     - :math:`E\,F\,\varphi`

Example: a charging station is always eventually reachable.

.. code-block:: text

   CTLSPEC { (always_globally (exists_finally (eq, pos, charger))) }

Node-status atoms
-----------------

Inside specifications only, four predicates are available that refer to
the last-tick status of a named node:

- ``(success node_name)``
- ``(failure node_name)``
- ``(running node_name)``
- ``(active node_name)`` -- the node was evaluated on the last tick.

These are translated by BehaVerify into boolean expressions over the
internal status encoding, so they compose naturally with the temporal
operators above.

Contingency monitors
--------------------

The ``monitors { ... }`` block attaches an LTL formula to an action
that fires when the monitor becomes violated, turning a specification
into runtime enforcement.

.. code-block:: text

   monitors {
       collision_monitor {
           specification LTLSPEC (globally (not collision_detected))
           trigger_action { emergency_stop }
       }
   }

This emits three things:

1. An SMV constraint used by nuXmv to detect unreachable monitor
   states.
2. A compiled monitor class for the Python / C++ / Haskell runtimes.
3. A hook in the generated runner that calls the named
   ``trigger_action`` when the monitor fires.

See the "Verification of Behavior Trees with Contingency Monitors"
paper (FMAS 2024) for the formal semantics.

Noisy environments
------------------

All four families above (INVAR, LTL, CTL, monitors) are handled by
nuXmv. Stochasticity in the environment --- a noisy sensor, a random
action outcome --- is encoded as *non-deterministic* choice, so the
verifier proves the property against the worst case.

..
   Closing pointer to the planned probabilistic strategy is
   commented out while that work is parked.
..
   See :doc:`verification-strategies` for where probabilistic
   strategies are planned to slot in.
