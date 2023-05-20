import py_trees
import math
import operator
import random
import serene_safe_assignment


class need_side(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(need_side, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('need_side_reached'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (self.blackboard.need_side_reached) else (py_trees.common.Status.FAILURE))
