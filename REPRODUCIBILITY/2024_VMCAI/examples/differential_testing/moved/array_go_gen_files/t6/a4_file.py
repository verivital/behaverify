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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.a4_read_before_1__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a4_read_before_1__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        self.environment.delay_this_action(self.environment.a4_write_before_0__0, self)
        if (not (((self.blackboard.blVAR0[2] or self.blackboard.blDEFINE6(1)) ^ (51 < self.blackboard.blDEFINE5())))):
            return_status = py_trees.common.Status.FAILURE
        elif (True == self.blackboard.blVAR0[1]):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        if self.environment.a4_read_after_1__condition(self):
            self.blackboard.blVAR4 = serene_safe_assignment.blVAR4(self.environment.a4_read_after_1__0(self))
        if self.environment.a4_read_after_0__condition(self):
            self.blackboard.blVAR4 = serene_safe_assignment.blVAR4(self.environment.a4_read_after_0__0(self))
        return return_status
