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
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.environment.delay_this_action(self.environment.a3_write_before_1__0, self)
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0((
            min(5, max(2, 76))
            if ((False != False) ^ True) else
            (
            min(5, max(2, ((self.blackboard.blVAR0 * self.blackboard.blVAR0 * self.blackboard.blVAR0) * ([(-44 >= -36), (not ((False ^ True))), (True or False), ('no' == 'no')].count(True)) * self.blackboard.blVAR0)))
        )))
        if (not (((-67 > 52) ^ False))):
            return_status = py_trees.common.Status.RUNNING
        elif ((-51 < self.blackboard.blVAR0) or (-41 > self.blackboard.blVAR0)):
            return_status = py_trees.common.Status.FAILURE
        elif False:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
