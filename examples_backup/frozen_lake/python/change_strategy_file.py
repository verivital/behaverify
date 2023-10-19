import py_trees
import math
import operator
import random
import serene_safe_assignment


class change_strategy(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(change_strategy, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('strategy'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.strategy = serene_safe_assignment.strategy((
            'y_first'
            if (self.blackboard.strategy == 'x_first') else
            (
            'x_first'
        )))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
