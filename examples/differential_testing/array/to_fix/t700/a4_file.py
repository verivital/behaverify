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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR0([(0, (
                    min(5, max(2, (-12)))
                    if ((True or True) == (False and False)) else
                    (
                        min(5, max(2, (min(50, max((-50), (self.blackboard.blDEFINE7() - self.blackboard.blDEFINE7()))))))
                        if ((True ^ False) and (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, self.blackboard.blDEFINE7())), 3)] <= (-46))) else
                        (
                        min(5, max(2, ([(self.blackboard.blDEFINE7() < self.blackboard.blDEFINE7()), (False and False), ('both' != 'yes'), ((-50) <= (-6))].count(True))))
                )))), (1, (
                    min(5, max(2, (-12)))
                    if ((True or True) == (False and False)) else
                    (
                        min(5, max(2, (min(50, max((-50), (self.blackboard.blDEFINE7() - self.blackboard.blDEFINE7()))))))
                        if ((True ^ False) and (self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, self.blackboard.blDEFINE7())), 3)] <= (-46))) else
                        (
                        min(5, max(2, ([(self.blackboard.blDEFINE7() < self.blackboard.blDEFINE7()), (False and False), ('both' != 'yes'), ((-50) <= (-6))].count(True))))
                ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        self.environment.delay_this_action(self.environment.a4_write_before_0__0, self)
        if (self.blackboard.blVAR3 > self.blackboard.blDEFINE7()):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
