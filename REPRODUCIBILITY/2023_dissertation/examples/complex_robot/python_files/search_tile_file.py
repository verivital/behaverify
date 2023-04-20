import py_trees
import math
import operator
import random
import complex_robot_environment


class search_tile(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(search_tile, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('have_flag'), access = py_trees.common.Access.WRITE)
        self.tile_searched = False

    def update(self):
        temp_vals = complex_robot_environment.search_tile(self.tile_searched)
        if temp_vals[0]:
            (_, self.tile_searched, self.blackboard.have_flag) = temp_vals
        complex_robot_environment.update_search(self.tile_searched)
        if (self.tile_searched and self.blackboard.have_flag):
            return_status = py_trees.common.Status.RUNNING
        elif self.tile_searched:
            return_status = py_trees.common.Status.RUNNING
        else:
            return_status = py_trees.common.Status.RUNNING
        return return_status
