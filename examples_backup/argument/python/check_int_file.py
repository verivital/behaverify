import py_trees
import math
import operator
import random
import serene_safe_assignment


class check_int(py_trees.behaviour.Behaviour):
    def __init__(self, name, arg_name):
        self.arg_name = arg_name
        super(check_int, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.arg_name == 55)) else (py_trees.common.Status.FAILURE))
        return return_status
