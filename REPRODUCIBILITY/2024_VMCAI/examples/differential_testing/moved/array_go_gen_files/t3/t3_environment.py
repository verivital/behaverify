import random
import serene_safe_assignment


class t3_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, self.blackboard.blVAR0[2])), 'no')])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, (max(self.envDEFINE7(), -22) + self.envDEFINE7() + (self.blackboard.blVAR0[2] - 82)))), (
            self.envVAR1[1]
            if ((not (self.envDEFINE9())) or (True)) else
            (
            self.envVAR1[0]
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, self.blackboard.blVAR0[0])), (
            'no'
            if (-13 >= self.envDEFINE7()) else
            (
            'no'
        ))), (min(1, max(0, max(([(self.envVAR1[0] != self.envVAR1[0]), (self.blackboard.blVAR0[0] < self.blackboard.blVAR0[2]), (self.envDEFINE7() >= self.blackboard.blVAR0[1]), (self.blackboard.blVAR3 and False)].count(True)), abs(self.envDEFINE7())))), (
            'no'
            if (abs(self.blackboard.blVAR0[2]) > 80) else
            (
            'both'
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, 70)), (
            self.envVAR1[0]
            if False else
            (
            'yes'
        ))), (min(1, max(0, -90)), (
            'no'
            if (self.blackboard.blVAR0[0] < -88) else
            (
            'no'
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE7():
            return (
                min(-2, max(-5, -56))
                if (self.blackboard.blVAR3 and (93 <= self.blackboard.blVAR0[1])) else
                (
                    min(-2, max(-5, abs(([((self.blackboard.blVAR3 == False) ^ (-84 < self.blackboard.blVAR0[0])), (self.blackboard.blVAR3 and ((not (self.blackboard.blVAR3)) or (self.blackboard.blVAR3)))].count(True)))))
                    if (abs(-97) <= 10) else
                    (
                    min(-2, max(-5, self.blackboard.blVAR0[0]))
            )))

        self.envDEFINE7 = envDEFINE7


        def envDEFINE9():
            return (self.blackboard.blVAR3 or (False == self.blackboard.blVAR3))

        self.envDEFINE9 = envDEFINE9
        self.envVAR1 = [None] * 2
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            'no'
            if (False or False) else
            (
                'yes'
                if (abs(self.blackboard.blVAR0[0]) > self.blackboard.blVAR0[2]) else
                (
                'yes'
        )))), (1, 'both')])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val

    def a1_write_before_1__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, max(-58, 68))), (
            self.envVAR1[1]
            if node.localFROZENVAR6 else
            (
            'yes'
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_write_before_2__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, min((-27 - self.envDEFINE7()), abs(73)))), (
            'yes'
            if (self.envDEFINE7() < self.blackboard.blVAR0[1]) else
            (
            'yes'
        ))), (min(1, max(0, abs(max(78, 96)))), (
            'no'
            if (node.localVAR4 != node.localVAR4) else
            (
            'yes'
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_write_before_1__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, (self.envDEFINE7() - 5))), (
            'both'
            if (self.envDEFINE9() or True) else
            (
                self.envVAR1[0]
                if (11 == -15) else
                (
                'no'
        )))), (min(1, max(0, 93)), (
            'no'
            if (self.blackboard.blVAR3 ^ True) else
            (
                'yes'
                if (-89 > self.blackboard.blVAR0[1]) else
                (
                self.envVAR1[0]
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_write_before_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, ((-44 + 48) - max(self.envDEFINE7(), self.blackboard.blVAR0[0])))), self.envVAR1[1]), (min(1, max(0, min(self.envDEFINE7(), -(61)))), 'no')])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_read_after_0__condition(self, node):
        if (self.envVAR1[0] == self.envVAR1[0]):
            return True
        else:
            return False


    def a4_read_after_0__0(self, node):
        return (
            (node.localVAR4 == True)
            if (False ^ True) else
            (
            (node.localVAR4 and False)
        ))
