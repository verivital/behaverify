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
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0((
            min(5, max(2, ([(False == False), (not ((True ^ True))), (False and True)].count(True))))
            if True else
            (
            min(5, max(2, (-65 * self.blackboard.blVAR0 * -91)))
        )))
        if True:
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        if self.environment.a4_read_after_1__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a4_read_after_1__0(self))
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a4_read_after_1__1(self))
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(min(5, max(2, min(-10, min(-2, 89)))))
        return return_status
