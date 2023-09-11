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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)


        def localDEFINE10():
            return (
                (self.blackboard.blDEFINE7(2) ^ False)
                if (37 >= abs(-23)) else
                (
                    (self.blackboard.blVAR0 > self.blackboard.blVAR0)
                    if ('no' != 'both') else
                    (
                    (False == (self.blackboard.blDEFINE7(1) == False))
            )))

        self.localDEFINE10 = localDEFINE10
        self.localVAR4 = serene_safe_assignment.localVAR4((self.blackboard.blVAR3 <= (self.blackboard.blVAR0 * self.blackboard.blVAR0 * -88 * 59)))


        def localDEFINE8():
            return (
                min(5, max(2, min(self.blackboard.blVAR0, self.blackboard.blVAR3)))
                if False else
                (
                    min(5, max(2, ((-(self.blackboard.blVAR0) + (self.blackboard.blVAR3 * self.blackboard.blVAR0)) + -89 + 57 + abs(self.blackboard.blVAR3))))
                    if self.blackboard.blDEFINE7(1) else
                    (
                    min(5, max(2, min(15, 79)))
            )))

        self.localDEFINE8 = localDEFINE8

    def update(self):
        if ((not ((False or self.localVAR4))) or (self.localVAR4)):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
