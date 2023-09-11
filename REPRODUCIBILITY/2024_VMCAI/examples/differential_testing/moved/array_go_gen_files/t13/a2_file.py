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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)


        def localDEFINE7():
            return (
                min(5, max(2, ([((19 < self.blackboard.blVAR0) == (True and True)), (False ^ (self.blackboard.blVAR0 != 60)), (abs(([(self.blackboard.blVAR3[0] != 'both'), (False ^ False), (True and False), (False and True)].count(True))) <= (self.blackboard.blVAR0 * -39 * self.blackboard.blVAR0))].count(True))))
                if True else
                (
                    min(5, max(2, 24))
                    if (-59 < min(72, max(-23, self.blackboard.blVAR0))) else
                    (
                    min(5, max(2, ([(-6 <= self.blackboard.blVAR0), (self.blackboard.blVAR0 == -36), (False ^ (self.blackboard.blVAR3[1] == self.blackboard.blVAR3[0]))].count(True))))
            )))

        self.localDEFINE7 = localDEFINE7

    def update(self):
        self.environment.delay_this_action(self.environment.a2_write_before_0__0, self)
        if False:
            return_status = py_trees.common.Status.SUCCESS
        elif (self.blackboard.blVAR0 < (self.blackboard.blVAR0 + self.blackboard.blVAR0 + 56)):
            return_status = py_trees.common.Status.RUNNING
        elif True:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.environment.a2_write_after_0__0(self)
        self.environment.delay_this_action(self.environment.a2_write_after_0__1, self)
        return return_status
