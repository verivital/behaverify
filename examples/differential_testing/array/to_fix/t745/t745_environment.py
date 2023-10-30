import random
import serene_safe_assignment


class t745_environment():
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
        __temp_var__ = serene_safe_assignment.envVAR1([(max(0, min(1, (min(50, max((-50), max((-47), (-1))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, (-5)))))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), max((-47), (-1))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, (-5)))))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), max((-47), (-1))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, (-5)))))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), max((-47), (-1))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, (-5)))))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), max((-47), (-1))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, (-5)))))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), max((-47), (-1))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, (-5)))))))))), (
                    self.blackboard.blVAR0
                    if ((not ((True ^ True))) or (self.envDEFINE6(max(0, min(1, (-17)))) ^ (True or True))) else
                    (
                    'yes'
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), (self.envVAR2 - self.envVAR2)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                ))), (max(0, min(1, (min(50, max((-50), abs(33)))))), (
                    self.envFROZENVAR4
                    if ((min(50, max((-50), abs(self.envDEFINE7(max(0, min(1, self.envVAR3))))))) < (min(50, max((-50), (26 + 26 + 26 + 26))))) else
                    (
                    self.blackboard.blVAR0
                )))])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR2 = serene_safe_assignment.envVAR2((
            min(5, max(2, (min(50, max((-50), min(17, (min(50, max((-50), min(25, 42))))))))))
            if (self.envDEFINE6(max(0, min(1, 23))) == ((min(50, max((-50), min((-18), 19)))) == (min(50, max((-50), min(self.envVAR3, self.envVAR3)))))) else
            (
            min(5, max(2, (7 if (self.envVAR3 <= (-14)) else self.envVAR3)))
        )))
        print('ENV----> ' + str(self.envVAR2))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.envVAR1 = [(
            self.blackboard.blVAR0
            if (not (((False ^ False) ^ (True ^ False)))) else
            (
            'no'
        )) for _ in range(2)]
        __temp_var__ = serene_safe_assignment.envVAR1([(max(0, min(1, 5)), 'both'), (max(0, min(1, 5)), 'both')])
        for (index, val) in __temp_var__:
            self.envVAR1[index] = val
        self.envVAR2 = serene_safe_assignment.envVAR2((
            min(5, max(2, (min(50, max((-50), ((min(50, max((-50), (2 * (-22))))) + 13))))))
            if False else
            (
                min(5, max(2, (min(50, max((-50), ((min(50, max((-50), (25 + 25 + 36 + 36)))) - (min(50, max((-50), min(4, 4))))))))))
                if (4 <= (19 if (False ^ True) else 5)) else
                (
                min(5, max(2, (min(50, max((-50), ((-49) - ([((not False) or False), ((-38) != 3), (True == False), (False and True)].count(True))))))))
        ))))
        self.envVAR3 = serene_safe_assignment.envVAR3((
            min((-2), max((-5), self.envVAR2))
            if False else
            (
            min((-2), max((-5), (min(50, max((-50), (self.envVAR2 + self.envVAR2 + 21 + self.envVAR2))))))
        )))
        self.envFROZENVAR4 = serene_safe_assignment.envFROZENVAR4((
            'both'
            if ((min(50, max((-50), -(self.envVAR2)))) >= (25 if (self.envVAR3 > self.envVAR3) else self.envVAR2)) else
            (
            'both'
        )))


        def envDEFINE6(index):
            if type(index) is not int:
                raise TypeError('Index must be an int when accessing envDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise ValueError('Index out of bounds when accessing envDEFINE6: ' + str(index))
            envDEFINE6 = [(
                (not ((True ^ False)))
                if False else
                (
                    (True ^ True)
                    if (((-47) > 14) == ((False and False) == False)) else
                    (
                    (self.envVAR1[serene_safe_assignment.index_func(max(0, min(1, self.envVAR3)), 2)] == 'both')
            ))) for _ in range(2)]
            seen_indices = set()
            for (new_index, new_value) in [(max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True), (max(0, min(1, ((-33) if (27 < 43) else 41))), True)]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                if type(new_index) is not int:
                    raise TypeError('Index must be an int when accessing envDEFINE6: ' + str(type(new_index)))
                if new_index < 0 or new_index >= 2:
                    raise ValueError('Index out of bounds when accessing envDEFINE6: ' + str(new_index))
                if type(new_value) is not bool:
                    raise ValueError('Variable envDEFINE6 is type bool. Got type(new_value)')
                envDEFINE6[new_index] = new_value
            return envDEFINE6[index]

        self.envDEFINE6 = envDEFINE6


        def envDEFINE7(index):
            if type(index) is not int:
                raise TypeError('Index must be an int when accessing envDEFINE7: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise ValueError('Index out of bounds when accessing envDEFINE7: ' + str(index))
            envDEFINE7 = [min((-2), max((-5), (min(50, max((-50), max(self.envVAR2, self.envVAR2)))))) for _ in range(2)]
            seen_indices = set()
            for (new_index, new_value) in [(max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, (min(50, max((-50), ((min(50, max((-50), max(45, self.envVAR3)))) + (self.envVAR2 if (46 <= 32) else 7) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))) + (min(50, max((-50), max(self.envVAR3, self.envVAR3)))))))))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    )))), (max(0, min(1, ([((True and False) ^ False), (self.envDEFINE6(max(0, min(1, self.envVAR3))) or ((not True) or True))].count(True)))), (
                        min((-2), max((-5), ((min(50, max((-50), max(self.envVAR2, self.envVAR3)))) if ((min(50, max((-50), max((-5), self.envVAR3)))) > (-24)) else (self.envVAR3 if (self.envVAR2 < (-41)) else self.envVAR3))))
                        if (self.envVAR3 > (min(50, max((-50), max((-30), self.envVAR2))))) else
                        (
                            min((-2), max((-5), self.envVAR2))
                            if self.envDEFINE6(max(0, min(1, self.envVAR2))) else
                            (
                            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((self.envVAR2 if (True ^ False) else self.envVAR3) + (self.envVAR2 if (False and False) else (-34)))))) + (-25) + (self.envVAR3 if ((-36) >= 14) else self.envVAR3)))))))
                    ))))]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                if type(new_index) is not int:
                    raise TypeError('Index must be an int when accessing envDEFINE7: ' + str(type(new_index)))
                if new_index < 0 or new_index >= 2:
                    raise ValueError('Index out of bounds when accessing envDEFINE7: ' + str(new_index))
                if type(new_value) is not int:
                    raise ValueError('Variable envDEFINE7 is type int. Got type(new_value)')
                envDEFINE7[new_index] = new_value
            return envDEFINE7[index]

        self.envDEFINE7 = envDEFINE7

    def a1_read_before_0__condition(self, node):
        if self.envDEFINE6(max(0, min(1, (-2)))):
            return True
        else:
            return False


    def a1_read_before_0__0(self, node):
        return 'yes'

    def a1_read_after_0__condition(self, node):
        if ((not False) or (self.envVAR3 < 30)):
            return True
        else:
            return False


    def a1_read_after_0__0(self, node):
        return self.envVAR1[serene_safe_assignment.index_func(max(0, min(1, (-42))), 2)]

    def a1_read_after_0__1(self, node):
        return 'yes'

    def a3_write_before_0__0(self, node):
        self.envVAR2 = serene_safe_assignment.envVAR2((
            min(5, max(2, (-17)))
            if False else
            (
            min(5, max(2, (((min(50, max((-50), -((-2))))) if (self.envFROZENVAR4 != self.envFROZENVAR4) else (min(50, max((-50), ((-31) + (-31) + (-31) + 28))))) if (((min(50, max((-50), (self.envDEFINE7(max(0, min(1, (-45)))) + 13)))) if ((-39) == (43 if (False == True) else 48)) else (min(50, max((-50), min((-1), (-1)))))) <= (min(50, max((-50), -(self.envVAR2))))) else (min(50, max((-50), max((min(50, max((-50), max(3, 3)))), self.envVAR2)))))))
        )))
        print('A3_instant----> ' + str(self.envVAR2))
        return

    def a4_write_before_0__0(self, node):
        self.envVAR2 = serene_safe_assignment.envVAR2((
            min(5, max(2, (min(50, max((-50), (38 + 38 + (min(50, max((-50), max((-41), 5))))))))))
            if ((min(50, max((-50), -(21)))) <= (min(50, max((-50), (self.envVAR2 * self.envVAR2 * self.envVAR2 * self.envVAR2))))) else
            (
                min(5, max(2, self.envVAR2))
                if ((min(50, max((-50), -((-49))))) > (min(50, max((-50), abs(self.envVAR3))))) else
                (
                min(5, max(2, self.envVAR3))
        ))))
        print('A4_delay----> ' + str(self.envVAR2))
        return
