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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, 96)), (
            min(5, max(2, (self.blackboard.blFROZENVAR5[1] + max(-53, self.envVAR1[1]) + self.blackboard.blDEFINE8(1))))
            if (True == self.envDEFINE9(0)) else
            (
            min(5, max(2, (self.blackboard.blFROZENVAR5[2] - self.blackboard.blDEFINE8(0))))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, ([(((not (False)) or (False)) == ((not (((not (False)) or (self.blackboard.blVAR2)))) or (True))), (False ^ (self.envVAR1[1] >= self.blackboard.blDEFINE8(1)))].count(True)))), min(5, max(2, -12)))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, self.blackboard.blFROZENVAR5[1])), (
            min(5, max(2, ([(-84 > 35), (self.envVAR1[0] >= 47), (-35 != 6)].count(True))))
            if (self.envVAR1[1] <= -77) else
            (
                min(5, max(2, self.envVAR1[0]))
                if (self.blackboard.blFROZENVAR5[1] < 49) else
                (
                min(5, max(2, abs(([(self.blackboard.blVAR3 < 85), (self.blackboard.blVAR0[0] == 'no'), (not ((self.envDEFINE9(1) ^ False)))].count(True)))))
        )))), (min(1, max(0, self.envVAR1[0])), (
            min(5, max(2, -(-(-54))))
            if (True ^ ((not (False)) or (False))) else
            (
                min(5, max(2, max((75 + -88 + 9), abs((-24 - self.blackboard.blFROZENVAR5[2])))))
                if (True == self.blackboard.blVAR2) else
                (
                min(5, max(2, max(min(73, self.blackboard.blDEFINE8(0)), (self.blackboard.blVAR3 * -3 * -50))))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE9(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE9: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing envDEFINE9: ' + str(index))
            if index == 0:
                return self.blackboard.blVAR2
            elif index == 1:
                return self.blackboard.blVAR2
            elif index == 2:
                return self.blackboard.blVAR2
            raise Exception('Reached unreachable state when accessing envDEFINE9: ' + str(index))

        self.envDEFINE9 = envDEFINE9
        self.envVAR1 = [None] * 2
        __temp_var__ = serene_safe_assignment.envVAR1([(0, min(5, max(2, ([(-3 <= 79), (22 <= 74), (False == False)].count(True))))), (1, min(5, max(2, ([(-3 <= 79), (22 <= 74), (False == False)].count(True)))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envFROZENVAR4 = serene_safe_assignment.envFROZENVAR4(self.blackboard.blVAR0[1])

    def a2_read_after_0__condition(self, node):
        if ((not ((41 >= 73))) or ((self.blackboard.blVAR3 > -63))):
            return True
        else:
            return False


    def a2_read_after_0__0(self, node):
        return (
            min(5, max(2, (-(self.blackboard.blDEFINE8(1)) + -75 + self.blackboard.blFROZENVAR5[1])))
            if self.envDEFINE9(2) else
            (
            min(5, max(2, -(-73)))
        ))

    def a3_write_before_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, ([((not (False)) or (self.blackboard.blVAR2)), (False ^ True), (not ((self.envDEFINE9(0) ^ False)))].count(True)))), (
            min(5, max(2, ([(self.blackboard.blVAR2 == False), (61 >= self.blackboard.blFROZENVAR5[2])].count(True))))
            if (self.envDEFINE9(0) != (self.envDEFINE9(1) == False)) else
            (
                min(5, max(2, min(self.envVAR1[0], self.blackboard.blDEFINE8(1))))
                if (56 <= self.blackboard.blFROZENVAR5[1]) else
                (
                min(5, max(2, ([(False or False), (True != False)].count(True))))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a3_write_before_0__1(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, -17)), (
            min(5, max(2, ([('yes' != 'both'), (not (((self.blackboard.blVAR2 and self.envDEFINE9(0)) ^ (self.blackboard.blVAR0[0] == 'yes')))), ((-42 * 86 * -97) <= (abs(-74) - max(self.blackboard.blVAR3, -77))), (11 < (-73 * self.blackboard.blVAR3 * self.envVAR1[0] * self.blackboard.blDEFINE8(1)))].count(True))))
            if (self.blackboard.blFROZENVAR5[2] < -(-69)) else
            (
                min(5, max(2, -(55)))
                if (self.blackboard.blVAR2 or (self.blackboard.blVAR3 <= self.blackboard.blFROZENVAR5[2])) else
                (
                min(5, max(2, 70))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a3_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(1, max(0, (0 * (self.blackboard.blVAR3 + self.blackboard.blVAR3)))), min(5, max(2, -(self.blackboard.blDEFINE8(0)))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return
