import py_trees
import math
import operator
import random


class read_battery(py_trees.behaviour.Behaviour):
	def __init__(self, name):
		super(read_battery, self).__init__(name)
		self.name = name
		self.blackboard = py_trees.blackboard.Blackboard()
		self.blackboard.battery_reading = random.choice([10])



	def update(self):
		self.blackboard.battery_reading = random.choice([self.blackboard.battery_reading])
		return_status = random.choice([py_trees.common.Status.FAILURE])
		return return_status
