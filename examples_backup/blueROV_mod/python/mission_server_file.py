import py_trees
import math
import operator
import random
import serene_safe_assignment


class mission_server(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(mission_server, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('finished_missions'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('bb_rth_warning'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('bb_mission'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('emergency_stop_warning'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('next_mission'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.mission_server_read__condition(self):
            self.blackboard.finished_missions = serene_safe_assignment.finished_missions(self.environment.mission_server_read__0(self))
        self.blackboard.bb_rth_warning = serene_safe_assignment.bb_rth_warning((
            self.blackboard.finished_missions
            if self.blackboard.next_mission else
            (
            self.blackboard.bb_rth_warning
        )))
        if self.environment.mission_server_read2__condition(self):
            self.blackboard.bb_mission = serene_safe_assignment.bb_mission(self.environment.mission_server_read2__0(self))
        self.blackboard.emergency_stop_warning = serene_safe_assignment.emergency_stop_warning((
            True
            if ((self.blackboard.next_mission and not (self.blackboard.finished_missions)) and ('e_stop' == self.blackboard.bb_mission)) else
            (
            self.blackboard.emergency_stop_warning
        )))
        self.blackboard.next_mission = serene_safe_assignment.next_mission(False)
        return_status = py_trees.common.Status.RUNNING
        return return_status
