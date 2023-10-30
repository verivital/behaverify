import py_trees
import math
import operator
import random
import serene_safe_assignment


class a1(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(a1, self).__init__(name)
        self.__serene_print__ = 'INVALID'
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.a1_read_before_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a1_read_before_0__0(self))
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a1_read_before_0__1(self))
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a1_read_before_0__2(self))
        if ((min(50, max((-50), (self.blackboard.blDEFINE8() - self.blackboard.blDEFINE8())))) >= (min(50, max((-50), (self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5()))))):
            return_status = py_trees.common.Status.RUNNING
        elif ((min(50, max((-50), abs(self.blackboard.blDEFINE5())))) >= self.blackboard.blDEFINE5()):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
