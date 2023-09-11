import random
import serene_safe_assignment


class t8_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, (self.envVAR1[2] * abs(abs(18)) * self.envVAR3))), (
            min(-2, max(-5, -52))
            if (([(True and True), (self.envDEFINE9() < self.envVAR1[0]), (self.envVAR3 < 82), (True == self.blackboard.blVAR0)].count(True)) == (0 - -47)) else
            (
                min(-2, max(-5, 1))
                if ((self.envVAR1[2] > self.envVAR1[1]) ^ False) else
                (
                min(-2, max(-5, max(-18, 30)))
        )))), (min(2, max(0, (abs(self.envDEFINE9()) + self.envDEFINE9()))), (
            min(-2, max(-5, self.envVAR3))
            if ((not (True)) or (True)) else
            (
                min(-2, max(-5, (([(-52 < self.envDEFINE9()), (True == False), (self.envDEFINE9() <= -89)].count(True)) - abs(31))))
                if True else
                (
                min(-2, max(-5, (([(self.blackboard.blVAR0 == False), (False and False), (self.envDEFINE9() <= 34), (True == self.blackboard.blVAR0)].count(True)) * max(-96, self.envDEFINE9()) * self.envVAR3 * abs(([(25 < 67), (not ((self.blackboard.blVAR0 ^ self.blackboard.blVAR0)))].count(True))))))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR3 = serene_safe_assignment.envVAR3((
            min(-2, max(-5, max(([(self.envVAR3 < 6), ((not (self.blackboard.blVAR0)) or (True)), (self.envDEFINE9() <= -95)].count(True)), 52)))
            if (-92 == -28) else
            (
                min(-2, max(-5, abs(max(self.envVAR3, -43))))
                if (self.blackboard.blVAR0 ^ self.blackboard.blVAR0) else
                (
                min(-2, max(-5, -33))
        ))))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE9():
            return (
                min(5, max(2, abs(min(self.envVAR1[2], -18))))
                if (self.blackboard.blFROZENVAR6[0] != 'both') else
                (
                    min(5, max(2, min(([('yes' == 'yes'), (90 < self.envVAR1[2])].count(True)), ([((not ((self.blackboard.blVAR0 ^ self.blackboard.blVAR0))) == self.blackboard.blVAR0), ((self.envVAR3 - -41) > -60), (self.blackboard.blVAR0 ^ self.blackboard.blVAR0), (not ((True ^ self.blackboard.blVAR0)))].count(True)))))
                    if (self.envVAR3 >= self.envVAR3) else
                    (
                    min(5, max(2, abs(self.envVAR1[1])))
            )))

        self.envDEFINE9 = envDEFINE9
        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, min(-2, max(-5, -3))), (1, min(-2, max(-5, -3))), (2, min(-2, max(-5, -3)))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR3 = serene_safe_assignment.envVAR3(min(-2, max(-5, ([(not ((self.blackboard.blVAR0 ^ (not ((False ^ False)))))), (self.blackboard.blVAR0 and (87 >= -82)), (58 > -26)].count(True)))))

    def a1_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, 45)), (
            min(-2, max(-5, -(abs(-97))))
            if (False and (self.blackboard.blVAR0 != False)) else
            (
            min(-2, max(-5, (self.envVAR3 * -(91) * ([((-41 * 36) <= min(self.envVAR3, 91)), ((self.blackboard.blVAR0 and False) == (not ((self.blackboard.blVAR0 ^ self.blackboard.blVAR0)))), (not (((self.envVAR1[2] < self.envDEFINE9()) ^ True)))].count(True)) * self.envDEFINE9())))
        ))), (min(2, max(0, (-(-93) + (-40 - -1) + abs(12)))), (
            min(-2, max(-5, (37 - (abs(-47) + -(-43) + (31 * self.envDEFINE9() * self.envVAR1[2])))))
            if (not (((4 > node.localDEFINE10()) ^ (self.blackboard.blVAR0 == self.blackboard.blVAR0)))) else
            (
            min(-2, max(-5, 19))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a2_read_after_0__condition(self, node):
        if self.blackboard.blVAR0:
            return True
        else:
            return False


    def a2_read_after_0__0(self, node):
        return (
            'yes'
            if (True or False) else
            (
                self.blackboard.blFROZENVAR6[0]
                if (self.envVAR1[2] >= -15) else
                (
                self.blackboard.blFROZENVAR6[0]
        )))

    def a2_read_after_0__1(self, node):
        return (
            self.blackboard.blVAR0
            if False else
            (
                ((True and self.blackboard.blVAR0) ^ (False ^ self.blackboard.blVAR0))
                if self.blackboard.blVAR0 else
                (
                True
        )))

    def a2_read_after_0__2(self, node):
        return (
            'both'
            if ((False or True) or False) else
            (
            'both'
        ))

    def a2_read_after_0__3(self, node):
        return (
            self.blackboard.blDEFINE8()
            if True else
            (
                self.blackboard.blDEFINE8()
                if (self.blackboard.blVAR0 ^ self.blackboard.blVAR0) else
                (
                node.localVAR2
        )))

    def a3_read_after_0__condition(self, node):
        if ((False == self.blackboard.blVAR0) or (self.blackboard.blVAR0 ^ True)):
            return True
        else:
            return False


    def a3_read_after_0__0(self, node):
        return (self.envVAR1[2] > 2)

    def a3_read_after_0__1(self, node):
        return True
