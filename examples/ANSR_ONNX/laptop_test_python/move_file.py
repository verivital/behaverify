import py_trees
import math
import operator
import random
import serene_safe_assignment


class move(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment, delta_x, delta_y):
        self.delta_x = delta_x
        self.delta_y = delta_y
        super(move, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cur_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.cur_x = serene_safe_assignment.cur_x(max(0, min(8, (self.delta_x + self.blackboard.cur_x))))
        self.blackboard.cur_y = serene_safe_assignment.cur_y(max(0, min(8, (self.delta_y + self.blackboard.cur_y))))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
