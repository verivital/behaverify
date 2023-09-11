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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)


        def localDEFINE8():
            return (
                min(5, max(2, abs(self.blackboard.blVAR0[2])))
                if (not ((self.blackboard.blDEFINE7(1) ^ True))) else
                (
                    min(5, max(2, max(-49, abs(self.blackboard.blVAR0[2]))))
                    if (not (((False == (self.blackboard.blDEFINE7(1) ^ self.blackboard.blDEFINE7(0))) ^ self.blackboard.blDEFINE7(1)))) else
                    (
                    min(5, max(2, min(self.blackboard.blVAR0[0], self.blackboard.blVAR0[1])))
            )))

        self.localDEFINE8 = localDEFINE8

    def update(self):
        self.environment.delay_this_action(self.environment.a1_write_before_1__0, self)
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, ([(False != self.blackboard.blDEFINE7(0)), (-(self.blackboard.blVAR0[2]) < 58)].count(True)))), min(-2, max(-5, -50))), (min(2, max(0, min((self.localDEFINE8() * -12 * self.localDEFINE8() * self.blackboard.blVAR0[0]), self.localDEFINE8()))), min(-2, max(-5, abs(20))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        if (not ((self.blackboard.blDEFINE5(1) ^ (self.blackboard.blDEFINE5(2) == self.blackboard.blDEFINE7(0))))):
            return_status = py_trees.common.Status.SUCCESS
        elif self.blackboard.blDEFINE7(1):
            return_status = py_trees.common.Status.RUNNING
        elif (((not ((self.blackboard.blDEFINE5(2) and False))) or (True)) ^ (([((not (False)) or (self.blackboard.blDEFINE5(2))), (self.blackboard.blDEFINE7(0) == True)].count(True)) >= -46)):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
