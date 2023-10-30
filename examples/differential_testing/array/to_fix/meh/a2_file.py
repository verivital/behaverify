import py_trees
import math
import operator
import random
import serene_safe_assignment


class a2(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(a2, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('blVAR0'), access = py_trees.common.Access.WRITE)
        self.localFROZENVAR5 = [(
            min((-2), max((-5), (min(50, max((-50), max((5 if (True ^ False) else 16), (-48)))))))
            if ('both' == self.blackboard.blVAR0) else
            (
                min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), -((-6))))) + (min(50, max((-50), -((-6))))) + (-2) + (-2)))))))
                if ((True == False) and True) else
                (
                min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), abs((-36))))) + (min(50, max((-50), abs((-36))))) + (min(50, max((-50), abs((-36))))) + ((-48) if (3 < 10) else (-11))))))))
        ))) for _ in range(2)]
        __temp_var__ = serene_safe_assignment.localFROZENVAR5([(0, (
                    min((-2), max((-5), (-5)))
                    if (4 < (-5)) else
                    (
                        min((-2), max((-5), (-3)))
                        if (True == False) else
                        (
                        min((-2), max((-5), (min(50, max((-50), (0 - (4 if (2 != (-3)) else 15)))))))
                )))), (1, (
                    min((-2), max((-5), (-5)))
                    if (4 < (-5)) else
                    (
                        min((-2), max((-5), (-3)))
                        if (True == False) else
                        (
                        min((-2), max((-5), (min(50, max((-50), (0 - (4 if (2 != (-3)) else 15)))))))
                ))))])
        for (index, val) in __temp_var__:
            self.localFROZENVAR5[index] = val

    def update(self):
        if (False or False):
            return_status = py_trees.common.Status.RUNNING
        elif ((min(50, max((-50), -((-32))))) >= (min(50, max((-50), min(self.localFROZENVAR5[serene_safe_assignment.index_func(max(0, min(1, (-32))), 2)], self.localFROZENVAR5[serene_safe_assignment.index_func(max(0, min(1, (-32))), 2)]))))):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.RUNNING
        return return_status
