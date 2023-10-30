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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)

    def update(self):
        if (self.blackboard.blDEFINE7() >= (self.blackboard.blVAR3 if (False == False) else self.blackboard.blVAR3)):
            return_status = py_trees.common.Status.RUNNING
        elif False:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        self.environment.a2_write_after_0__0(self)
        return return_status
