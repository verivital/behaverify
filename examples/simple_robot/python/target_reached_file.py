import py_trees
import math
import operator
import random


class target_reached(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(target_reached, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('target_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('target_y'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (((self.blackboard.x == self.blackboard.target_x) and (self.blackboard.y == self.blackboard.target_y))) else (py_trees.common.Status.FAILURE))

