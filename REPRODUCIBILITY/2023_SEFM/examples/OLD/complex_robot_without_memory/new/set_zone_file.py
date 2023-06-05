import py_trees
import math
import operator
import random
import serene_safe_assignment


class set_zone(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(set_zone, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('zone'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.compute_zone_func__condition(self):
            self.blackboard.zone = serene_safe_assignment.zone(self.environment.compute_zone_func__0(self))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
