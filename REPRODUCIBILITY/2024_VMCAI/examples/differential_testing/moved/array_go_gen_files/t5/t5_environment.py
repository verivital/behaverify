import random
import serene_safe_assignment


class t5_environment():
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



        def envDEFINE7():
            return (
                'no'
                if (False == False) else
                (
                'both'
            ))

        self.envDEFINE7 = envDEFINE7
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, min(93, max(-91, 27))))
            if (4 < 5) else
            (
                min(5, max(2, ([(((-2 - -27) + ([(-14 <= 4), (True == False), (-4 != 3), ((not (True)) or (False))].count(True)) + (2 * 2 * 4 * -22)) > (-66 + -23 + -5 + -88)), ((not ((self.blackboard.blVAR0 != 'yes'))) or ((False == False)))].count(True))))
                if (False ^ False) else
                (
                min(5, max(2, (-60 * -81 * 4)))
        ))))
        self.envFROZENVAR5 = serene_safe_assignment.envFROZENVAR5(min(5, max(2, (self.envVAR1 - -87))))

    def a1_read_before_2__condition(self, node):
        if (True ^ False):
            return True
        else:
            return False


    def a1_read_before_2__0(self, node):
        return (
            min(5, max(2, max(self.blackboard.blFROZENVAR4[0], self.envVAR1)))
            if True else
            (
                min(5, max(2, (91 - self.envVAR1)))
                if ((not (False)) or ((self.envDEFINE7() != 'both'))) else
                (
                min(5, max(2, abs(abs(-82))))
        )))

    def a1_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, self.blackboard.blDEFINE6()))
            if ((not ((True ^ True))) == (True == False)) else
            (
                min(5, max(2, self.envVAR1))
                if (37 >= (33 - -24)) else
                (
                min(5, max(2, -28))
        ))))
        return

    def a1_write_before_0__1(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, 20))
            if (((not ((False ^ True))) == (True and False)) ^ False) else
            (
                min(5, max(2, ([(self.envDEFINE7() != self.envDEFINE7()), (81 <= max(self.envVAR1, 60)), (True and (-25 < 78))].count(True))))
                if (((not (False)) or (False)) and (True ^ False)) else
                (
                min(5, max(2, (-77 - self.blackboard.blFROZENVAR4[1])))
        ))))
        return

    def a1_read_after_0__condition(self, node):
        if (True and (True ^ True)):
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return (
            'no'
            if (not ((True ^ (self.blackboard.blDEFINE6() < -62)))) else
            (
            'both'
        ))

    def a2_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, node.localVAR2))
            if (-86 <= self.envFROZENVAR5) else
            (
            min(5, max(2, (abs(node.localVAR2) * -35)))
        )))
        return

    def a3_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, max(self.envVAR1, 74)))
            if False else
            (
                min(5, max(2, ((self.blackboard.blDEFINE6() * self.envVAR1 * 90) - abs(-98))))
                if (False and True) else
                (
                min(5, max(2, 4))
        ))))
        return

    def a3_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, (-(self.blackboard.blFROZENVAR4[1]) + abs(69) + self.blackboard.blDEFINE6() + (27 * max(18, 78)))))
            if (min(-4, self.blackboard.blDEFINE6()) > -(38)) else
            (
            min(5, max(2, -(abs(self.blackboard.blFROZENVAR4[0]))))
        )))
        return
