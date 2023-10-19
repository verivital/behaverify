import py_trees
import math
import operator
import random
import serene_safe_assignment


class next_mission_node(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(next_mission_node, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('next_mission'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.next_mission = serene_safe_assignment.next_mission(True)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
