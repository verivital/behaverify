import py_trees
import math
import operator
import random
import serene_safe_assignment


class a3(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(a3, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.a3_read_before_1__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a3_read_before_1__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        if self.environment.a3_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a3_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        if (([((not (True)) or (False)), (True and False), (True == True)].count(True)) >= abs(self.blackboard.blDEFINE5())):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, ([(self.blackboard.blVAR0[0] >= -90), ((not ((False == (True ^ True)))) or ((self.blackboard.blDEFINE5() >= self.blackboard.blDEFINE5())))].count(True)))), (
            min(-2, max(-5, self.blackboard.blVAR0[1]))
            if (-71 > self.blackboard.blVAR0[0]) else
            (
            min(-2, max(-5, abs(-31)))
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        if self.environment.a3_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a3_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return return_status
