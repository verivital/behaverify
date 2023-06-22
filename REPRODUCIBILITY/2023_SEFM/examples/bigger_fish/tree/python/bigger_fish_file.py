import py_trees
import math
import operator
import random
import serene_safe_assignment


class bigger_fish(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(bigger_fish, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('biggest_fish'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.biggest_fish = serene_safe_assignment.biggest_fish(min((1 + self.blackboard.biggest_fish), 199))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
