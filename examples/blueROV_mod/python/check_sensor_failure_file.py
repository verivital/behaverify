import py_trees
import math
import operator
import random
import serene_safe_assignment


class check_sensor_failure(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(check_sensor_failure, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('bb_sensor_failure_warning'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.bb_sensor_failure_warning == True)) else (py_trees.common.Status.FAILURE))
        return return_status
