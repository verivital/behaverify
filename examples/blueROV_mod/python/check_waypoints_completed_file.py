import py_trees
import math
import operator
import random
import serene_safe_assignment


class check_waypoints_completed(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(check_waypoints_completed, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.environment.check_waypoints_completed(self)) else (py_trees.common.Status.FAILURE))
        return return_status
