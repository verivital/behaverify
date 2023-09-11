import random
import serene_safe_assignment


class t12_environment():
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
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, self.envDEFINE5(0)))
            if self.blackboard.blVAR0 else
            (
            min(-2, max(-5, -97))
        )))
        self.envVAR2 = serene_safe_assignment.envVAR2((
            self.envVAR2
            if self.envDEFINE6(0) else
            (
            self.envVAR2
        )))
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
                    min(-2, max(-5, self.blackboard.blDEFINE3()))
                    if ((89 > self.blackboard.blDEFINE3()) or ((not ((self.envVAR1 >= -31))) or (False))) else
                    (
                    min(-2, max(-5, -(-4)))
                ))
            elif index == 1:
                return min(-2, max(-5, 19))
            raise Exception('Reached unreachable state when accessing envDEFINE5: ' + str(index))

        self.envDEFINE5 = envDEFINE5


        def envDEFINE6(index):
            if not isinstance(index, int):
                raise Exception('Index must be an int when accessing envDEFINE6: ' + str(type(index)))
            if index < 0 or index >= 3:
                raise Exception('Index out of bounds when accessing envDEFINE6: ' + str(index))
            if index == 0:
                return (86 <= 12)
            elif index == 1:
                return (86 <= 12)
            elif index == 2:
                return (86 <= 12)
            raise Exception('Reached unreachable state when accessing envDEFINE6: ' + str(index))

        self.envDEFINE6 = envDEFINE6
        self.envVAR1 = serene_safe_assignment.envVAR1((
            min(-2, max(-5, 2))
            if (-94 > -39) else
            (
            min(-2, max(-5, min(-71, abs(-3))))
        )))
        self.envVAR2 = serene_safe_assignment.envVAR2('no')

    def a1_write_after_0__0(self, node):
        self.envVAR2 = serene_safe_assignment.envVAR2(self.envVAR2)
        return

    def a2_read_before_0__condition(self, node):
        if (not ((True ^ True))):
            return True
        else:
            return False


    def a2_read_before_0__0(self, node):
        return False

    def a2_read_before_0__1(self, node):
        return (
            (-(20) > max(self.blackboard.blDEFINE4(), 86))
            if (not ((self.envDEFINE6(1) ^ True))) else
            (
            ((not (self.blackboard.blVAR0)) or ((-72 == 30)))
        ))

    def a2_read_after_1__condition(self, node):
        if (self.envVAR1 < self.blackboard.blDEFINE4()):
            return True
        else:
            return False


    def a2_read_after_1__0(self, node):
        return ((not ((self.blackboard.blVAR0 ^ self.envDEFINE6(0)))) == (self.blackboard.blVAR0 == True))

    def a3_write_after_0__0(self, node):
        self.envVAR1 = serene_safe_assignment.envVAR1(min(-2, max(-5, (((self.blackboard.blDEFINE4() + 87) + self.envDEFINE5(0)) + min(self.envVAR1, min(-27, 93)) + (-(35) * -12 * -73) + abs(self.envVAR1)))))
        return
