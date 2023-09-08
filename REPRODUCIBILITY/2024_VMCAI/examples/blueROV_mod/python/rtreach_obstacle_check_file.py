import py_trees
import math
import operator
import random
import serene_safe_assignment


class rtreach_obstacle_check(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(rtreach_obstacle_check, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('rtreach_obstacle_warning'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.rtreach_obstacle_warning == False)) else (py_trees.common.Status.FAILURE))
        return return_status
