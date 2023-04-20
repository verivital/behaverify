import py_trees
import math
import operator
import random


class in_target(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(in_target, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('zone'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if ((self.blackboard.zone == 'target')) else (py_trees.common.Status.FAILURE))

