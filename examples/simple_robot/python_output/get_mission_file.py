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
        self.blackboard.mission = random.choice([False])
        self.blackboard.target_x = random.choice([0])
        self.blackboard.target_y = random.choice([0])

    def update(self):
        (self.saw_target, self.blackboard.target_x, self.blackboard.target_y) = robot.get_mission()
        if self.saw_target:
            self.blackboard.mission = random.choice([True])
        else:
            self.blackboard.mission = random.choice([False])
        if self.saw_target:
            return_status = py_trees.common.Status.FAILURE
        else:
            return_status = py_trees.common.Status.FAILURE
        return return_status
