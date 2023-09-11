import random
import serene_safe_assignment


class t9_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, (76 - max(self.envVAR2[1], self.envVAR1[0])))), min(5, max(2, self.envVAR2[1]))), (min(2, max(0, min(max(80, -4), (self.blackboard.blDEFINE6() * self.blackboard.blDEFINE6())))), min(5, max(2, abs(min(38, (self.envVAR2[1] - self.envVAR2[0])))))), (min(2, max(0, self.envVAR2[1])), min(5, max(2, -(77))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, (min(self.blackboard.blFROZENVAR4[0], 31) + 55))), (
            min(5, max(2, max(-64, -96)))
            if (self.blackboard.blVAR0 != self.blackboard.blVAR0) else
            (
            min(5, max(2, abs(74)))
        ))), (min(2, max(0, ((([(-90 < self.blackboard.blDEFINE6()), ('no' == self.blackboard.blVAR0), (self.blackboard.blVAR3[1] or False), (-48 <= self.envVAR1[2])].count(True)) - self.blackboard.blFROZENVAR4[0]) + self.blackboard.blDEFINE6() + (-90 - 46) + min(self.blackboard.blDEFINE6(), self.envVAR1[1])))), (
            min(5, max(2, -(max(min(self.envVAR2[0], self.envVAR1[1]), max(-89, self.blackboard.blFROZENVAR4[1])))))
            if ((self.blackboard.blVAR3[0] or False) == (self.envVAR1[0] <= self.envVAR1[1])) else
            (
            min(5, max(2, (-69 + (21 - 8))))
        ))), (min(2, max(0, max((self.blackboard.blDEFINE6() + self.envVAR2[0] + -5), -51))), (
            min(5, max(2, -(max(self.blackboard.blDEFINE6(), self.blackboard.blFROZENVAR4[0]))))
            if ((False or ((not (False)) or (False))) ^ self.blackboard.blVAR3[1]) else
            (
            min(5, max(2, -(50)))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, ([(self.blackboard.blVAR3[0] and True), (self.blackboard.blVAR3[1] == self.blackboard.blVAR3[1]), (self.envVAR1[2] <= self.blackboard.blFROZENVAR4[0])].count(True)))), min(5, max(2, (self.envVAR2[1] - (-78 - 35))))), (min(2, max(0, ((65 * (4 + self.blackboard.blDEFINE6() + self.blackboard.blDEFINE6()) * self.envVAR1[1] * 54) - (-44 - self.blackboard.blDEFINE6())))), min(5, max(2, (abs(self.blackboard.blFROZENVAR4[0]) + max(37, self.envVAR1[2]) + self.blackboard.blDEFINE6()))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR2([(min(1, max(0, self.blackboard.blDEFINE6())), (
            min(5, max(2, max(-(-74), (-96 + -77 + self.envVAR2[0] + -13))))
            if (((not (self.blackboard.blVAR3[0])) or (self.blackboard.blVAR3[0])) ^ self.blackboard.blVAR3[0]) else
            (
                min(5, max(2, max(20, self.blackboard.blDEFINE6())))
                if (self.blackboard.blVAR3[1] and self.blackboard.blVAR3[0]) else
                (
                min(5, max(2, abs(self.blackboard.blDEFINE6())))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE7(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE7: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing envDEFINE7: ' + str(index))
            if index == 0:
                return (
                    'yes'
                    if (not ((self.blackboard.blVAR3[0] ^ False))) else
                    (
                    self.blackboard.blVAR0
                ))
            elif index == 1:
                return (
                    'yes'
                    if (not ((self.blackboard.blVAR3[0] ^ False))) else
                    (
                    self.blackboard.blVAR0
                ))
            elif index == 2:
                return (
                    'yes'
                    if (not ((self.blackboard.blVAR3[0] ^ False))) else
                    (
                    self.blackboard.blVAR0
                ))
            raise Exception('Reached unreachable state when accessing envDEFINE7: ' + str(index))

        self.envDEFINE7 = envDEFINE7
        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            min(5, max(2, ([(73 <= -90), (-5 < 43)].count(True))))
            if False else
            (
                min(5, max(2, (4 - -61)))
                if ((True == True) == (False ^ True)) else
                (
                min(5, max(2, -(60)))
        )))), (1, (
            min(5, max(2, ([(73 <= -90), (-5 < 43)].count(True))))
            if False else
            (
                min(5, max(2, (4 - -61)))
                if ((True == True) == (False ^ True)) else
                (
                min(5, max(2, -(60)))
        )))), (2, (
            min(5, max(2, ([(73 <= -90), (-5 < 43)].count(True))))
            if False else
            (
                min(5, max(2, (4 - -61)))
                if ((True == True) == (False ^ True)) else
                (
                min(5, max(2, -(60)))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR2 = [None] * 2
        __temp_var__ = serene_safe_assignment.envVAR2([(0, (
            min(5, max(2, min(-(-53), -5)))
            if ((False ^ True) == (False or True)) else
            (
            min(5, max(2, -7))
        ))), (1, min(5, max(2, self.envVAR1[2])))])
        for (index, val) in __temp_var__:
            self.envVAR2[index] = val

    def a1_write_before_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, 60)), (
            min(5, max(2, -(self.envVAR2[1])))
            if (True and True) else
            (
            min(5, max(2, ([(not ((True ^ self.blackboard.blVAR3[0]))), (self.blackboard.blVAR3[1] and False), (False ^ False), (True == True)].count(True))))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a1_read_after_0__condition(self, node):
        if (node.localDEFINE5(2) == 'no'):
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return [(min(1, max(0, abs(-41))), (-(90) < max(-63, self.envVAR1[2])))]

    def a4_read_before_0__condition(self, node):
        if ((not (('yes' != 'both'))) or (False)):
            return True
        else:
            return False


    def a4_read_before_0__0(self, node):
        return [(min(1, max(0, -(abs(-100)))), (self.blackboard.blVAR3[0] ^ False)), (min(1, max(0, (self.blackboard.blFROZENVAR4[0] - 100))), (self.blackboard.blDEFINE6() > self.blackboard.blDEFINE6()))]

    def a4_read_before_0__1(self, node):
        return (
            'no'
            if (self.blackboard.blVAR3[1] and True) else
            (
            'both'
        ))

    def a4_read_after_0__condition(self, node):
        if self.blackboard.blVAR3[1]:
            return True
        else:
            return False


    def a4_read_after_0__0(self, node):
        return 'both'
