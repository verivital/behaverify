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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)


        def localDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE6: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, abs(-42)))
                    if False else
                    (
                    min(-2, max(-5, self.blackboard.blDEFINE5(1)))
                ))
            elif index == 1:
                return (
                    min(-2, max(-5, abs(-42)))
                    if False else
                    (
                    min(-2, max(-5, self.blackboard.blDEFINE5(1)))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE6: ' + str(index))

        self.localDEFINE6 = localDEFINE6


        def localDEFINE4():
            return (
                'yes'
                if True else
                (
                'yes'
            ))

        self.localDEFINE4 = localDEFINE4

    def update(self):
        return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.environment.delay_this_action(self.environment.a4_write_after_0__0, self)
        return return_status
