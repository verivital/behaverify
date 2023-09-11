import random
import serene_safe_assignment


class t19_environment():
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
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = [None] * 2
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            ((self.blackboard.blVAR0 == -44) ^ (False == True))
            if ((True or False) == (False == True)) else
            (
                ((63 <= 60) == True)
                if (self.blackboard.blVAR0 != 24) else
                (
                (False ^ (True != (True and True)))
        )))), (1, (-94 >= -17))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR2 = serene_safe_assignment.envVAR2('no')
        self.envFROZENVAR3 = [None] * 3
        __temp_var__ = serene_safe_assignment.envFROZENVAR3([(0, (
            self.envVAR2
            if (not ((False ^ True))) else
            (
            'no'
        ))), (1, self.envVAR2), (2, (
            'both'
            if True else
            (
                'no'
                if (False and False) else
                (
                'no'
        ))))])
        for (index, val) in __temp_var__:
            self.envFROZENVAR3[index] = val
        self.envFROZENVAR4 = [None] * 3
        __temp_var__ = serene_safe_assignment.envFROZENVAR4([(0, (
            min(-2, max(-5, abs(self.blackboard.blVAR0)))
            if (-(self.blackboard.blVAR0) > self.blackboard.blVAR0) else
            (
            min(-2, max(-5, min(self.blackboard.blVAR0, self.blackboard.blVAR0)))
        ))), (1, (
            min(-2, max(-5, abs(self.blackboard.blVAR0)))
            if (-(self.blackboard.blVAR0) > self.blackboard.blVAR0) else
            (
            min(-2, max(-5, min(self.blackboard.blVAR0, self.blackboard.blVAR0)))
        ))), (2, (
            min(-2, max(-5, abs(self.blackboard.blVAR0)))
            if (-(self.blackboard.blVAR0) > self.blackboard.blVAR0) else
            (
            min(-2, max(-5, min(self.blackboard.blVAR0, self.blackboard.blVAR0)))
        )))])
        for (index, val) in __temp_var__:
            self.envFROZENVAR4[index] = val

    def a1_read_after_0__condition(self, node):
        if ((not ((57 != node.localDEFINE5(0)))) or ((False and self.envVAR1[1]))):
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return (
            min(5, max(2, ([(True ^ (False and True)), (max(55, 2) != 38), ((([(self.envVAR1[0] != self.envVAR1[1]), (64 <= self.envFROZENVAR4[2])].count(True)) > -35) == False), (max(self.envFROZENVAR4[0], self.blackboard.blVAR0) >= (-84 - max(node.localDEFINE5(1), self.envFROZENVAR4[2])))].count(True))))
            if (True and (True == self.envVAR1[0])) else
            (
                min(5, max(2, max(10, (90 - 95))))
                if (True or True) else
                (
                min(5, max(2, ([((not (True)) or ((self.envVAR1[0] ^ self.envVAR1[0]))), ((17 <= -47) or (self.blackboard.blVAR0 >= self.blackboard.blVAR0)), ((44 + 55 + self.blackboard.blVAR0 + node.localDEFINE5(1)) >= max(-(-81), 99)), ((node.localDEFINE5(0) * 55) > -18)].count(True))))
        )))

    def a1_read_after_0__1(self, node):
        return (
            min(5, max(2, -(([(False == self.envVAR1[1]), (not ((False ^ False))), ('no' == 'yes'), (self.envVAR1[1] ^ self.envVAR1[1])].count(True)))))
            if (self.envVAR2 != self.envFROZENVAR3[1]) else
            (
                min(5, max(2, (4 - self.blackboard.blVAR0)))
                if (self.envVAR1[0] or self.envVAR1[1]) else
                (
                min(5, max(2, -78))
        )))

    def a1_read_after_0__2(self, node):
        return (
            min(5, max(2, abs(max(-56, node.localDEFINE5(1)))))
            if True else
            (
            min(5, max(2, -((node.localDEFINE5(0) - node.localDEFINE5(0)))))
        ))

    def a3_write_before_1__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, ([(self.envVAR1[1] or False), (self.envFROZENVAR4[1] != -77), (self.envFROZENVAR4[1] >= -26)].count(True)))), (
            (min(49, 73) <= (71 + self.blackboard.blVAR0))
            if (([(self.blackboard.blVAR0 > -42), (False or True), (self.envVAR1[0] ^ True)].count(True)) != min(43, -76)) else
            (
                (self.envVAR1[0] or False)
                if ((not ((False ^ self.envVAR1[0]))) or False) else
                (
                (-((self.blackboard.blVAR0 * self.blackboard.blVAR0 * 23 * self.envFROZENVAR4[0])) >= 16)
        )))), (min(1, max(0, (self.blackboard.blVAR0 * self.envFROZENVAR4[0]))), (
            ((self.envFROZENVAR4[2] < 80) == (-(self.envFROZENVAR4[0]) < -(-22)))
            if (-45 < max(self.envFROZENVAR4[0], self.envFROZENVAR4[0])) else
            (
                ((self.blackboard.blVAR0 + self.blackboard.blVAR0) >= ([(True != False), (self.envVAR1[1] and False), ((not (self.envVAR1[1])) or (self.envVAR1[0]))].count(True)))
                if (self.blackboard.blVAR0 < 24) else
                (
                self.envVAR1[0]
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_read_after_1__condition(self, node):
        if ((not (self.envVAR1[1])) or ((self.envFROZENVAR4[2] < self.envFROZENVAR4[0]))):
            return True
        else:
            return False


    def a4_read_after_1__0(self, node):
        return min(5, max(2, -((-42 * self.envFROZENVAR4[2]))))

    def a4_read_after_1__1(self, node):
        return min(5, max(2, -21))
