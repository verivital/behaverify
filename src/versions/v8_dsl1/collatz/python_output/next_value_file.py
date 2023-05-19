import py_trees
import math
import operator
import random


class next_value(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(next_value, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('value'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('finished'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('overflow_failure'), access = py_trees.common.Access.WRITE)
        self.blackboard.finished = random.choice([False])
        self.blackboard.overflow_failure = random.choice([False])
        self.blackboard.value = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    def update(self):
        if self.blackboard.value % 2 == 0:
            self.blackboard.value = random.choice([self.blackboard.value / 2])
        else:
            self.blackboard.value = random.choice([min(self.blackboard.value * 3 + 1, 1000)])
        self.blackboard.finished = random.choice([self.blackboard.value == 1])
        self.blackboard.overflow_failure = random.choice([self.blackboard.value == 1000])
        return_status = random.choice([py_trees.common.Status.SUCCESS])
        return return_status
