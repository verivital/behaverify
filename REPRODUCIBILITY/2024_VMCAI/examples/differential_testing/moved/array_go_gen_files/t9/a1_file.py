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
        self.blackboard.register_key(key = ('blFROZENVAR4'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)


        def localDEFINE5(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE5: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE5: ' + str(index))
            if index == 0:
                return 'yes'
            elif index == 1:
                return self.blackboard.blVAR0
            elif index == 2:
                return self.blackboard.blVAR0
            raise Exception('Reached unreachable state when accessing localDEFINE5: ' + str(index))

        self.localDEFINE5 = localDEFINE5

    def update(self):
        self.environment.a1_write_before_0__0(self)
        if self.blackboard.blVAR3[0]:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a1_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR3(self.environment.a1_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR3[index] = val
        return return_status
