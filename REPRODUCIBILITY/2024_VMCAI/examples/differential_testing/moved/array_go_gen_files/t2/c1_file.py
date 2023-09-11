import py_trees
import math
import operator
import random
import serene_safe_assignment


class c1(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(c1, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('blFROZENVAR5'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((True or self.blackboard.blVAR2)) else (py_trees.common.Status.FAILURE))
        self.__serene_print__ = return_status.value
        return return_status
