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
        self.blackboard.register_key(key = ('blDEFINE3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)

    def update(self):
        return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
