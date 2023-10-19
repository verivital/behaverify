import py_trees
import math
import operator
import random
import serene_safe_assignment


class send_light_signal(py_trees.behaviour.Behaviour):
    def __init__(self, name, environment):
        super(send_light_signal, self).__init__(name)
        self.name = name
        self.environment = environment
        self.blackboard = self.attach_blackboard_client(name = name)
        self.blackboard.register_key(key = ('direction'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('signal'), access = py_trees.common.Access.READ)
        self.blackboard.register_key(key = ('fairness_counter'), access = py_trees.common.Access.WRITE)

    def update(self):
        self.blackboard.fairness_counter = serene_safe_assignment.fairness_counter(min(4, (self.blackboard.fairness_counter + 1)))
        self.environment.delay_this_action(self.environment.light_signal_func__0, self)
        return_status = py_trees.common.Status.SUCCESS
        return return_status
