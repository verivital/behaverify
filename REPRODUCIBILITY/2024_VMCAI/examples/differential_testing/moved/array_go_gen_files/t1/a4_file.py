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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)


        def localDEFINE6():
            return (
                (27 == self.blackboard.blVAR0[0])
                if (self.blackboard.blDEFINE7() and True) else
                (
                (self.blackboard.blDEFINE7() and (False ^ self.blackboard.blDEFINE7()))
            ))

        self.localDEFINE6 = localDEFINE6

    def update(self):
        if self.environment.a4_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a4_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        if False:
            return_status = py_trees.common.Status.FAILURE
        elif (-(-98) > -68):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
