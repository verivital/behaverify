import py_trees
import math
import operator
import random
import serene_safe_assignment


class set_new_subgoal(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(set_new_subgoal, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('subgoal'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.subgoal = serene_safe_assignment.subgoal((
            0
            if (self.blackboard.subgoal == 15) else
            (
            (1 + self.blackboard.subgoal)
        )))
        return_status = py_trees.common.Status.SUCCESS
        return return_status
