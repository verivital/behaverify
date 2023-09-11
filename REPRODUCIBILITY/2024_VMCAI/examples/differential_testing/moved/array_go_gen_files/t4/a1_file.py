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


        def localDEFINE4(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE4: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE4: ' + str(index))
            if index == 0:
                return (
                    min(5, max(2, self.blackboard.blVAR0[1]))
                    if ((self.blackboard.blVAR0[1] != self.blackboard.blVAR0[1]) == ((-32 > self.blackboard.blVAR0[1]) or False)) else
                    (
                    min(5, max(2, (8 - self.blackboard.blVAR0[0])))
                ))
            elif index == 1:
                return (
                    min(5, max(2, (50 - self.blackboard.blVAR0[0])))
                    if (self.blackboard.blVAR0[1] < (self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0])) else
                    (
                        min(5, max(2, (self.blackboard.blVAR0[0] + self.blackboard.blVAR0[0])))
                        if (self.blackboard.blVAR0[0] > abs(self.blackboard.blVAR0[1])) else
                        (
                        min(5, max(2, self.blackboard.blVAR0[0]))
                )))
            raise Exception('Reached unreachable state when accessing localDEFINE4: ' + str(index))

        self.localDEFINE4 = localDEFINE4
        self.localVAR3 = serene_safe_assignment.localVAR3((
            ((([(self.blackboard.blVAR0[0] <= -83), (-94 > -94), (not ((False ^ False))), (False and False)].count(True)) < max(-84, self.blackboard.blDEFINE5())) == (True or True))
            if False else
            (
                (False and False)
                if ((3 + -(38)) == ([(True == False), (True ^ True), (True == True)].count(True))) else
                (
                (((not (False)) or ((self.blackboard.blDEFINE5() == self.blackboard.blVAR0[0]))) ^ (self.blackboard.blDEFINE5() < -34))
        ))))

    def update(self):
        if ((-62 <= self.localDEFINE4(1)) == (False or True)):
            return_status = py_trees.common.Status.SUCCESS
        elif (-78 > self.blackboard.blDEFINE5()):
            return_status = py_trees.common.Status.SUCCESS
        elif False:
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.delay_this_action(self.environment.a1_write_after_1__0, self)
        self.environment.delay_this_action(self.environment.a1_write_after_1__1, self)
        self.environment.a1_write_after_1__2(self)
        self.environment.a1_write_after_0__0(self)
        return return_status
