import py_trees
import math
import operator
import random
import serene_safe_assignment


class check_lec2am_rs(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(check_lec2am_rs, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('lec2_am_r_speed_warning'), access = py_trees.common.Access.READ)

    def update(self):
        return_status = ((py_trees.common.Status.SUCCESS) if ((self.blackboard.lec2_am_r_speed_warning == True)) else (py_trees.common.Status.FAILURE))
        return return_status
