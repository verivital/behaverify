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
        self.blackboard.register_key(key = ('blDEFINE3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.a2_read_before_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__0(self))
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__1(self))
        return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        if self.environment.a2_read_after_1__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a2_read_after_1__0(self))
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0((([((self.blackboard.blVAR0 and self.blackboard.blVAR0) and (not ((True ^ False)))), (99 <= -(60)), (max(self.blackboard.blDEFINE4(), self.blackboard.blDEFINE4()) == self.blackboard.blDEFINE4())].count(True)) >= -(-68)))
        return return_status
