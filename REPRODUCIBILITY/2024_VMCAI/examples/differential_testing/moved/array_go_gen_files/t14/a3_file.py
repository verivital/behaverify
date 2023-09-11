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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)


        def localDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing localDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing localDEFINE6: ' + str(index))
            if index == 0:
                return (
                    self.blackboard.blVAR0[0]
                    if True else
                    (
                        (False and True)
                        if (max((self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5()), abs(self.blackboard.blDEFINE5())) < 3) else
                        (
                        ((57 + -(82)) <= (self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5()))
                )))
            elif index == 1:
                return (
                    self.blackboard.blVAR0[0]
                    if True else
                    (
                        (False and True)
                        if (max((self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5()), abs(self.blackboard.blDEFINE5())) < 3) else
                        (
                        ((57 + -(82)) <= (self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5()))
                )))
            elif index == 2:
                return (
                    self.blackboard.blVAR0[0]
                    if True else
                    (
                        (False and True)
                        if (max((self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5()), abs(self.blackboard.blDEFINE5())) < 3) else
                        (
                        ((57 + -(82)) <= (self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5()))
                )))
            raise Exception('Reached unreachable state when accessing localDEFINE6: ' + str(index))

        self.localDEFINE6 = localDEFINE6
        self.localFROZENVAR4 = serene_safe_assignment.localFROZENVAR4((96 == self.blackboard.blDEFINE5()))

    def update(self):
        if (self.localFROZENVAR4 or False):
            return_status = py_trees.common.Status.FAILURE
        elif (abs(-76) >= min((self.blackboard.blDEFINE5() + -48), (self.blackboard.blDEFINE5() - 60))):
            return_status = py_trees.common.Status.FAILURE
        elif (self.localFROZENVAR4 or self.localDEFINE6(2)):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, ([(99 >= -59), ((not (False)) or (('no' == 'yes'))), (True and (self.blackboard.blDEFINE5() > 50))].count(True)))), (
            (self.localDEFINE6(1) == True)
            if (False and False) else
            (
            ((not ((False != False))) or (True))
        )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        self.environment.delay_this_action(self.environment.a3_write_after_0__0, self)
        return return_status
