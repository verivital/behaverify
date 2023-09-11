import py_trees
import math
import operator
import random
import serene_safe_assignment


class a4(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(a4, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = [None] * 2
        __temp_var__ = serene_safe_assignment.localVAR2([(0, (
            (max(-63, self.blackboard.blDEFINE5()) > -(max(-55, self.blackboard.blVAR0[1])))
            if (True or False) else
            (
            False
        ))), (1, (
            ((self.blackboard.blVAR0[0] < self.blackboard.blDEFINE5()) ^ (False ^ False))
            if False else
            (
            (((not (True)) or (False)) or (False == False))
        )))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val

    def update(self):
        if ((self.localVAR2[1] == self.localVAR2[0]) == self.localVAR2[0]):
            return_status = py_trees.common.Status.SUCCESS
        elif (not ((self.localVAR2[1] ^ (self.blackboard.blVAR0[1] > self.blackboard.blVAR0[0])))):
            return_status = py_trees.common.Status.RUNNING
        elif (self.localVAR2[1] or True):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
