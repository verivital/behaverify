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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)


        def localDEFINE4(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE4: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE4: ' + str(index))
            if index == 0:
                return (
                    min(5, max(2, 15))
                    if True else
                    (
                    min(5, max(2, 70))
                ))
            elif index == 1:
                return (
                    min(5, max(2, ([((True or True) == True), (-(self.blackboard.blVAR0[0]) >= (96 - -91)), ((-30 <= self.blackboard.blVAR0[1]) == ((not (False)) or (True)))].count(True))))
                    if ((self.blackboard.blVAR0[1] * 37 * -76 * 86) == self.blackboard.blVAR0[1]) else
                    (
                    min(5, max(2, (17 - ((self.blackboard.blVAR0[0] * self.blackboard.blVAR0[0]) * 27))))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE4: ' + str(index))

        self.localDEFINE4 = localDEFINE4

    def update(self):
        if self.environment.a2_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        if self.environment.a2_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_after_0__1(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return return_status
