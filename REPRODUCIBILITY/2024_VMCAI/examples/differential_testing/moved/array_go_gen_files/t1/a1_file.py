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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)


        def localDEFINE5():
            return min(5, max(2, ((self.blackboard.blVAR0[0] * 50 * -15 * self.blackboard.blVAR0[1]) * -(self.blackboard.blVAR0[0]) * self.blackboard.blVAR0[1])))

        self.localDEFINE5 = localDEFINE5

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, max(33, -79))), (
            min(-2, max(-5, min(self.blackboard.blVAR0[0], 41)))
            if (True == (self.localDEFINE5() <= 91)) else
            (
            min(-2, max(-5, self.blackboard.blVAR0[0]))
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
