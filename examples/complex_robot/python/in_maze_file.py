import py_trees
import math
import operator
import random
import serene_safe_assignment


class in_maze(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(in_maze, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('zone'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.zone == 'maze')) else (py_trees.common.Status.FAILURE))
        return return_status
