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

    def update(self):
        if self.environment.a1_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a1_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a1_read_before_0__1(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        if (((not (True)) or (True)) == (False or (True or True))):
            return_status = py_trees.common.Status.RUNNING
        elif (True == False):
            return_status = py_trees.common.Status.FAILURE
        elif (not ((True ^ (min(64, self.blackboard.blVAR0[0]) >= (self.blackboard.blVAR0[0] + -23))))):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.environment.a1_write_after_0__0(self)
        return return_status
