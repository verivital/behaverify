import py_trees
import math
import operator
import random


class execute(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(execute, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = random.choice([py_trees.common.Status.SUCCESS])
        return return_status
