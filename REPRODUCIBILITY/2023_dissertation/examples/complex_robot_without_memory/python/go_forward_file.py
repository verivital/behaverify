import py_trees
import math
import operator
import random
import serene_safe_assignment
import complex_robot_environment


class go_forward(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(go_forward, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('forward'), access = py_trees.common.Access.READ)

    def update(self):
        complex_robot_environment.delay_this_action(complex_robot_environment.go_forward_func__0, self)
        return_status = py_trees.common.Status.RUNNING
        return return_status
