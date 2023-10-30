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
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = [min((-2), max((-5), self.blackboard.blDEFINE5())) for _ in range(3)]
        __temp_var__ = serene_safe_assignment.localVAR2([(max(0, min(2, (min(50, max((-50), (16 * 16 * 16)))))), (
                    min((-2), max((-5), (-41)))
                    if (not ((True ^ True))) else
                    (
                    min((-2), max((-5), (min(50, max((-50), -(self.blackboard.blDEFINE6(max(0, min(2, (-3))))))))))
                ))), (max(0, min(2, (min(50, max((-50), (16 * 16 * 16)))))), (
                    min((-2), max((-5), (-41)))
                    if (not ((True ^ True))) else
                    (
                    min((-2), max((-5), (min(50, max((-50), -(self.blackboard.blDEFINE6(max(0, min(2, (-3))))))))))
                ))), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min((-4), (-5))))) * (min(50, max((-50), min((-4), (-5))))) * ([((not self.blackboard.blVAR0) or False), (not ((False ^ False)))].count(True)) * 3)))))), (
                    min((-2), max((-5), (min(50, max((-50), (34 - 34))))))
                    if (self.blackboard.blVAR0 or False) else
                    (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                        if self.blackboard.blVAR0 else
                        (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                )))), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min((-4), (-5))))) * (min(50, max((-50), min((-4), (-5))))) * ([((not self.blackboard.blVAR0) or False), (not ((False ^ False)))].count(True)) * 3)))))), (
                    min((-2), max((-5), (min(50, max((-50), (34 - 34))))))
                    if (self.blackboard.blVAR0 or False) else
                    (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                        if self.blackboard.blVAR0 else
                        (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                )))), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min((-4), (-5))))) * (min(50, max((-50), min((-4), (-5))))) * ([((not self.blackboard.blVAR0) or False), (not ((False ^ False)))].count(True)) * 3)))))), (
                    min((-2), max((-5), (min(50, max((-50), (34 - 34))))))
                    if (self.blackboard.blVAR0 or False) else
                    (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                        if self.blackboard.blVAR0 else
                        (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                )))), (max(0, min(2, (min(50, max((-50), ((min(50, max((-50), min((-4), (-5))))) * (min(50, max((-50), min((-4), (-5))))) * ([((not self.blackboard.blVAR0) or False), (not ((False ^ False)))].count(True)) * 3)))))), (
                    min((-2), max((-5), (min(50, max((-50), (34 - 34))))))
                    if (self.blackboard.blVAR0 or False) else
                    (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                        if self.blackboard.blVAR0 else
                        (
                        min((-2), max((-5), self.blackboard.blDEFINE5()))
                ))))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val

    def update(self):
        if True:
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        if self.environment.a3_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.localVAR2(self.environment.a3_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.localVAR2[index] = val
        return return_status
