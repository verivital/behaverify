import py_trees
import math
import operator
import random
import serene_safe_assignment


class speed_min_task(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(speed_min_task, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('HSD_out'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.HSD_out = serene_safe_assignment.HSD_out('uuv_min_speed')
        return_status = py_trees.common.Status.SUCCESS
        return return_status
