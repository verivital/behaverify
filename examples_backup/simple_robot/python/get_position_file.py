import py_trees
import math
import operator
import random
import serene_safe_assignment


class get_position(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(get_position, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('y'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.position_func__condition(self):
            self.blackboard.x = serene_safe_assignment.x(self.environment.position_func__0(self))
            self.blackboard.y = serene_safe_assignment.y(self.environment.position_func__1(self))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
