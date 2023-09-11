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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.blVAR2 = serene_safe_assignment.blVAR2((
            min(-2, max(-5, min(100, max(-100, (-42 + min(100, max(-100, -(self.blackboard.blDEFINE4()))) + min(100, max(-100, (-11 + self.blackboard.blVAR0[0]))))))))
            if (min(100, max(-100, (self.blackboard.blVAR0[1] + self.blackboard.blVAR2 + 87))) <= -28) else
            (
                min(-2, max(-5, min(100, max(-100, min(min(100, max(-100, max(-68, 95))), self.blackboard.blDEFINE4())))))
                if True else
                (
                min(-2, max(-5, 35))
        ))))
        if self.environment.a2_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
            self.blackboard.blVAR2 = serene_safe_assignment.blVAR2(self.environment.a2_read_before_0__1(self))
        if True:
            return_status = py_trees.common.Status.RUNNING
        elif False:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
