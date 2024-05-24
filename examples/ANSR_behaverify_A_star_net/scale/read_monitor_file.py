import py_trees
import math
import operator

from collision_monitor import transition as collision_transition, reset as collision_reset
from loop_monitor import transition as loop_transition, reset as loop_reset
COLLISION_MONITOR = collision_reset()
LOOP_MONITOR = loop_reset()

class read_monitor(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_monitor, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_speed'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('monitor_var'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.drone_speed = 2
        global COLLISION_MONITOR, LOOP_MONITOR
        (COLLISION_MONITOR, self.blackboard.monitor_var) = collision_transition(
            COLLISION_MONITOR,
            {
                'drone_x' : self.blackboard.drone_x,
                'drone_y' : self.blackboard.drone_y,
                'delta_x' : self.blackboard.delta_x,
                'delta_y' : self.blackboard.delta_y,
                'obstacles' : self.environment.obstacles,
                'obstacle_sizes' : self.environment.obstacle_sizes
            }
        )
        COLLISION_MONITOR = collision_reset()
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        (LOOP_MONITOR, self.blackboard.monitor_var) = loop_transition(
            LOOP_MONITOR,
            {
                'current_action' : self.blackboard.current_action,
            }
        )
        if self.blackboard.monitor_var == 'unsafe':
            LOOP_MONITOR = loop_reset()
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
