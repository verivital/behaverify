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
        self.blackboard.register_key(key = ('blFROZENVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.a4_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR3(self.environment.a4_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR3[index] = val
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a4_read_before_0__1(self))
        if False:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a4_read_after_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a4_read_after_0__0(self))
        return return_status
