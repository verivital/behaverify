import random
import serene_safe_assignment


class t11_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, self.envVAR1[0])), (
            min(5, max(2, ([((self.blackboard.blVAR2 or self.blackboard.blVAR2) ^ (not ((True ^ True)))), ((True == False) == (True and self.blackboard.blVAR2)), ((-19 >= 36) and (False or self.envDEFINE5(2))), (-73 < abs(self.blackboard.blDEFINE4()))].count(True))))
            if ((False == (self.blackboard.blVAR2 or self.blackboard.blVAR2)) ^ (self.blackboard.blVAR0 < self.envVAR1[1])) else
            (
            min(5, max(2, -28))
        ))), (min(2, max(0, -(-4))), (
            min(5, max(2, -84))
            if (((self.blackboard.blVAR0 - 35) * -76 * (self.blackboard.blDEFINE4() * self.blackboard.blDEFINE4() * 93 * self.blackboard.blVAR0) * -49) == self.blackboard.blVAR0) else
            (
            min(5, max(2, self.blackboard.blVAR0))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, 13)), (
            min(5, max(2, min(-11, abs(34))))
            if (False == False) else
            (
            min(5, max(2, abs(([((not (True)) or (self.envDEFINE5(0))), (False == True)].count(True)))))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, abs(min(-(-37), -71)))), (
            min(5, max(2, -(self.blackboard.blVAR0)))
            if True else
            (
            min(5, max(2, (27 * (39 * -77 * (44 - 48) * -11) * self.envVAR1[0])))
        ))), (min(2, max(0, ((64 + -55) * (3 - self.envVAR1[1]) * ([(self.envVAR1[1] == 41), (False == True), (self.envDEFINE5(0) ^ self.envDEFINE5(0))].count(True)) * self.blackboard.blDEFINE4()))), (
            min(5, max(2, ([(True ^ ((not (self.envDEFINE5(2))) or (False))), (-80 > (-25 - -42))].count(True))))
            if True else
            (
            min(5, max(2, min(15, self.blackboard.blVAR0)))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, max(self.envVAR1[1], -86))), (
            min(5, max(2, self.blackboard.blDEFINE4()))
            if self.blackboard.blVAR2 else
            (
            min(5, max(2, self.blackboard.blVAR0))
        ))), (min(2, max(0, ([(True and self.envDEFINE5(0)), (self.blackboard.blDEFINE4() < -31), ((not (True)) or (True))].count(True)))), (
            min(5, max(2, ([(([(self.blackboard.blVAR2 == False), (91 <= -39), (self.envDEFINE5(2) ^ self.blackboard.blVAR2), (True == True)].count(True)) > (49 + -29 + self.blackboard.blVAR0 + self.blackboard.blVAR0)), ((self.envVAR1[1] < 95) and False), ((self.blackboard.blVAR2 or self.blackboard.blVAR2) != True), (max(76, -72) >= -2)].count(True))))
            if (-5 >= self.blackboard.blDEFINE4()) else
            (
            min(5, max(2, abs(([(63 < self.blackboard.blDEFINE4()), (self.blackboard.blVAR2 == True)].count(True)))))
        ))), (min(2, max(0, 18)), (
            min(5, max(2, -(min(self.envVAR1[0], 95))))
            if (self.blackboard.blVAR0 == -(-29)) else
            (
            min(5, max(2, max(max(44, self.blackboard.blDEFINE4()), (66 * abs(self.blackboard.blDEFINE4()) * -44 * -94))))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def envDEFINE5(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE5: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing envDEFINE5: ' + str(index))
            if index == 0:
                return (
                    (self.blackboard.blVAR2 == self.blackboard.blVAR2)
                    if ((not ((self.blackboard.blVAR2 == True))) or (True)) else
                    (
                        (-2 <= -3)
                        if (self.blackboard.blVAR2 ^ self.blackboard.blVAR2) else
                        (
                        (self.blackboard.blVAR0 != min(-95, self.blackboard.blDEFINE4()))
                )))
            elif index == 1:
                return (
                    True
                    if (10 > 99) else
                    (
                        (not ((self.blackboard.blVAR2 ^ True)))
                        if self.blackboard.blVAR2 else
                        (
                        ((0 - 42) >= self.blackboard.blDEFINE4())
                )))
            elif index == 2:
                return (
                    ((80 + -27 + self.envVAR1[0] + self.blackboard.blVAR0) > max(27, -51))
                    if (True and (self.blackboard.blDEFINE4() >= self.blackboard.blVAR0)) else
                    (
                    (self.blackboard.blVAR2 == (self.blackboard.blVAR0 <= self.blackboard.blDEFINE4()))
                ))
            raise Exception('Reached unreachable state when accessing envDEFINE5: ' + str(index))

        self.envDEFINE5 = envDEFINE5
        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            min(5, max(2, max((37 - self.blackboard.blVAR0), abs(self.blackboard.blVAR0))))
            if ((not ((True or False))) or ((self.blackboard.blVAR0 == (-98 - self.blackboard.blVAR0)))) else
            (
            min(5, max(2, self.blackboard.blVAR0))
        ))), (1, (
            min(5, max(2, max((37 - self.blackboard.blVAR0), abs(self.blackboard.blVAR0))))
            if ((not ((True or False))) or ((self.blackboard.blVAR0 == (-98 - self.blackboard.blVAR0)))) else
            (
            min(5, max(2, self.blackboard.blVAR0))
        ))), (2, (
            min(5, max(2, max((37 - self.blackboard.blVAR0), abs(self.blackboard.blVAR0))))
            if ((not ((True or False))) or ((self.blackboard.blVAR0 == (-98 - self.blackboard.blVAR0)))) else
            (
            min(5, max(2, self.blackboard.blVAR0))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val

    def a1_read_before_0__condition(self, node):
        if (-(80) > (71 * -5 * max(-80, self.blackboard.blVAR0) * -32)):
            return True
        else:
            return False


    def a1_read_before_0__0(self, node):
        return False

    def a3_write_before_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, ([((not (True)) or ((self.envDEFINE5(1) or self.blackboard.blVAR2))), (self.envDEFINE5(1) != self.envDEFINE5(0)), (-90 != node.localDEFINE3(0)), ((not (True)) or (False))].count(True)))), min(5, max(2, -((([(True or self.blackboard.blVAR2), ((not (False)) or (self.blackboard.blVAR2)), ((not (True)) or (self.blackboard.blVAR2)), (False ^ True)].count(True)) - -(self.blackboard.blDEFINE4())))))), (min(2, max(0, -23)), min(5, max(2, ([(min(-14, -95) >= min(-50, 18)), (not ((self.blackboard.blVAR2 ^ (not ((self.envDEFINE5(0) ^ True)))))), (True == False)].count(True)))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_read_before_1__condition(self, node):
        if (not ((self.blackboard.blVAR2 ^ self.envDEFINE5(2)))):
            return True
        else:
            return False


    def a4_read_before_1__0(self, node):
        return min(-2, max(-5, ([(True == (self.envDEFINE5(1) and self.blackboard.blVAR2)), ((-41 >= self.blackboard.blVAR0) or self.envDEFINE5(1)), ((self.envDEFINE5(0) ^ self.envDEFINE5(1)) ^ True)].count(True))))

    def a4_read_before_0__condition(self, node):
        if (self.envDEFINE5(0) == False):
            return True
        else:
            return False


    def a4_read_before_0__0(self, node):
        return (
            min(-2, max(-5, (self.blackboard.blDEFINE4() + self.envVAR1[2])))
            if (-(self.blackboard.blDEFINE4()) <= -(self.envVAR1[2])) else
            (
            min(-2, max(-5, -31))
        ))

    def a4_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, 88)), (
            min(5, max(2, min(self.envVAR1[1], 72)))
            if (-(self.blackboard.blDEFINE4()) >= -70) else
            (
                min(5, max(2, min(max(self.blackboard.blDEFINE4(), 6), ([(min(self.envVAR1[0], 31) <= self.blackboard.blVAR0), ((not ((self.blackboard.blVAR0 <= self.blackboard.blDEFINE4()))) or (((not (False)) or (self.envDEFINE5(2))))), ((self.envDEFINE5(0) and False) ^ ((not (False)) or (True)))].count(True)))))
                if ((self.envVAR1[2] >= -97) != (self.blackboard.blVAR2 and True)) else
                (
                min(5, max(2, self.blackboard.blDEFINE4()))
        )))), (min(2, max(0, -(6))), (
            min(5, max(2, (min(self.blackboard.blDEFINE4(), self.blackboard.blDEFINE4()) + (self.blackboard.blVAR0 * 76) + 16)))
            if ((True and False) != False) else
            (
                min(5, max(2, max(-6, self.blackboard.blDEFINE4())))
                if (61 <= (min(self.envVAR1[0], self.envVAR1[1]) - (self.blackboard.blDEFINE4() * self.blackboard.blDEFINE4() * self.blackboard.blDEFINE4()))) else
                (
                min(5, max(2, self.envVAR1[1]))
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return
