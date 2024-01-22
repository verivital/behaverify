import py_trees
import math
import operator
import random
import serene_safe_assignment


class get_next_subgoal(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(get_next_subgoal, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('subgoal'), access = py_trees.common.Access.WRITE)

    def update(self):
        if self.environment.subgoal_calculation__condition(self):
            __temp_var__ = serene_safe_assignment.subgoal(self.environment.subgoal_calculation__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.subgoal[index] = val
        return_status = py_trees.common.Status.SUCCESS
        return return_status
