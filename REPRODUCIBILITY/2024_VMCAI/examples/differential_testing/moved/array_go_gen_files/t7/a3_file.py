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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)
        self.localFROZENVAR4 = serene_safe_assignment.localFROZENVAR4(min(5, max(2, max(81, (-71 + self.blackboard.blVAR0[2])))))

    def update(self):
        self.environment.delay_this_action(self.environment.a3_write_before_0__0, self)
        self.environment.delay_this_action(self.environment.a3_write_before_0__1, self)
        if (self.localFROZENVAR4 >= self.blackboard.blVAR0[1]):
            return_status = py_trees.common.Status.RUNNING
        elif (-41 > self.blackboard.blVAR0[0]):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
