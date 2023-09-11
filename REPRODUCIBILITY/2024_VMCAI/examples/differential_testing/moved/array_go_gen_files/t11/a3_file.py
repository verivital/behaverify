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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)


        def localDEFINE3(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE3: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE3: ' + str(index))
            if index == 0:
                return (
                    min(5, max(2, max(self.blackboard.blVAR0, self.blackboard.blVAR0)))
                    if (self.blackboard.blVAR0 < self.blackboard.blVAR0) else
                    (
                    min(5, max(2, (-66 + -68 + abs(self.blackboard.blVAR0) + 17)))
                ))
            elif index == 1:
                return (
                    min(5, max(2, max(self.blackboard.blVAR0, self.blackboard.blVAR0)))
                    if (self.blackboard.blVAR0 < self.blackboard.blVAR0) else
                    (
                    min(5, max(2, (-66 + -68 + abs(self.blackboard.blVAR0) + 17)))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE3: ' + str(index))

        self.localDEFINE3 = localDEFINE3

    def update(self):
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0((
            min(-2, max(-5, (abs(min(-62, -61)) * abs((73 + self.localDEFINE3(0) + 37 + 92)))))
            if (abs(self.blackboard.blVAR0) < 51) else
            (
            min(-2, max(-5, min(-(self.localDEFINE3(0)), ((19 - self.blackboard.blVAR0) + self.blackboard.blDEFINE4() + (self.localDEFINE3(0) + self.localDEFINE3(0) + self.blackboard.blVAR0 + -100)))))
        )))
        self.environment.a3_write_before_0__0(self)
        if False:
            return_status = py_trees.common.Status.SUCCESS
        elif (((self.localDEFINE3(0) + 79) >= (-26 - self.blackboard.blVAR0)) == (self.blackboard.blVAR2 != True)):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
