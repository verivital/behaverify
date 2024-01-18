import py_trees
import math
import operator
import random
import serene_safe_assignment


class call_xy_net(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(call_xy_net, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('x_net'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('y_net'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dest_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('dest_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.dest_x = serene_safe_assignment.dest_x(max(0, min(8, self.blackboard.x_net(0))))
        self.blackboard.dest_y = serene_safe_assignment.dest_y(max(0, min(8, self.blackboard.y_net(0))))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
