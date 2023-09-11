import random
import serene_safe_assignment


class t16_environment():
    def delay_this_action(self, action, node):
        self.delayed_action_queue.append((action, node))

    def execute_delayed_action_queue(self):
        for (delayed_action, node) in self.delayed_action_queue:
            delayed_action(node)
        self.delayed_action_queue = []
        return

    def pre_tick_environment_update(self):
        return

    def post_tick_environment_update(self):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            (True == self.envVAR1)
            if False else
            (
            (64 < 36)
        )))
        self.envVAR2 = serene_safe_assignment.envVAR2(self.envVAR2)
        self.envVAR2 = serene_safe_assignment.envVAR2((
            self.envVAR2
            if (max(self.blackboard.blVAR0, self.blackboard.blVAR3) == abs(-31)) else
            (
            self.envVAR2
        )))
        self.envVAR1 = serene_safe_assignment.envVAR1(self.blackboard.blDEFINE7(2))
        self.envVAR2 = serene_safe_assignment.envVAR2((
            self.envVAR2
            if (27 == self.blackboard.blVAR3) else
            (
            self.envVAR2
        )))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = serene_safe_assignment.envVAR1((
            False
            if (self.blackboard.blVAR0 > ((-64 + -49 + self.blackboard.blVAR0 + -44) - (-1 + 0))) else
            (
            False
        )))
        self.envVAR2 = serene_safe_assignment.envVAR2((
            'both'
            if ('yes' == 'no') else
            (
                'both'
                if (88 < -67) else
                (
                'yes'
        ))))
        self.envFROZENVAR5 = serene_safe_assignment.envFROZENVAR5((
            min(5, max(2, min(-(self.blackboard.blVAR3), max(72, -23))))
            if ((self.blackboard.blVAR0 + 92 + self.blackboard.blVAR0 + self.blackboard.blVAR0) <= (self.blackboard.blVAR0 - 21)) else
            (
            min(5, max(2, (-3 * 54 * self.blackboard.blVAR3 * 20)))
        )))
        self.envFROZENVAR6 = [None] * 2
        __temp_var__ = serene_safe_assignment.envFROZENVAR6([(0, (
            (8 >= self.blackboard.blVAR0)
            if ('both' == 'both') else
            (
                False
                if (True == self.envVAR1) else
                (
                self.envVAR1
        )))), (1, (
            (self.blackboard.blVAR0 > self.blackboard.blVAR3)
            if (not ((self.envVAR1 ^ True))) else
            (
                (self.envVAR1 or self.envVAR1)
                if (self.envVAR1 or self.envVAR1) else
                (
                (self.blackboard.blVAR0 < self.envFROZENVAR5)
        ))))])
        for (index, val) in __temp_var__:
            self.envFROZENVAR6[index] = val

    def a4_read_before_1__condition(self, node):
        if self.envFROZENVAR6[1]:
            return True
        else:
            return False


    def a4_read_before_1__0(self, node):
        return (
            min(5, max(2, -74))
            if ((-53 >= self.envFROZENVAR5) == ((False == self.blackboard.blDEFINE7(2)) ^ (True and True))) else
            (
            min(5, max(2, abs(max(self.blackboard.blVAR3, -33))))
        ))

    def a4_read_before_0__condition(self, node):
        if (node.localDEFINE9(2) <= -(self.blackboard.blVAR3)):
            return True
        else:
            return False


    def a4_read_before_0__0(self, node):
        return (
            min(5, max(2, -(self.blackboard.blVAR3)))
            if (node.localDEFINE8() >= 65) else
            (
                min(5, max(2, max(max(64, -91), node.localDEFINE8())))
                if (abs(92) >= node.localDEFINE8()) else
                (
                min(5, max(2, (75 + 33 + 27)))
        )))

    def a4_write_after_0__0(self, node):
        self.envVAR2 = serene_safe_assignment.envVAR2((
            self.envVAR2
            if True else
            (
                self.envVAR2
                if ((not ((self.envVAR1 ^ self.blackboard.blDEFINE7(0)))) or (True and self.envFROZENVAR6[0])) else
                (
                self.envVAR2
        ))))
        return
