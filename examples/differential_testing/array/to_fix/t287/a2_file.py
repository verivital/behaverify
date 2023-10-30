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
        self.blackboard.register_key(key = ('blDEFINE6'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE8'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = [(
            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), (5 + 5)))) - (min(50, max((-50), min((-4), (-4)))))))))))
            if (True ^ (3 >= 2)) else
            (
                min((-2), max((-5), (min(50, max((-50), max((-50), (-50)))))))
                if True else
                (
                min((-2), max((-5), (min(50, max((-50), min((-4), 30))))))
        ))) for _ in range(3)]
        __temp_var__ = serene_safe_assignment.localVAR2([(0, (
                    min((-2), max((-5), 7))
                    if False else
                    (
                        min((-2), max((-5), ((min(50, max((-50), max(22, 22)))) if (not ((((-15) <= (-6)) ^ ((-27) >= 13)))) else (min(50, max((-50), ((-46) + (-46) + (-46))))))))
                        if ((not ((True ^ self.blackboard.blVAR0))) and self.blackboard.blVAR0) else
                        (
                        min((-2), max((-5), (-1)))
                )))), (1, (
                    min((-2), max((-5), 7))
                    if False else
                    (
                        min((-2), max((-5), ((min(50, max((-50), max(22, 22)))) if (not ((((-15) <= (-6)) ^ ((-27) >= 13)))) else (min(50, max((-50), ((-46) + (-46) + (-46))))))))
                        if ((not ((True ^ self.blackboard.blVAR0))) and self.blackboard.blVAR0) else
                        (
                        min((-2), max((-5), (-1)))
                ))))])
        for (index, val) in __temp_var__:
            self.localVAR2[index] = val

    def update(self):
        if ((min(50, max((-50), max(34, 5)))) > (min(50, max((-50), max(3, 3))))):
            return_status = py_trees.common.Status.SUCCESS
        elif self.blackboard.blVAR0:
            return_status = py_trees.common.Status.RUNNING
        elif (33 < (min(50, max((-50), ((-40) + (-40)))))):
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        self.environment.delay_this_action(self.environment.a2_write_after_0__0, self)
        self.environment.a2_write_after_0__1(self)
        self.environment.delay_this_action(self.environment.a2_write_after_0__2, self)
        return return_status
