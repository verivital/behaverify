import random
import serene_safe_assignment


class new_array_environment():
    def delay_this_action(self, action, node):
        self.delayed_action_queue.append((action, node))

    def execute_delayed_action_queue(self):
        for (delayed_action, node) in self.delayed_action_queue:
            delayed_action(node)
        self.delayed_action_queue = []
        return

    def between_tick_environment_update(self):
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.test = [None] * 3
        __temp_var__ = serene_safe_assignment.test([(0, 0), (1, 1), (2, 2)])
        for (index, val) in __temp_var__:
            self.test[index] = val

    def idk__0(self, node):
        __temp_var__ = serene_safe_assignment.test([(0, abs(self.test[0]))])
        for (index, val) in __temp_var__:
            self.test[index] = val
        return
