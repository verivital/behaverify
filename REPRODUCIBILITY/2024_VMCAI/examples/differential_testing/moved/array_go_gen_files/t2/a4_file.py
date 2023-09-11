import py_trees
import math
import operator
import random
import serene_safe_assignment


class a4(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(a4, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.localVAR4 = serene_safe_assignment.localVAR4((
            (True ^ False)
            if True else
            (
            (([(False == True), (not ((True ^ True)))].count(True)) >= self.blackboard.blVAR0)
        )))

    def update(self):
        if self.environment.a4_read_before_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a4_read_before_0__0(self))
        if (-35 <= 33):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.a4_write_after_0__0(self)
        return return_status
