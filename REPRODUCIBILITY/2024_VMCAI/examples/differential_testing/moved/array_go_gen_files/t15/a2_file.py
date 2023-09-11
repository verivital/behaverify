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
        self.blackboard.register_key(key = ('blFROZENVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE4'), access = py_trees.common.Access.WRITE)


        def localDEFINE5():
            return (
                min(-2, max(-5, ((self.blackboard.blVAR0 + 75 + 76) * (self.blackboard.blFROZENVAR3 * self.blackboard.blVAR0 * 9))))
                if False else
                (
                    min(-2, max(-5, -(self.blackboard.blFROZENVAR3)))
                    if (True ^ False) else
                    (
                    min(-2, max(-5, (max(self.blackboard.blDEFINE4(1), self.blackboard.blDEFINE4(0)) + -5 + self.blackboard.blDEFINE4(1) + abs(-23))))
            )))

        self.localDEFINE5 = localDEFINE5

    def update(self):
        self.environment.a2_write_before_0__0(self)
        return_status = py_trees.common.Status.SUCCESS
        self.__serene_print__ = return_status.value
        self.environment.a2_write_after_0__0(self)
        return return_status
