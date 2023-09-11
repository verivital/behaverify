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
        self.blackboard.register_key(key = ('blFROZENVAR6'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2((
            'no'
            if (True == (-46 <= 4)) else
            (
            'yes'
        )))


        def localDEFINE7(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE7: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE7: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, -2))
                    if ('yes' == 'yes') else
                    (
                        min(-2, max(-5, ([(5 <= 3), (self.blackboard.blVAR0 ^ False), (-5 > -42), (True or self.blackboard.blVAR0)].count(True))))
                        if (self.blackboard.blVAR0 and (-3 >= 83)) else
                        (
                        min(-2, max(-5, max(22, (-4 - -9))))
                )))
            elif index == 1:
                return (
                    min(-2, max(-5, -2))
                    if ('yes' == 'yes') else
                    (
                        min(-2, max(-5, ([(5 <= 3), (self.blackboard.blVAR0 ^ False), (-5 > -42), (True or self.blackboard.blVAR0)].count(True))))
                        if (self.blackboard.blVAR0 and (-3 >= 83)) else
                        (
                        min(-2, max(-5, max(22, (-4 - -9))))
                )))
            elif index == 2:
                return (
                    min(-2, max(-5, -2))
                    if ('yes' == 'yes') else
                    (
                        min(-2, max(-5, ([(5 <= 3), (self.blackboard.blVAR0 ^ False), (-5 > -42), (True or self.blackboard.blVAR0)].count(True))))
                        if (self.blackboard.blVAR0 and (-3 >= 83)) else
                        (
                        min(-2, max(-5, max(22, (-4 - -9))))
                )))
            raise Exception('Reached unreachable state when accessing localDEFINE7: ' + str(index))

        self.localDEFINE7 = localDEFINE7


        def localDEFINE10():
            return (
                min(-2, max(-5, min((-3 - -54), -5)))
                if (False and True) else
                (
                    min(-2, max(-5, (-2 * -31 * 4 * 69)))
                    if ((not (self.blackboard.blVAR0)) or (False)) else
                    (
                    min(-2, max(-5, (-2 + max(46, 39) + ([(self.blackboard.blVAR0 and self.blackboard.blVAR0), ((not (True)) or (False)), (self.blackboard.blVAR0 == self.blackboard.blVAR0), (not ((True ^ self.blackboard.blVAR0)))].count(True)) + abs(99))))
            )))

        self.localDEFINE10 = localDEFINE10

    def update(self):
        if (-81 > (-79 - -48)):
            return_status = py_trees.common.Status.SUCCESS
        elif (self.blackboard.blVAR0 and False):
            return_status = py_trees.common.Status.SUCCESS
        elif ((not ((self.localDEFINE7(0) > 4))) or ((not ((True ^ self.blackboard.blVAR0))))):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a3_read_after_0__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a3_read_after_0__0(self))
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a3_read_after_0__1(self))
        return return_status
