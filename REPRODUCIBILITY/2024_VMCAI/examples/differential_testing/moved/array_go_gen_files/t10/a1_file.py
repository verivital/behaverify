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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = [None] * 3
        __temp_var__ = serene_safe_assignment.localVAR2([(0, min(5, max(2, 5))), (1, (
            min(5, max(2, (abs(-4) + abs(7) + abs((12 * -2)))))
            if (True == (False and False)) else
            (
            min(5, max(2, 44))
        ))), (2, (
            min(5, max(2, -(-14)))
            if True else
            (
                min(5, max(2, (0 * abs(4))))
                if (True == False) else
                (
                min(5, max(2, min(51, 3)))
        ))))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val


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


        def localDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE6: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, abs(-42)))
                    if False else
                    (
                    min(-2, max(-5, self.blackboard.blDEFINE5(1)))
                ))
            elif index == 1:
                return (
                    min(-2, max(-5, abs(-42)))
                    if False else
                    (
                    min(-2, max(-5, self.blackboard.blDEFINE5(1)))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE6: ' + str(index))

        self.localDEFINE6 = localDEFINE6

    def update(self):
        if self.environment.a1_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.localVAR2(self.environment.a1_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.localVAR2[index] = val
        if False:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.blackboard.blVAR3 = serene_safe_assignment.blVAR3((
            self.localDEFINE4()
            if ((87 <= ([(82 <= 83), (self.localVAR2[1] <= self.blackboard.blDEFINE5(1)), ((not (True)) or (False)), (False == True)].count(True))) == False) else
            (
                self.localDEFINE4()
                if (self.localVAR2[2] <= 17) else
                (
                self.localDEFINE4()
        ))))
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, self.blackboard.blDEFINE5(0))), self.localDEFINE4()), (min(2, max(0, abs(abs(-45)))), self.blackboard.blVAR0[1])])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return return_status
