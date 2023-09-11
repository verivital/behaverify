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

    def update(self):
        if self.environment.a2_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__1(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        if (39 > -2):
            return_status = py_trees.common.Status.FAILURE
        elif (True or self.blackboard.blDEFINE5(1)):
            return_status = py_trees.common.Status.RUNNING
        elif (self.blackboard.blDEFINE5(0) and True):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
