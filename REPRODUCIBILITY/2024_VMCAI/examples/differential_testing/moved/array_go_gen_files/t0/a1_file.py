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
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.a1_read_before_0__condition(self):
            self.blackboard.blVAR2 = serene_safe_assignment.blVAR2(self.environment.a1_read_before_0__0(self))
        if (False == (-64 >= -35)):
            return_status = py_trees.common.Status.FAILURE
        elif True:
            return_status = py_trees.common.Status.SUCCESS
        elif (self.blackboard.blVAR2 != self.blackboard.blVAR0[0]):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.a1_write_after_1__0(self)
        self.environment.delay_this_action(self.environment.a1_write_after_1__1, self)
        self.environment.a1_write_after_0__0(self)
        return return_status
