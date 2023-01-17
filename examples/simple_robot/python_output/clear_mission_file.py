import py_trees
import math
import operator
import random


class clear_mission(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(clear_mission, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('mission'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.mission = random.choice([False])
        return_status = py_trees.common.Status.SUCCESS
        return return_status
