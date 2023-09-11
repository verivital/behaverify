import random
import serene_safe_assignment


class t13_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, 23)), (
            self.envVAR2[0]
            if (False and False) else
            (
                'yes'
                if (not ((False ^ True))) else
                (
                'no'
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, abs(max(-98, 29)))), (
            self.envVAR2[0]
            if (abs(69) >= -42) else
            (
                self.envVAR2[0]
                if ((54 >= self.envVAR4) and (self.blackboard.blVAR0 == -20)) else
                (
                self.blackboard.blDEFINE5()
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, abs(-31))), (
            self.blackboard.blDEFINE5()
            if True else
            (
            'no'
        ))), (min(2, max(0, ([(abs(self.envVAR4) > (-98 - (23 * self.blackboard.blVAR0))), (([(False != (40 < self.envVAR4)), (False ^ True), (not ((((not (True)) or (True)) ^ (not ((False ^ False)))))), (self.blackboard.blVAR0 >= -43)].count(True)) == self.envVAR4), ((True and True) and (-43 <= self.envVAR4)), ((self.envVAR4 + 91 + self.blackboard.blVAR0) <= max(-99, 36))].count(True)))), (
            'no'
            if ((not (True)) or (False)) else
            (
            self.blackboard.blDEFINE5()
        ))), (min(2, max(0, -47)), (
            'yes'
            if (([(self.envVAR4 != (45 - 27)), (False != True), ((True ^ False) != (self.blackboard.blVAR0 <= self.envVAR4))].count(True)) > ([(True ^ False), (self.envVAR2[1] != 'no'), (self.envVAR4 <= self.blackboard.blVAR0), (True or True)].count(True))) else
            (
            self.blackboard.blVAR3[0]
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR4 = serene_safe_assignment.envVAR4(min(5, max(2, (min(-13, -24) + abs(-33) + self.blackboard.blVAR0))))
        self.envVAR4 = serene_safe_assignment.envVAR4(min(5, max(2, -99)))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, 'both'), (1, (
            'both'
            if (-93 >= self.blackboard.blVAR0) else
            (
                'both'
                if (False and False) else
                (
                'no'
        )))), (2, 'no')])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR2 = [None] * 2
        __temp_var__ = serene_safe_assignment.envVAR2([(0, 'yes'), (1, (
            'no'
            if True else
            (
            self.envVAR1[0]
        )))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        self.envVAR4 = serene_safe_assignment.envVAR4(min(5, max(2, abs(-(self.blackboard.blVAR0)))))

    def a2_write_before_0__0(self, node):
        self.envVAR4 = serene_safe_assignment.envVAR4((
            min(5, max(2, (-(self.envVAR4) * -59 * -90)))
            if (node.localDEFINE7() <= self.blackboard.blVAR0) else
            (
                min(5, max(2, (-47 * -(self.envVAR4))))
                if (not ((('no' != self.blackboard.blVAR3[1]) ^ (9 != (-21 - -99))))) else
                (
                min(5, max(2, min(self.blackboard.blVAR0, node.localDEFINE7())))
        ))))
        return

    def a2_write_after_0__0(self, node):
        self.envVAR4 = serene_safe_assignment.envVAR4(min(5, max(2, 21)))
        return

    def a2_write_after_0__1(self, node):
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, (-59 + node.localDEFINE7() + -55 + 92))), (
            'yes'
            if ((False != True) ^ ((self.envVAR4 > self.blackboard.blVAR0) and False)) else
            (
                self.envVAR2[1]
                if (True or (node.localDEFINE7() >= self.envVAR4)) else
                (
                'both'
        )))), (min(1, max(0, -45)), (
            self.envVAR2[1]
            if False else
            (
                'no'
                if (True == False) else
                (
                self.blackboard.blVAR3[1]
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        return

    def a3_read_before_2__condition(self, node):
        if (self.envVAR1[2] != 'both'):
            return True
        else:
            return False


    def a3_read_before_2__0(self, node):
        return [(min(1, max(0, -((76 * -36 * self.envVAR4 * -22)))), (
            'no'
            if (max(29, min(self.blackboard.blVAR0, -26)) < ([((node.localDEFINE7() <= node.localDEFINE7()) ^ (False == True)), (False or False)].count(True))) else
            (
            self.envVAR2[1]
        ))), (min(1, max(0, max(node.localDEFINE7(), self.envVAR4))), (
            'both'
            if (not (((True != True) ^ (-8 < 36)))) else
            (
            self.envVAR1[2]
        )))]

    def a3_read_before_0__condition(self, node):
        if True:
            return True
        else:
            return False


    def a3_read_before_0__0(self, node):
        return (
            min(5, max(2, 38))
            if (False and True) else
            (
            min(5, max(2, abs(node.localDEFINE7())))
        ))

    def a3_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, max((32 - self.blackboard.blVAR0), (self.blackboard.blVAR0 - 45)))), (
            self.blackboard.blDEFINE5()
            if ((True == True) and False) else
            (
                'no'
                if (node.localDEFINE7() < -(-28)) else
                (
                'both'
        )))), (min(1, max(0, min(66, -91))), (
            'both'
            if ((not (True)) or (True)) else
            (
                'both'
                if (-3 > self.envVAR4) else
                (
                'both'
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        return

    def a4_read_after_0__condition(self, node):
        if ((False and True) == (self.envVAR4 != node.localDEFINE6(2))):
            return True
        else:
            return False


    def a4_read_after_0__0(self, node):
        return (
            min(5, max(2, 36))
            if (((False and False) ^ False) == (True == False)) else
            (
                min(5, max(2, self.envVAR4))
                if (False == True) else
                (
                min(5, max(2, -(max(-89, node.localDEFINE6(2)))))
        )))
