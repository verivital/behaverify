import py_trees
import math
import operator
import random
import serene_safe_assignment


class need_up(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(need_up, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('y_subgoal'), access = py_trees.common.Access.READ)

    def update(self):
        return ((py_trees.common.Status.SUCCESS) if (self.environment.need_up(self)) else (py_trees.common.Status.FAILURE))