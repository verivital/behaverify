import py_trees
import math
import operator
import random
import serene_safe_assignment


class send_victory(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(send_victory, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('victory'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.victory = serene_safe_assignment.victory(True)
        return_status = py_trees.common.Status.FAILURE
        return return_status
