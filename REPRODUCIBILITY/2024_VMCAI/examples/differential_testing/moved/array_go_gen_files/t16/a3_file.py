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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)
        self.localVAR4 = serene_safe_assignment.localVAR4((
            (True and (self.blackboard.blVAR0 >= self.blackboard.blVAR3))
            if False else
            (
                (6 >= self.blackboard.blVAR3)
                if (self.blackboard.blVAR0 > self.blackboard.blVAR0) else
                (
                True
        ))))


        def localDEFINE9(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE9: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE9: ' + str(index))
            if index == 0:
                return (
                    min(5, max(2, (([(True == True), (True == self.blackboard.blDEFINE7(2)), (self.blackboard.blVAR3 >= self.blackboard.blVAR0)].count(True)) * self.blackboard.blVAR0)))
                    if (not ((False ^ self.blackboard.blDEFINE7(1)))) else
                    (
                    min(5, max(2, (self.blackboard.blVAR0 - -29)))
                ))
            elif index == 1:
                return (
                    min(5, max(2, (([(True == True), (True == self.blackboard.blDEFINE7(2)), (self.blackboard.blVAR3 >= self.blackboard.blVAR0)].count(True)) * self.blackboard.blVAR0)))
                    if (not ((False ^ self.blackboard.blDEFINE7(1)))) else
                    (
                    min(5, max(2, (self.blackboard.blVAR0 - -29)))
                ))
            elif index == 2:
                return (
                    min(5, max(2, (([(True == True), (True == self.blackboard.blDEFINE7(2)), (self.blackboard.blVAR3 >= self.blackboard.blVAR0)].count(True)) * self.blackboard.blVAR0)))
                    if (not ((False ^ self.blackboard.blDEFINE7(1)))) else
                    (
                    min(5, max(2, (self.blackboard.blVAR0 - -29)))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE9: ' + str(index))

        self.localDEFINE9 = localDEFINE9

    def update(self):
        if ((not ((3 != -74))) or ((50 >= self.localDEFINE9(2)))):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.localVAR4 = serene_safe_assignment.localVAR4((
            (self.blackboard.blVAR0 < 46)
            if ((not (True)) or (self.localVAR4)) else
            (
                (self.blackboard.blVAR0 < self.localDEFINE9(2))
                if self.blackboard.blDEFINE7(0) else
                (
                (not (((True and self.localVAR4) ^ ((not (self.blackboard.blDEFINE7(0))) or (self.blackboard.blDEFINE7(0))))))
        ))))
        return return_status
