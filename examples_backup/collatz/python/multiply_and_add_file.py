import py_trees
import math
import operator
import random
import serene_safe_assignment


class multiply_and_add(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(multiply_and_add, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('value'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.value = serene_safe_assignment.value(((self.blackboard.value * 3) + 1))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
