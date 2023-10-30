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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.environment.a3_write_before_0__0(self)
        if (((-2) != (-33)) ^ self.blackboard.blVAR0):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0((
            ((False or True) == (False == self.blackboard.blVAR0))
            if (self.blackboard.blVAR3[serene_safe_assignment.index_func(max(0, min(1, (-2))), 2)] or True) else
            (
                (37 >= (-23))
                if ((min(50, max((-50), (13 * 13 * (-5) * 47)))) <= (min(50, max((-50), min(2, 41))))) else
                (
                (((self.blackboard.blVAR0 != self.blackboard.blVAR0) == (not ((True ^ True)))) ^ ((True == self.blackboard.blVAR0) == True))
        ))))
        if self.environment.a3_read_after_1__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR2(self.environment.a3_read_after_1__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR2[index] = val
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0((self.blackboard.blVAR3[serene_safe_assignment.index_func(max(0, min(1, (-50))), 2)] == (True or self.blackboard.blVAR0)))
        print('A3----> ' + str(self.blackboard.blVAR2))
        return return_status
