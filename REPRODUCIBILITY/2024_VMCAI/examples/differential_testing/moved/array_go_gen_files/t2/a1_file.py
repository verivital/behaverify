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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)

    def update(self):
        return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        if self.environment.a1_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR3(self.environment.a1_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR3[index] = val
            self.blackboard.blVAR2 = serene_safe_assignment.blVAR2(self.environment.a1_read_after_0__1(self))
            self.blackboard.blVAR2 = serene_safe_assignment.blVAR2(self.environment.a1_read_after_0__2(self))
        return return_status
