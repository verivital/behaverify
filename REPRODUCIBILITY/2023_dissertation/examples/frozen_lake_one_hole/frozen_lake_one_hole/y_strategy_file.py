import py_trees
import math
import operator
import random
import serene_safe_assignment


class y_strategy(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(y_strategy, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('strategy'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if ((self.blackboard.strategy == 'y_first')) else (py_trees.common.Status.FAILURE))