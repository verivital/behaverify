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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = [None] * 3


        def localDEFINE4():
            return (
                'no'
                if (False or False) else
                (
                    'both'
                    if (-3 <= -3) else
                    (
                    'both'
            )))

        self.localDEFINE4 = localDEFINE4
        __temp_var__ = serene_safe_assignment.localVAR2([(0, min(5, max(2, -(abs(self.blackboard.blDEFINE5(1)))))), (1, min(5, max(2, (29 - ((8 * self.blackboard.blDEFINE5(0) * -63 * self.blackboard.blDEFINE5(0)) + min(-36, self.blackboard.blDEFINE5(0)) + (self.blackboard.blDEFINE5(1) - self.blackboard.blDEFINE5(1))))))), (2, min(5, max(2, abs((-65 - self.blackboard.blDEFINE5(1))))))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val


        def localDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE6: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, self.blackboard.blDEFINE5(0)))
                    if (max(self.blackboard.blDEFINE5(1), -1) > -(self.blackboard.blDEFINE5(1))) else
                    (
                    min(-2, max(-5, 6))
                ))
            elif index == 1:
                return (
                    min(-2, max(-5, ((self.blackboard.blDEFINE5(0) + 15) - self.blackboard.blDEFINE5(1))))
                    if True else
                    (
                    min(-2, max(-5, -((self.blackboard.blDEFINE5(1) * self.blackboard.blDEFINE5(1)))))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE6: ' + str(index))

        self.localDEFINE6 = localDEFINE6

    def update(self):
        if (False ^ False):
            return_status = py_trees.common.Status.SUCCESS
        elif True:
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
