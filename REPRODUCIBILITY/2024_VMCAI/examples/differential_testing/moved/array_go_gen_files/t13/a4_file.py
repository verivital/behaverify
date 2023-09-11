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
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE6: ' + str(index))
            if index == 0:
                return min(-2, max(-5, min(40, self.blackboard.blVAR0)))
            elif index == 1:
                return min(-2, max(-5, -17))
            elif index == 2:
                return min(-2, max(-5, min(max(-96, self.blackboard.blVAR0), max(78, self.blackboard.blVAR0))))
            raise Exception('Reached unreachable state when accessing localDEFINE6: ' + str(index))

        self.localDEFINE6 = localDEFINE6

    def update(self):
        if (max(93, self.localDEFINE6(0)) <= self.localDEFINE6(2)):
            return_status = py_trees.common.Status.FAILURE
        elif False:
            return_status = py_trees.common.Status.RUNNING
        elif (False ^ False):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        if self.environment.a4_read_after_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a4_read_after_0__0(self))
        return return_status
