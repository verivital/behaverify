import random
import serene_safe_assignment


class t1_environment():
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
        self.envVAR3 = serene_safe_assignment.envVAR3((
            min(5, max(2, (self.blackboard.blVAR0[0] - self.envVAR1[1])))
            if (self.blackboard.blDEFINE7() == (70 < self.blackboard.blVAR0[0])) else
            (
            min(5, max(2, ((self.envFROZENVAR4[0] * -16 * 61) * self.envFROZENVAR4[1] * self.blackboard.blVAR0[1] * max(76, -78))))
        )))
        __temp_var__ = serene_safe_assignment.envVAR2([(min(2, max(0, (max(self.envFROZENVAR4[1], 67) * max(abs(self.envVAR1[0]), 0) * (self.envVAR1[2] + -12 + self.envVAR2[2])))), (
            min(-2, max(-5, -26))
            if ((self.blackboard.blDEFINE7() and False) == True) else
            (
                min(-2, max(-5, ([((not (((True == True) ^ (False ^ False)))) or (False)), (-39 < self.envVAR1[1]), (not (((not ((self.blackboard.blDEFINE7() ^ self.blackboard.blDEFINE7()))) ^ ((not (False)) or (True))))), (-61 >= max(-82, self.blackboard.blVAR0[0]))].count(True))))
                if self.blackboard.blDEFINE7() else
                (
                min(-2, max(-5, self.envFROZENVAR4[0]))
        )))), (min(2, max(0, (-58 - -97))), (
            min(-2, max(-5, self.blackboard.blVAR0[1]))
            if ((not ((False ^ True))) and self.blackboard.blDEFINE7()) else
            (
                min(-2, max(-5, abs(min(self.envFROZENVAR4[1], -93))))
                if (True or self.blackboard.blDEFINE7()) else
                (
                min(-2, max(-5, (max(([(False == True), (-54 <= self.envVAR2[0]), (True ^ self.blackboard.blDEFINE7())].count(True)), (self.envVAR3 * 6)) + -16 + -(26) + max(77, -24))))
        )))), (min(2, max(0, -22)), (
            min(-2, max(-5, -(73)))
            if ((not (False)) or (self.blackboard.blDEFINE7())) else
            (
                min(-2, max(-5, max(max(self.envVAR3, self.envVAR3), -19)))
                if ((-75 != self.envVAR2[1]) and self.blackboard.blDEFINE7()) else
                (
                min(-2, max(-5, 38))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, ([((self.envVAR3 - -73) == (97 * self.envVAR1[0] * self.envVAR3)), ((-36 != self.envVAR2[0]) and (self.envVAR3 < 81)), (43 < self.envFROZENVAR4[0]), ((self.envFROZENVAR4[1] > self.envVAR2[1]) ^ True)].count(True)))), (
            min(5, max(2, (min(self.envVAR3, -1) - -27)))
            if (self.blackboard.blDEFINE7() or self.blackboard.blDEFINE7()) else
            (
                min(5, max(2, -59))
                if (self.blackboard.blDEFINE7() == (self.envVAR1[1] < self.envVAR1[2])) else
                (
                min(5, max(2, (self.blackboard.blVAR0[0] * ((-99 * self.envVAR3 * 89) * abs(50)))))
        )))), (min(2, max(0, (abs(39) * (-42 * self.blackboard.blVAR0[1] * -37 * -65) * ([(self.blackboard.blDEFINE7() or True), (-59 <= -65), (self.blackboard.blDEFINE7() == False), (-61 == 47)].count(True)) * (95 * 10 * 69)))), (
            min(5, max(2, ([(True or True), (True == self.blackboard.blDEFINE7())].count(True))))
            if ((not (self.blackboard.blDEFINE7())) or (True)) else
            (
                min(5, max(2, max(-62, -95)))
                if (self.envVAR1[1] >= self.envVAR2[0]) else
                (
                min(5, max(2, max(self.envVAR3, self.envVAR3)))
        )))), (min(2, max(0, abs(-38))), (
            min(5, max(2, (((-77 * 26 * self.envVAR2[2] * self.blackboard.blVAR0[0]) - -94) - (self.envVAR2[1] - self.envVAR1[1]))))
            if (self.blackboard.blDEFINE7() == (53 < 61)) else
            (
                min(5, max(2, (abs(self.envFROZENVAR4[0]) - ([(self.envVAR3 > -31), (not ((False ^ True)))].count(True)))))
                if False else
                (
                min(5, max(2, self.envFROZENVAR4[0]))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, ([(self.blackboard.blDEFINE7() or True), (self.blackboard.blDEFINE7() == False), (self.envFROZENVAR4[0] <= 93)].count(True)))), min(5, max(2, min(([(self.blackboard.blVAR0[1] <= -(self.blackboard.blVAR0[1])), ((not ((False or self.blackboard.blDEFINE7()))) or ((True and self.blackboard.blDEFINE7()))), (not (((not ((True ^ self.blackboard.blDEFINE7()))) ^ False)))].count(True)), abs(abs(-1)))))), (min(2, max(0, (42 * (-100 * -49)))), min(5, max(2, abs(self.envVAR3))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            min(5, max(2, abs(self.blackboard.blVAR0[1])))
            if ((57 - 1) >= max(self.blackboard.blVAR0[1], self.blackboard.blVAR0[0])) else
            (
                min(5, max(2, abs(self.blackboard.blVAR0[1])))
                if (((not (False)) or (True)) and False) else
                (
                min(5, max(2, 11))
        )))), (1, min(5, max(2, -(([(False == False), (-80 > -59), ((not (True)) or (False))].count(True)))))), (2, min(5, max(2, abs(self.blackboard.blVAR0[0]))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR2 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR2([(0, min(-2, max(-5, ([(False and (True ^ True)), (30 > 63)].count(True))))), (1, (
            min(-2, max(-5, ((self.blackboard.blVAR0[0] * -22 * 89) - -10)))
            if (abs(self.envVAR1[0]) < (-87 * -16 * self.envVAR1[1] * -1)) else
            (
                min(-2, max(-5, ((min(self.envVAR1[2], self.envVAR1[2]) * self.blackboard.blVAR0[0]) - (-28 * 8 * self.envVAR1[1] * self.envVAR1[0]))))
                if (((self.envVAR1[0] - 74) > 54) ^ (36 <= self.envVAR1[1])) else
                (
                min(-2, max(-5, -61))
        )))), (2, (
            min(-2, max(-5, self.envVAR1[1]))
            if True else
            (
            min(-2, max(-5, max((self.envVAR1[1] + 27), -3)))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        self.envVAR3 = serene_safe_assignment.envVAR3(min(5, max(2, ([(self.envVAR2[0] >= -36), (True == True)].count(True)))))
        self.envFROZENVAR4 = [None] * 2
        __temp_var__ = serene_safe_assignment.envFROZENVAR4([(0, min(5, max(2, self.blackboard.blVAR0[1]))), (1, min(5, max(2, self.blackboard.blVAR0[1])))])
        for (index, val) in __temp_var__:
            self.envFROZENVAR4[index] = val

    def a3_read_after_0__condition(self, node):
        if (self.blackboard.blDEFINE7() or (38 >= -17)):
            return True
        else:
            return False


    def a3_read_after_0__0(self, node):
        return [(min(1, max(0, abs(86))), min(-2, max(-5, max(self.envVAR1[2], min(([(15 > 85), ((not (self.blackboard.blDEFINE7())) or (False))].count(True)), abs(self.envVAR3))))))]

    def a4_read_before_0__condition(self, node):
        if ((-47 == 87) == (42 < (5 * -17))):
            return True
        else:
            return False


    def a4_read_before_0__0(self, node):
        return [(min(1, max(0, min(2, self.envVAR1[0]))), min(-2, max(-5, -(abs(self.blackboard.blVAR0[0])))))]
