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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.localFROZENVAR6 = serene_safe_assignment.localFROZENVAR6((
            True
            if (True and (12 <= 78)) else
            (
            self.blackboard.blVAR3
        )))


        def localDEFINE8():
            return (19 > -35)

        self.localDEFINE8 = localDEFINE8

    def update(self):
        self.environment.delay_this_action(self.environment.a1_write_before_1__0, self)
        self.blackboard.blVAR3 = serene_safe_assignment.blVAR3((
            ((66 + -65) >= self.blackboard.blVAR0[2])
            if False else
            (
            ((17 * self.blackboard.blVAR0[1]) != self.blackboard.blVAR0[2])
        )))
        if False:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, self.blackboard.blVAR0[2])), (
            min(-2, max(-5, ((65 + -90 + max(self.blackboard.blVAR0[2], 10)) + (max(self.blackboard.blVAR0[2], -71) + -(self.blackboard.blVAR0[2])))))
            if (not (((self.blackboard.blVAR3 and True) ^ True))) else
            (
                min(-2, max(-5, abs(self.blackboard.blVAR0[1])))
                if False else
                (
                min(-2, max(-5, (self.blackboard.blVAR0[2] * 8)))
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return return_status
