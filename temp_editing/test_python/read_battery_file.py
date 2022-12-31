import py_trees
import math
import operator
import random
import robot_environ


class read_battery(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(read_battery, self).__init__(name)
        self.name = name
        self.blackboard = py_trees.blackboard.Blackboard()
        self.blackboard.battery_reading = random.choice([10])

    def update(self):

        (got_value, new_value) = robot_environ.get_battery()
        if got_value: self.blackboard.battery_reading = new_value

        if got_value: return_status = py_trees.common.Status.SUCCESS
        else: return_status = py_trees.common.Status.FAILURE
        return return_status
