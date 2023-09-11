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
        self.localFROZENVAR5 = [None] * 2
        __temp_var__ = serene_safe_assignment.localFROZENVAR5([(0, 'both'), (1, 'both')])
        for (index, val) in __temp_var__:
            self.localFROZENVAR5[index] = val
        self.localVAR4 = serene_safe_assignment.localVAR4((
            ((self.blackboard.blVAR0[1] <= 21) != False)
            if False else
            (
            False
        )))
        self.localFROZENVAR6 = serene_safe_assignment.localFROZENVAR6((
            self.blackboard.blVAR3
            if (True and False) else
            (
            self.blackboard.blVAR3
        )))

    def update(self):
        if (-16 < self.blackboard.blVAR0[1]):
            return_status = py_trees.common.Status.RUNNING
        elif (([(True ^ (69 < 69)), (self.blackboard.blVAR0[0] >= max(19, 88))].count(True)) == (abs(-68) * max(-56, 63) * (-30 - self.blackboard.blVAR0[0]))):
            return_status = py_trees.common.Status.RUNNING
        elif (65 > ([(self.localFROZENVAR6 ^ False), ('yes' == self.localFROZENVAR5[1]), (24 > -17)].count(True))):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.localVAR4 = serene_safe_assignment.localVAR4((
            (-70 < (-7 * 64 * self.blackboard.blVAR0[0] * self.blackboard.blVAR0[2]))
            if False else
            (
            (min(self.blackboard.blVAR0[0], self.blackboard.blVAR0[1]) < (-97 + self.blackboard.blVAR0[1] + 37 + 3))
        )))
        return return_status
