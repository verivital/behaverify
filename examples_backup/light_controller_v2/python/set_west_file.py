import py_trees
import math
import operator
import random
import serene_safe_assignment


class set_west(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(set_west, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('direction'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('fairness_counter'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.direction = serene_safe_assignment.direction('west_to_east')
        self.blackboard.fairness_counter = serene_safe_assignment.fairness_counter(0)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
