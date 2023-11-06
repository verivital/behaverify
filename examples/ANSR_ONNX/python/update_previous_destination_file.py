import py_trees
import math
import operator
import random
import serene_safe_assignment


class update_previous_destination(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(update_previous_destination, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cur_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('prev_dest_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('prev_dest_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.prev_dest_x = serene_safe_assignment.prev_dest_x(self.blackboard.cur_x)
        self.blackboard.prev_dest_y = serene_safe_assignment.prev_dest_y(self.blackboard.cur_y)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
