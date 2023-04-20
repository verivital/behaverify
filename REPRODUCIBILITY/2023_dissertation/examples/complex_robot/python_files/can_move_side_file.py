import py_trees
import math
import operator
import random
import complex_robot_environment


class can_move_side(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(can_move_side, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('side'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (complex_robot_environment.can_move_side()) else (py_trees.common.Status.FAILURE))

