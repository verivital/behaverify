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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.localVAR3 = [None] * 2
        __temp_var__ = serene_safe_assignment.localVAR3([(0, (
            ('both' != 'both')
            if (True == True) else
            (
                (-26 < -63)
                if True else
                (
                True
        )))), (1, (
            True
            if False else
            (
            ('yes' != 'no')
        )))])
        for (index, val) in __temp_var__:
            self.localVAR3[index] = val

    def update(self):
        return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        self.environment.a2_write_after_1__0(self)
        __temp_var__ = serene_safe_assignment.localVAR3([(min(1, max(0, 74)), (
            True
            if (self.localVAR3[0] != self.localVAR3[0]) else
            (
            (self.blackboard.blDEFINE5() < (self.blackboard.blVAR0[2] * self.blackboard.blVAR0[2] * 67))
        )))])
        for (index, val) in __temp_var__:
            self.localVAR3[index] = val
        return return_status
