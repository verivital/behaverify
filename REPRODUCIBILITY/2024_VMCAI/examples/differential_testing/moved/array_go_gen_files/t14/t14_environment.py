import random
import serene_safe_assignment


class t14_environment():
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
            min(5, max(2, min(self.envVAR1, self.blackboard.blDEFINE5())))
            if (self.envVAR2[1] == 'no') else
            (
            min(5, max(2, max(self.envVAR1, self.envFROZENVAR3[1])))
        )))
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, -87)), (
            self.envVAR2[1]
            if ((not ((self.blackboard.blVAR0[1] ^ False))) == (([(False == True), (not ((False ^ True))), (self.envFROZENVAR3[1] >= self.envVAR1)].count(True)) >= self.envFROZENVAR3[0])) else
            (
                'no'
                if self.blackboard.blVAR0[2] else
                (
                self.envVAR2[0]
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, (self.envFROZENVAR3[1] - 55))), 'no')])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, ((self.envVAR1 - self.envVAR1) - abs(abs(self.envFROZENVAR3[1]))))))
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, max(self.envFROZENVAR3[1], self.envVAR1))), (
            self.envVAR2[0]
            if ((not (self.blackboard.blVAR0[0])) or ((69 >= abs(self.envFROZENVAR3[1])))) else
            (
                self.envVAR2[1]
                if ((-14 - -17) == (self.envFROZENVAR3[1] + self.blackboard.blDEFINE5())) else
                (
                'both'
        )))), (min(1, max(0, abs((70 * 30)))), (
            'no'
            if (self.envVAR2[1] != 'no') else
            (
                self.envVAR2[0]
                if True else
                (
                self.envVAR2[1]
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, (4 - -2))))
        self.envVAR2 = [None] * 2
        __temp_var__ = serene_safe_assignment.envVAR2([(0, (
            'yes'
            if ((not (self.blackboard.blVAR0[0])) or (self.blackboard.blVAR0[1])) else
            (
            'both'
        ))), (1, (
            'yes'
            if ((not (self.blackboard.blVAR0[0])) or (self.blackboard.blVAR0[1])) else
            (
            'both'
        )))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        self.envFROZENVAR3 = [None] * 2
        __temp_var__ = serene_safe_assignment.envFROZENVAR3([(0, min(5, max(2, ([(False or True), ((False ^ (self.blackboard.blVAR0[0] or self.blackboard.blVAR0[2])) ^ (self.envVAR1 < abs(-52))), (self.blackboard.blVAR0[0] or True), ((not (((not (self.blackboard.blVAR0[2])) or (self.blackboard.blVAR0[1])))) or ((max(-22, self.envVAR1) <= -(self.envVAR1))))].count(True))))), (1, min(5, max(2, max(max(max(-23, self.envVAR1), self.envVAR1), abs(-63)))))])
        for (index, val) in __temp_var__:
            self.envFROZENVAR3[index] = val

    def a2_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, ([(self.envVAR1 >= (self.envFROZENVAR3[1] * 71)), ((node.localDEFINE6(0) != self.blackboard.blVAR0[0]) ^ (self.blackboard.blVAR0[0] != True)), ((self.envVAR1 >= self.blackboard.blDEFINE5()) ^ (79 > 59)), ((30 >= 87) or True)].count(True))))
            if True else
            (
                min(5, max(2, self.blackboard.blDEFINE5()))
                if (25 <= self.envFROZENVAR3[0]) else
                (
                min(5, max(2, 18))
        ))))
        return

    def a2_write_after_0__1(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, self.blackboard.blDEFINE5())))
        return

    def a2_write_after_0__2(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, self.envFROZENVAR3[0])))
        return

    def a2_write_after_0__3(self, node):
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, abs(min(-89, self.envVAR1)))), (
            self.envVAR2[0]
            if (False == (True and True)) else
            (
            'yes'
        )))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        return

    def a3_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, (79 * -77 * 35 * 72))), self.envVAR2[1])])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        return
