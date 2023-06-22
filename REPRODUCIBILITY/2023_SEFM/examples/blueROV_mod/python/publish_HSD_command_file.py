import py_trees
import math
import operator
import random
import serene_safe_assignment


class publish_HSD_command(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(publish_HSD_command, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = py_trees.common.Status.RUNNING
        return return_status
