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
        return (self.blackboard.drone_x)

    def r_0_1(self, node):
        return (max(0, (self.blackboard.drone_x - 1)))

    def r_0_2(self, node):
        return (min(399, (self.blackboard.drone_x + 1)))

    def r_0(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_0_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_1_0(self, node):
        return (self.blackboard.drone_y)

    def r_1_1(self, node):
        return (max(0, (self.blackboard.drone_y - 1)))

    def r_1_2(self, node):
        return (min(399, (self.blackboard.drone_y + 1)))

    def r_1(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_1_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_2_0(self, node):
        return (self.blackboard.drone_z)

    def r_2_1(self, node):
        return (max(0, (self.blackboard.drone_z - 1)))

    def r_2_2(self, node):
        return (min(25, (self.blackboard.drone_z + 1)))

    def r_2(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_2_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_3_0(self, node):
        return (self.blackboard.destination_x)

    def r_3_1(self, node):
        return (max(0, (self.blackboard.destination_x - 1)))

    def r_3_2(self, node):
        return (min(399, (self.blackboard.destination_x + 1)))

    def r_3(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_3_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_4_0(self, node):
        return (self.blackboard.destination_y)

    def r_4_1(self, node):
        return (max(0, (self.blackboard.destination_y - 1)))

    def r_4_2(self, node):
        return (min(399, (self.blackboard.destination_y + 1)))

    def r_4(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_4_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_5_0(self, node):
        return (self.blackboard.destination_z)

    def r_5_1(self, node):
        return (max(0, (self.blackboard.destination_z - 1)))

    def r_5_2(self, node):
        return (min(25, (self.blackboard.destination_z + 1)))

    def r_5(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_5_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
