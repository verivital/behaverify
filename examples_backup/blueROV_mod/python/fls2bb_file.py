import py_trees
import math
import operator
import random
import serene_safe_assignment


class fls2bb(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(fls2bb, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('fls_range'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('obstacle_standoff_warning'), access = py_trees.common.Access.WRITE)
        self.read_success = serene_safe_assignment.read_success(False)

    def update(self):
        if self.environment.fls2bb_read__condition(self):
            self.read_success = serene_safe_assignment.read_success(True)
            self.blackboard.obstacle_standoff_warning = serene_safe_assignment.obstacle_standoff_warning(self.environment.fls2bb_read__0(self))
        else:
            self.read_success = serene_safe_assignment.read_success(True)
        if self.read_success:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        return return_status
