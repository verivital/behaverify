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
        self.blackboard.register_key(key = ('blVAR2'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)

    def update(self):
        __temp_var__ = serene_safe_assignment.blVAR3([(0, (
                    (((-39) > (min(50, max((-50), abs((-2)))))) and False)
                    if ((False != True) != ((-38) > 5)) else
                    (
                    ((min(50, max((-50), ((min(50, max((-50), max(4, 4)))) * (min(50, max((-50), max(4, 4)))))))) < (min(50, max((-50), ((-24) - (min(50, max((-50), (18 + 18 + 18 + 18)))))))))
                ))), (1, (
                    (((-39) > (min(50, max((-50), abs((-2)))))) and False)
                    if ((False != True) != ((-38) > 5)) else
                    (
                    ((min(50, max((-50), ((min(50, max((-50), max(4, 4)))) * (min(50, max((-50), max(4, 4)))))))) < (min(50, max((-50), ((-24) - (min(50, max((-50), (18 + 18 + 18 + 18)))))))))
                )))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR3[index] = val
        __temp_var__ = serene_safe_assignment.blVAR2([(0, (
                    'yes'
                    if (True == ((-5) <= (-30))) else
                    (
                        'yes'
                        if ((not ('yes' == self.blackboard.blVAR2[serene_safe_assignment.index_func(max(0, min(1, (-13))), 2)])) or (True and self.blackboard.blVAR0)) else
                        (
                        self.blackboard.blDEFINE5()
                )))), (1, (
                    'yes'
                    if (True == ((-5) <= (-30))) else
                    (
                        'yes'
                        if ((not ('yes' == self.blackboard.blVAR2[serene_safe_assignment.index_func(max(0, min(1, (-13))), 2)])) or (True and self.blackboard.blVAR0)) else
                        (
                        self.blackboard.blDEFINE5()
                ))))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR2[index] = val
        __temp_var__ = serene_safe_assignment.blVAR3([(max(0, min(1, ((-3) if (True == False) else 2))), (((-30) < 46) and True))])
        for (index, val) in __temp_var__:
            self.blackboard.blVAR3[index] = val
        if ((not self.blackboard.blVAR0) or ((-2) >= (-44))):
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        self.__serene_print__ = return_status.value
        print('A2------> ' + str(self.blackboard.blVAR2))
        return return_status
