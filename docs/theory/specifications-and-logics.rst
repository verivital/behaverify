Specifications and Temporal Logics
==================================

.. rst-class:: lead

   BehaVerify accepts properties in three logics: **INVAR** (state
   invariants), **LTL** (linear temporal logic), and **CTL**
   (computation tree logic). This page is the formal reference for
   their syntax, semantics, and expressive power.

Model of the system
-------------------

BehaVerify's SMV output is a **Kripke structure**
:math:`M = (S, s_0, R, L)` where

- :math:`S` is the set of reachable blackboard+BT-pc states;
- :math:`s_0 \in S` is the initial state;
- :math:`R \subseteq S \times S` is the SMV transition relation (one
  BT tick per SMV step under the default fast-forwarding encoding ---
  see :doc:`bt-to-smv`);
- :math:`L : S \to 2^{AP}` labels each state with the set of atomic
  propositions that hold in it.

For BehaVerify, :math:`AP` is the set of boolean combinations of
blackboard-variable tests, node-status predicates (``success``,
``failure``, ``running``, ``active``), and constants.

A **path** in :math:`M` is an infinite sequence
:math:`\pi = s_0 s_1 s_2 \ldots` with :math:`(s_i, s_{i+1}) \in R`.

Invariants (``INVARSPEC``)
--------------------------

An invariant is a propositional formula :math:`\varphi` asserting a
property that holds in every reachable state:

.. math::

   M \models \mathbf{INVAR}\,\varphi
   \quad\Leftrightarrow\quad
   \forall s \in \mathrm{Reach}(s_0).\; s \models \varphi.

nuXmv decides invariants by BDD-based forward reachability (or IC3
when enabled). Proof obligations are on a single tick of the system
--- no temporal nesting --- so invariants are typically the cheapest
property to discharge.

DSL examples:

.. code-block:: text

   INVARSPEC { (gte, battery_level, 0) }
   INVARSPEC { (and (gte, pos_x, 0) (lte, pos_x, x_max)) }

Linear Temporal Logic (``LTLSPEC``)
-----------------------------------

LTL formulas quantify over *all* infinite paths. Syntax:

.. math::

   \varphi ::= p \mid \neg\varphi \mid \varphi \wedge \varphi
   \mid X\,\varphi \mid G\,\varphi \mid F\,\varphi
   \mid \varphi\,U\,\varphi \mid \varphi\,R\,\varphi.

Semantics (using :math:`\pi^i` for the suffix :math:`s_i s_{i+1}
\ldots`):

.. math::

   \pi \models p &\Leftrightarrow p \in L(s_0), \\
   \pi \models X\,\varphi &\Leftrightarrow \pi^1 \models \varphi, \\
   \pi \models G\,\varphi &\Leftrightarrow \forall i\;\pi^i \models \varphi, \\
   \pi \models F\,\varphi &\Leftrightarrow \exists i\;\pi^i \models \varphi, \\
   \pi \models \varphi\,U\,\psi &\Leftrightarrow
     \exists j.\; \pi^j \models \psi \;\wedge\; \forall i<j.\; \pi^i \models \varphi, \\
   M \models \varphi &\Leftrightarrow \forall \pi \in \mathrm{Paths}(s_0).\; \pi \models \varphi.

BehaVerify's prefix-notation vocabulary:

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

Example:

.. code-block:: text

   LTLSPEC {
     (globally (implies (lt, battery, 20) (finally at_home)))
   }

reads "always, if the battery drops below 20 then eventually the drone
is at home". nuXmv discharges LTL via automata-theoretic decomposition:
negate the formula, build a Büchi automaton for :math:`\neg\varphi`,
take the product with :math:`M`, and check non-emptiness.

Computation Tree Logic (``CTLSPEC``)
------------------------------------

CTL quantifies over paths *inside* each temporal operator, so its
syntax explicitly pairs a path quantifier (:math:`A`: for all,
:math:`E`: exists) with a temporal operator (:math:`X, G, F, U`):

.. math::

   \varphi ::= p \mid \neg\varphi \mid \varphi \wedge \varphi
   \mid A\,X\,\varphi \mid E\,X\,\varphi
   \mid A\,G\,\varphi \mid E\,G\,\varphi
   \mid A\,F\,\varphi \mid E\,F\,\varphi
   \mid A[\varphi\,U\,\psi] \mid E[\varphi\,U\,\psi].

BehaVerify's prefix forms:

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

Example ("a charger is always eventually reachable"):

.. code-block:: text

   CTLSPEC { (always_globally (exists_finally (eq, pos, charger))) }

CTL is decided by symbolic BDD fixpoint computation (the classical
:math:`\mu`-calculus encoding of CTL operators).

LTL vs. CTL
-----------

The two logics are *incomparable*. LTL can express fairness
(:math:`GF\,\varphi`), but it cannot express "there exists a path that
always avoids :math:`\psi`". CTL can express the latter
(:math:`EG\,\neg\psi`), but it cannot express
:math:`GF\,\varphi`. A user wanting both expressiveness axes should
pick CTL\*, which BehaVerify does not currently expose.

Rule of thumb: if your question is "along *every* path, ..." use LTL.
If it is "there *exists* a path along which ...", use CTL.

Node-status atoms
-----------------

Inside any of the three families, BehaVerify exposes four atoms
referring to the *last tick's* status of a named node:

- ``(success node)`` --- the node returned **SUCCESS**;
- ``(failure node)``;
- ``(running node)``;
- ``(active node)`` --- the node was evaluated on the last tick.

These are compiled into boolean expressions over the internal status
encoding, so they compose freely with every temporal operator.

Contingency monitors
--------------------

The ``monitors { ... }`` block attaches an LTL formula to an
actionable trigger. Semantically, a monitor is an automaton
:math:`\mathcal{A}_{\neg\varphi}` for the negation of the monitored
property; when :math:`\mathcal{A}_{\neg\varphi}` enters an accepting
state on the current run, the monitor fires. See :doc:`monitors`.

References
----------

- Baier, Katoen. *Principles of Model Checking.* MIT Press, 2008.
  --- canonical textbook reference for every formula and algorithm on
  this page.
- Clarke, Grumberg, Peled. *Model Checking.* MIT Press, 1999.
- Cavada et al. The nuXmv Symbolic Model Checker. *CAV* 2014.
