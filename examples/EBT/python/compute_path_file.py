import py_trees
import math
import operator
import random
import serene_safe_assignment


class compute_path(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(compute_path, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path_computed_bool'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_storage_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_storage_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.calculate_path__condition(self):
            __temp_var__ = serene_safe_assignment.path_storage_x(self.environment.calculate_path__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.path_storage_x[index] = val
            __temp_var__ = serene_safe_assignment.path_storage_y(self.environment.calculate_path__1(self))
            for (index, val) in __temp_var__:
                self.blackboard.path_storage_y[index] = val
        self.blackboard.path_computed_bool = serene_safe_assignment.path_computed_bool(True)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
