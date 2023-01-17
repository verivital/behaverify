import py_trees
import math
import operator
import random


class safe_battery(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(safe_battery, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('battery_reading'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('battery_threshold'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (self.blackboard.battery_reading >= self.blackboard.battery_threshold) else (py_trees.common.Status.FAILURE))

