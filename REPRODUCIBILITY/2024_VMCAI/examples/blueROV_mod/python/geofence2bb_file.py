import py_trees
import math
import operator
import random
import serene_safe_assignment


class geofence2bb(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(geofence2bb, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('bb_geofence_warning'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('bb_geofence'), access = py_trees.common.Access.WRITE)
        self.read_success = serene_safe_assignment.read_success(False)

    def update(self):
        if self.environment.geofence2bb_read__condition(self):
            self.read_success = serene_safe_assignment.read_success(True)
            self.blackboard.bb_geofence_warning = serene_safe_assignment.bb_geofence_warning(self.environment.geofence2bb_read__0(self))
        else:
            self.read_success = serene_safe_assignment.read_success(True)
        if self.read_success:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        return return_status
