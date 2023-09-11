import random
import serene_safe_assignment


class t15_environment():
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

        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, -64)))

    def a1_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, (node.localDEFINE5() - self.blackboard.blVAR0)))
            if True else
            (
                min(5, max(2, (-6 + -68 + -80)))
                if False else
                (
                min(5, max(2, (min(-98, self.blackboard.blVAR0) * -(-62))))
        ))))
        return

    def a1_read_after_0__condition(self, node):
        if ('both' != 'no'):
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return min(5, max(2, (-54 + self.blackboard.blFROZENVAR3 + node.localDEFINE5())))

    def a2_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, (-58 * (93 - self.blackboard.blDEFINE4(1)) * self.blackboard.blFROZENVAR3))))
        return

    def a2_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, abs(min(self.blackboard.blDEFINE4(1), 63)))))
        return

    def a3_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, self.blackboard.blFROZENVAR3)))
        return

    def a3_write_after_1__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, self.blackboard.blVAR0))
            if (not ((True ^ False))) else
            (
                min(5, max(2, (-(self.blackboard.blVAR0) - self.blackboard.blFROZENVAR3)))
                if True else
                (
                min(5, max(2, 85))
        ))))
        return

    def a3_write_after_1__1(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(5, max(2, self.blackboard.blDEFINE4(1)))
            if True else
            (
            min(5, max(2, (-24 * (67 * -68 * 29) * -77)))
        )))
        return

    def a4_read_before_1__condition(self, node):
        if (-22 <= (self.blackboard.blFROZENVAR3 * -86 * self.blackboard.blDEFINE4(0))):
            return True
        else:
            return False


    def a4_read_before_1__0(self, node):
        return (
            'both'
            if True else
            (
                'no'
                if (not ((True ^ (False != True)))) else
                (
                node.localVAR2
        )))

    def a4_read_before_1__1(self, node):
        return (
            'both'
            if False else
            (
            'yes'
        ))

    def a4_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(5, max(2, (self.blackboard.blVAR0 - abs(80)))))
        return
