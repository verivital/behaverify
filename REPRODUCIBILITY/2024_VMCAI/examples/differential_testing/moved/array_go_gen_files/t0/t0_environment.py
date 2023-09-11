import random
import serene_safe_assignment


class t0_environment():
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
            min(-2, max(-5, ([(self.envVAR1 >= 53), ((not (True)) or ((True ^ True))), ((not (False)) or ((False == False))), ((not ((93 >= self.envVAR1))) or ((min(100, max(-100, (self.blackboard.blVAR2 + self.envFROZENVAR3[1] + -17))) < self.blackboard.blDEFINE4())))].count(True))))
            if (False != True) else
            (
            min(-2, max(-5, -88))
        )))
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, min(100, max(-100, (self.envFROZENVAR3[2] - min(100, max(-100, -(self.envFROZENVAR3[2]))))))))
            if (False and self.envDEFINE5()) else
            (
            min(-2, max(-5, min(100, max(-100, (min(100, max(-100, (57 + self.envVAR1 + -37 + 75))) - self.envVAR1)))))
        )))
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, min(100, max(-100, -(self.envFROZENVAR3[1])))))
            if self.envDEFINE5() else
            (
            min(-2, max(-5, min(100, max(-100, (self.blackboard.blVAR2 + self.envVAR1)))))
        )))
        self.envVAR1 = serene_safe_assignment.envVAR1(min(-2, max(-5, min(100, max(-100, (45 + self.blackboard.blVAR0[1] + self.blackboard.blVAR2))))))
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, min(100, max(-100, abs(min(100, max(-100, (37 - self.blackboard.blVAR0[0]))))))))
            if (not ((self.envDEFINE5() ^ (-35 < -64)))) else
            (
            min(-2, max(-5, min(100, max(-100, abs(([(not ((False ^ self.envDEFINE5()))), (self.blackboard.blDEFINE4() >= -19), (self.envDEFINE5() ^ self.envDEFINE5())].count(True)))))))
        )))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE5():
            return (not (((self.envFROZENVAR3[1] != self.blackboard.blVAR0[1]) ^ True)))

        self.envDEFINE5 = envDEFINE5
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, 23))
            if (False == True) else
            (
                min(-2, max(-5, min(100, max(-100, abs(min(100, max(-100, (([((not (True)) or (True)), (-64 > self.blackboard.blVAR0[1]), (True ^ False), (self.blackboard.blVAR0[0] >= -3)].count(True)) * min(100, max(-100, max(self.blackboard.blVAR0[0], self.blackboard.blVAR0[1]))) * min(100, max(-100, abs(-43))) * min(100, max(-100, max(48, self.blackboard.blVAR0[1])))))))))))
                if (min(100, max(-100, (self.blackboard.blVAR0[0] + 32 + self.blackboard.blVAR0[0] + 22))) == min(100, max(-100, (self.blackboard.blVAR0[0] - min(100, max(-100, min(-80, self.blackboard.blVAR0[0]))))))) else
                (
                min(-2, max(-5, min(100, max(-100, -(min(100, max(-100, (self.blackboard.blVAR0[1] + ([((not (True)) or (True)), (not ((True ^ True))), (not ((True ^ False)))].count(True)) + min(100, max(-100, (-37 * self.blackboard.blVAR0[0] * self.blackboard.blVAR0[0] * 83))) + 42))))))))
        ))))
        self.envFROZENVAR3 = [None] * 3
        __temp_var__ = serene_safe_assignment.envFROZENVAR3([(0, min(5, max(2, min(100, max(-100, min(min(100, max(-100, (55 * -2))), min(100, max(-100, (41 * self.envVAR1))))))))), (1, min(5, max(2, min(100, max(-100, min(min(100, max(-100, (55 * -2))), min(100, max(-100, (41 * self.envVAR1))))))))), (2, min(5, max(2, min(100, max(-100, min(min(100, max(-100, (55 * -2))), min(100, max(-100, (41 * self.envVAR1)))))))))])
        for (index, val) in __temp_var__:
            self.envFROZENVAR3[index] = val

    def a1_read_before_0__condition(self, node):
        if (self.envFROZENVAR3[2] > self.envVAR1):
            return True
        else:
            return False


    def a1_read_before_0__0(self, node):
        return (
            min(-2, max(-5, ([((self.blackboard.blVAR0[0] < min(100, max(-100, min(self.blackboard.blVAR0[1], self.blackboard.blDEFINE4())))) == (self.envDEFINE5() == (True or False))), (min(100, max(-100, (([(False == self.envDEFINE5()), (True == self.envDEFINE5()), (self.blackboard.blVAR2 > -42)].count(True)) * -11))) >= ([(self.envDEFINE5() and False), (False == False)].count(True))), (self.envDEFINE5() or (self.envVAR1 <= 44))].count(True))))
            if (78 < -99) else
            (
                min(-2, max(-5, min(100, max(-100, max(min(100, max(-100, min(self.envVAR1, self.blackboard.blVAR0[1]))), min(100, max(-100, min(self.envVAR1, self.blackboard.blDEFINE4()))))))))
                if False else
                (
                min(-2, max(-5, ([(min(100, max(-100, (([(self.envDEFINE5() ^ True), (self.envDEFINE5() != self.envDEFINE5()), (self.envFROZENVAR3[1] < 60)].count(True)) + min(100, max(-100, abs(57)))))) <= min(100, max(-100, (min(100, max(-100, min(self.envVAR1, 99))) * ([(-42 == self.blackboard.blVAR2), (self.envDEFINE5() != False), (self.envVAR1 >= self.blackboard.blVAR0[0]), (False == False)].count(True)) * -17)))), (((self.blackboard.blDEFINE4() >= self.blackboard.blVAR0[1]) and (False ^ True)) and self.envDEFINE5())].count(True))))
        )))

    def a1_write_after_1__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, min(100, max(-100, max(self.blackboard.blVAR0[0], self.envFROZENVAR3[1])))))
            if ((not (self.envDEFINE5())) or ((97 < self.envVAR1))) else
            (
            min(-2, max(-5, min(100, max(-100, (self.envFROZENVAR3[1] - self.envVAR1)))))
        )))
        return

    def a1_write_after_1__1(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(-2, max(-5, min(100, max(-100, abs(85))))))
        return

    def a1_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, min(100, max(-100, -(self.envVAR1)))))
            if ((not (self.envDEFINE5())) or (True)) else
            (
            min(-2, max(-5, min(100, max(-100, abs(-50)))))
        )))
        return

    def a2_read_before_0__condition(self, node):
        if (-39 != -61):
            return True
        else:
            return False


    def a2_read_before_0__0(self, node):
        return [(min(1, max(0, min(100, max(-100, abs(self.blackboard.blVAR2))))), min(5, max(2, min(100, max(-100, max(self.blackboard.blDEFINE4(), min(100, max(-100, -(46)))))))))]

    def a2_read_before_0__1(self, node):
        return min(-2, max(-5, 38))

    def a4_read_after_0__condition(self, node):
        if (min(100, max(-100, -(81))) != min(100, max(-100, abs(self.blackboard.blVAR2)))):
            return True
        else:
            return False


    def a4_read_after_0__0(self, node):
        return [(min(1, max(0, min(100, max(-100, (self.envFROZENVAR3[0] * 3 * -78))))), (
            min(5, max(2, min(100, max(-100, (-25 - min(100, max(-100, max(self.blackboard.blDEFINE4(), 32))))))))
            if (not (((self.blackboard.blVAR0[0] < -66) ^ (71 > -2)))) else
            (
            min(5, max(2, min(100, max(-100, (([(63 >= self.envVAR1), (self.blackboard.blDEFINE4() >= 36), (self.envDEFINE5() and False)].count(True)) + 71 + self.envVAR1)))))
        ))), (min(1, max(0, min(100, max(-100, (-5 - ([(81 >= self.blackboard.blVAR2), (self.blackboard.blDEFINE4() < -43)].count(True))))))), (
            min(5, max(2, min(100, max(-100, -(min(100, max(-100, (self.blackboard.blVAR0[1] * min(100, max(-100, (self.blackboard.blVAR2 + self.blackboard.blVAR0[0])))))))))))
            if ((8 >= -63) or (self.blackboard.blVAR0[0] <= -5)) else
            (
            min(5, max(2, min(100, max(-100, (51 * 98 * self.blackboard.blDEFINE4())))))
        )))]
