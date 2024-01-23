from pathlib import Path
import onnxruntime


class ANSR_ONNX_2_environment():
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
        self.tar_x = (
            self.blackboard.serene_randomizer.r_22(node)
            if (self.timer == 0) else
            (
            self.blackboard.serene_randomizer.r_23(node)
        ))
        self.tar_y = (
            self.blackboard.serene_randomizer.r_24(node)
            if (self.timer == 0) else
            (
            self.blackboard.serene_randomizer.r_25(node)
        ))
        self.timer = (
            self.blackboard.serene_randomizer.r_26(node)
            if (self.timer == 0) else
            (
            self.blackboard.serene_randomizer.r_27(node)
        ))
        return

    def check_tick_condition(self):
        return not (self.blackboard.victory)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.tree_x = None
        self.tree_y = None
        self.tar_x = None
        self.tar_y = None
        self.timer = None
        return

    def initialize_environment(self):
        node = None


        def tree_x(index):
            tree_x = [self.blackboard.serene_randomizer.r_28(node) for _ in range(2)]
            seen_indices = set()
            for (new_index, new_value) in [(1, self.blackboard.serene_randomizer.r_29(node))]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                tree_x[new_index] = new_value
            return tree_x[index]

        self.tree_x = tree_x


        def tree_y(index):
            tree_y = [self.blackboard.serene_randomizer.r_30(node) for _ in range(2)]
            seen_indices = set()
            for (new_index, new_value) in [(1, self.blackboard.serene_randomizer.r_31(node))]:
                if new_index in seen_indices:
                    continue
                seen_indices.add(new_index)
                tree_y[new_index] = new_value
            return tree_y[index]

        self.tree_y = tree_y
        self.tar_x = self.blackboard.serene_randomizer.r_32(node)
        self.tar_y = self.blackboard.serene_randomizer.r_33(node)
        self.timer = self.blackboard.serene_randomizer.r_34(node)
        return


    def target_in_sight(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (((abs((self.blackboard.cur_x - self.tar_x)) + abs((self.blackboard.cur_y - self.tar_y))) <= 4) and (((abs((self.tree_x(0) - self.tar_x)) + abs((self.tree_y(0) - self.tar_y))) > 2) or ((self.tree_x(0) == self.blackboard.cur_x) and (self.tree_y(0) == self.blackboard.cur_y)) or ((self.tree_x(0) == self.tar_x) and (self.tree_y(0) == self.tar_y)) or ((self.tree_x(0) < self.blackboard.cur_x) and (self.tree_x(0) < self.tar_x)) or ((self.tree_y(0) < self.blackboard.cur_y) and (self.tree_y(0) < self.tar_y)) or ((self.tree_x(0) > self.blackboard.cur_x) and (self.tree_x(0) > self.tar_x)) or ((self.tree_y(0) > self.blackboard.cur_y) and (self.tree_y(0) > self.tar_y))) and (((abs((self.tree_x(1) - self.tar_x)) + abs((self.tree_y(1) - self.tar_y))) > 2) or ((self.tree_x(1) == self.blackboard.cur_x) and (self.tree_y(1) == self.blackboard.cur_y)) or ((self.tree_x(1) == self.tar_x) and (self.tree_y(1) == self.tar_y)) or ((self.tree_x(1) < self.blackboard.cur_x) and (self.tree_x(1) < self.tar_x)) or ((self.tree_y(1) < self.blackboard.cur_y) and (self.tree_y(1) < self.tar_y)) or ((self.tree_x(1) > self.blackboard.cur_x) and (self.tree_x(1) > self.tar_x)) or ((self.tree_y(1) > self.blackboard.cur_y) and (self.tree_y(1) > self.tar_y))))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (((abs((self.blackboard.cur_x - self.tar_x)) + abs((self.blackboard.cur_y - self.tar_y))) <= 4) and (((abs((self.tree_x(0) - self.tar_x)) + abs((self.tree_y(0) - self.tar_y))) > 2) or ((self.tree_x(0) == self.blackboard.cur_x) and (self.tree_y(0) == self.blackboard.cur_y)) or ((self.tree_x(0) == self.tar_x) and (self.tree_y(0) == self.tar_y)) or ((self.tree_x(0) < self.blackboard.cur_x) and (self.tree_x(0) < self.tar_x)) or ((self.tree_y(0) < self.blackboard.cur_y) and (self.tree_y(0) < self.tar_y)) or ((self.tree_x(0) > self.blackboard.cur_x) and (self.tree_x(0) > self.tar_x)) or ((self.tree_y(0) > self.blackboard.cur_y) and (self.tree_y(0) > self.tar_y))) and (((abs((self.tree_x(1) - self.tar_x)) + abs((self.tree_y(1) - self.tar_y))) > 2) or ((self.tree_x(1) == self.blackboard.cur_x) and (self.tree_y(1) == self.blackboard.cur_y)) or ((self.tree_x(1) == self.tar_x) and (self.tree_y(1) == self.tar_y)) or ((self.tree_x(1) < self.blackboard.cur_x) and (self.tree_x(1) < self.tar_x)) or ((self.tree_y(1) < self.blackboard.cur_y) and (self.tree_y(1) < self.tar_y)) or ((self.tree_x(1) > self.blackboard.cur_x) and (self.tree_x(1) > self.tar_x)) or ((self.tree_y(1) > self.blackboard.cur_y) and (self.tree_y(1) > self.tar_y))))
