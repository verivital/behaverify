import py_trees
import math
import operator
import random
import serene_safe_assignment


class check_surface(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(check_surface, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('bb_home_reached'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.bb_home_reached == True)) else (py_trees.common.Status.FAILURE))
        return return_status
