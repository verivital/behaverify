import py_trees
import math
import operator
import random
import serene_safe_assignment


class can_move_side(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(can_move_side, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('side'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (self.environment.can_move_side(self)) else (py_trees.common.Status.FAILURE))