import py_trees
import math
import operator
import random
import serene_safe_assignment


class y_too_small(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(y_too_small, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.environment.y_too_small(self)) else (py_trees.common.Status.FAILURE))
        return return_status
