import py_trees
import math
import operator
import random
import serene_safe_assignment


class battery_low_fs(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(battery_low_fs, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('battery_low_warning'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.battery_low_warning == True)) else (py_trees.common.Status.FAILURE))
        return return_status
