import py_trees
import math
import operator
import random
import serene_safe_assignment


class suc(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(suc, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (True) else (py_trees.common.Status.FAILURE))
