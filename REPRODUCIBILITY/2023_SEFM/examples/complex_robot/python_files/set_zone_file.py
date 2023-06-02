import py_trees
import math
import operator
import random
import complex_robot_environment


class set_zone(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(set_zone, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('zone'), access = py_trees.common.Access.WRITE)

    def update(self):
        temp_vals = complex_robot_environment.compute_zone()
        if temp_vals[0]:
            (_, self.blackboard.zone) = temp_vals
        return_status = py_trees.common.Status.SUCCESS
        return return_status
