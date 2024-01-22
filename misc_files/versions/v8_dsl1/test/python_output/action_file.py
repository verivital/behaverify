import py_trees
import math
import operator
import random


class action(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(action, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('c'), access = py_trees.common.Access.WRITE)
        self.a = random.choice([1])
        self.b = random.choice([self.a + 1])
        if self.a == self.b:
            self.blackboard.c = random.choice([True])
        else:
            self.blackboard.c = random.choice([False])

    def update(self):
        self.b = random.choice([self.a, self.a + 1])
        if self.a <= self.b:
            self.blackboard.c = random.choice([True])
        else:
            self.blackboard.c = random.choice([False])
        if self.blackboard.c:
            return_status = random.choice([py_trees.common.Status.SUCCESS])
        else:
            return_status = random.choice([py_trees.common.Status.FAILURE, py_trees.common.Status.RUNNING])
        return return_status
