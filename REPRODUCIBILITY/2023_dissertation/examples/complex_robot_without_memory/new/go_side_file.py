import py_trees
import math
import operator
import random
import serene_safe_assignment


class go_side(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(go_side, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('side'), access = py_trees.common.Access.READ)

    def update(self):
        self.environment.delay_this_action(self.environment.go_side_func__0, self)
        return_status = py_trees.common.Status.RUNNING
        return return_status
