import py_trees
import math
import operator
import random
import serene_safe_assignment


class never_need_side(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(never_need_side, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('need_side_reached'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.need_side_reached = serene_safe_assignment.need_side_reached(False)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
