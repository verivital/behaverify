import py_trees
import math
import operator
import random
import robot


class get_mission(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(get_mission, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('mission'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('target_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('target_y'), access = py_trees.common.Access.WRITE)
        self.blackboard.mission = False
        self.blackboard.target_x = 0
        self.blackboard.target_y = 0

    def update(self):
        temp_vals = robot.get_mission()
        if temp_vals[0]:
            (self.saw_target, self.blackboard.target_x, self.blackboard.target_y) = temp_vals
        else:
            self.saw_target = False
        if self.saw_target:
            self.blackboard.mission = True
        else:
            self.blackboard.mission = False
        if self.saw_target:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        return return_status
