import py_trees
import math
import operator
import random
import serene_safe_assignment


class get_info(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(get_info, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('tiles'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.get_info_func__condition(self):
            __temp_var__ = serene_safe_assignment.tiles(self.environment.get_info_func__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.tiles[index] = val
        return_status = py_trees.common.Status.SUCCESS
        return return_status
