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
        self.localVAR2 = serene_safe_assignment.localVAR2((
            min(5, max(2, (82 * self.blackboard.blVAR0[1] * self.blackboard.blVAR0[0])))
            if ((abs(47) - abs(self.blackboard.blVAR0[0])) != (self.blackboard.blVAR0[1] + self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0] + self.blackboard.blVAR0[1])) else
            (
            min(5, max(2, 10))
        )))


        def localDEFINE4(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE4: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE4: ' + str(index))
            if index == 0:
                return (
                    'yes'
                    if (True or False) else
                    (
                        'yes'
                        if True else
                        (
                        'yes'
                )))
            elif index == 1:
                return (
                    'both'
                    if True else
                    (
                        'yes'
                        if True else
                        (
                        'both'
                )))
            elif index == 2:
                return (
                    'yes'
                    if True else
                    (
                        'both'
                        if False else
                        (
                        'no'
                )))
            raise Exception('Reached unreachable state when accessing localDEFINE4: ' + str(index))

        self.localDEFINE4 = localDEFINE4

    def update(self):
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
