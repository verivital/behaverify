import py_trees
import math
import operator
import random
import serene_safe_assignment


class x_too_big(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(x_too_big, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('target_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('x'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.x > self.blackboard.target_x)) else (py_trees.common.Status.FAILURE))
        return return_status
