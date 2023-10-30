import random
import serene_safe_assignment


class t287_environment():
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
        self.envVAR4 = serene_safe_assignment.envVAR4((
            min(5, max(2, self.blackboard.blDEFINE6(max(0, min(2, (-45))))))
            if (self.envDEFINE7() and (False ^ self.blackboard.blVAR0)) else
            (
                min(5, max(2, (min(50, max((-50), -((-15)))))))
                if ((min(50, max((-50), (self.blackboard.blDEFINE8() - self.blackboard.blDEFINE8())))) <= (min(50, max((-50), (self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5() + 9 + 27))))) else
                (
                min(5, max(2, (min(50, max((-50), (self.envVAR4 + self.envVAR4 + (min(50, max((-50), (((-5) if (self.blackboard.blVAR0 and self.envDEFINE7()) else self.blackboard.blDEFINE8()) - ((-5) if (self.blackboard.blVAR0 and self.envDEFINE7()) else self.blackboard.blDEFINE8()))))) + 2))))))
        ))))
        self.envVAR1 = serene_safe_assignment.envVAR1(min((-2), max((-5), (-33))))
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), ([(self.envDEFINE7() == (13 <= (-44))), ((min(50, max((-50), (self.blackboard.blDEFINE6(max(0, min(2, self.blackboard.blDEFINE8()))) * self.blackboard.blDEFINE6(max(0, min(2, self.blackboard.blDEFINE8()))) * self.blackboard.blDEFINE6(max(0, min(2, self.blackboard.blDEFINE8()))))))) > (min(50, max((-50), ((-12) - (-12)))))), (True ^ self.envDEFINE7())].count(True))))
            if ((True and False) ^ self.envDEFINE7()) else
            (
                min((-2), max((-5), 31))
                if (self.blackboard.blDEFINE8() >= self.blackboard.blDEFINE5()) else
                (
                min((-2), max((-5), (([(2 <= 14), (self.envDEFINE7() == self.blackboard.blVAR0), ((self.envDEFINE7() == self.blackboard.blVAR0) ^ ((-2) == (-46)))].count(True)) if ((min(50, max((-50), max(self.envVAR1, self.envVAR1)))) > ((min(50, max((-50), (42 - 42)))) if ((17 >= 20) == (self.envVAR1 < self.blackboard.blDEFINE5())) else (self.envVAR4 if (self.envVAR4 >= 10) else (-2)))) else (min(50, max((-50), min(([(not ((False ^ self.blackboard.blVAR0))), ((-17) != (-10)), (16 <= self.envVAR4), (False or self.envDEFINE7())].count(True)), self.blackboard.blDEFINE8())))))))
        ))))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), (min(50, max((-50), -((min(50, max((-50), min((min(50, max((-50), (28 * 28 * 44 * (-2))))), (-3)))))))))))
            if (((-5) if (25 > (-35)) else (-3)) > (min(50, max((-50), (29 + 5 + 11))))) else
            (
                min((-2), max((-5), (-3)))
                if True else
                (
                min((-2), max((-5), (min(50, max((-50), ((-16) + (-41)))))))
        ))))
        self.envVAR4 = serene_safe_assignment.envVAR4((
            min(5, max(2, 16))
            if False else
            (
            min(5, max(2, (min(50, max((-50), (self.envVAR1 - (min(50, max((-50), (self.envVAR1 - self.envVAR1))))))))))
        )))


        def envDEFINE7():
            return (((not self.blackboard.blVAR0) or True) == self.blackboard.blVAR0)

        self.envDEFINE7 = envDEFINE7

    def a1_read_before_0__condition(self, node):
        if self.envDEFINE7():
            return True
        else:
            return False


    def a1_read_before_0__0(self, node):
        return (
            ((min(50, max((-50), max((-23), 16)))) > self.blackboard.blDEFINE8())
            if (11 < 8) else
            (
                (37 < self.blackboard.blDEFINE6(max(0, min(2, (-39)))))
                if ((min(50, max((-50), max(20, self.blackboard.blDEFINE5())))) != (min(50, max((-50), max(self.envVAR1, self.envVAR1))))) else
                (
                ((-2) != self.envVAR1)
        )))

    def a1_read_before_0__1(self, node):
        return (
            (self.blackboard.blDEFINE5() <= (min(50, max((-50), min(self.blackboard.blDEFINE8(), self.blackboard.blDEFINE8())))))
            if ((self.blackboard.blDEFINE8() == (-16)) == ((self.blackboard.blDEFINE6(max(0, min(2, self.blackboard.blDEFINE5()))) >= 3) and (self.blackboard.blVAR0 == self.envDEFINE7()))) else
            (
                True
                if (self.envVAR1 > (-21)) else
                (
                self.envDEFINE7()
        )))

    def a1_read_before_0__2(self, node):
        return (
            (not ((False ^ (not ((False ^ False))))))
            if (20 < (-34)) else
            (
                ((min(50, max((-50), ((-17) + (-17) + (-17))))) != (-1))
                if (self.envDEFINE7() and self.blackboard.blVAR0) else
                (
                (self.envVAR1 >= self.blackboard.blDEFINE5())
        )))

    def a2_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), (-10)))
            if (not ((self.blackboard.blVAR0 ^ ((self.envVAR4 if (self.blackboard.blVAR0 and True) else self.envVAR1) > 16)))) else
            (
                min((-2), max((-5), 15))
                if ((min(50, max((-50), max(self.blackboard.blDEFINE5(), self.blackboard.blDEFINE5())))) >= (8 if (self.blackboard.blVAR0 != False) else self.envVAR1)) else
                (
                min((-2), max((-5), ([(not ((False ^ self.blackboard.blVAR0))), (self.blackboard.blDEFINE6(max(0, min(2, (-48)))) == self.envVAR4), (self.blackboard.blVAR0 or True)].count(True))))
        ))))
        return

    def a2_write_after_0__1(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), ([(self.envDEFINE7() or self.blackboard.blVAR0), (self.envVAR4 <= (-17)), (self.blackboard.blVAR0 == self.blackboard.blVAR0), (self.envDEFINE7() and True)].count(True))))
            if ((min(50, max((-50), (self.blackboard.blDEFINE5() + (-24) + (-24))))) <= (-18)) else
            (
                min((-2), max((-5), (min(50, max((-50), -((min(50, max((-50), abs((-36)))))))))))
                if (([((10 if (True == self.blackboard.blVAR0) else (-18)) <= (min(50, max((-50), (self.blackboard.blDEFINE8() * self.blackboard.blDEFINE8() * 2 * 2))))), ((not (False == self.blackboard.blVAR0)) or self.blackboard.blVAR0), (26 == self.blackboard.blDEFINE5())].count(True)) <= self.blackboard.blDEFINE5()) else
                (
                min((-2), max((-5), (min(50, max((-50), (((-39) if (self.blackboard.blDEFINE5() < self.blackboard.blDEFINE5()) else 15) + (min(50, max((-50), (self.blackboard.blDEFINE6(max(0, min(2, (-39)))) * self.blackboard.blDEFINE6(max(0, min(2, (-39)))) * self.blackboard.blDEFINE6(max(0, min(2, (-39)))))))) + (min(50, max((-50), (self.blackboard.blDEFINE6(max(0, min(2, (-39)))) * self.blackboard.blDEFINE6(max(0, min(2, (-39)))) * self.blackboard.blDEFINE6(max(0, min(2, (-39))))))))))))))
        ))))
        return

    def a2_write_after_0__2(self, node):
        self.envVAR4 = serene_safe_assignment.envVAR4(min(5, max(2, ([((self.blackboard.blDEFINE8() <= node.localVAR2[serene_safe_assignment.index_func(max(0, min(2, self.envVAR1)), 3)]) and True), ((self.envVAR4 >= self.blackboard.blDEFINE5()) == False), (((-7) > self.envVAR4) == (31 >= (-40)))].count(True)))))
        return

    def a3_read_after_0__condition(self, node):
        if (not ((True ^ self.blackboard.blVAR0))):
            return True
        else:
            return False


    def a3_read_after_0__0(self, node):
        return [(0, (
                    min((-2), max((-5), (min(50, max((-50), max(14, (min(50, max((-50), max(47, 47))))))))))
                    if (self.blackboard.blVAR0 and (self.blackboard.blVAR0 != (28 == self.blackboard.blDEFINE5()))) else
                    (
                        min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), (3 * 3 * 24)))) + (min(50, max((-50), (3 * 3 * 24)))) + (min(50, max((-50), ((-6) * (-6) * (-6))))) + (min(50, max((-50), (node.localVAR2[serene_safe_assignment.index_func(max(0, min(2, 22)), 3)] - (-29)))))))))))
                        if ((False == False) and self.envDEFINE7()) else
                        (
                        min((-2), max((-5), (min(50, max((-50), -(self.blackboard.blDEFINE5()))))))
                )))), (1, (
                    min((-2), max((-5), (min(50, max((-50), max(14, (min(50, max((-50), max(47, 47))))))))))
                    if (self.blackboard.blVAR0 and (self.blackboard.blVAR0 != (28 == self.blackboard.blDEFINE5()))) else
                    (
                        min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), (3 * 3 * 24)))) + (min(50, max((-50), (3 * 3 * 24)))) + (min(50, max((-50), ((-6) * (-6) * (-6))))) + (min(50, max((-50), (node.localVAR2[serene_safe_assignment.index_func(max(0, min(2, 22)), 3)] - (-29)))))))))))
                        if ((False == False) and self.envDEFINE7()) else
                        (
                        min((-2), max((-5), (min(50, max((-50), -(self.blackboard.blDEFINE5()))))))
                ))))]

    def a4_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), self.blackboard.blDEFINE6(max(0, min(2, (-20))))))
            if ((-49) < (-20)) else
            (
                min((-2), max((-5), (min(50, max((-50), max((-28), self.blackboard.blDEFINE8()))))))
                if ((not (False == self.blackboard.blVAR0)) or ((self.blackboard.blVAR0 == self.envDEFINE7()) ^ self.blackboard.blVAR0)) else
                (
                min((-2), max((-5), (min(50, max((-50), -(self.envVAR1))))))
        ))))
        return

    def a4_write_after_0__1(self, node):
        self.envVAR4 = serene_safe_assignment.envVAR4((
            min(5, max(2, (min(50, max((-50), ((min(50, max((-50), ((-43) - (-31))))) - (min(50, max((-50), ((-43) - (-31)))))))))))
            if (23 >= (min(50, max((-50), -(14))))) else
            (
                min(5, max(2, (-41)))
                if ((min(50, max((-50), max(self.blackboard.blDEFINE8(), (-10))))) >= node.localVAR2[serene_safe_assignment.index_func(max(0, min(2, (-2))), 3)]) else
                (
                min(5, max(2, (-36)))
        ))))
        return
