from pathlib import Path
import random
import onnxruntime


class EBT_environment():
    def delay_this_action(self, action, node):
        self.delayed_action_queue.append((action, node))

    def execute_delayed_action_queue(self):
        for (delayed_action, node) in self.delayed_action_queue:
            delayed_action(node)
        self.delayed_action_queue = []
        return

    def pre_tick_environment_update(self):
        node = None
        return

    def post_tick_environment_update(self):
        node = None
        return

    def check_tick_condition(self):
        return (True)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []
        return

    def initialize_environment(self):
        node = None
        return


    def calculate_path__condition(self, node):
        if True:
            return random.choice([True, False])
        else:
            return False


    def calculate_path__0(self, node):
        return [(0, self.blackboard.serene_randomizer.r_13(node)), (1, self.blackboard.serene_randomizer.r_14(node)), (2, self.blackboard.serene_randomizer.r_15(node)), (3, self.blackboard.serene_randomizer.r_16(node)), (4, self.blackboard.serene_randomizer.r_17(node)), (5, self.blackboard.serene_randomizer.r_18(node)), (6, self.blackboard.serene_randomizer.r_19(node)), (7, self.blackboard.serene_randomizer.r_20(node)), (8, self.blackboard.serene_randomizer.r_21(node)), (9, self.blackboard.serene_randomizer.r_22(node)), (10, self.blackboard.serene_randomizer.r_23(node)), (11, self.blackboard.serene_randomizer.r_24(node)), (12, self.blackboard.serene_randomizer.r_25(node)), (13, self.blackboard.serene_randomizer.r_26(node)), (14, self.blackboard.serene_randomizer.r_27(node)), (15, self.blackboard.serene_randomizer.r_28(node)), (16, self.blackboard.serene_randomizer.r_29(node)), (17, self.blackboard.serene_randomizer.r_30(node)), (18, self.blackboard.serene_randomizer.r_31(node)), (19, self.blackboard.serene_randomizer.r_32(node)), (20, self.blackboard.serene_randomizer.r_33(node)), (21, self.blackboard.serene_randomizer.r_34(node)), (22, self.blackboard.serene_randomizer.r_35(node)), (23, self.blackboard.serene_randomizer.r_36(node)), (24, self.blackboard.serene_randomizer.r_37(node))]

    def calculate_path__1(self, node):
        return [(0, self.blackboard.serene_randomizer.r_38(node)), (1, self.blackboard.serene_randomizer.r_39(node)), (2, self.blackboard.serene_randomizer.r_40(node)), (3, self.blackboard.serene_randomizer.r_41(node)), (4, self.blackboard.serene_randomizer.r_42(node)), (5, self.blackboard.serene_randomizer.r_43(node)), (6, self.blackboard.serene_randomizer.r_44(node)), (7, self.blackboard.serene_randomizer.r_45(node)), (8, self.blackboard.serene_randomizer.r_46(node)), (9, self.blackboard.serene_randomizer.r_47(node)), (10, self.blackboard.serene_randomizer.r_48(node)), (11, self.blackboard.serene_randomizer.r_49(node)), (12, self.blackboard.serene_randomizer.r_50(node)), (13, self.blackboard.serene_randomizer.r_51(node)), (14, self.blackboard.serene_randomizer.r_52(node)), (15, self.blackboard.serene_randomizer.r_53(node)), (16, self.blackboard.serene_randomizer.r_54(node)), (17, self.blackboard.serene_randomizer.r_55(node)), (18, self.blackboard.serene_randomizer.r_56(node)), (19, self.blackboard.serene_randomizer.r_57(node)), (20, self.blackboard.serene_randomizer.r_58(node)), (21, self.blackboard.serene_randomizer.r_59(node)), (22, self.blackboard.serene_randomizer.r_60(node)), (23, self.blackboard.serene_randomizer.r_61(node)), (24, self.blackboard.serene_randomizer.r_62(node))]

    def subgoal_calculation__condition(self, node):
        if True:
            return True
        else:
            return False


    def subgoal_calculation__0(self, node):
        return [(0, self.blackboard.serene_randomizer.r_63(node)), (1, self.blackboard.serene_randomizer.r_64(node))]

    def compute_state__condition(self, node):
        if True:
            return True
        else:
            return False


    def compute_state__0(self, node):
        return [(0, self.blackboard.serene_randomizer.r_65(node)), (1, self.blackboard.serene_randomizer.r_66(node))]

    def send_action__condition(self, node):
        if True:
            return True
        else:
            return False


    def send_action__0(self, node):
        return [(0, self.blackboard.serene_randomizer.r_67(node)), (1, self.blackboard.serene_randomizer.r_68(node))]

    def send_action__1(self, node):
        return [(0, self.blackboard.serene_randomizer.r_69(node)), (1, self.blackboard.serene_randomizer.r_70(node))]
