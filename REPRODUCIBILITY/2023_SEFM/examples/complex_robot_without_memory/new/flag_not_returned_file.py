import py_trees
import math
import operator
import random
import serene_safe_assignment


class flag_not_returned(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(flag_not_returned, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (self.environment.flag_not_returned(self)) else (py_trees.common.Status.FAILURE))
