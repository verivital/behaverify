import random
import serene_safe_assignment


class array_test_environment():
    def delay_this_action(self, action, node):
        self.delayed_action_queue.append((action, node))

    def execute_delayed_action_queue(self):
        for (delayed_action, node) in self.delayed_action_queue:
            delayed_action(node)
        self.delayed_action_queue = []
        return

    def between_tick_environment_update(self):
        __temp_var__ = serene_safe_assignment.test([(0, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[0] == 10) else
            (
            self.test[0]
        ))), (1, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[1] == 10) else
            (
            self.test[1]
        ))), (2, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[2] == 10) else
            (
            self.test[2]
        ))), (3, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[3] == 10) else
            (
            self.test[3]
        ))), (4, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[4] == 10) else
            (
            self.test[4]
        ))), (5, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[5] == 10) else
            (
            self.test[5]
        ))), (6, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[6] == 10) else
            (
            self.test[6]
        ))), (7, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[7] == 10) else
            (
            self.test[7]
        ))), (8, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[8] == 10) else
            (
            self.test[8]
        ))), (9, (
            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            if (self.test[9] == 10) else
            (
            self.test[9]
        )))])
        for (index, val) in __temp_var__:
            self.test[index] = val
        __temp_var__ = serene_safe_assignment.test([(self.test[0], (
            (self.test[self.test[0]] + 2)
            if ((self.test[self.test[0]] % 2) == 0) else
            (
            (self.test[self.test[0]] + 1)
        ))), (self.test[9], (
            (self.test[self.test[9]] + 2)
            if ((self.test[self.test[9]] % 2) == 0) else
            (
            (self.test[self.test[9]] + 1)
        )))])
        for (index, val) in __temp_var__:
            self.test[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.test = [None] * 10
        __temp_var__ = serene_safe_assignment.test([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])
        for (index, val) in __temp_var__:
            self.test[index] = val

    def idk__0(self, node):
        __temp_var__ = serene_safe_assignment.test([(1, abs(self.test[0]))])
        for (index, val) in __temp_var__:
            self.test[index] = val
        return

    def idk__0(self, node):
        __temp_var__ = serene_safe_assignment.test([(1, abs(self.test[0]))])
        for (index, val) in __temp_var__:
            self.test[index] = val
        return
