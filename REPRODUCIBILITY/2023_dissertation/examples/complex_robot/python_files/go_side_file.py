import py_trees
import math
import operator
import random
import complex_robot_environment


class go_side(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(go_side, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('side'), access = py_trees.common.Access.READ)

    def update(self):
        complex_robot_environment.go_side(self.blackboard.side)
        return_status = py_trees.common.Status.RUNNING
        return return_status