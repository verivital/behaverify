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
        self.blackboard.register_key(key = ('blFROZENVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2('both')


        def localDEFINE5():
            return (
                min(-2, max(-5, (min(self.blackboard.blFROZENVAR3, self.blackboard.blVAR0) - self.blackboard.blVAR0)))
                if (-52 >= 63) else
                (
                min(-2, max(-5, 14))
            ))

        self.localDEFINE5 = localDEFINE5

    def update(self):
        if self.environment.a4_read_before_1__condition(self):
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a4_read_before_1__0(self))
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a4_read_before_1__1(self))
        self.localVAR2 = serene_safe_assignment.localVAR2('no')
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.a4_write_after_0__0(self)
        return return_status
