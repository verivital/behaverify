import py_trees
import math
import operator
import random
import serene_safe_assignment


class divide_by_2(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(divide_by_2, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('value'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.value = serene_safe_assignment.value((int((self.blackboard.value)/ (2))))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
