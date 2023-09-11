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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = [None] * 2


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
        __temp_var__ = serene_safe_assignment.localVAR2([(0, (
            (self.blackboard.blDEFINE5() > self.blackboard.blVAR0[0])
            if ((not (False)) or (False)) else
            (
                False
                if ((not ((False == False))) or ((False or True))) else
                (
                (not (((-76 > 69) ^ (False != True))))
        )))), (1, (
            (False ^ True)
            if (False and True) else
            (
                True
                if ((self.blackboard.blDEFINE5() > 78) and True) else
                (
                ((True and False) != False)
        ))))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val

    def update(self):
        __temp_var__ = serene_safe_assignment.localVAR2([(min(1, max(0, self.localDEFINE4(1))), (
            ((self.blackboard.blVAR0[1] - 67) != (18 - -4))
            if (self.blackboard.blDEFINE5() == 15) else
            (
            (99 < min(self.blackboard.blVAR0[1], -29))
        )))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val
        if (self.blackboard.blDEFINE5() < self.blackboard.blDEFINE5()):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        self.environment.a3_write_after_1__0(self)
        self.environment.delay_this_action(self.environment.a3_write_after_1__1, self)
        self.environment.a3_write_after_0__0(self)
        return return_status
