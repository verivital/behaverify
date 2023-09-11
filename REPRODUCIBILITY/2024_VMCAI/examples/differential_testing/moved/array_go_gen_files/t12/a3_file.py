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
        self.blackboard.register_key(key = ('blDEFINE3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)

    def update(self):
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.delay_this_action(self.environment.a3_write_after_0__0, self)
        return return_status
