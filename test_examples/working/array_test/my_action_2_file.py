import py_trees
import math
import operator
import random
import serene_safe_assignment


class my_action_2(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(my_action_2, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('a'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('b'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('c'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('d'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('e'), access = py_trees.common.Access.WRITE)
        self.f = [None] * 4
        __temp_var__ = serene_safe_assignment.f([(0, 'hi'), (1, 'hi'), (2, 'hi'), (3, 'hi')])
        for (index, val) in __temp_var__:
            self.f[index] = val

    def update(self):
        self.environment.idk__0(self)
        return_status = py_trees.common.Status.SUCCESS
        __temp_var__ = serene_safe_assignment.e([(max(0, min(self.blackboard.a[0], self.blackboard.b[0])), False), (max(0, min(self.blackboard.a[1], self.blackboard.b[1])), False), (max(0, min(self.blackboard.a[2], self.blackboard.b[2])), False)])
        for (index, val) in __temp_var__:
            self.blackboard.e[index] = val
        return return_status
