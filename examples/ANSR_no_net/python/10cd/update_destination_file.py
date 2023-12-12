import py_trees
import math
import operator
import random
import serene_safe_assignment


class update_destination(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(update_destination, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('y_dir'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('x_mode'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dest_x'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('dest_y'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.dest_x = serene_safe_assignment.dest_x((
            (0 if (self.blackboard.dest_x == 10) else 10)
            if self.blackboard.x_mode else
            (
            self.blackboard.dest_x
        )))
        self.blackboard.dest_y = serene_safe_assignment.dest_y((
            min(10, max(0, (self.blackboard.dest_y + (self.blackboard.y_dir * 2))))
            if not (self.blackboard.x_mode) else
            (
            self.blackboard.dest_y
        )))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
