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

    def r_0(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_0_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_1_0(self, node):
        return (10)

    def r_1(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_1_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_2_0(self, node):
        return (min(10, max(0, (self.blackboard.dest_y + (self.blackboard.dir_int() * self.blackboard.y_net(0) * 2)))))

    def r_2(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_2_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_3_0(self, node):
        return (max(0, min(10, (node.delta_x + self.blackboard.cur_x))))

    def r_3(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_3_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_4_0(self, node):
        return (max(0, min(10, (node.delta_y + self.blackboard.cur_y))))

    def r_4(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_4_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_5_0(self, node):
        return (True)

    def r_5(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_5_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_6_0(self, node):
        return ('Down')

    def r_6(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_6_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_7_0(self, node):
        return ('Up')

    def r_7(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_7_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_8_0(self, node):
        return (self.blackboard.dir)

    def r_8(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_8_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_9_0(self, node):
        return (self.blackboard.cur_x_bool())

    def r_9(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_9_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_10_0(self, node):
        return (0)

    def r_10(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_10_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_11_0(self, node):
        return (0)

    def r_11(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_11_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_12_0(self, node):
        return (0)

    def r_12(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_12_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_13_0(self, node):
        return ((int((0 + 10) / 2)))

    def r_13(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_13_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_14_0(self, node):
        return (0)

    def r_14(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_14_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_15_0(self, node):
        return (1)

    def r_15(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_15_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_16_0(self, node):
        return (0)

    def r_16(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_16_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_17_0(self, node):
        return (0)

    def r_17(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_17_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_18_0(self, node):
        return ('Up')

    def r_18(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_18_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_19_0(self, node):
        return (1)

    def r_19(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_19_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_20_0(self, node):
        return ((-1))

    def r_20(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_20_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_21_0(self, node):
        return (False)

    def r_21(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_21_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_22_0(self, node):
        return (self.environment.tar_x)

    def r_22_1(self, node):
        return (min(10, (self.environment.tar_x + 1)))

    def r_22_2(self, node):
        return (max(0, (self.environment.tar_x - 1)))

    def r_22(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_22_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_23_0(self, node):
        return (self.environment.tar_x)

    def r_23(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_23_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_24_0(self, node):
        return (self.environment.tar_y)

    def r_24_1(self, node):
        return (min(10, (self.environment.tar_y + 1)))

    def r_24_2(self, node):
        return (max(0, (self.environment.tar_y - 1)))

    def r_24(self, node):
        random_val = random.randint(0, 2)
        function_name = 'r_24_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_25_0(self, node):
        return (self.environment.tar_y)

    def r_25(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_25_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_26_0(self, node):
        return (7)

    def r_26(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_26_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_27_0(self, node):
        return (max(0, (self.environment.timer - 1)))

    def r_27(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_27_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_28_0(self, node):
        return (2)

    def r_28(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_28_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_29_0(self, node):
        return (5)

    def r_29(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_29_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_30_0(self, node):
        return (2)

    def r_30(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_30_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_31_0(self, node):
        return (5)

    def r_31(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_31_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_32_0(self, node):
        return (0)

    def r_32_1(self, node):
        return (1)

    def r_32_2(self, node):
        return (2)

    def r_32_3(self, node):
        return (3)

    def r_32_4(self, node):
        return (4)

    def r_32_5(self, node):
        return (5)

    def r_32_6(self, node):
        return (6)

    def r_32_7(self, node):
        return (7)

    def r_32_8(self, node):
        return (8)

    def r_32_9(self, node):
        return (9)

    def r_32_10(self, node):
        return (10)

    def r_32(self, node):
        random_val = random.randint(0, 10)
        function_name = 'r_32_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_33_0(self, node):
        return (0)

    def r_33_1(self, node):
        return (1)

    def r_33_2(self, node):
        return (2)

    def r_33_3(self, node):
        return (3)

    def r_33_4(self, node):
        return (4)

    def r_33_5(self, node):
        return (5)

    def r_33_6(self, node):
        return (6)

    def r_33_7(self, node):
        return (7)

    def r_33_8(self, node):
        return (8)

    def r_33_9(self, node):
        return (9)

    def r_33_10(self, node):
        return (10)

    def r_33(self, node):
        random_val = random.randint(0, 10)
        function_name = 'r_33_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
    def r_34_0(self, node):
        return (7)

    def r_34(self, node):
        random_val = random.randint(0, 0)
        function_name = 'r_34_' + str(random_val)
        function = getattr(self, function_name)
        return function(node)

    #---------------------
