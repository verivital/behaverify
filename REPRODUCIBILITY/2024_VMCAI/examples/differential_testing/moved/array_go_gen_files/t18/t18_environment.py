import random
import serene_safe_assignment


class t18_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, min(self.blackboard.blVAR2[2], self.blackboard.blDEFINE7(1)))), (
            'yes'
            if ('both' == self.envDEFINE5(0)) else
            (
                'both'
                if (self.blackboard.blVAR0[0] >= (self.envDEFINE6(1) + -12 + (self.envVAR3 - self.blackboard.blVAR2[1]) + -(39))) else
                (
                self.envVAR1[2]
        )))), (min(2, max(0, (self.envVAR3 + min(self.blackboard.blVAR2[1], self.envVAR3) + ([(self.blackboard.blDEFINE4() or self.blackboard.blDEFINE4()), (self.envVAR1[0] != self.envVAR1[1])].count(True))))), (
            self.envDEFINE5(0)
            if (-2 > ((-82 - self.envDEFINE6(1)) - (94 + 37 + -63 + -99))) else
            (
                self.envVAR1[1]
                if (self.blackboard.blDEFINE7(0) >= self.envVAR3) else
                (
                'no'
        )))), (min(2, max(0, -(-73))), (
            self.envVAR1[0]
            if ((-39 > self.blackboard.blVAR0[1]) and (self.blackboard.blDEFINE4() or False)) else
            (
                'no'
                if True else
                (
                self.envVAR1[1]
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, max(self.envDEFINE6(1), self.envDEFINE6(1)))), self.envDEFINE5(0)), (min(2, max(0, (abs(-83) + max(38, 54) + (self.blackboard.blVAR0[0] + 17 + self.blackboard.blVAR2[0] + 90)))), self.envDEFINE5(0))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, min(73, 3))), 'both')])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        __temp_var__ = serene_safe_assignment.envVAR1([(min(2, max(0, -(-(self.blackboard.blVAR2[0])))), (
            'both'
            if (self.envVAR1[2] != self.envDEFINE5(1)) else
            (
            self.envDEFINE5(0)
        ))), (min(2, max(0, (self.blackboard.blVAR0[1] - 45))), (
            self.envDEFINE5(1)
            if ((self.envVAR1[0] != 'both') ^ self.blackboard.blDEFINE4()) else
            (
            self.envDEFINE5(0)
        ))), (min(2, max(0, self.blackboard.blDEFINE7(0))), (
            self.envVAR1[2]
            if ('yes' == 'yes') else
            (
            self.envDEFINE5(1)
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
            if index < 0 or index >= 2:
                raise Exception('Index out of bounds when accessing envDEFINE5: ' + str(index))
            if index == 0:
                return (
                    self.envVAR1[0]
                    if (69 > 33) else
                    (
                        self.envVAR1[1]
                        if False else
                        (
                        'yes'
                )))
            elif index == 1:
                return 'no'
            raise Exception('Reached unreachable state when accessing envDEFINE5: ' + str(index))

        self.envDEFINE5 = envDEFINE5


        def envDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing envDEFINE6: ' + str(index))
            if index == 0:
                return min(5, max(2, max(-(-51), self.blackboard.blVAR2[1])))
            elif index == 1:
                return (
                    min(5, max(2, self.envVAR3))
                    if True else
                    (
                    min(5, max(2, min(-(-37), -70)))
                ))
            elif index == 2:
                return (
                    min(5, max(2, self.envVAR3))
                    if (self.blackboard.blDEFINE4() or False) else
                    (
                        min(5, max(2, (34 + self.envVAR3 + 45 + 58)))
                        if ((self.blackboard.blVAR0[1] + -16 + 21) <= -(self.envVAR3)) else
                        (
                        min(5, max(2, self.blackboard.blVAR2[0]))
                )))
            raise Exception('Reached unreachable state when accessing envDEFINE6: ' + str(index))

        self.envDEFINE6 = envDEFINE6
        self.envVAR1 = [None] * 3
        __temp_var__ = serene_safe_assignment.envVAR1([(0, (
            'no'
            if (True != (True or False)) else
            (
                'both'
                if ((self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0] + 17) >= 39) else
                (
                'yes'
        )))), (1, (
            'no'
            if (True != (True or False)) else
            (
                'both'
                if ((self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0] + 17) >= 39) else
                (
                'yes'
        )))), (2, (
            'no'
            if (True != (True or False)) else
            (
                'both'
                if ((self.blackboard.blVAR0[1] + self.blackboard.blVAR0[0] + 17) >= 39) else
                (
                'yes'
        ))))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR3 = serene_safe_assignment.envVAR3((
            min(5, max(2, max((self.blackboard.blVAR2[2] + self.blackboard.blVAR0[1]), min(-56, 88))))
            if True else
            (
                min(5, max(2, -(self.blackboard.blVAR2[2])))
                if ((self.blackboard.blVAR2[0] < self.blackboard.blVAR0[1]) == (not ((True ^ False)))) else
                (
                min(5, max(2, -(abs(-20))))
        ))))
