import random
import serene_safe_assignment


class t10_environment():
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
            min(5, max(2, self.blackboard.blDEFINE5(1)))
            if (False or (self.blackboard.blDEFINE5(0) < self.blackboard.blDEFINE5(0))) else
            (
            min(5, max(2, ([(False ^ True), (True or False), (False != False), (True and False)].count(True))))
        )))
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, (-45 * -66 * -14)))
            if False else
            (
            min(5, max(2, max(min(50, ([(7 > 37), (not ((False ^ True))), (False ^ True)].count(True))), self.blackboard.blDEFINE5(0))))
        )))
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, (self.blackboard.blDEFINE5(0) + ((41 + -36) + self.blackboard.blDEFINE5(0) + self.blackboard.blDEFINE5(0) + -(self.envVAR1)) + (([(-10 >= self.envVAR1), (self.envVAR1 < self.envVAR1), ((not (False)) or (False))].count(True)) + self.blackboard.blDEFINE5(1)) + 18)))
            if ((not (True)) or (True)) else
            (
            min(5, max(2, (54 * self.blackboard.blDEFINE5(1))))
        )))
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, min(66, 31)))
            if True else
            (
                min(5, max(2, min(self.envVAR1, self.blackboard.blDEFINE5(0))))
                if (-81 <= self.blackboard.blDEFINE5(1)) else
                (
                min(5, max(2, self.envVAR1))
        ))))
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, -((self.blackboard.blDEFINE5(1) * 86 * 53)))))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, ([((not ((5 > 5))) or (False)), (4 <= -(-87)), ((max(-34, -87) - max(-3, -84)) < (-4 + -2 + -5 + 3)), (True ^ (94 < abs(-2)))].count(True))))
            if True else
            (
            min(5, max(2, -(-3)))
        )))

    def a1_read_before_0__condition(self, node):
        if (not (((True or True) ^ (True and True)))):
            return True
        else:
            return False


    def a1_read_before_0__0(self, node):
        return [(min(2, max(0, ([((95 - -68) <= max(node.localVAR2[0], -92)), (False == (False or False))].count(True)))), (
            min(5, max(2, (-34 + -96 + self.envVAR1)))
            if True else
            (
                min(5, max(2, ((max(85, node.localDEFINE6(0)) + 95 + max(2, -17)) - (node.localDEFINE6(1) * -(self.blackboard.blDEFINE5(1)) * ([(True == False), (True and False)].count(True))))))
                if ((min(79, self.blackboard.blDEFINE5(1)) <= max(-70, node.localVAR2[2])) == False) else
                (
                min(5, max(2, min(15, node.localDEFINE6(1))))
        )))), (min(2, max(0, (self.envVAR1 * self.blackboard.blDEFINE5(1)))), (
            min(5, max(2, ([((node.localDEFINE6(0) + self.envVAR1 + self.blackboard.blDEFINE5(1)) < -77), ((True or True) == False), ((not (True)) or (False))].count(True))))
            if (node.localDEFINE4() != self.blackboard.blVAR0[1]) else
            (
                min(5, max(2, abs(node.localDEFINE6(1))))
                if (not (((-35 > self.envVAR1) ^ True))) else
                (
                min(5, max(2, -27))
        )))), (min(2, max(0, self.envVAR1)), (
            min(5, max(2, self.envVAR1))
            if (16 > min(self.envVAR1, node.localDEFINE6(0))) else
            (
                min(5, max(2, -80))
                if False else
                (
                min(5, max(2, abs(58)))
        ))))]

    def a4_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, ([(False == (self.envVAR1 < self.envVAR1)), (True == ((not (True)) or (True)))].count(True)))))
        return
