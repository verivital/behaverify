import py_trees
import math
import operator
import random
import serene_safe_assignment
import complex_robot_environment


class can_move_forward(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(can_move_forward, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('forward'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (complex_robot_environment.can_move_forward(self)) else (py_trees.common.Status.FAILURE))
