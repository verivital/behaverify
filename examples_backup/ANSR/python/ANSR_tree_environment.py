import random
import serene_safe_assignment


class ANSR_tree_environment():
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
        self.tar_x = serene_safe_assignment.tar_x((
            random.choice([self.tar_x, min(10, (self.tar_x + 1)), max(0, (self.tar_x - 1))])
            if (self.timer == 0) else
            (
            self.tar_x
        )))
        self.tar_y = serene_safe_assignment.tar_y((
            random.choice([self.tar_y, min(10, (self.tar_y + 1)), max(0, (self.tar_y - 1))])
            if (self.timer == 0) else
            (
            self.tar_y
        )))
        self.timer = serene_safe_assignment.timer((
            5
            if (self.timer == 0) else
            (
            max(0, (self.timer - 1))
        )))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.tree_x = [None] * 2
        __temp_var__ = serene_safe_assignment.tree_x([(0, random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])), (1, random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))])
        for (index, val) in __temp_var__:
            self.tree_x[index] = val
        self.tree_y = [None] * 2
        __temp_var__ = serene_safe_assignment.tree_y([(0, random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])), (1, random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))])
        for (index, val) in __temp_var__:
            self.tree_y[index] = val
        self.tar_x = serene_safe_assignment.tar_x(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        self.tar_y = serene_safe_assignment.tar_y(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        self.timer = serene_safe_assignment.timer(5)

    def target_in_sight(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (((abs((self.blackboard.cur_x - self.tar_x)) + abs((self.blackboard.cur_y - self.tar_y))) <= 4) and (((abs((self.tree_x[0] - self.tar_x)) + abs((self.tree_y[0] - self.tar_y))) > 4) or ((self.tree_x[0] == self.blackboard.cur_x) and (self.tree_y[0] == self.blackboard.cur_y)) or ((self.tree_x[0] < self.blackboard.cur_x) and (self.tree_x[0] < self.tar_x)) or ((self.tree_y[0] < self.blackboard.cur_y) and (self.tree_y[0] < self.tar_y)) or ((self.tree_x[0] > self.blackboard.cur_x) and (self.tree_x[0] > self.tar_x)) or ((self.tree_y[0] > self.blackboard.cur_y) and (self.tree_y[0] > self.tar_y))))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (((abs((self.blackboard.cur_x - self.tar_x)) + abs((self.blackboard.cur_y - self.tar_y))) <= 4) and (((abs((self.tree_x[0] - self.tar_x)) + abs((self.tree_y[0] - self.tar_y))) > 4) or ((self.tree_x[0] == self.blackboard.cur_x) and (self.tree_y[0] == self.blackboard.cur_y)) or ((self.tree_x[0] < self.blackboard.cur_x) and (self.tree_x[0] < self.tar_x)) or ((self.tree_y[0] < self.blackboard.cur_y) and (self.tree_y[0] < self.tar_y)) or ((self.tree_x[0] > self.blackboard.cur_x) and (self.tree_x[0] > self.tar_x)) or ((self.tree_y[0] > self.blackboard.cur_y) and (self.tree_y[0] > self.tar_y))))
