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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blFROZENVAR5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)


        def localDEFINE7(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE7: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing localDEFINE7: ' + str(index))
            if index == 0:
                return self.blackboard.blVAR0[0]
            elif index == 1:
                return (
                    'no'
                    if (-18 >= self.blackboard.blVAR3) else
                    (
                    'both'
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE7: ' + str(index))

        self.localDEFINE7 = localDEFINE7

    def update(self):
        if ((False == False) and (self.blackboard.blVAR2 and True)):
            return_status = py_trees.common.Status.SUCCESS
        elif self.blackboard.blVAR2:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        self.blackboard.blVAR3 = serene_safe_assignment.blVAR3((
            min(5, max(2, max(self.blackboard.blVAR3, 10)))
            if True else
            (
            min(5, max(2, abs(self.blackboard.blFROZENVAR5[2])))
        )))
        if self.environment.a2_read_after_0__condition(self):
            self.blackboard.blVAR3 = serene_safe_assignment.blVAR3(self.environment.a2_read_after_0__0(self))
        return return_status
