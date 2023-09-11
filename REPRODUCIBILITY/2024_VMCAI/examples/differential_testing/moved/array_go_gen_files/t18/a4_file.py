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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR2([(min(2, max(0, self.blackboard.blDEFINE7(1))), (
            min(5, max(2, ([(-93 > max(-69, self.blackboard.blVAR0[1])), (self.blackboard.blVAR2[2] > (15 * -71 * 55 * self.blackboard.blVAR2[1])), (-(4) < (self.blackboard.blDEFINE7(2) * -9 * self.blackboard.blVAR2[1])), (self.blackboard.blVAR0[1] != -58)].count(True))))
            if ((not (self.blackboard.blDEFINE4())) or (True)) else
            (
            min(5, max(2, abs((-25 + self.blackboard.blVAR0[0] + self.blackboard.blDEFINE7(0) + 85))))
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR2[index] = val
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, abs(abs(-37)))), (
            min(-2, max(-5, 42))
            if ((not (self.blackboard.blDEFINE4())) or (self.blackboard.blDEFINE4())) else
            (
            min(-2, max(-5, -42))
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        if ((not ((self.blackboard.blVAR0[1] < self.blackboard.blVAR2[1]))) or (self.blackboard.blDEFINE4())):
            return_status = py_trees.common.Status.FAILURE
        elif (self.blackboard.blDEFINE4() and False):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
