import random
import serene_safe_assignment


class t17_environment():
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



        def envDEFINE6():
            return (
                True
                if self.envVAR4 else
                (
                (self.blackboard.blDEFINE5() < self.blackboard.blVAR0[2])
            ))

        self.envDEFINE6 = envDEFINE6
        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            'yes'
            if ((self.blackboard.blVAR0[1] + -7) < abs(-94)) else
            (
            'yes'
        ))), (1, (
            'yes'
            if (True == True) else
            (
                'yes'
                if ((not ((True or True))) or (('no' == 'both'))) else
                (
                'no'
        )))), (2, (
            'yes'
            if (True != False) else
            (
                'yes'
                if False else
                (
                'no'
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR2 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR2([(0, (
            'no'
            if (False or (True or True)) else
            (
                self.envVAR1[0]
                if ((not (True)) or (False)) else
                (
                'both'
        )))), (1, (
            self.envVAR1[1]
            if ('both' != 'no') else
            (
                self.envVAR1[2]
                if (92 < (([(False != True), (True and True)].count(True)) - ([(True or False), (-54 >= 40), (True != True), (self.blackboard.blVAR0[1] >= self.blackboard.blVAR0[1])].count(True)))) else
                (
                'both'
        )))), (2, (
            'both'
            if ((not (False)) or ((self.blackboard.blVAR0[1] < self.blackboard.blVAR0[2]))) else
            (
                self.envVAR1[0]
                if False else
                (
                self.envVAR1[1]
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        self.envVAR4 = serene_safe_assignment.envVAR4((
            (16 > -20)
            if ((self.blackboard.blVAR0[2] - self.blackboard.blVAR0[0]) != ([(False ^ (False ^ False)), (False or (False == False))].count(True))) else
            (
                (not ((True ^ True)))
                if (True and False) else
                (
                ((not (False)) or ((97 > self.blackboard.blVAR0[0])))
        ))))

    def a1_read_before_0__condition(self, node):
        if ((not ((not ((((not (False)) or (self.envDEFINE6())) ^ (self.envDEFINE6() or self.envVAR4)))))) or ((-26 > -97))):
            return True
        else:
            return False


    def a1_read_before_0__0(self, node):
        return [(min(2, max(0, ([(self.blackboard.blVAR0[2] < min(-22, self.blackboard.blVAR0[1])), (self.blackboard.blDEFINE5() <= self.blackboard.blDEFINE5())].count(True)))), min(-2, max(-5, 19)))]

    def a2_write_after_1__0(self, node):
        self.envVAR4 = serene_safe_assignment.envVAR4((
            (self.blackboard.blVAR0[1] >= min(self.blackboard.blDEFINE5(), self.blackboard.blDEFINE5()))
            if (self.envVAR4 ^ False) else
            (
            (False or self.envVAR4)
        )))
        return

    def a3_read_before_1__condition(self, node):
        if (False ^ self.envDEFINE6()):
            return True
        else:
            return False


    def a3_read_before_1__0(self, node):
        return [(min(2, max(0, (30 * -15 * -(-93)))), (
            min(-2, max(-5, self.blackboard.blDEFINE5()))
            if False else
            (
                min(-2, max(-5, 33))
                if (max(41, 12) > max(-12, self.blackboard.blVAR0[0])) else
                (
                min(-2, max(-5, -((76 - min(self.blackboard.blDEFINE5(), -47)))))
        )))), (min(2, max(0, max(89, -12))), (
            min(-2, max(-5, abs(-84)))
            if (31 >= ([(self.blackboard.blDEFINE5() != 24), (self.envVAR4 and self.envVAR4), (self.blackboard.blDEFINE5() < self.blackboard.blDEFINE5()), (-49 < self.blackboard.blDEFINE5())].count(True))) else
            (
                min(-2, max(-5, max(98, self.blackboard.blDEFINE5())))
                if (False != True) else
                (
                min(-2, max(-5, ([(self.envVAR4 == self.envVAR4), (-72 >= self.blackboard.blVAR0[2])].count(True))))
        )))), (min(2, max(0, self.blackboard.blVAR0[1])), (
            min(-2, max(-5, -(-13)))
            if (self.envVAR1[1] == 'both') else
            (
                min(-2, max(-5, ([(-91 <= self.blackboard.blVAR0[2]), (self.blackboard.blVAR0[1] < self.blackboard.blVAR0[2]), (self.envDEFINE6() and self.envDEFINE6()), ((not (False)) or (False))].count(True))))
                if (84 != (51 + self.blackboard.blDEFINE5() + self.blackboard.blDEFINE5() + 33)) else
                (
                min(-2, max(-5, -(self.blackboard.blVAR0[1])))
        ))))]

    def a3_read_before_0__condition(self, node):
        if (([(self.envVAR4 == self.envDEFINE6()), (self.blackboard.blDEFINE5() >= self.blackboard.blDEFINE5()), (True == self.envDEFINE6())].count(True)) >= -(self.blackboard.blDEFINE5())):
            return True
        else:
            return False


    def a3_read_before_0__0(self, node):
        return [(min(2, max(0, 96)), (
            min(-2, max(-5, 56))
            if (self.envVAR4 and (False != False)) else
            (
                min(-2, max(-5, -(([(False or self.envDEFINE6()), (False == self.envDEFINE6()), ((not (self.envDEFINE6())) or (True)), ((not (False)) or (True))].count(True)))))
                if (True ^ True) else
                (
                min(-2, max(-5, -(self.blackboard.blVAR0[0])))
        )))), (min(2, max(0, abs(self.blackboard.blDEFINE5()))), (
            min(-2, max(-5, 63))
            if False else
            (
                min(-2, max(-5, ([(self.envDEFINE6() == False), (-83 >= 10), (self.blackboard.blDEFINE5() < self.blackboard.blVAR0[2])].count(True))))
                if self.envDEFINE6() else
                (
                min(-2, max(-5, -33))
        ))))]

    def a3_read_after_0__condition(self, node):
        if (True ^ True):
            return True
        else:
            return False


    def a3_read_after_0__0(self, node):
        return [(min(2, max(0, -(max(-52, -32)))), (
            min(-2, max(-5, (-42 * self.blackboard.blVAR0[0] * -58)))
            if (False and False) else
            (
            min(-2, max(-5, -(self.blackboard.blDEFINE5())))
        )))]
