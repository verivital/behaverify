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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR2([(min(2, max(0, -(max(-5, self.blackboard.blVAR0[1])))), min(5, max(2, (min(self.blackboard.blVAR2[2], self.blackboard.blDEFINE7(2)) - -5)))), (min(2, max(0, (self.blackboard.blDEFINE7(2) - -34))), min(5, max(2, self.blackboard.blVAR2[1])))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR2[index] = val
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
