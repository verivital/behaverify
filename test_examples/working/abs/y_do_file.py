import py_trees
import math
import operator
import random
import serene_safe_assignment


class y_do(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(y_do, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('test'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.test = serene_safe_assignment.test(abs(self.blackboard.test))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
