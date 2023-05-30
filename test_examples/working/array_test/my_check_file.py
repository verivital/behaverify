import py_trees
import math
import operator
import random
import serene_safe_assignment


class my_check(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(my_check, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('a'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('b'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if ((self.blackboard.a[min(2, self.blackboard.b[0])] == self.blackboard.b[min(2, self.blackboard.a[0])])) else (py_trees.common.Status.FAILURE))
