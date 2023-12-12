import py_trees
import math
import operator
import random
import serene_safe_assignment


class target_in_sight(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(target_in_sight, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cur_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.environment.target_in_sight(self)) else (py_trees.common.Status.FAILURE))
        return return_status
