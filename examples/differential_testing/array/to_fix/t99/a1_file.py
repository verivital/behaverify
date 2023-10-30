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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.environment.a1_write_before_1__0(self)
        self.environment.a1_write_before_0__0(self)
        if (False ^ (5 > (-9))):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR2([(0, (
                    self.blackboard.blDEFINE5()
                    if ((-5) < 2) else
                    (
                        self.blackboard.blDEFINE5()
                        if ((min(50, max((-50), ((-4) - 28)))) <= 4) else
                        (
                        self.blackboard.blDEFINE5()
                )))), (1, (
                    self.blackboard.blDEFINE5()
                    if ((-5) < 2) else
                    (
                        self.blackboard.blDEFINE5()
                        if ((min(50, max((-50), ((-4) - 28)))) <= 4) else
                        (
                        self.blackboard.blDEFINE5()
                ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR2[index] = val
        print('A1----> ' + str(self.blackboard.blVAR2))
        return return_status
