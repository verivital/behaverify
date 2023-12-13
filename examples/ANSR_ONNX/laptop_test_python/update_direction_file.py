import py_trees
import math
import operator
import random
import serene_safe_assignment


class update_direction(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(update_direction, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('cur_y'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('dir'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.dir = serene_safe_assignment.dir((
            'Down'
            if (self.blackboard.cur_y == 8) else
            (
                'Up'
                if (self.blackboard.cur_y == 0) else
                (
                self.blackboard.dir
        ))))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
