import py_trees
import math
import operator
import random
import robot


class go_right(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(go_right, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        robot.go_right()
        return_status = py_trees.common.Status.SUCCESS
        return return_status
