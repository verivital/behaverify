import py_trees
import math
import operator
import random


class not_finished(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(not_finished, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('finished'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('overflow_failure'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (not(self.blackboard.finished) and not(self.blackboard.overflow_failure)) else (py_trees.common.Status.FAILURE))

