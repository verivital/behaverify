import py_trees
import math
import operator
import random
import serene_safe_assignment


class prepare_round(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(prepare_round, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('signal'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.signal = serene_safe_assignment.signal(True)
        return_status = py_trees.common.Status.RUNNING
        return return_status
