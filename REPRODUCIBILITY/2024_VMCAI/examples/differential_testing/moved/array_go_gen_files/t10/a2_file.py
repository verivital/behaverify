import py_trees
import math
import operator
import random
import serene_safe_assignment


class a2(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(a2, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = [None] * 3
        __temp_var__ = serene_safe_assignment.localVAR2([(0, (
            min(5, max(2, (-71 + -88)))
            if ((False == False) and (self.blackboard.blDEFINE5(0) <= self.blackboard.blDEFINE5(1))) else
            (
            min(5, max(2, -(abs(6))))
        ))), (1, (
            min(5, max(2, -97))
            if True else
            (
            min(5, max(2, max(self.blackboard.blDEFINE5(1), 51)))
        ))), (2, (
            min(5, max(2, ([((57 + self.blackboard.blDEFINE5(1) + self.blackboard.blDEFINE5(0)) < self.blackboard.blDEFINE5(1)), (11 >= ((self.blackboard.blDEFINE5(1) * self.blackboard.blDEFINE5(0) * 15 * self.blackboard.blDEFINE5(1)) - self.blackboard.blDEFINE5(0))), (True or (5 != abs(-52))), (abs(self.blackboard.blDEFINE5(0)) > max((63 - self.blackboard.blDEFINE5(0)), -22))].count(True))))
            if ((-95 + 91) < max(max(self.blackboard.blDEFINE5(1), self.blackboard.blDEFINE5(1)), abs(-50))) else
            (
            min(5, max(2, (-59 * -92 * -(-15))))
        )))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val

    def update(self):
        if ((not ((False ^ True))) ^ False):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.localVAR2([(min(2, max(0, self.localVAR2[2])), min(5, max(2, max(-37, -74)))), (min(2, max(0, self.blackboard.blDEFINE5(1))), min(5, max(2, -(self.blackboard.blDEFINE5(0))))), (min(2, max(0, abs(-49))), min(5, max(2, -(self.blackboard.blDEFINE5(1)))))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val
        __temp_var__ = serene_safe_assignment.localVAR2([(min(2, max(0, 13)), min(5, max(2, ((-4 - 40) + self.blackboard.blDEFINE5(1) + self.blackboard.blDEFINE5(1))))), (min(2, max(0, (([(not ((False ^ True))), ((not (True)) or (False))].count(True)) + min(61, self.localVAR2[0]) + min(72, self.blackboard.blDEFINE5(0))))), min(5, max(2, self.localVAR2[2]))), (min(2, max(0, -((self.localVAR2[2] * self.localVAR2[2])))), min(5, max(2, max(([((not (False)) or (False)), ((False and False) == False), ((-98 * self.localVAR2[1]) < min(self.blackboard.blDEFINE5(0), self.localVAR2[2]))].count(True)), 5))))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val
        return return_status
