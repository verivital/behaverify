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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.localFROZENVAR5 = [None] * 2
        __temp_var__ = serene_safe_assignment.localFROZENVAR5([(0, 'both'), (1, 'both')])
        for (index, val) in __temp_var__:
            self.localFROZENVAR5[index] = val
        self.localVAR4 = serene_safe_assignment.localVAR4((
            self.blackboard.blVAR3
            if ((-54 > self.blackboard.blVAR0[0]) or ((not (False)) or (False))) else
            (
            (self.blackboard.blVAR0[1] > self.blackboard.blVAR0[2])
        )))
        self.localFROZENVAR6 = serene_safe_assignment.localFROZENVAR6((
            ('yes' != 'no')
            if (self.blackboard.blVAR0[2] < self.blackboard.blVAR0[1]) else
            (
                False
                if (-18 >= self.blackboard.blVAR0[0]) else
                (
                ((self.blackboard.blVAR0[0] < 3) and (self.blackboard.blVAR3 == self.blackboard.blVAR3))
        ))))

    def update(self):
        self.blackboard.blVAR3 = serene_safe_assignment.blVAR3((max(max(self.blackboard.blVAR0[0], -18), (-100 - 71)) < -10))
        self.localVAR4 = serene_safe_assignment.localVAR4(((max(self.blackboard.blVAR0[0], -98) > (74 * self.blackboard.blVAR0[1])) ^ self.blackboard.blVAR3))
        return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
