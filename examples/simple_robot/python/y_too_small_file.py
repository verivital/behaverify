import py_trees
import math
import operator
import random
import serene_safe_assignment


class y_too_small(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(y_too_small, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('target_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('y'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if ((self.blackboard.y < self.blackboard.target_y)) else (py_trees.common.Status.FAILURE))
