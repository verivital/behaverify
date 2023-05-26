import py_trees
import math
import operator
import random
import serene_safe_assignment


class change_side(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(change_side, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('side'), access = py_trees.common.Access.WRITE)

    def update(self):
        if (self.blackboard.side == 1):
            self.blackboard.side = serene_safe_assignment.side(-1)
        else:
            self.blackboard.side = serene_safe_assignment.side(1)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
