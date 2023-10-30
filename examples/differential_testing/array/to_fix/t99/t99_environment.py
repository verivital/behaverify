import random
import serene_safe_assignment


class t99_environment():
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

        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), 3))
            if (not (((self.blackboard.blVAR0 != True) ^ (True == False)))) else
            (
            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), ((min(50, max((-50), ((-5) * (-5) * (-34) * 4)))) * 35 * 50)))) - ((-2) if (32 < 3) else 2)))))))
        )))


        def envDEFINE4(index):
            if type(index) is not int:
                raise TypeError('Index must be an int when accessing envDEFINE4: ' + str(type(index)))
            if index < 0 or index >= 2:
                raise ValueError('Index out of bounds when accessing envDEFINE4: ' + str(index))
            envDEFINE4 = [(
                min(5, max(2, self.envVAR1))
                if ((not self.blackboard.blVAR0) or self.blackboard.blVAR0) else
                (
                min(5, max(2, (min(50, max((-50), ((-33) * (-33) * self.envVAR1))))))
            )) for _ in range(2)]
            seen_indices = set()
            for (new_index, new_value) in [(0, (
                        min(5, max(2, (min(50, max((-50), min(self.envVAR1, self.envVAR1))))))
                        if self.blackboard.blVAR0 else
                        (
                            min(5, max(2, (-4)))
                            if ((min(50, max((-50), (self.envVAR1 + self.envVAR1 + 13)))) <= (-22)) else
                            (
                            min(5, max(2, (min(50, max((-50), min((min(50, max((-50), ((min(50, max((-50), max((-32), (-32))))) - self.envVAR1)))), (min(50, max((-50), ((min(50, max((-50), max((-32), (-32))))) - self.envVAR1))))))))))
                    )))), (1, (
                        min(5, max(2, (min(50, max((-50), min(self.envVAR1, self.envVAR1))))))
                        if self.blackboard.blVAR0 else
                        (
                            min(5, max(2, (-4)))
                            if ((min(50, max((-50), (self.envVAR1 + self.envVAR1 + 13)))) <= (-22)) else
                            (
                            min(5, max(2, (min(50, max((-50), min((min(50, max((-50), ((min(50, max((-50), max((-32), (-32))))) - self.envVAR1)))), (min(50, max((-50), ((min(50, max((-50), max((-32), (-32))))) - self.envVAR1))))))))))
                    ))))]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                if type(new_index) is not int:
                    raise TypeError('Index must be an int when accessing envDEFINE4: ' + str(type(new_index)))
                if new_index < 0 or new_index >= 2:
                    raise ValueError('Index out of bounds when accessing envDEFINE4: ' + str(new_index))
                if type(new_value) is not int:
                    raise ValueError('Variable envDEFINE4 is type int. Got type(new_value)')
                envDEFINE4[new_index] = new_value
            return envDEFINE4[index]

        self.envDEFINE4 = envDEFINE4

    def a1_write_before_1__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), (min(50, max((-50), (([('no' != 'no'), (((not True) or False) != False), (True or False), ((not True) or False)].count(True)) - ([('no' != 'no'), (((not True) or False) != False), (True or False), ((not True) or False)].count(True))))))))
            if self.blackboard.blVAR3[serene_safe_assignment.index_func(max(0, min(1, self.envVAR1)), 2)] else
            (
            min((-2), max((-5), (min(50, max((-50), ((min(50, max((-50), max(4, 4)))) - (min(50, max((-50), max(4, 4))))))))))
        )))
        return

    def a1_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min((-2), max((-5), (min(50, max((-50), (self.envDEFINE4(max(0, min(1, self.envVAR1))) - self.envVAR1)))))))
        return

    def a3_write_before_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min((-2), max((-5), (19 if (self.blackboard.blVAR3[serene_safe_assignment.index_func(max(0, min(1, (-20))), 2)] == True) else 2)))
            if True else
            (
                min((-2), max((-5), (min(50, max((-50), abs(4))))))
                if True else
                (
                min((-2), max((-5), self.envVAR1))
        ))))
        return

    def a3_read_after_1__condition(self, node):
        if ((((not self.blackboard.blVAR0) or True) and (not ((False ^ True)))) ^ (False and False)):
            return True
        else:
            return False


    def a3_read_after_1__0(self, node):
        return [(max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both'), (max(0, min(1, (29 if (True ^ self.blackboard.blVAR0) else 19))), 'both'), (max(0, min(1, (min(50, max((-50), min((-34), (-34))))))), 'both')]

    def a4_read_after_0__condition(self, node):
        if (not ((False ^ self.blackboard.blVAR0))):
            return True
        else:
            return False


    def a4_read_after_0__0(self, node):
        return ((self.blackboard.blVAR3[serene_safe_assignment.index_func(max(0, min(1, self.envVAR1)), 2)] or (5 <= (-26))) != ((not True) or (3 != (-2))))
