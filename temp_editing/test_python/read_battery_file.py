import py_trees
import math
import operator
import random
import robot_environ


class read_battery(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(read_battery, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('battery_reading'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('battery_threshold'), access = py_trees.common.Access.WRITE)
        self.blackboard.battery_reading = random.choice([10])
        self.blackboard.battery_threshold = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def update(self):

        (got_value, new_value) = robot_environ.get_battery()
        if got_value: self.blackboard.battery_reading = new_value

        if got_value: return_status = py_trees.common.Status.SUCCESS
        else: return_status = py_trees.common.Status.FAILURE
        return return_status
