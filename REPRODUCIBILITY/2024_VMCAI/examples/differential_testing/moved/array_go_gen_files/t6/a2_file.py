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
        self.blackboard.register_key(key = ('blVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)


        def localDEFINE7():
            return False

        self.localDEFINE7 = localDEFINE7

    def update(self):
        if (((not (self.blackboard.blVAR0[2])) or (self.blackboard.blDEFINE6(0))) == True):
            return_status = py_trees.common.Status.RUNNING
        elif ((not ((not ((True ^ self.blackboard.blVAR0[0]))))) or ((not ((self.blackboard.blDEFINE6(1) ^ self.localDEFINE7()))))):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
