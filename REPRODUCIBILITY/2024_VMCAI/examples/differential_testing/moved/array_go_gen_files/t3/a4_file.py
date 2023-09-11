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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.localVAR4 = serene_safe_assignment.localVAR4((
            (self.blackboard.blVAR0[0] > -50)
            if ('yes' != 'both') else
            (
                ((max(self.blackboard.blVAR0[1], self.blackboard.blVAR0[1]) * (-9 * self.blackboard.blVAR0[0] * 36) * -(-4) * self.blackboard.blVAR0[1]) >= -28)
                if ((-2 >= 12) or (-80 < 37)) else
                (
                (-51 > -(self.blackboard.blVAR0[1]))
        ))))

    def update(self):
        self.environment.a4_write_before_2__0(self)
        self.environment.delay_this_action(self.environment.a4_write_before_1__0, self)
        self.environment.a4_write_before_0__0(self)
        if (self.blackboard.blVAR0[1] < self.blackboard.blVAR0[2]):
            return_status = py_trees.common.Status.RUNNING
        elif self.localVAR4:
            return_status = py_trees.common.Status.RUNNING
        elif (self.blackboard.blVAR3 or False):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a4_read_after_0__condition(self):
            self.blackboard.blVAR3 = serene_safe_assignment.blVAR3(self.environment.a4_read_after_0__0(self))
        return return_status
