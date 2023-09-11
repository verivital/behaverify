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
        self.blackboard.register_key(key = ('blFROZENVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)

    def update(self):
        if (self.blackboard.blVAR3[1] and (self.blackboard.blVAR3[0] and self.blackboard.blVAR3[0])):
            return_status = py_trees.common.Status.FAILURE
        elif (((self.blackboard.blDEFINE6() - -27) > (28 + self.blackboard.blFROZENVAR4[0] + -39 + 90)) or (-(40) > max(self.blackboard.blFROZENVAR4[0], self.blackboard.blFROZENVAR4[0]))):
            return_status = py_trees.common.Status.FAILURE
        elif (abs(self.blackboard.blDEFINE6()) < max(self.blackboard.blDEFINE6(), self.blackboard.blFROZENVAR4[1])):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
