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
        self.blackboard.register_key(key = ('blFROZENVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2(min(5, max(2, max(78, -76))))

    def update(self):
        self.environment.delay_this_action(self.environment.a2_write_before_0__0, self)
        return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
