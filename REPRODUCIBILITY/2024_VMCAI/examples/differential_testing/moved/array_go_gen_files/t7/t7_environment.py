import random
import serene_safe_assignment


class t7_environment():
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



        def envDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing envDEFINE6: ' + str(index))
            if index == 0:
                return min(5, max(2, self.blackboard.blVAR0[2]))
            elif index == 1:
                return min(5, max(2, self.blackboard.blVAR0[2]))
            elif index == 2:
                return min(5, max(2, self.blackboard.blVAR0[2]))
            raise Exception('Reached unreachable state when accessing envDEFINE6: ' + str(index))

        self.envDEFINE6 = envDEFINE6
        self.envVAR1 = serene_safe_assignment.envVAR1((
            (self.blackboard.blVAR0[0] == min(-77, self.blackboard.blVAR0[0]))
            if False else
            (
            ((self.blackboard.blVAR0[1] < -4) ^ (not ((False ^ True))))
        )))
        self.envVAR2 = serene_safe_assignment.envVAR2((self.blackboard.blVAR0[0] < (self.blackboard.blVAR0[1] - self.blackboard.blVAR0[2])))
        self.envFROZENVAR3 = serene_safe_assignment.envFROZENVAR3((self.envVAR2 and True))

    def a1_write_before_1__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            ((self.envVAR1 ^ True) == (min(node.localDEFINE8(), -83) == ([(self.blackboard.blDEFINE5(0) == self.envFROZENVAR3), (-51 > -9), (True ^ True), (False == self.envVAR1)].count(True))))
            if (((node.localDEFINE8() * self.envDEFINE6(1) * 67) == -(self.envDEFINE6(0))) ^ True) else
            (
                (not (((node.localDEFINE8() <= abs(node.localDEFINE8())) ^ ((not (False)) or (False)))))
                if (self.blackboard.blDEFINE7(0) ^ ((not (False)) or (self.envVAR2))) else
                (
                False
        ))))
        return

    def a2_read_before_0__condition(self, node):
        if ((not ((False ^ (self.envFROZENVAR3 == self.blackboard.blDEFINE7(0))))) == (self.blackboard.blVAR0[0] != 14)):
            return True
        else:
            return False


    def a2_read_before_0__0(self, node):
        return [(min(2, max(0, ([(self.envFROZENVAR3 or self.envFROZENVAR3), (node.localDEFINE8() < -90)].count(True)))), (
            min(-2, max(-5, max(self.envDEFINE6(1), (node.localDEFINE8() * -32))))
            if (38 >= self.blackboard.blVAR0[1]) else
            (
                min(-2, max(-5, ([((self.envDEFINE6(2) <= (node.localDEFINE8() + 51 + self.envDEFINE6(0) + self.envDEFINE6(1))) and (self.envVAR1 == (not ((True ^ False))))), (abs(self.blackboard.blVAR0[1]) != (self.blackboard.blVAR0[1] - -58)), ((False and False) or (28 == (38 * -99 * node.localDEFINE8())))].count(True))))
                if (-11 <= self.blackboard.blVAR0[1]) else
                (
                min(-2, max(-5, max(self.blackboard.blVAR0[2], min(-93, self.envDEFINE6(1)))))
        ))))]

    def a3_write_before_0__0(self, node):
        self.envVAR2 = serene_safe_assignment.envVAR2((
            self.envFROZENVAR3
            if (node.localFROZENVAR4 > self.envDEFINE6(1)) else
            (
            (min(50, -73) > node.localFROZENVAR4)
        )))
        return

    def a3_write_before_0__1(self, node):
        self.envVAR2 = serene_safe_assignment.envVAR2((
            True
            if False else
            (
                (self.envVAR1 == False)
                if (not ((True ^ True))) else
                (
                ((not ((self.blackboard.blDEFINE7(0) ^ False))) ^ (self.envFROZENVAR3 and self.blackboard.blDEFINE5(0)))
        ))))
        return

    def a4_write_before_0__0(self, node):
        self.envVAR2 = serene_safe_assignment.envVAR2((self.envVAR1 and self.envFROZENVAR3))
        return

    def a4_write_before_0__1(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((False or False))
        return
