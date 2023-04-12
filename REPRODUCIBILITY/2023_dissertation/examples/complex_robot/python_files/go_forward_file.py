import py_trees
import math
import operator
import random
import complex_robot_environment


class go_forward(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(go_forward, self).__init__(name)
        self.name = name
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('forward'), access = py_trees.common.Access.WRITE)
        if self.blackboard.have_flag:
            self.blackboard.forward = -1
        else:
            self.blackboard.forward = 1

    def update(self):
        complex_robot_environment.go_forward(self.blackboard.forward)
        return_status = py_trees.common.Status.RUNNING
        return return_status
