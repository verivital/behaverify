import py_trees
import math
import operator
import os

class read_monitor(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(read_monitor, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('delta_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('current_action'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_speed'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('monitor_var'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.drone_speed = 2
        temp = 2
        self.blackboard.monitor_var = ('safe' if temp == 1 else ('unknown' if temp == 0 else 'unsafe'))
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        temp = 2
        self.blackboard.monitor_var = ('safe' if temp == 1 else ('unknown' if temp == 0 else 'unsafe'))
        if self.blackboard.monitor_var == 'unsafe':
            NEEDS_RESET = True
        self.blackboard.drone_speed = (
            1
            if (self.blackboard.monitor_var == 'unsafe') else
            (
            self.blackboard.drone_speed
        ))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
