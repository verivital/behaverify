import py_trees
import math
import operator
import random
import serene_safe_assignment


class is_path_computed(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(is_path_computed, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('path_computed_bool'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (self.blackboard.path_computed_bool) else (py_trees.common.Status.FAILURE))
        return return_status
