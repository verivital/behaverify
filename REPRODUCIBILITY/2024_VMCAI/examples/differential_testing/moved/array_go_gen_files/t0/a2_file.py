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

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, abs(92))), (
            min(5, max(2, self.blackboard.blVAR0[1]))
            if ('both' == 'yes') else
            (
            min(5, max(2, max(self.blackboard.blVAR0[0], 30)))
        ))), (min(1, max(0, self.blackboard.blVAR0[1])), (
            min(5, max(2, -(self.blackboard.blVAR0[1])))
            if True else
            (
            min(5, max(2, -8))
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        if self.environment.a2_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__1(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a2_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return return_status
