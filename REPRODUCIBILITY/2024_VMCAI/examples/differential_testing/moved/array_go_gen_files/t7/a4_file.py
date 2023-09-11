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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)
        self.localFROZENVAR4 = serene_safe_assignment.localFROZENVAR4((
            min(5, max(2, -12))
            if (self.blackboard.blDEFINE5(1) or (False and self.blackboard.blDEFINE7(0))) else
            (
                min(5, max(2, (-5 - -59)))
                if (False ^ False) else
                (
                min(5, max(2, (max(-91, -93) + self.blackboard.blVAR0[0] + 8)))
        ))))


        def localDEFINE8():
            return (
                min(5, max(2, min(min(self.blackboard.blVAR0[1], self.blackboard.blVAR0[0]), 72)))
                if ((True ^ self.blackboard.blDEFINE7(0)) or False) else
                (
                min(5, max(2, abs(-72)))
            ))

        self.localDEFINE8 = localDEFINE8

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, abs(max(self.blackboard.blVAR0[2], self.localDEFINE8())))), min(-2, max(-5, ([((self.blackboard.blVAR0[2] + self.localDEFINE8() + 41) >= ([(True ^ False), (self.blackboard.blDEFINE7(0) == True), (self.blackboard.blDEFINE7(1) == False)].count(True))), ((not ((True == False))) or (self.blackboard.blDEFINE7(0))), ((-(-26) > self.localFROZENVAR4) ^ (self.localDEFINE8() >= 99)), (self.localDEFINE8() <= ((self.localDEFINE8() * 39) - -75))].count(True)))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        self.environment.delay_this_action(self.environment.a4_write_before_0__0, self)
        self.environment.a4_write_before_0__1(self)
        if (not ((self.blackboard.blDEFINE7(1) ^ self.blackboard.blDEFINE5(1)))):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        return return_status
