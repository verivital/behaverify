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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)

    def update(self):
        return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, self.blackboard.blVAR0[0])), (
            min(-2, max(-5, self.blackboard.blVAR0[0]))
            if (self.blackboard.blDEFINE7() ^ self.blackboard.blDEFINE7()) else
            (
                min(-2, max(-5, 3))
                if (-(self.blackboard.blVAR0[0]) >= (max(self.blackboard.blVAR0[1], 10) + abs(60) + 27)) else
                (
                min(-2, max(-5, self.blackboard.blVAR0[0]))
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, self.blackboard.blVAR0[0])), (
            min(-2, max(-5, -(-36)))
            if (-(self.blackboard.blVAR0[0]) == min(max(12, self.blackboard.blVAR0[0]), (self.blackboard.blVAR0[0] - self.blackboard.blVAR0[1]))) else
            (
                min(-2, max(-5, self.blackboard.blVAR0[0]))
                if (5 >= (31 + -78 + (-48 * self.blackboard.blVAR0[0] * self.blackboard.blVAR0[1] * -6))) else
                (
                min(-2, max(-5, 86))
        )))), (min(1, max(0, (self.blackboard.blVAR0[0] * 61 * 40))), (
            min(-2, max(-5, (self.blackboard.blVAR0[0] - self.blackboard.blVAR0[1])))
            if ((-94 <= self.blackboard.blVAR0[1]) or (self.blackboard.blVAR0[1] > 90)) else
            (
                min(-2, max(-5, self.blackboard.blVAR0[1]))
                if True else
                (
                min(-2, max(-5, ((self.blackboard.blVAR0[1] * -13 * -97) - self.blackboard.blVAR0[0])))
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        if self.environment.a3_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a3_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return return_status
