import py_trees
import math
import operator
import random


class never_need_side(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(never_need_side, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('need_side_reached'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.need_side_reached = False
        return_status = py_trees.common.Status.SUCCESS
        return return_status
