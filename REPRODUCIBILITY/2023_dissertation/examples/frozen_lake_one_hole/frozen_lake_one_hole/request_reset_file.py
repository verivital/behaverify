import py_trees
import math
import operator
import random
import serene_safe_assignment


class request_reset(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(request_reset, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('action'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.action = serene_safe_assignment.action(-1)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
