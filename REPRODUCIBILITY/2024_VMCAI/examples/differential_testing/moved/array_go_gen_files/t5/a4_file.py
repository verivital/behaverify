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
        self.blackboard.register_key(key = ('blFROZENVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)

    def update(self):
        if (22 < -46):
            return_status = py_trees.common.Status.SUCCESS
        elif ((-76 * self.blackboard.blFROZENVAR4[1] * 83 * self.blackboard.blFROZENVAR4[0]) == self.blackboard.blDEFINE6()):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
