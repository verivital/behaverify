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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2(min(-2, max(-5, (self.blackboard.blVAR3 * max(-99, self.blackboard.blVAR3) * self.blackboard.blDEFINE5() * 24))))

    def update(self):
        if self.environment.a3_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a3_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        if (self.blackboard.blVAR3 != -79):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
