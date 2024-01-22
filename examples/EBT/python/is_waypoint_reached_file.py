import py_trees
import math
import operator
import random
import serene_safe_assignment


class is_waypoint_reached(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(is_waypoint_reached, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path_computed_bool'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('waypoint_location'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_location'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (((self.blackboard.drone_location[serene_safe_assignment.index_func(0, 2)] == self.blackboard.waypoint_location[serene_safe_assignment.index_func(0, 2)]) and (self.blackboard.drone_location[serene_safe_assignment.index_func(1, 2)] == self.blackboard.waypoint_location[serene_safe_assignment.index_func(1, 2)]))) else (py_trees.common.Status.FAILURE))
        return return_status
