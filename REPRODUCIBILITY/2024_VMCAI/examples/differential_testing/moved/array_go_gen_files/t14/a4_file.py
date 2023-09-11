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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)


        def localDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE6: ' + str(index))
            if index == 0:
                return (38 > min(-75, self.blackboard.blDEFINE5()))
            elif index == 1:
                return (self.blackboard.blVAR0[1] or True)
            elif index == 2:
                return ('both' != 'both')
            raise Exception('Reached unreachable state when accessing localDEFINE6: ' + str(index))

        self.localDEFINE6 = localDEFINE6

    def update(self):
        if (not ((('both' == 'no') ^ (self.blackboard.blDEFINE5() <= self.blackboard.blDEFINE5())))):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, min(min(self.blackboard.blDEFINE5(), self.blackboard.blDEFINE5()), 48))), (
            (self.blackboard.blDEFINE5() >= self.blackboard.blDEFINE5())
            if (True ^ self.localDEFINE6(2)) else
            (
            (False != True)
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return return_status
