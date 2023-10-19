import py_trees
import math
import operator
import random
import serene_safe_assignment


class obstacle_avoidance(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(obstacle_avoidance, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('bb_obstacle_warning'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('cm_hsd_input'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.obstacle_avoidance_read__condition(self):
            self.blackboard.bb_obstacle_warning = serene_safe_assignment.bb_obstacle_warning(self.environment.obstacle_avoidance_read__0(self))
        self.blackboard.cm_hsd_input = serene_safe_assignment.cm_hsd_input((
            'cm_obstacle_avoidance_task'
            if self.blackboard.bb_obstacle_warning else
            (
            self.blackboard.cm_hsd_input
        )))
        return_status = py_trees.common.Status.RUNNING
        return return_status
