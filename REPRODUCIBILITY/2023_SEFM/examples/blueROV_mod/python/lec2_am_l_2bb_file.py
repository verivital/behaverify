import py_trees
import math
import operator
import random
import serene_safe_assignment


class lec2_am_l_2bb(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(lec2_am_l_2bb, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('lec2_am_l_speed_warning'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('lec2_am_l_pipe_warning'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('lec2_am_l'), access = py_trees.common.Access.WRITE)
        self.read_success = serene_safe_assignment.read_success(False)

    def update(self):
        if self.environment.lec2_am_l_2bb_read__condition(self):
            self.read_success = serene_safe_assignment.read_success(True)
            self.blackboard.lec2_am_l_speed_warning = serene_safe_assignment.lec2_am_l_speed_warning(self.environment.lec2_am_l_2bb_read__0(self))
            self.blackboard.lec2_am_l_pipe_warning = serene_safe_assignment.lec2_am_l_pipe_warning(self.environment.lec2_am_l_2bb_read__1(self))
        else:
            self.read_success = serene_safe_assignment.read_success(True)
        if self.read_success:
            return_status = py_trees.common.Status.SUCCESS
        else:
            return_status = py_trees.common.Status.RUNNING
        return return_status
