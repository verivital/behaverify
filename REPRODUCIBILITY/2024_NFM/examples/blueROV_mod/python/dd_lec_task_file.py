import py_trees
import math
import operator
import random
import serene_safe_assignment


class dd_lec_task(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(dd_lec_task, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('dd_z_axis_warning'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('dd_xy_axis_degradation'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('dd_output'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.dd_lec_read__condition(self):
            self.blackboard.dd_output = serene_safe_assignment.dd_output(self.environment.dd_lec_read__0(self))
        self.blackboard.dd_z_axis_warning = serene_safe_assignment.dd_z_axis_warning(((self.blackboard.dd_output == 'z_warn') or (self.blackboard.dd_z_axis_warning and not ((self.blackboard.dd_output == 'safe')))))
        self.blackboard.dd_xy_axis_degradation = serene_safe_assignment.dd_xy_axis_degradation(((self.blackboard.dd_output == 'xy_warn') or (self.blackboard.dd_xy_axis_degradation and not ((self.blackboard.dd_output == 'safe')))))
        return_status = py_trees.common.Status.FAILURE
        return return_status
