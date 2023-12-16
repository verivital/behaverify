import py_trees
import math
import operator
import random
import serene_safe_assignment


class move(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, x_dir, y_dir):
        self.x_dir = x_dir
        self.y_dir = y_dir
        super(move, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('x_true'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('y_true'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.x_true = serene_safe_assignment.x_true(max(0, min(10, (self.blackboard.x_true + self.x_dir))))
        self.blackboard.y_true = serene_safe_assignment.y_true(max(0, min(10, (self.blackboard.y_true + self.y_dir))))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
