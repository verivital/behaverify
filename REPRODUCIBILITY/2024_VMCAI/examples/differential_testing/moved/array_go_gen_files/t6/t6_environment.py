import random
import serene_safe_assignment


class t6_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, self.blackboard.blVAR4)), (
            min(-2, max(-5, abs(self.blackboard.blVAR3)))
            if (self.envVAR1[1] >= self.envVAR1[1]) else
            (
            min(-2, max(-5, max(-8, self.envVAR1[1])))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, self.blackboard.blVAR4)), (
            min(-2, max(-5, ((self.blackboard.blDEFINE5() + 65) + 43)))
            if True else
            (
            min(-2, max(-5, min(39, (self.envVAR1[1] - -94))))
        ))), (min(1, max(0, (55 * 86 * self.envVAR1[1]))), (
            min(-2, max(-5, min(self.blackboard.blVAR3, self.blackboard.blVAR3)))
            if (-28 < self.blackboard.blDEFINE5()) else
            (
            min(-2, max(-5, (-(-(self.blackboard.blVAR4)) - self.envVAR1[1])))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = [None] * 2
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            min(-2, max(-5, 3))
            if False else
            (
                min(-2, max(-5, ([((32 - 3) > abs(-4)), (-2 < ((13 - 97) * -(-76))), (-88 < -100), (([(37 < -2), ((3 * -5 * -41) <= 3), (-3 > 4)].count(True)) >= max(abs(-3), min(68, 92)))].count(True))))
                if (not (((-4 > 5) ^ ((True or self.blackboard.blVAR0[2]) or self.blackboard.blVAR0[2])))) else
                (
                min(-2, max(-5, (-2 + -11)))
        )))), (1, min(-2, max(-5, 64)))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val

    def a3_read_before_0__condition(self, node):
        if (62 <= self.blackboard.blVAR3):
            return True
        else:
            return False


    def a3_read_before_0__0(self, node):
        return [(min(2, max(0, min(-70, 27))), (
            False
            if (-91 >= self.blackboard.blVAR4) else
            (
                (self.blackboard.blVAR0[1] and self.blackboard.blDEFINE6(0))
                if self.blackboard.blVAR0[0] else
                (
                (self.envVAR1[0] >= node.localVAR2)
        ))))]

    def a4_read_before_1__condition(self, node):
        if False:
            return True
        else:
            return False


    def a4_read_before_1__0(self, node):
        return [(min(2, max(0, (-78 + self.blackboard.blVAR3))), (
            self.blackboard.blDEFINE6(0)
            if (self.envVAR1[1] > -63) else
            (
            ((self.blackboard.blVAR3 <= self.blackboard.blDEFINE5()) != (True == True))
        )))]

    def a4_write_before_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, 82)), (
            min(-2, max(-5, self.blackboard.blVAR3))
            if self.blackboard.blVAR0[2] else
            (
            min(-2, max(-5, min(abs(self.blackboard.blVAR3), -(46))))
        ))), (min(1, max(0, (-51 + -4))), (
            min(-2, max(-5, min(max(([(self.blackboard.blDEFINE5() > 50), (False or False), (94 <= self.blackboard.blDEFINE5())].count(True)), 75), ([(-(self.blackboard.blVAR3) != -43), (max(self.blackboard.blDEFINE5(), self.blackboard.blDEFINE5()) < -(self.blackboard.blVAR3)), ((False == False) == True), (False == self.blackboard.blDEFINE6(2))].count(True)))))
            if ((self.envVAR1[1] - self.blackboard.blVAR4) >= (self.envVAR1[1] * 32 * 13 * self.blackboard.blDEFINE5())) else
            (
            min(-2, max(-5, 89))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_read_after_1__condition(self, node):
        if ((77 - -69) != self.envVAR1[0]):
            return True
        else:
            return False


    def a4_read_after_1__0(self, node):
        return (
            min(5, max(2, min(-(self.blackboard.blDEFINE5()), max(-5, self.blackboard.blDEFINE5()))))
            if (False or self.blackboard.blDEFINE6(2)) else
            (
                min(5, max(2, (-(self.blackboard.blDEFINE5()) * ([((not (self.blackboard.blVAR0[1])) or (self.blackboard.blDEFINE6(1))), (self.blackboard.blDEFINE6(2) != self.blackboard.blVAR0[2]), (self.blackboard.blDEFINE6(0) ^ self.blackboard.blDEFINE6(1)), (not ((False ^ self.blackboard.blDEFINE6(0))))].count(True)))))
                if True else
                (
                min(5, max(2, max(-(-59), -78)))
        )))

    def a4_read_after_0__condition(self, node):
        if (True or self.blackboard.blDEFINE6(1)):
            return True
        else:
            return False


    def a4_read_after_0__0(self, node):
        return (
            min(5, max(2, abs(min(self.blackboard.blVAR4, 32))))
            if self.blackboard.blDEFINE6(2) else
            (
            min(5, max(2, ([(False or self.blackboard.blVAR0[1]), (abs(self.envVAR1[0]) > min(self.blackboard.blVAR3, -73)), (self.blackboard.blVAR0[1] or (not (((self.blackboard.blVAR0[0] or self.blackboard.blDEFINE6(0)) ^ False))))].count(True))))
        ))
