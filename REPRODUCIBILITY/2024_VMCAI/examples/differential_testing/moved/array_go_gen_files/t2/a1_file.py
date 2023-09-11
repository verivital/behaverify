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
                return (
                    'no'
                    if (self.blackboard.blVAR3 > -24) else
                    (
                        'no'
                        if (((not (False)) or (True)) or (self.blackboard.blDEFINE8(0) > (-56 + -77 + 25 + self.blackboard.blVAR3))) else
                        (
                        self.blackboard.blVAR0[0]
                )))
            elif index == 1:
                return (
                    'yes'
                    if (self.blackboard.blDEFINE8(0) == self.blackboard.blFROZENVAR5[2]) else
                    (
                        'both'
                        if ((False or (self.blackboard.blFROZENVAR5[2] == -94)) and (False ^ self.blackboard.blVAR2)) else
                        (
                        'yes'
                )))
            raise Exception('Reached unreachable state when accessing localDEFINE7: ' + str(index))

        self.localDEFINE7 = localDEFINE7

    def update(self):
        self.blackboard.blVAR2 = serene_safe_assignment.blVAR2((self.blackboard.blFROZENVAR5[0] >= self.blackboard.blFROZENVAR5[1]))
        if ((True or True) and (-94 >= self.blackboard.blVAR3)):
            return_status = py_trees.common.Status.RUNNING
        elif (True == False):
            return_status = py_trees.common.Status.RUNNING
        elif (self.blackboard.blDEFINE8(1) != min(self.blackboard.blVAR3, -83)):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, -(self.blackboard.blVAR3))), (
            'both'
            if (self.blackboard.blVAR0[1] != self.blackboard.blVAR0[0]) else
            (
                'no'
                if self.blackboard.blVAR2 else
                (
                self.localDEFINE7(1)
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return return_status
