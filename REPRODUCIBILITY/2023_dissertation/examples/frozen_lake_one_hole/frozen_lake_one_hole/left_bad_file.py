import py_trees
import math
import operator
import random
import serene_safe_assignment


class left_bad(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(left_bad, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('tiles'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (self.environment.left_bad(self)) else (py_trees.common.Status.FAILURE))
