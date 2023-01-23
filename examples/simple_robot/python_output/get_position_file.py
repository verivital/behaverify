import py_trees
import math
import operator
import random
import robot


class get_position(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(get_position, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('y'), access = py_trees.common.Access.WRITE)
        self.blackboard.x = 0
        self.blackboard.y = 0

    def update(self):
        (self.blackboard.x, self.blackboard.y) = robot.get_position()
        return_status = py_trees.common.Status.SUCCESS
        return return_status
