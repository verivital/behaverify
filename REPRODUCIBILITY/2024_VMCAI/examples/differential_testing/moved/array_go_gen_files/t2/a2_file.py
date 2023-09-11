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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)

    def update(self):
        if (-1 <= self.blackboard.blVAR0):
            return_status = py_trees.common.Status.SUCCESS
        elif (self.blackboard.blVAR0 == self.blackboard.blVAR0):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR3([(min(1, max(0, min(100, max(-100, -(self.blackboard.blVAR0))))), (
            'yes'
            if (min(100, max(-100, max(24, -19))) <= min(100, max(-100, min(self.blackboard.blVAR0, self.blackboard.blVAR0)))) else
            (
                self.blackboard.blVAR2
                if (17 < min(100, max(-100, (self.blackboard.blVAR0 + min(100, max(-100, -(self.blackboard.blVAR0))) + min(100, max(-100, (self.blackboard.blVAR0 * self.blackboard.blVAR0))))))) else
                (
                self.blackboard.blVAR3[1]
        )))), (min(1, max(0, min(100, max(-100, (64 + self.blackboard.blVAR0))))), (
            self.blackboard.blVAR3[0]
            if (False == (False == True)) else
            (
                'no'
                if (self.blackboard.blVAR0 <= self.blackboard.blVAR0) else
                (
                'both'
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR3[index] = val
        __temp_var__ = serene_safe_assignment.blVAR3([(min(1, max(0, min(100, max(-100, (min(100, max(-100, (-82 - self.blackboard.blVAR0))) * -59 * self.blackboard.blVAR0))))), (
            'yes'
            if (([(self.blackboard.blVAR0 <= ([(False ^ True), (self.blackboard.blVAR0 > self.blackboard.blVAR0), (self.blackboard.blVAR0 >= -10)].count(True))), (True or False), (True or True)].count(True)) >= ([(min(100, max(-100, (self.blackboard.blVAR0 + -80))) <= self.blackboard.blVAR0), (('both' == 'both') and False), (self.blackboard.blVAR0 >= self.blackboard.blVAR0), (False == True)].count(True))) else
            (
            self.blackboard.blVAR3[0]
        ))), (min(1, max(0, min(100, max(-100, (63 + self.blackboard.blVAR0))))), (
            'no'
            if ('yes' != 'both') else
            (
            'both'
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR3[index] = val
        return return_status
