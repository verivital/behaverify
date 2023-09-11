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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, self.blackboard.blDEFINE5())), min(-2, max(-5, self.blackboard.blDEFINE5()))), (min(2, max(0, max(self.blackboard.blDEFINE5(), (0 + 5)))), min(-2, max(-5, max((self.blackboard.blVAR0[1] + self.blackboard.blDEFINE5() + self.blackboard.blVAR0[1] + self.blackboard.blDEFINE5()), self.blackboard.blVAR0[1]))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        if self.environment.a1_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a1_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
