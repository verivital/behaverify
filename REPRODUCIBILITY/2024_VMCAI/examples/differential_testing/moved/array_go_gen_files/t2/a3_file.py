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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.localVAR4 = serene_safe_assignment.localVAR4((
            ((False or False) and (False ^ (False == True)))
            if (self.blackboard.blVAR0 != 18) else
            (
            (self.blackboard.blVAR0 > min(100, max(-100, -(self.blackboard.blVAR0))))
        )))

    def update(self):
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0((
            min(-2, max(-5, ([(min(100, max(-100, (self.blackboard.blVAR0 - self.blackboard.blVAR0))) <= min(100, max(-100, abs(47)))), (min(100, max(-100, (self.blackboard.blVAR0 * self.blackboard.blVAR0 * self.blackboard.blVAR0 * self.blackboard.blVAR0))) < min(100, max(-100, abs(self.blackboard.blVAR0))))].count(True))))
            if (self.localVAR4 ^ True) else
            (
            min(-2, max(-5, min(100, max(-100, (self.blackboard.blVAR0 - 25)))))
        )))
        self.environment.delay_this_action(self.environment.a3_write_before_2__0, self)
        self.blackboard.blVAR2 = serene_safe_assignment.blVAR2((
            self.blackboard.blVAR3[1]
            if (True or True) else
            (
                'no'
                if self.localVAR4 else
                (
                self.blackboard.blVAR3[1]
        ))))
        self.environment.delay_this_action(self.environment.a3_write_before_0__0, self)
        return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
