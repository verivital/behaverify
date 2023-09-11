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
        self.localVAR2 = serene_safe_assignment.localVAR2((
            min(5, max(2, min(100, max(-100, (min(100, max(-100, (60 * -2 * 5 * -74))) + min(100, max(-100, (58 * 79))) + 2 + min(100, max(-100, abs(3))))))))
            if (self.blackboard.blDEFINE5(1) and (-5 < 76)) else
            (
            min(5, max(2, 22))
        )))

    def update(self):
        if True:
            return_status = py_trees.common.Status.SUCCESS
        elif (not (((not ((True ^ self.blackboard.blDEFINE5(1)))) ^ (self.blackboard.blDEFINE5(1) == False)))):
            return_status = py_trees.common.Status.RUNNING
        elif ((self.localVAR2 <= self.localVAR2) == ((not (self.blackboard.blDEFINE5(1))) or (True))):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.a3_write_after_1__0(self)
        self.environment.delay_this_action(self.environment.a3_write_after_1__1, self)
        self.environment.a3_write_after_1__2(self)
        if self.environment.a3_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a3_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return return_status
