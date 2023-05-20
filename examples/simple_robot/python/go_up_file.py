import py_trees
import math
import operator
import random
import serene_safe_assignment
import simple_robot_environment


class go_up(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(go_up, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)

    def update(self):
        simple_robot_environment.delay_this_action(simple_robot_environment.go_up_func__0, self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
