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
        self.blackboard.register_key(key = ('blVAR3'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE5'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('blDEFINE7'), access = py_trees.common.Access.WRITE)
        self.localVAR2 = serene_safe_assignment.localVAR2((
            min((-2), max((-5), (-4)))
            if (([((-27) <= self.blackboard.blVAR0[serene_safe_assignment.index_func(max(0, min(2, 39)), 3)]), (False or True), ('yes' != 'yes'), (True == False)].count(True)) == (-16)) else
            (
            min((-2), max((-5), (min(50, max((-50), -(3))))))
        )))

    def update(self):
        if True:
            return_status = py_trees.common.Status.SUCCESS
        elif (False and False):
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.RUNNING
        self.__serene_print__ = return_status.value
        return return_status
