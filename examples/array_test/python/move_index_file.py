import py_trees
import math
import operator
import random
import serene_safe_assignment


class move_index(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(move_index, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('index_var'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.index_var = serene_safe_assignment.index_var(((self.blackboard.index_var + 1) % 3))
        return_status = py_trees.common.Status.FAILURE
        return return_status
