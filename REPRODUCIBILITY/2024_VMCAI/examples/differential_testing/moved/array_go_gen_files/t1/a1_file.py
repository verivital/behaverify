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
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, min(100, max(-100, max(-39, 5))))), (
            self.blackboard.blVAR0[1]
            if (self.blackboard.blVAR0[0] == 'both') else
            (
                self.blackboard.blVAR0[0]
                if (86 <= 79) else
                (
                self.blackboard.blVAR0[0]
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        self.environment.a1_write_before_1__0(self)
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, 4)), (
            'both'
            if (True == True) else
            (
                'both'
                if (False ^ ((-95 <= -33) == self.blackboard.blDEFINE5(1))) else
                (
                self.blackboard.blVAR0[0]
        )))), (min(2, max(0, min(100, max(-100, (-4 + 4 + 4))))), (
            'yes'
            if self.blackboard.blDEFINE5(1) else
            (
                self.blackboard.blVAR0[2]
                if (min(100, max(-100, (-3 + 3 + -4))) != 33) else
                (
                'yes'
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a1_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a1_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return return_status
