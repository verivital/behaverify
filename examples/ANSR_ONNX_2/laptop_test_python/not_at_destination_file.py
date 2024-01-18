import py_trees
import math
import operator
import random
import serene_safe_assignment


class not_at_destination(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(not_at_destination, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cur_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dest_x'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dest_y'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (not (((self.blackboard.cur_x == self.blackboard.dest_x) and (self.blackboard.cur_y == self.blackboard.dest_y)))) else (py_trees.common.Status.FAILURE))
        return return_status
