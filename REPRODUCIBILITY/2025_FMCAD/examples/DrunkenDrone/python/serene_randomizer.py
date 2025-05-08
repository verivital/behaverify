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
        return ('No')

    def r_0_1(self, node):
        return ('So')

    def r_0_2(self, node):
        return ('We')

    def r_0_3(self, node):
        return ('Ea')

    def r_0(self, node):
        random_val = random.randint(0, 3)
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

    def r_1_7(self, node):
        return (7)

    def r_1_8(self, node):
        return (8)

    def r_1_9(self, node):
        return (9)

    def r_1_10(self, node):
        return (10)

    def r_1_11(self, node):
        return (11)

    def r_1_12(self, node):
        return (12)

    def r_1_13(self, node):
        return (13)

    def r_1_14(self, node):
        return (14)

    def r_1_15(self, node):
        return (15)

    def r_1_16(self, node):
        return (16)

    def r_1_17(self, node):
        return (17)

    def r_1_18(self, node):
        return (18)

    def r_1_19(self, node):
        return (19)

    def r_1(self, node):
        random_val = random.randint(0, 19)
        function_name = 'r_1_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_2_0(self, node):
        return (0)

    def r_2_1(self, node):
        return (1)

    def r_2_2(self, node):
        return (2)

    def r_2_3(self, node):
        return (3)

    def r_2_4(self, node):
        return (4)

    def r_2_5(self, node):
        return (5)

    def r_2_6(self, node):
        return (6)

    def r_2_7(self, node):
        return (7)

    def r_2_8(self, node):
        return (8)

    def r_2_9(self, node):
        return (9)

    def r_2_10(self, node):
        return (10)

    def r_2_11(self, node):
        return (11)

    def r_2_12(self, node):
        return (12)

    def r_2_13(self, node):
        return (13)

    def r_2_14(self, node):
        return (14)

    def r_2_15(self, node):
        return (15)

    def r_2_16(self, node):
        return (16)

    def r_2_17(self, node):
        return (17)

    def r_2_18(self, node):
        return (18)

    def r_2_19(self, node):
        return (19)

    def r_2(self, node):
        random_val = random.randint(0, 19)
        function_name = 'r_2_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
