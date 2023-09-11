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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blFROZENVAR5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.environment.delay_this_action(self.environment.a3_write_before_0__0, self)
        self.environment.a3_write_before_0__1(self)
        if (95 == min(6, self.blackboard.blFROZENVAR5[0])):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.environment.delay_this_action(self.environment.a3_write_after_0__0, self)
        return return_status
