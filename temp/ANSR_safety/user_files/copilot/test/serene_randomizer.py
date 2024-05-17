import random

class serene_randomizer():
    def __init__(self):
        self.blackboard = None
        self.environment = None
        return

    def set_blackboard_and_environment(self, blackboard, environment):
        self.blackboard = blackboard
        self.environment = environment
        return

    def r_0_0(self, node):
        return (0)

    def r_0_1(self, node):
        return (1)

    def r_0_2(self, node):
        return (2)

    def r_0_3(self, node):
        return (3)

    def r_0_4(self, node):
        return (4)

    def r_0_5(self, node):
        return (5)

    def r_0_6(self, node):
        return (6)

    def r_0(self, node):
        random_val = random.randint(0, 6)
        function_name = 'r_0_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_1_0(self, node):
        return (0)

    def r_1_1(self, node):
        return (1)

    def r_1_2(self, node):
        return (2)

    def r_1_3(self, node):
        return (3)

    def r_1_4(self, node):
        return (4)

    def r_1_5(self, node):
        return (5)

    def r_1_6(self, node):
        return (6)

    def r_1(self, node):
        random_val = random.randint(0, 6)
        function_name = 'r_1_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
