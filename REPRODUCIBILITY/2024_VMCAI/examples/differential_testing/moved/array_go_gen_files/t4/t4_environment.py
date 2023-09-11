import random
import serene_safe_assignment


class t4_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, max(self.blackboard.blDEFINE5(), self.envVAR1[0]))), (
            min(5, max(2, self.envVAR1[0]))
            if (self.envVAR1[1] != abs(95)) else
            (
                min(5, max(2, (self.blackboard.blVAR0[0] - self.blackboard.blVAR0[1])))
                if (self.envVAR1[0] >= -68) else
                (
                min(5, max(2, -(41)))
        )))), (min(1, max(0, -14)), (
            min(5, max(2, ([((self.blackboard.blDEFINE5() + -47 + -100 + self.blackboard.blDEFINE5()) <= 4), ((not (((not (True)) or (False)))) or ((True or False))), (max(self.envVAR1[0], self.blackboard.blVAR0[1]) != 90), (abs(-58) != (99 + -64 + self.blackboard.blVAR0[0] + 79))].count(True))))
            if True else
            (
                min(5, max(2, (self.envVAR1[1] * -14 * -4 * self.envVAR1[0])))
                if (self.envVAR1[1] > 26) else
                (
                min(5, max(2, self.blackboard.blVAR0[0]))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, 81)), min(5, max(2, max(self.blackboard.blDEFINE5(), self.envVAR1[0]))))])
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
            min(5, max(2, min(self.blackboard.blVAR0[0], 72)))
            if True else
            (
                min(5, max(2, min(([(False == True), (False and True), (False == True), (False or True)].count(True)), max(max(-6, 50), ([(-55 >= self.blackboard.blVAR0[1]), (False == False), (True or False), (self.blackboard.blVAR0[1] > self.blackboard.blVAR0[1])].count(True))))))
                if False else
                (
                min(5, max(2, min(min(self.blackboard.blVAR0[0], -89), -50)))
        )))), (1, (
            min(5, max(2, min(self.blackboard.blVAR0[0], 72)))
            if True else
            (
                min(5, max(2, min(([(False == True), (False and True), (False == True), (False or True)].count(True)), max(max(-6, 50), ([(-55 >= self.blackboard.blVAR0[1]), (False == False), (True or False), (self.blackboard.blVAR0[1] > self.blackboard.blVAR0[1])].count(True))))))
                if False else
                (
                min(5, max(2, min(min(self.blackboard.blVAR0[0], -89), -50)))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val

    def a1_write_after_1__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, self.envVAR1[0])), min(5, max(2, abs(77)))), (min(1, max(0, min(19, self.blackboard.blDEFINE5()))), min(5, max(2, min(-60, self.envVAR1[1]))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a1_write_after_1__1(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, 85)), min(5, max(2, min(self.blackboard.blDEFINE5(), (-81 + 85))))), (min(1, max(0, 15)), min(5, max(2, -(50))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a1_write_after_1__2(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, self.blackboard.blDEFINE5())), (
            min(5, max(2, -(71)))
            if ((84 <= self.blackboard.blDEFINE5()) == False) else
            (
                min(5, max(2, -((self.blackboard.blVAR0[0] - self.envVAR1[0]))))
                if (False and True) else
                (
                min(5, max(2, self.envVAR1[1]))
        )))), (min(1, max(0, node.localDEFINE4(1))), (
            min(5, max(2, (49 + node.localDEFINE4(0))))
            if (not ((False ^ (node.localVAR3 and False)))) else
            (
                min(5, max(2, ((-48 * -79 * -62 * 59) + min(self.envVAR1[1], -78))))
                if node.localVAR3 else
                (
                min(5, max(2, self.blackboard.blVAR0[1]))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a1_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, -(self.blackboard.blVAR0[1]))), min(5, max(2, ([((-92 <= self.blackboard.blDEFINE5()) == (self.blackboard.blVAR0[1] > self.envVAR1[0])), (min(self.blackboard.blVAR0[1], -26) > (35 + node.localDEFINE4(0) + -82)), (False ^ (node.localVAR3 == True))].count(True))))), (min(1, max(0, abs(self.blackboard.blVAR0[0]))), min(5, max(2, 51)))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a2_read_before_0__condition(self, node):
        if ((self.blackboard.blVAR0[0] - self.blackboard.blDEFINE5()) > (self.blackboard.blDEFINE5() + -68 + node.localDEFINE4(0))):
            return True
        else:
            return False


    def a2_read_before_0__0(self, node):
        return [(min(1, max(0, -71)), min(-2, max(-5, (63 - 11))))]

    def a2_read_after_0__condition(self, node):
        if False:
            return True
        else:
            return False


    def a2_read_after_0__0(self, node):
        return [(min(1, max(0, min(abs(node.localDEFINE4(0)), self.blackboard.blVAR0[0]))), (
            min(-2, max(-5, (node.localDEFINE4(1) * node.localDEFINE4(0) * node.localDEFINE4(1) * -86)))
            if (-(80) > (self.blackboard.blDEFINE5() + -96)) else
            (
            min(-2, max(-5, ((34 - -70) - 25)))
        ))), (min(1, max(0, -30)), (
            min(-2, max(-5, (self.blackboard.blVAR0[0] * 3 * (([(False == False), (True or True), (node.localDEFINE4(0) <= self.blackboard.blDEFINE5()), (True and False)].count(True)) * (node.localDEFINE4(0) - 89) * -61) * self.blackboard.blVAR0[1])))
            if (False == ((not (False)) or (False))) else
            (
            min(-2, max(-5, self.blackboard.blVAR0[1]))
        )))]

    def a2_read_after_0__1(self, node):
        return [(min(1, max(0, abs(self.blackboard.blVAR0[0]))), (
            min(-2, max(-5, self.blackboard.blVAR0[1]))
            if True else
            (
                min(-2, max(-5, min(-(-26), -(self.envVAR1[1]))))
                if (False == True) else
                (
                min(-2, max(-5, (self.blackboard.blVAR0[0] - -8)))
        ))))]

    def a3_write_after_1__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, min(-22, self.blackboard.blVAR0[0]))), (
            min(5, max(2, abs(abs((-74 * -52 * node.localDEFINE4(0))))))
            if False else
            (
                min(5, max(2, -(node.localDEFINE4(1))))
                if node.localVAR2[0] else
                (
                min(5, max(2, self.envVAR1[1]))
        )))), (min(1, max(0, min(min(-6, -24), min(18, self.blackboard.blVAR0[0])))), (
            min(5, max(2, min(node.localDEFINE4(0), -56)))
            if node.localVAR2[0] else
            (
                min(5, max(2, (((self.blackboard.blVAR0[1] * node.localDEFINE4(0)) * node.localDEFINE4(1)) * (-(node.localDEFINE4(1)) * min(-28, 56) * ([(41 < self.envVAR1[1]), (-85 < -51)].count(True)) * node.localDEFINE4(1)))))
                if True else
                (
                min(5, max(2, (8 - -18)))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a3_write_after_1__1(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, (min(-75, -65) + ([(node.localVAR2[0] == False), ((not (node.localVAR2[0])) or (False)), (True == False), (node.localDEFINE4(0) < 51)].count(True))))), (
            min(5, max(2, ([((True ^ True) != True), (node.localDEFINE4(0) <= -57), ((-9 - self.blackboard.blVAR0[0]) < node.localDEFINE4(0)), (-62 > -94)].count(True))))
            if (node.localVAR2[1] == (node.localDEFINE4(1) == self.blackboard.blDEFINE5())) else
            (
            min(5, max(2, (abs(72) + (31 + self.blackboard.blVAR0[0]) + (node.localDEFINE4(0) * self.envVAR1[1]) + self.envVAR1[0])))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a3_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, -69)), min(5, max(2, -19)))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return
