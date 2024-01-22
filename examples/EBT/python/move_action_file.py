import py_trees
import math
import operator
import random
import serene_safe_assignment


class move_action(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(move_action, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('subgoal'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('drone_velocity'), access = py_trees.common.Access.WRITE)
        self.blackboard.register_key(key = ('drone_location'), access = py_trees.common.Access.WRITE)
        self.drone_action = [0 for _ in range(2)]
        __temp_var__ = serene_safe_assignment.drone_action([])
        for (index, val) in __temp_var__:
            self.drone_action[index] = val

    def update(self):
        if self.environment.compute_state__condition(self):
            __temp_var__ = serene_safe_assignment.drone_action(self.environment.compute_state__0(self))
            for (index, val) in __temp_var__:
                self.drone_action[index] = val
        if self.environment.send_action__condition(self):
            __temp_var__ = serene_safe_assignment.drone_velocity(self.environment.send_action__0(self))
            for (index, val) in __temp_var__:
                self.blackboard.drone_velocity[index] = val
            __temp_var__ = serene_safe_assignment.drone_location(self.environment.send_action__1(self))
            for (index, val) in __temp_var__:
                self.blackboard.drone_location[index] = val
        return_status = py_trees.common.Status.SUCCESS
        return return_status
