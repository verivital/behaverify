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
        self.blackboard.register_key(key = ('blFROZENVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2(min(5, max(2, min(abs(self.blackboard.blDEFINE6()), self.blackboard.blFROZENVAR4[1]))))

    def update(self):
        if self.environment.a1_read_before_2__condition(self):
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a1_read_before_2__0(self))
        self.environment.delay_this_action(self.environment.a1_write_before_0__0, self)
        self.environment.delay_this_action(self.environment.a1_write_before_0__1, self)
        return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        if self.environment.a1_read_after_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a1_read_after_0__0(self))
        return return_status
