import py_trees
import math
import operator
import random
import serene_safe_assignment


class emergency_stop_task(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(emergency_stop_task, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = py_trees.common.Status.SUCCESS
        return return_status
