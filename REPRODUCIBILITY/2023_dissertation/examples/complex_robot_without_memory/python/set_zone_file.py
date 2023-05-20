import py_trees
import math
import operator
import random
import serene_safe_assignment
import complex_robot_environment


class set_zone(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(set_zone, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('zone'), access = py_trees.common.Access.WRITE)

    def update(self):
        if complex_robot_environment.compute_zone_func__condition(self):
            self.blackboard.zone = serene_safe_assignment.zone(complex_robot_environment.compute_zone_func__0(self))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
