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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, 79)), (
            min(-2, max(-5, ([(min(self.blackboard.blDEFINE7(1), -89) >= (7 + self.blackboard.blVAR2[2] + -53 + self.blackboard.blDEFINE7(0))), (((not ((False ^ self.blackboard.blDEFINE4()))) and self.blackboard.blDEFINE4()) ^ ((self.blackboard.blVAR0[0] * self.blackboard.blVAR0[0]) > -71))].count(True))))
            if (self.blackboard.blVAR2[0] >= self.blackboard.blVAR0[1]) else
            (
                min(-2, max(-5, (self.blackboard.blDEFINE7(0) + self.blackboard.blDEFINE7(2) + -76)))
                if (False == True) else
                (
                min(-2, max(-5, max(self.blackboard.blDEFINE7(2), 20)))
        )))), (min(1, max(0, ([('both' == 'no'), (self.blackboard.blDEFINE4() == True), (((not (True)) or (self.blackboard.blDEFINE4())) ^ False)].count(True)))), (
            min(-2, max(-5, (((-50 - -58) + (self.blackboard.blVAR0[0] * self.blackboard.blVAR2[0])) - self.blackboard.blDEFINE7(0))))
            if (80 > self.blackboard.blDEFINE7(2)) else
            (
                min(-2, max(-5, -((self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0] + -71))))
                if (max(self.blackboard.blVAR2[1], (self.blackboard.blVAR2[0] + -98 + self.blackboard.blVAR0[1] + 35)) <= -(77)) else
                (
                min(-2, max(-5, (self.blackboard.blDEFINE7(2) - self.blackboard.blDEFINE7(1))))
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        if ((-12 + -88 + (-52 - self.blackboard.blVAR0[0])) > self.blackboard.blVAR0[1]):
            return_status = py_trees.common.Status.FAILURE
        elif self.blackboard.blDEFINE4():
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
