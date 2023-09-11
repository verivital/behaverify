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
        self.localVAR2 = serene_safe_assignment.localVAR2(min(5, max(2, min(100, max(-100, -(min(100, max(-100, max(80, 10)))))))))


        def localDEFINE3(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE3: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE3: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, min(100, max(-100, max(min(100, max(-100, -(min(100, max(-100, max(-13, 13)))))), min(100, max(-100, min(min(100, max(-100, abs(-3))), -43))))))))
                    if (-95 <= 2) else
                    (
                    min(-2, max(-5, ([(not ((((not ((True ^ False))) ^ True) ^ (2 >= -3)))), ((not ((False ^ True))) != (-2 <= 4)), (True ^ (True == (True or True)))].count(True))))
                ))
            elif index == 1:
                return (
                    min(-2, max(-5, ([((min(100, max(-100, max(76, 2))) >= min(100, max(-100, min(-5, 2)))) ^ (True == False)), (not (((True or False) ^ True))), (min(100, max(-100, abs(-2))) > 2), ((not (False)) or ((False and True)))].count(True))))
                    if ((False and False) ^ False) else
                    (
                        min(-2, max(-5, -37))
                        if (True or (41 >= 34)) else
                        (
                        min(-2, max(-5, min(100, max(-100, (3 - -96)))))
                )))
            raise Exception('Reached unreachable state when accessing localDEFINE3: ' + str(index))

        self.localDEFINE3 = localDEFINE3

    def update(self):
        if (False ^ (False and self.blackboard.blDEFINE5(0))):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a4_read_after_2__condition(self):
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a4_read_after_2__0(self))
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a4_read_after_2__1(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        self.localVAR2 = serene_safe_assignment.localVAR2(min(5, max(2, min(100, max(-100, -(([((not (self.blackboard.blDEFINE5(0))) or (self.blackboard.blDEFINE5(0))), (self.localVAR2 > -12), (-21 == self.localVAR2)].count(True))))))))
        if self.environment.a4_read_after_0__condition(self):
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a4_read_after_0__0(self))
        return return_status
