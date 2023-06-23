import py_trees
import math
import operator
import random
import serene_safe_assignment


class get_mission(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(get_mission, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('mission'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('target_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('target_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.mission_func__condition(self):
            self.blackboard.target_x = serene_safe_assignment.target_x(self.environment.mission_func__0(self))
            self.blackboard.target_y = serene_safe_assignment.target_y(self.environment.mission_func__1(self))
        self.blackboard.mission = serene_safe_assignment.mission(True)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
