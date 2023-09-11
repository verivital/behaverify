import py_trees
import math
import operator
import random
import serene_safe_assignment


class pipe_mapping_disable_task(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(pipe_mapping_disable_task, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('pipe_mapping_enable'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.pipe_mapping_enable = serene_safe_assignment.pipe_mapping_enable(False)
        return_status = py_trees.common.Status.RUNNING
        return return_status
