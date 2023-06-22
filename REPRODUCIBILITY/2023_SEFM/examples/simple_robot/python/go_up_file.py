import py_trees
import math
import operator
import random
import serene_safe_assignment


class go_up(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(go_up, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        self.environment.delay_this_action(self.environment.up_func__0, self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
