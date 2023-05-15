import py_trees
import math
import operator
import random
import complex_robot_environment


class flag_not_returned(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(flag_not_returned, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (complex_robot_environment.check_flag_not_returned()) else (py_trees.common.Status.FAILURE))

