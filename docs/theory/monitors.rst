Contingency Monitors
====================

.. rst-class:: lead

   A **contingency monitor** is a pair :math:`(\varphi, a)` of an LTL
   specification and an action. The monitor runs alongside the BT and
   invokes :math:`a` whenever :math:`\varphi` becomes violated.
   Serbinowska, Potteiger, Tumlin & Johnson (FMAS 2024) formalise the
   construction and give BehaVerify's compile path.

Formalisation
-------------

A monitor for :math:`\varphi` is a deterministic finite automaton
:math:`\mathcal{A}_{\neg\varphi}` that observes every tick and enters
an accepting state iff the observed trace so far satisfies
:math:`\neg\varphi` --- i.e. a *bad prefix* has been seen.

Not every LTL formula admits a *safety* monitor; some liveness
properties cannot be monitored with a finite automaton because no
finite bad prefix exists. BehaVerify restricts monitor syntax to the
**safety fragment** of LTL:

.. math::

   \varphi ::= G\,\psi \;\mid\; G(\psi \Rightarrow X\,\chi)
   \;\mid\; \ldots

i.e. formulas without an unbounded :math:`F` at the outermost
position. The safety fragment is exactly where :math:`\neg\varphi`
has bad prefixes; membership can be decided in polynomial time.

Emission
--------

For each ``monitor { ... }`` block BehaVerify emits:

1. An SMV constraint that implies the monitor's safety specification;
   nuXmv can discharge this alongside the rest of the model.
2. A runtime monitor class (Python / C++ / Haskell, depending on
   target) that executes the automaton tick-by-tick and invokes the
   trigger action when appropriate.

The runtime monitor and the SMV constraint are generated from the
same automaton, so nuXmv's verdict ("the monitor never fires under
the assumed adversary") matches what the on-robot monitor actually
does.

Composition
-----------

Multiple monitors compose conjunctively: their automata are
synchronised to run in parallel, each observing the same tick.
Because monitors are *passive* --- they only observe the tick; they
don't alter the blackboard until they fire --- composition is
commutative up to tie-breaking on simultaneous fires.

Example
-------

.. code-block:: text

   monitors {
       collision_monitor {
           specification LTLSPEC (globally (not collision_detected))
           trigger_action { emergency_stop }
       }
       loop_detector {
           specification LTLSPEC (globally (implies
               (at_waypoint w) (finally (at_waypoint (not w)))))
           trigger_action { replan_path }
       }
   }

The first is a classical safety monitor (never collide). The second
is a liveness-flavoured monitor restricted to a safety fragment via
a bounded-horizon approximation --- see the FMAS 2024 paper for the
translation.

References
----------

- Serbinowska, Potteiger, Tumlin, Johnson. Verification of Behavior
  Trees with Contingency Monitors. *FMAS* 2024, EPTCS 411, pp. 56-72.
  https://dx.doi.org/10.4204/EPTCS.411.4
- Kupferman, Vardi. Model checking of safety properties. *CAV* 1999.
