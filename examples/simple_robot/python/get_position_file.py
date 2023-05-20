import py_trees
import math
import operator
import random
import serene_safe_assignment
import simple_robot_environment


class get_position(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(get_position, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('y'), access = py_trees.common.Access.WRITE)

    def update(self):
        if simple_robot_environment.get_position_func__condition(self):
            self.blackboard.x = serene_safe_assignment.x(simple_robot_environment.get_position_func__0(self))
            self.blackboard.y = serene_safe_assignment.y(simple_robot_environment.get_position_func__1(self))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
