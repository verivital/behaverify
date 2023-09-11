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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)


        def localDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE6: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, abs(max(-67, -61))))
                    if False else
                    (
                    min(-2, max(-5, (self.blackboard.blVAR0 - self.blackboard.blVAR0)))
                ))
            elif index == 1:
                return (
                    min(-2, max(-5, max(self.blackboard.blVAR0, ([('both' == 'yes'), (not ((True ^ False)))].count(True)))))
                    if False else
                    (
                    min(-2, max(-5, (([(True or True), (False and False), (98 >= -10), (False and True)].count(True)) - self.blackboard.blVAR0)))
                ))
            elif index == 2:
                return min(-2, max(-5, 79))
            raise Exception('Reached unreachable state when accessing localDEFINE6: ' + str(index))

        self.localDEFINE6 = localDEFINE6

    def update(self):
        if (-(self.blackboard.blVAR0) <= (52 + 20 + self.localDEFINE6(2) + -79)):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        return return_status
