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
        self.blackboard.register_key(key = ('blFROZENVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)


        def localDEFINE5():
            return (
                min(-2, max(-5, self.blackboard.blVAR0))
                if (([(not ((False ^ False))), (self.blackboard.blVAR0 >= 39), (not ((True ^ False)))].count(True)) < -(self.blackboard.blFROZENVAR3)) else
                (
                    min(-2, max(-5, -79))
                    if (self.blackboard.blDEFINE4(0) > (self.blackboard.blVAR0 + self.blackboard.blFROZENVAR3 + 100 + self.blackboard.blVAR0)) else
                    (
                    min(-2, max(-5, -(74)))
            )))

        self.localDEFINE5 = localDEFINE5

    def update(self):
        self.environment.delay_this_action(self.environment.a1_write_before_0__0, self)
        if (True ^ True):
            return_status = py_trees.common.Status.RUNNING
        elif True:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        if self.environment.a1_read_after_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a1_read_after_0__0(self))
        return return_status
