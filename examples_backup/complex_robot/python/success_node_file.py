import py_trees
import math
import operator
import random
import serene_safe_assignment


class success_node(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(success_node, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if (True) else (py_trees.common.Status.FAILURE))
        return return_status
