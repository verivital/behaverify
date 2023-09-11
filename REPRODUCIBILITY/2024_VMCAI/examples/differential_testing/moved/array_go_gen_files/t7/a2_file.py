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
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)


        def localDEFINE8():
            return (
                min(5, max(2, abs(self.blackboard.blVAR0[1])))
                if (False == True) else
                (
                    min(5, max(2, (self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0] + 55 + -97)))
                    if self.blackboard.blDEFINE7(0) else
                    (
                    min(5, max(2, min(8, ([((not (False)) or (self.blackboard.blDEFINE7(0))), (self.blackboard.blDEFINE5(0) and True), (self.blackboard.blDEFINE5(1) or False)].count(True)))))
            )))

        self.localDEFINE8 = localDEFINE8

    def update(self):
        if self.environment.a2_read_before_0__condition(self):
            __temp_var__ = serene_safe_assignment.blVAR0(self.environment.a2_read_before_0__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.blVAR0[index] = val
        if (abs(94) >= 18):
            return_status = py_trees.common.Status.SUCCESS
        elif (abs(-67) < max(self.localDEFINE8(), 75)):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        __temp_var__ = serene_safe_assignment.blVAR0([(min(2, max(0, min(abs(32), -97))), min(-2, max(-5, -14))), (min(2, max(0, -29)), min(-2, max(-5, max(-2, self.localDEFINE8())))), (min(2, max(0, min((6 * min(2, self.localDEFINE8())), (69 * self.blackboard.blVAR0[2])))), min(-2, max(-5, (self.blackboard.blVAR0[1] + max(86, 33) + max(self.localDEFINE8(), -7) + max(self.blackboard.blVAR0[1], -33)))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR0[index] = val
        return return_status
