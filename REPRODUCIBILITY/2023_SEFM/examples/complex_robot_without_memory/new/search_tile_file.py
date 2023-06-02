import py_trees
import math
import operator
import random
import serene_safe_assignment


class search_tile(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(search_tile, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('have_flag'), access = py_trees.common.Access.WRITE)
        self.tile_searched = serene_safe_assignment.tile_searched(False)

    def update(self):
        if self.environment.search_tile_func__condition(self):
            self.tile_searched = serene_safe_assignment.tile_searched(self.environment.search_tile_func__0(self))
            self.blackboard.have_flag = serene_safe_assignment.have_flag(self.environment.search_tile_func__1(self))
        self.environment.delay_this_action(self.environment.update_search_func__0, self)
        if (self.tile_searched and self.blackboard.have_flag):
            return_status = py_trees.common.Status.SUCCESS
        elif self.tile_searched:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.RUNNING
        return return_status
