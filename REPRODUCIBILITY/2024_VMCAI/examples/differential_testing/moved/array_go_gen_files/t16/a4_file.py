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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)


        def localDEFINE8():
            return (
                min(5, max(2, abs(min(-(-91), ([(self.blackboard.blDEFINE7(0) or self.blackboard.blDEFINE7(1)), (-12 <= self.blackboard.blVAR0)].count(True))))))
                if ((False ^ (not ((True ^ self.blackboard.blDEFINE7(2))))) or (16 >= self.blackboard.blVAR3)) else
                (
                    min(5, max(2, (-15 * max(max(self.blackboard.blVAR3, 26), -(25)))))
                    if (self.blackboard.blDEFINE7(1) or (True ^ True)) else
                    (
                    min(5, max(2, (-(self.blackboard.blVAR0) * self.blackboard.blVAR3)))
            )))

        self.localDEFINE8 = localDEFINE8


        def localDEFINE9(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE9: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE9: ' + str(index))
            if index == 0:
                return (
                    min(5, max(2, (0 - self.blackboard.blVAR3)))
                    if ((-38 <= self.blackboard.blVAR0) == False) else
                    (
                    min(5, max(2, self.blackboard.blVAR3))
                ))
            elif index == 1:
                return (
                    min(5, max(2, max(-(self.blackboard.blVAR3), (self.blackboard.blVAR3 + 37 + 4 + self.blackboard.blVAR3))))
                    if ((not (False)) or (self.blackboard.blDEFINE7(2))) else
                    (
                    min(5, max(2, ([(self.blackboard.blDEFINE7(0) ^ True), (False ^ False)].count(True))))
                ))
            elif index == 2:
                return (
                    min(5, max(2, self.blackboard.blVAR0))
                    if (-2 == -23) else
                    (
                    min(5, max(2, ([(self.blackboard.blVAR3 >= ([(-83 >= self.blackboard.blVAR3), (-90 < max(self.blackboard.blVAR3, -51)), (self.blackboard.blVAR0 <= (self.blackboard.blVAR0 * -68 * 57 * self.blackboard.blVAR0)), (not ((True ^ (self.blackboard.blVAR3 > -92))))].count(True))), (71 <= min(-94, -75))].count(True))))
                ))
            raise Exception('Reached unreachable state when accessing localDEFINE9: ' + str(index))

        self.localDEFINE9 = localDEFINE9

    def update(self):
        if self.environment.a4_read_before_1__condition(self):
            self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(self.environment.a4_read_before_1__0(self))
        if self.environment.a4_read_before_0__condition(self):
            self.blackboard.blVAR3 = serene_safe_assignment.blVAR3(self.environment.a4_read_before_0__0(self))
        if (abs(56) > min(-30, self.localDEFINE8())):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.blackboard.blVAR3 = serene_safe_assignment.blVAR3((
            min(5, max(2, -(-91)))
            if (True ^ False) else
            (
                min(5, max(2, -(-70)))
                if ((self.blackboard.blVAR3 * 8) > (self.blackboard.blVAR0 + -67 + abs(-44))) else
                (
                min(5, max(2, ([(self.blackboard.blDEFINE7(0) ^ False), ((not ((self.blackboard.blDEFINE7(2) ^ self.blackboard.blDEFINE7(0)))) ^ self.blackboard.blDEFINE7(0)), (((39 - 70) >= min(-36, 35)) and (35 <= (-22 + self.blackboard.blVAR3)))].count(True))))
        ))))
        self.environment.a4_write_after_0__0(self)
        return return_status
