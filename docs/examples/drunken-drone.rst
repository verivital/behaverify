DrunkenDrone
============

A single-file example of a drone that wanders randomly while its
battery drains, then returns home to recharge.

Location
--------

``examples/DrunkenDrone/DrunkenDrone.tree``

Features exercised
------------------

- Blackboard variables with integer ranges.
- ``check`` and ``action`` leaves.
- A two-child selector at the root.
- Invariant and LTL specifications.

Invocation
----------

.. code-block:: bash

   python -m behaverify nuxmv examples/DrunkenDrone/DrunkenDrone.tree \
       ../behaverify_demo/ --generate --invar --ltl --nuxmv_path ../nuXmv

What to look for
----------------

- ``INVARSPEC { (gte, battery, 0) }`` -- the battery can never go
  negative.
- ``LTLSPEC { (globally (implies battery_low (finally at_home))) }``
  -- whenever the battery dips below the low threshold, the drone
  eventually reaches the charging station.

Both specifications should return ``is true``. Toggle the return-home
branch off to watch the LTL property become false and produce a
counter-example trace you can render with the ``trace`` mode.
