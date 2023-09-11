import random
import serene_safe_assignment


class t0_environment():
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



        def envDEFINE5(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE5: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing envDEFINE5: ' + str(index))
            if index == 0:
                return (
                    min(-2, max(-5, ([(not (((True != self.envVAR1[1]) ^ ('yes' != 'yes')))), (False == (self.blackboard.blVAR0[0] < self.blackboard.blVAR0[0])), (-(-90) >= self.blackboard.blVAR0[0]), (self.envFROZENVAR3[0] == 'no')].count(True))))
                    if ((True or self.envVAR1[0]) or True) else
                    (
                    min(-2, max(-5, (self.blackboard.blVAR0[1] - self.blackboard.blVAR0[1])))
                ))
            elif index == 1:
                return (
                    min(-2, max(-5, self.blackboard.blVAR0[0]))
                    if (self.envVAR1[1] ^ ('yes' != 'no')) else
                    (
                        min(-2, max(-5, abs(min(79, -91))))
                        if (not ((self.envVAR1[0] ^ self.envVAR1[1]))) else
                        (
                        min(-2, max(-5, max(37, self.blackboard.blVAR0[0])))
                )))
            elif index == 2:
                return min(-2, max(-5, -(min(25, self.blackboard.blVAR0[1]))))
            raise Exception('Reached unreachable state when accessing envDEFINE5: ' + str(index))

        self.envDEFINE5 = envDEFINE5


        def envDEFINE6():
            return (
                (((not (self.envVAR1[0])) or (False)) ^ (not (((self.envVAR1[2] ^ self.envVAR1[0]) ^ True))))
                if (not ((self.envVAR1[2] ^ False))) else
                (
                (self.blackboard.blVAR0[0] <= 70)
            ))

        self.envDEFINE6 = envDEFINE6


        def envDEFINE7():
            return (
                self.envVAR1[1]
                if (False and ((not ((False == True))) or (self.envDEFINE6()))) else
                (
                self.envDEFINE6()
            ))

        self.envDEFINE7 = envDEFINE7
        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            False
            if ((self.blackboard.blVAR0[0] * self.blackboard.blVAR0[1] * self.blackboard.blVAR0[0] * self.blackboard.blVAR0[1]) > (39 + -62 + self.blackboard.blVAR0[1])) else
            (
            False
        ))), (1, (
            False
            if ((self.blackboard.blVAR0[0] * self.blackboard.blVAR0[1] * self.blackboard.blVAR0[0] * self.blackboard.blVAR0[1]) > (39 + -62 + self.blackboard.blVAR0[1])) else
            (
            False
        ))), (2, (
            False
            if ((self.blackboard.blVAR0[0] * self.blackboard.blVAR0[1] * self.blackboard.blVAR0[0] * self.blackboard.blVAR0[1]) > (39 + -62 + self.blackboard.blVAR0[1])) else
            (
            False
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envFROZENVAR3 = [None] * 3
        __temp_var__ = serene_safe_assignment.envFROZENVAR3([(0, 'both'), (1, (
            'both'
            if True else
            (
                'yes'
                if (self.blackboard.blVAR0[0] >= (self.blackboard.blVAR0[0] + self.blackboard.blVAR0[1] + -88 + self.blackboard.blVAR0[0])) else
                (
                'both'
        )))), (2, (
            'no'
            if True else
            (
            'yes'
        )))])
        for (index, val) in __temp_var__:
            self.envFROZENVAR3[index] = val

    def a1_read_before_0__condition(self, node):
        if ((not (((self.envDEFINE5(0) > self.envDEFINE5(1)) ^ (77 < self.blackboard.blVAR0[1])))) ^ (False and self.envDEFINE6())):
            return True
        else:
            return False


    def a1_read_before_0__0(self, node):
        return [(min(1, max(0, ([(True ^ (False or self.envDEFINE7())), (self.envDEFINE5(1) != 88), ('yes' == 'yes')].count(True)))), min(5, max(2, self.blackboard.blVAR0[1])))]

    def a1_read_before_0__1(self, node):
        return [(min(1, max(0, self.envDEFINE5(0))), (
            min(5, max(2, -(self.blackboard.blVAR0[1])))
            if ((-32 * self.blackboard.blVAR0[0] * 14 * 0) != 14) else
            (
            min(5, max(2, max(([(self.envDEFINE5(0) >= (self.envDEFINE5(1) + self.envDEFINE5(1))), (True == True), (self.envFROZENVAR3[0] == 'no')].count(True)), min(8, -67))))
        ))), (min(1, max(0, self.envDEFINE5(0))), (
            min(5, max(2, min((self.envDEFINE5(1) + 76 + self.envDEFINE5(2)), (83 * (29 * -36 * -84 * -27)))))
            if True else
            (
            min(5, max(2, (-21 + self.envDEFINE5(2) + 67 + -63)))
        )))]

    def a1_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, (self.blackboard.blVAR0[1] + self.envDEFINE5(1)))), (
            ('both' == 'both')
            if False else
            (
            (False == self.envDEFINE7())
        ))), (min(2, max(0, (abs(self.envDEFINE5(1)) * self.envDEFINE5(1)))), (
            (not (((self.envDEFINE5(1) > self.envDEFINE5(0)) ^ ((self.envDEFINE6() ^ self.envVAR1[2]) ^ True))))
            if ((40 < self.envDEFINE5(2)) == False) else
            (
            ((self.envDEFINE5(1) * self.envDEFINE5(1) * self.blackboard.blVAR0[0] * self.envDEFINE5(1)) <= self.envDEFINE5(0))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a2_read_before_0__condition(self, node):
        if (True ^ True):
            return True
        else:
            return False


    def a2_read_before_0__0(self, node):
        return [(min(1, max(0, 54)), (
            min(5, max(2, min(abs(3), self.blackboard.blVAR0[1])))
            if ((not (True)) or (True)) else
            (
                min(5, max(2, self.blackboard.blVAR0[1]))
                if (abs(34) == (self.envDEFINE5(2) - -40)) else
                (
                min(5, max(2, max(abs(self.envDEFINE5(0)), abs(self.envDEFINE5(0)))))
        ))))]

    def a2_read_before_0__1(self, node):
        return [(min(1, max(0, abs(abs(self.envDEFINE5(0))))), (
            min(5, max(2, self.blackboard.blVAR0[1]))
            if (15 >= -92) else
            (
                min(5, max(2, ([(not ((self.envVAR1[1] ^ self.envVAR1[0]))), (True ^ (not ((False ^ True)))), (-55 <= self.blackboard.blVAR0[1]), ((self.envDEFINE5(0) * -19 * self.envDEFINE5(1) * -97) <= (self.envDEFINE5(2) - 2))].count(True))))
                if (not ((self.envDEFINE6() ^ True))) else
                (
                min(5, max(2, abs(-65)))
        ))))]

    def a2_read_after_0__condition(self, node):
        if (False or True):
            return True
        else:
            return False


    def a2_read_after_0__0(self, node):
        return [(min(1, max(0, -((self.blackboard.blVAR0[1] * self.blackboard.blVAR0[0])))), min(5, max(2, -((self.blackboard.blVAR0[1] + 66)))))]

    def a4_write_after_2__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, min(self.envDEFINE5(1), 39))), (
            (self.envFROZENVAR3[0] != 'both')
            if (((self.envDEFINE5(2) + self.envDEFINE5(0) + self.blackboard.blVAR0[0] + self.envDEFINE5(0)) * max(10, self.envDEFINE5(2))) <= self.blackboard.blVAR0[1]) else
            (
                (False and (False == self.envVAR1[2]))
                if (-48 < self.blackboard.blVAR0[0]) else
                (
                ((self.envDEFINE5(1) - self.blackboard.blVAR0[1]) <= (([(True ^ False), (self.envVAR1[1] == True)].count(True)) + self.envDEFINE5(1)))
        )))), (min(2, max(0, min(self.envDEFINE5(2), 64))), (
            self.envDEFINE7()
            if (self.envDEFINE5(0) < -27) else
            (
                self.envDEFINE7()
                if self.envVAR1[2] else
                (
                (((self.blackboard.blVAR0[0] - 98) >= self.blackboard.blVAR0[1]) and (self.envDEFINE6() ^ False))
        )))), (min(2, max(0, -(self.envDEFINE5(2)))), (
            self.envVAR1[0]
            if True else
            (
                True
                if (self.blackboard.blVAR0[1] > min(self.blackboard.blVAR0[1], 12)) else
                (
                (abs(93) <= 53)
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_write_after_2__1(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, -64)), (
            (not ((self.envDEFINE6() ^ True)))
            if True else
            (
            True
        ))), (min(2, max(0, (100 - self.envDEFINE5(2)))), (
            ((21 * self.envDEFINE5(2)) < -(-4))
            if (((self.blackboard.blVAR0[1] != -41) or False) == (-59 > self.blackboard.blVAR0[0])) else
            (
            (-49 != min(20, -89))
        )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return

    def a4_read_after_1__condition(self, node):
        if (False == (not ((self.envVAR1[0] ^ self.envDEFINE6())))):
            return True
        else:
            return False


    def a4_read_after_1__0(self, node):
        return [(min(1, max(0, self.blackboard.blVAR0[0])), (
            min(5, max(2, max(-42, self.envDEFINE5(2))))
            if (self.envVAR1[1] == (self.blackboard.blVAR0[1] < self.envDEFINE5(2))) else
            (
            min(5, max(2, ((36 * self.envDEFINE5(0)) - ((self.envDEFINE5(2) * self.envDEFINE5(0)) + min(-6, self.blackboard.blVAR0[0])))))
        ))), (min(1, max(0, min(self.envDEFINE5(2), self.envDEFINE5(1)))), (
            min(5, max(2, -92))
            if (min(abs(59), self.envDEFINE5(0)) >= min(max(self.blackboard.blVAR0[1], 18), ([(not ((True ^ self.envDEFINE6()))), (True ^ True), (-79 != -90), (not ((True ^ self.envDEFINE7())))].count(True)))) else
            (
            min(5, max(2, (-78 * self.envDEFINE5(1) * -87 * 58)))
        )))]

    def a4_write_after_0__0(self, node):
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, -(-78))), (
            (self.blackboard.blVAR0[0] > 53)
            if self.envDEFINE7() else
            (
                (self.envDEFINE7() ^ self.envDEFINE7())
                if (not ((self.envDEFINE7() ^ True))) else
                (
                False
        )))), (min(2, max(0, self.envDEFINE5(2))), (
            (False == self.envDEFINE6())
            if ((self.blackboard.blVAR0[1] - -79) < -(self.envDEFINE5(1))) else
            (
                (self.envFROZENVAR3[1] == 'no')
                if (False and False) else
                (
                self.envDEFINE7()
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        return
