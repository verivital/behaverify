import py_trees
import math
import operator
import random
import serene_safe_assignment


class a1(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(a1, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)

    def update(self):
        if (-24 < -(max(17, self.blackboard.blDEFINE5()))):
            return_status = py_trees.common.Status.FAILURE
        elif ((self.blackboard.blVAR0[0] and True) ^ (self.blackboard.blDEFINE5() < self.blackboard.blDEFINE5())):
            return_status = py_trees.common.Status.FAILURE
        elif ((self.blackboard.blDEFINE5() > 80) ^ self.blackboard.blVAR0[2]):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
