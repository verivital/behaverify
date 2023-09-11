import py_trees
import math
import operator
import random
import serene_safe_assignment


class c2(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(c2, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (((not (True)) or (((self.blackboard.blVAR0[1] >= self.blackboard.blVAR0[0]) and (-80 > self.blackboard.blVAR0[1]))))) else (py_trees.common.Status.FAILURE))
        self.__serene_print__ = return_status.value
        return return_status
