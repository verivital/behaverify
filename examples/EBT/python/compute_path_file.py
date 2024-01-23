import py_trees
import math
import operator


class compute_path(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(compute_path, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('serene_randomizer'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('path_computed_bool'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_storage_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('path_storage_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.calculate_path__condition(self):
            self.blackboard.path_computed_bool = True
            __temp_var__ = self.environment.calculate_path__0(self)
            for (index, val) in __temp_var__:
                self.blackboard.path_storage_x[index] = val
            __temp_var__ = self.environment.calculate_path__1(self)
            for (index, val) in __temp_var__:
                self.blackboard.path_storage_y[index] = val
        else:
            self.blackboard.path_computed_bool = False
        if self.blackboard.path_computed_bool:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.FAILURE
        return return_status
