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
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)


        def localDEFINE5(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE5: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE5: ' + str(index))
            if index == 0:
                return (
                    min(5, max(2, -13))
                    if (-48 > -20) else
                    (
                    min(5, max(2, min((min(-97, 68) - 39), max(self.blackboard.blVAR0, self.blackboard.blVAR0))))
                ))
            elif index == 1:
                return (
                    min(5, max(2, -13))
                    if (-48 > -20) else
                    (
                    min(5, max(2, min((min(-97, 68) - 39), max(self.blackboard.blVAR0, self.blackboard.blVAR0))))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE5: ' + str(index))

        self.localDEFINE5 = localDEFINE5

    def update(self):
        if (self.localDEFINE5(0) <= 100):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
