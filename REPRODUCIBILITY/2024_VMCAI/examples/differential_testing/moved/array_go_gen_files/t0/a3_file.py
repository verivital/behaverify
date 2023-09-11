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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)

    def update(self):
        if (self.blackboard.blVAR0[1] < 27):
            return_status = py_trees.common.Status.SUCCESS
        elif False:
            return_status = py_trees.common.Status.FAILURE
        elif (-84 != min(100, max(-100, min(-4, self.blackboard.blDEFINE4())))):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, ([(True and True), (self.blackboard.blDEFINE4() != self.blackboard.blVAR2)].count(True)))), (
            min(5, max(2, min(100, max(-100, (self.blackboard.blVAR0[1] + self.blackboard.blDEFINE4() + self.blackboard.blVAR2 + self.blackboard.blDEFINE4())))))
            if (self.blackboard.blVAR0[1] <= min(100, max(-100, -(min(100, max(-100, -(self.blackboard.blVAR2))))))) else
            (
            min(5, max(2, min(100, max(-100, (37 * -70 * self.blackboard.blDEFINE4() * min(100, max(-100, (74 - -84))))))))
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        self.blackboard.blVAR2 = serene_safe_assignment.blVAR2((
            min(-2, max(-5, -34))
            if ((True == True) == True) else
            (
            min(-2, max(-5, self.blackboard.blVAR0[1]))
        )))
        return return_status
