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
        self.blackboard.register_key(key = ('blFROZENVAR6'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2((
            'no'
            if (True == (-46 <= 4)) else
            (
            'yes'
        )))


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


        def localDEFINE7(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE7: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE7: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, (([(87 >= 98), (-28 < 3), (4 > -2), (not ((True ^ self.blackboard.blVAR0)))].count(True)) - ([(2 <= -3), (True != True), (20 < -3), (-90 <= -2)].count(True)))))
                    if (([(True ^ True), (False and self.blackboard.blVAR0), (self.blackboard.blVAR0 and self.blackboard.blVAR0)].count(True)) > (82 - -43)) else
                    (
                    min(-2, max(-5, ([(-2 > (-3 * -62)), (([(False != self.blackboard.blVAR0), (-21 < 61)].count(True)) < min(14, 5)), (2 >= (96 * 1))].count(True))))
                ))
            elif index == 1:
                return (
                    min(-2, max(-5, min(-62, (31 - abs(5)))))
                    if ((78 < 80) or self.blackboard.blVAR0) else
                    (
                    min(-2, max(-5, (48 * abs(max(-40, 69)) * ([(self.blackboard.blDEFINE8() != self.blackboard.blFROZENVAR6[1]), (not ((True ^ self.blackboard.blVAR0)))].count(True)))))
                ))
            elif index == 2:
                return (
                    min(-2, max(-5, -(-3)))
                    if (min(abs(73), 67) <= 72) else
                    (
                    min(-2, max(-5, abs(abs(-5))))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE7: ' + str(index))

        self.localDEFINE7 = localDEFINE7

    def update(self):
        if ((not (False)) or ((False or self.blackboard.blVAR0))):
            return_status = py_trees.common.Status.FAILURE
        elif (self.blackboard.blFROZENVAR6[0] != self.localVAR2):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        if self.environment.a2_read_after_0__condition(self):
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a2_read_after_0__0(self))
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a2_read_after_0__1(self))
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a2_read_after_0__2(self))
            self.localVAR2 = serene_safe_assignment.localVAR2(self.environment.a2_read_after_0__3(self))
        return return_status
