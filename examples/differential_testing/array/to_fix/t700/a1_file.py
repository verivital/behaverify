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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2(min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), abs(self.blackboard.blVAR3)))) * (min(50, max((-50), (self.blackboard.blVAR3 - self.blackboard.blVAR3)))) * self.blackboard.blVAR3)))))))

    def update(self):
        self.localVAR2 = serene_safe_assignment.localVAR2((
            min((-2), max((-5), (min(50, max((-50), abs((min(50, max((-50), min(self.blackboard.blDEFINE7(), self.blackboard.blDEFINE7()))))))))))
            if ((min(50, max((-50), abs(self.blackboard.blDEFINE7())))) > (min(50, max((-50), min(self.blackboard.blVAR3, self.blackboard.blVAR3))))) else
            (
            min((-2), max((-5), self.blackboard.blDEFINE5(max(0, min(1, self.blackboard.blDEFINE7())))))
        )))
        self.localVAR2 = serene_safe_assignment.localVAR2(min((-2), max((-5), ([('both' != 'yes'), ('both' == 'yes')].count(True)))))
        if (False ^ True):
            return_status = py_trees.common.Status.FAILURE
        elif (False != True):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        if self.environment.a1_read_after_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a1_read_after_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        return return_status
