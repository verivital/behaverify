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
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)
        self.localVAR4 = serene_safe_assignment.localVAR4((
            (True and (self.blackboard.blVAR0 >= self.blackboard.blVAR3))
            if False else
            (
                (6 >= self.blackboard.blVAR3)
                if (self.blackboard.blVAR0 > self.blackboard.blVAR0) else
                (
                True
        ))))


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

    def update(self):
        return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        self.localVAR4 = serene_safe_assignment.localVAR4((
            ((not (False)) or ((23 > -59)))
            if ((-44 != -6) and (False or True)) else
            (
            (self.blackboard.blVAR0 != ((self.blackboard.blVAR0 + 8 + 13 + self.blackboard.blVAR3) - -53))
        )))
        self.blackboard.blVAR0 = serene_safe_assignment.blVAR0(min(5, max(2, 71)))
        return return_status
