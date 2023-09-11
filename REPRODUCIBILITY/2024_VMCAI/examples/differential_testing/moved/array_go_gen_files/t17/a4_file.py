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
        if ((min(51, self.blackboard.blVAR0[1]) == self.blackboard.blDEFINE5()) == (not ((False ^ (self.localVAR3[1] or self.localVAR3[1]))))):
            return_status = py_trees.common.Status.FAILURE
        elif (self.blackboard.blVAR0[2] >= (self.blackboard.blVAR0[0] - -63)):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
