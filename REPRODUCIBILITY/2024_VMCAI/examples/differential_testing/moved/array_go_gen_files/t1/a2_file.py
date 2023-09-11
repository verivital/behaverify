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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)


        def localDEFINE5():
            return (
                min(5, max(2, (min(-17, -47) * ([(True or True), (False or True)].count(True)) * (self.blackboard.blVAR0[0] - self.blackboard.blVAR0[1]))))
                if (abs(-6) != -(-30)) else
                (
                min(5, max(2, (([(True or (self.blackboard.blVAR0[1] >= self.blackboard.blVAR0[0])), ((not (False)) or (False)), (((not (False)) or (False)) or True), ((-93 + -35 + self.blackboard.blVAR0[0] + self.blackboard.blVAR0[0]) < self.blackboard.blVAR0[0])].count(True)) * ([((not (False)) or ((False == False))), (-81 <= (self.blackboard.blVAR0[0] - self.blackboard.blVAR0[1]))].count(True)) * max(self.blackboard.blVAR0[1], self.blackboard.blVAR0[0]) * min(46, 68))))
            ))

        self.localDEFINE5 = localDEFINE5

    def update(self):
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, max(abs(self.blackboard.blVAR0[0]), 62))), min(-2, max(-5, -72)))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        __temp_var__ = serene_safe_assignment.blVAR0([(min(1, max(0, ([(((not (self.blackboard.blDEFINE7())) or (False)) ^ self.blackboard.blDEFINE7()), ((self.blackboard.blDEFINE7() or (self.blackboard.blDEFINE7() ^ self.blackboard.blDEFINE7())) and True), ((not (self.blackboard.blDEFINE7())) or (self.blackboard.blDEFINE7()))].count(True)))), (
            min(-2, max(-5, 85))
            if ((15 + self.blackboard.blVAR0[0] + self.blackboard.blVAR0[0]) <= self.blackboard.blVAR0[1]) else
            (
                min(-2, max(-5, -(min(2, self.localDEFINE5()))))
                if (self.blackboard.blDEFINE7() or True) else
                (
                min(-2, max(-5, (([(5 < self.blackboard.blVAR0[1]), (self.blackboard.blDEFINE7() or self.blackboard.blDEFINE7()), (False or True)].count(True)) + (-(-86) + self.localDEFINE5() + 93))))
        )))), (min(1, max(0, (self.blackboard.blVAR0[1] * min(-51, self.blackboard.blVAR0[0])))), (
            min(-2, max(-5, max(-1, ((59 + self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0]) * -52))))
            if (self.blackboard.blDEFINE7() == self.blackboard.blDEFINE7()) else
            (
                min(-2, max(-5, -75))
                if (-30 >= self.localDEFINE5()) else
                (
                min(-2, max(-5, -(-77)))
        ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return return_status
