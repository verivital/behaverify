import random
import serene_safe_assignment


class t2_environment():
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
        self.envVAR1 = serene_safe_assignment.envVAR1(True)
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE5():
            return min(-2, max(-5, -16))

        self.envDEFINE5 = envDEFINE5


        def envDEFINE6():
            return self.blackboard.blVAR2

        self.envDEFINE6 = envDEFINE6


        def envDEFINE7():
            return (
                min(5, max(2, min(100, max(-100, (min(100, max(-100, abs(min(100, max(-100, min(self.envDEFINE5(), 19)))))) - ([((self.envVAR1 ^ self.envVAR1) ^ True), (min(100, max(-100, (self.envDEFINE5() - 94))) < min(100, max(-100, min(self.blackboard.blVAR0, self.envDEFINE5())))), ((True and self.envVAR1) and ((not (True)) or (False))), ((self.envVAR1 ^ False) and self.envVAR1)].count(True)))))))
                if (self.blackboard.blVAR2 != 'yes') else
                (
                    min(5, max(2, ([((not (self.envVAR1)) or ((self.envVAR1 == True))), ((not (((self.envVAR1 and True) ^ False))) ^ ((not ((self.envVAR1 ^ False))) or (self.blackboard.blVAR0 < self.envDEFINE5())))].count(True))))
                    if (min(100, max(-100, -(0))) > min(100, max(-100, (self.envDEFINE5() * self.envDEFINE5() * self.blackboard.blVAR0 * self.envDEFINE5())))) else
                    (
                    min(5, max(2, min(100, max(-100, max(self.blackboard.blVAR0, self.envDEFINE5())))))
            )))

        self.envDEFINE7 = envDEFINE7


        def envDEFINE8(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE8: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing envDEFINE8: ' + str(index))
            if index == 0:
                return min(5, max(2, self.envDEFINE7()))
            elif index == 1:
                return (
                    min(5, max(2, min(100, max(-100, -(-91)))))
                    if ((not ((self.envVAR1 ^ self.envVAR1))) and ((not (False)) or (True))) else
                    (
                    min(5, max(2, min(100, max(-100, (78 * -16 * 72)))))
                ))
            raise Exception('Reached unreachable state when accessing envDEFINE8: ' + str(index))

        self.envDEFINE8 = envDEFINE8
        self.envVAR1 = serene_safe_assignment.envVAR1(True)

    def a1_read_after_0__condition(self, node):
        if True:
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return [(min(1, max(0, min(100, max(-100, max(self.envDEFINE8(1), self.envDEFINE5()))))), (
            'no'
            if (self.envDEFINE7() > 8) else
            (
                'no'
                if (self.envDEFINE7() <= self.envDEFINE7()) else
                (
                'both'
        ))))]

    def a1_read_after_0__1(self, node):
        return (
            'both'
            if self.envVAR1 else
            (
                self.blackboard.blVAR3[1]
                if (74 < self.envDEFINE8(1)) else
                (
                'yes'
        )))

    def a1_read_after_0__2(self, node):
        return (
            'both'
            if (-66 <= min(100, max(-100, (self.blackboard.blVAR0 - 97)))) else
            (
                self.blackboard.blVAR3[0]
                if (min(100, max(-100, (76 * 94))) == self.envDEFINE5()) else
                (
                self.envDEFINE6()
        )))

    def a3_write_before_2__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            node.localVAR4
            if False else
            (
            True
        )))
        return

    def a3_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(node.localVAR4)
        return

    def a4_read_before_0__condition(self, node):
        if (True and self.envVAR1):
            return True
        else:
            return False


    def a4_read_before_0__0(self, node):
        return (
            min(-2, max(-5, -51))
            if (self.blackboard.blVAR0 >= self.envDEFINE5()) else
            (
            min(-2, max(-5, min(100, max(-100, max(self.envDEFINE8(0), self.envDEFINE7())))))
        ))

    def a4_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(True)
        return
