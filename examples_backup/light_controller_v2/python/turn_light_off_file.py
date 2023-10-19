import py_trees
import math
import operator
import random
import serene_safe_assignment


class turn_light_off(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(turn_light_off, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        self.environment.delay_this_action(self.environment.light_off_func__0, self)
        return_status = py_trees.common.Status.RUNNING
        return return_status
