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
        self.blackboard.register_key(key = ('blFROZENVAR6'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)
        self.localFROZENVAR5 = serene_safe_assignment.localFROZENVAR5((
            'both'
            if (((not (False)) or (self.blackboard.blVAR0)) or (-89 > -(-4))) else
            (
                'yes'
                if ('no' != self.blackboard.blFROZENVAR6[1]) else
                (
                self.blackboard.blFROZENVAR6[2]
        ))))


        def localDEFINE10():
            return (
                min(-2, max(-5, (-1 - 4)))
                if (abs(36) <= min(93, 6)) else
                (
                    min(-2, max(-5, abs(-5)))
                    if (self.blackboard.blVAR0 == False) else
                    (
                    min(-2, max(-5, min(5, -3)))
            )))

        self.localDEFINE10 = localDEFINE10

    def update(self):
        if True:
            return_status = py_trees.common.Status.FAILURE
        elif False:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.a1_write_after_0__0(self)
        return return_status
