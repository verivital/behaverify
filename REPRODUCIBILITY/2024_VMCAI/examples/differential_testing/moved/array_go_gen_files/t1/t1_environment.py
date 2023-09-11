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
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE4():
            return (
                min(-2, max(-5, min(100, max(-100, (min(100, max(-100, min(self.envVAR1[0], 5))) * min(100, max(-100, max(4, self.envVAR1[2]))) * min(100, max(-100, max(min(100, max(-100, (self.envVAR1[0] - -13))), ([(True == True), (self.blackboard.blVAR0[0] == 'yes')].count(True))))))))))
                if ('yes' == self.blackboard.blVAR0[0]) else
                (
                    min(-2, max(-5, min(100, max(-100, (self.envVAR1[2] - self.envVAR1[2])))))
                    if ((not (True)) or (True)) else
                    (
                    min(-2, max(-5, self.envVAR1[2]))
            )))

        self.envDEFINE4 = envDEFINE4
        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, min(-2, max(-5, min(100, max(-100, (-4 * min(100, max(-100, abs(-3))) * min(100, max(-100, -(5))) * min(100, max(-100, (80 - -3))))))))), (1, min(-2, max(-5, min(100, max(-100, min(94, 2)))))), (2, (
            min(-2, max(-5, ([(True == True), (3 >= 4)].count(True))))
            if True else
            (
                min(-2, max(-5, 4))
                if False else
                (
                min(-2, max(-5, min(100, max(-100, abs(-3)))))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val

    def a1_write_before_1__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, min(100, max(-100, min(min(100, max(-100, min(66, 94))), min(100, max(-100, min(-38, self.envVAR1[1])))))))), (
            min(-2, max(-5, min(100, max(-100, (self.envDEFINE4() * self.envDEFINE4())))))
            if (min(100, max(-100, (self.envVAR1[1] * min(100, max(-100, min(self.envDEFINE4(), 91))) * self.envVAR1[0]))) > min(100, max(-100, abs(83)))) else
            (
            min(-2, max(-5, ([((not (False)) or (self.blackboard.blDEFINE5(1))), (self.blackboard.blDEFINE5(0) or self.blackboard.blDEFINE5(1)), (not ((self.blackboard.blDEFINE5(1) ^ False))), (26 > self.envVAR1[2])].count(True))))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a1_read_after_0__condition(self, node):
        if (self.envDEFINE4() > self.envDEFINE4()):
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return [(min(2, max(0, min(100, max(-100, (self.envVAR1[1] + self.envDEFINE4()))))), 'both'), (min(2, max(0, min(100, max(-100, abs(min(100, max(-100, abs(12)))))))), 'yes')]

    def a2_read_before_0__condition(self, node):
        if False:
            return True
        else:
            return False


    def a2_read_before_0__0(self, node):
        return [(min(2, max(0, min(100, max(-100, min(([(self.envVAR1[2] == 83), ((self.envDEFINE4() < self.envDEFINE4()) == (False == self.blackboard.blDEFINE5(1))), (min(100, max(-100, abs(self.envDEFINE4()))) <= min(100, max(-100, -(1)))), (min(100, max(-100, (-97 + self.envVAR1[2] + 61))) <= -67)].count(True)), min(100, max(-100, (-89 + 9 + min(100, max(-100, -(self.envDEFINE4()))) + ([(36 <= self.envVAR1[2]), (False or self.blackboard.blDEFINE5(0)), (False == self.blackboard.blDEFINE5(0)), (self.blackboard.blDEFINE5(0) == self.blackboard.blDEFINE5(0))].count(True)))))))))), 'no'), (min(2, max(0, min(100, max(-100, -(min(100, max(-100, (-4 - 88)))))))), 'yes')]

    def a2_read_before_0__1(self, node):
        return [(min(2, max(0, ([(not (((self.envVAR1[0] == self.envVAR1[0]) ^ self.blackboard.blDEFINE5(1)))), (([(min(100, max(-100, (-15 - -29))) < -65), (self.blackboard.blVAR0[2] != self.blackboard.blVAR0[2]), ((self.envVAR1[0] <= self.envVAR1[0]) or False)].count(True)) <= min(100, max(-100, (self.envDEFINE4() + -43)))), (min(100, max(-100, abs(97))) < min(100, max(-100, (self.envDEFINE4() * self.envDEFINE4() * self.envVAR1[0] * -27)))), (([(self.blackboard.blDEFINE5(1) ^ False), (min(100, max(-100, -(self.envDEFINE4()))) >= min(100, max(-100, (self.envDEFINE4() - 96)))), (min(100, max(-100, abs(13))) < ([(not ((self.blackboard.blDEFINE5(0) ^ self.blackboard.blDEFINE5(1)))), (True and True), (False or True)].count(True)))].count(True)) <= min(100, max(-100, (-8 + self.envDEFINE4()))))].count(True)))), (
            self.blackboard.blVAR0[0]
            if (self.blackboard.blDEFINE5(1) == self.blackboard.blDEFINE5(0)) else
            (
                'both'
                if ('no' == 'no') else
                (
                'no'
        )))), (min(2, max(0, min(100, max(-100, (-58 - self.envDEFINE4()))))), (
            self.blackboard.blVAR0[2]
            if ((not ((not ((False ^ False))))) or ((-36 <= -61))) else
            (
                'both'
                if (False ^ self.blackboard.blDEFINE5(1)) else
                (
                self.blackboard.blVAR0[0]
        ))))]

    def a3_write_after_1__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, -74)), (
            min(-2, max(-5, -91))
            if True else
            (
                min(-2, max(-5, min(100, max(-100, (min(100, max(-100, abs(self.envVAR1[1]))) - min(100, max(-100, abs(57))))))))
                if True else
                (
                min(-2, max(-5, min(100, max(-100, min(-53, min(100, max(-100, (node.localVAR2 * -2 * self.envVAR1[2] * self.envVAR1[0]))))))))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a3_write_after_1__1(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, min(100, max(-100, (min(100, max(-100, (node.localVAR2 + 49 + self.envVAR1[0] + self.envVAR1[2]))) * min(100, max(-100, max(self.envDEFINE4(), self.envDEFINE4()))) * 96 * -98))))), (
            min(-2, max(-5, ([(not (((not ((self.blackboard.blDEFINE5(0) ^ self.blackboard.blDEFINE5(0)))) ^ (False ^ True)))), (23 <= min(100, max(-100, max(46, 5)))), (self.envVAR1[0] > ([(self.envDEFINE4() <= self.envVAR1[2]), ('no' != 'both')].count(True)))].count(True))))
            if False else
            (
                min(-2, max(-5, min(100, max(-100, (self.envVAR1[1] * self.envDEFINE4())))))
                if ('yes' != self.blackboard.blVAR0[1]) else
                (
                min(-2, max(-5, -18))
        )))), (min(2, max(0, min(100, max(-100, (32 - 67))))), (
            min(-2, max(-5, min(100, max(-100, (min(100, max(-100, max(([(node.localVAR2 > 70), (node.localVAR2 >= self.envDEFINE4())].count(True)), min(100, max(-100, -(node.localVAR2)))))) * min(100, max(-100, (33 - -5))))))))
            if (not ((False ^ (self.envVAR1[1] > self.envDEFINE4())))) else
            (
                min(-2, max(-5, ([(self.envDEFINE4() > self.envDEFINE4()), (node.localVAR2 >= self.envVAR1[2])].count(True))))
                if ((min(100, max(-100, abs(self.envDEFINE4()))) == self.envDEFINE4()) ^ self.blackboard.blDEFINE5(0)) else
                (
                min(-2, max(-5, 48))
        )))), (min(2, max(0, min(100, max(-100, (node.localVAR2 + 35 + min(100, max(-100, -(21)))))))), (
            min(-2, max(-5, min(100, max(-100, (-24 - self.envVAR1[1])))))
            if ((not (self.blackboard.blDEFINE5(0))) or (self.blackboard.blDEFINE5(1))) else
            (
                min(-2, max(-5, min(100, max(-100, (94 + -43 + 45 + 19)))))
                if ((not (self.blackboard.blDEFINE5(1))) or (self.blackboard.blDEFINE5(0))) else
                (
                min(-2, max(-5, min(100, max(-100, (19 + -93 + -3)))))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a3_write_after_1__2(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, min(100, max(-100, (min(100, max(-100, (min(100, max(-100, max(-3, self.envDEFINE4()))) + min(100, max(-100, max(node.localVAR2, self.envVAR1[1]))) + min(100, max(-100, max(self.envDEFINE4(), 40)))))) * min(100, max(-100, -(min(100, max(-100, abs(-73))))))))))), (
            min(-2, max(-5, min(100, max(-100, -(self.envDEFINE4())))))
            if (self.envVAR1[0] > node.localVAR2) else
            (
                min(-2, max(-5, min(100, max(-100, max(12, -21)))))
                if ((True and self.blackboard.blDEFINE5(1)) or (self.envDEFINE4() == -36)) else
                (
                min(-2, max(-5, min(100, max(-100, (([(71 <= 80), (-33 > -99), ((not (self.blackboard.blDEFINE5(0))) or (True)), (self.blackboard.blDEFINE5(1) and self.blackboard.blDEFINE5(1))].count(True)) * min(100, max(-100, (self.envDEFINE4() * -95))))))))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a3_read_after_0__condition(self, node):
        if True:
            return True
        else:
            return False


    def a3_read_after_0__0(self, node):
        return [(min(2, max(0, min(100, max(-100, abs(node.localVAR2))))), 'both'), (min(2, max(0, min(100, max(-100, max(min(100, max(-100, abs(-39))), self.envVAR1[0]))))), self.blackboard.blVAR0[2]), (min(2, max(0, ([(True ^ False), (True ^ self.blackboard.blDEFINE5(1)), (self.blackboard.blDEFINE5(0) == False), (self.blackboard.blDEFINE5(0) != self.blackboard.blDEFINE5(1))].count(True)))), self.blackboard.blVAR0[1])]

    def a4_read_after_2__condition(self, node):
        if (node.localVAR2 > -26):
            return True
        else:
            return False


    def a4_read_after_2__0(self, node):
        return min(5, max(2, min(100, max(-100, -(min(100, max(-100, (self.envDEFINE4() * self.envVAR1[2]))))))))

    def a4_read_after_2__1(self, node):
        return [(min(2, max(0, min(100, max(-100, (min(100, max(-100, (66 * 69))) * node.localVAR2))))), (
            self.blackboard.blVAR0[0]
            if (self.envVAR1[1] != -52) else
            (
            self.blackboard.blVAR0[0]
        ))), (min(2, max(0, min(100, max(-100, abs(min(100, max(-100, abs(45)))))))), (
            self.blackboard.blVAR0[0]
            if ((True and self.blackboard.blDEFINE5(1)) == False) else
            (
            'no'
        )))]

    def a4_read_after_0__condition(self, node):
        if (50 >= min(100, max(-100, max(20, 23)))):
            return True
        else:
            return False


    def a4_read_after_0__0(self, node):
        return (
            min(5, max(2, min(100, max(-100, max(node.localDEFINE3(0), -20)))))
            if ((self.blackboard.blDEFINE5(0) ^ self.blackboard.blDEFINE5(1)) or False) else
            (
                min(5, max(2, min(100, max(-100, (min(100, max(-100, max(self.envVAR1[1], self.envVAR1[0]))) * -95 * min(100, max(-100, (node.localVAR2 + node.localVAR2 + -28))) * min(100, max(-100, abs(-74))))))))
                if ((self.envDEFINE4() > self.envDEFINE4()) and (93 >= node.localVAR2)) else
                (
                min(5, max(2, node.localDEFINE3(0)))
        )))
