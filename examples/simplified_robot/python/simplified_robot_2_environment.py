import random
import serene_safe_assignment


class simplified_robot_2_environment():
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
        self.remaining_goals = serene_safe_assignment.remaining_goals((
            max(0, (self.remaining_goals - 1))
            if ((self.x_goal == self.x_true) and (self.y_goal == self.y_true)) else
            (
            self.remaining_goals
        )))
        self.x_goal = serene_safe_assignment.x_goal((
            self.x_goal
            if (0 == self.remaining_goals) else
            (
                random.choice([0, 1])
                if ((self.x_goal == self.x_true) and (self.y_goal == self.y_true)) else
                (
                self.x_goal
        ))))
        self.y_goal = serene_safe_assignment.y_goal((
            self.y_goal
            if (0 == self.remaining_goals) else
            (
                random.choice([0, 1])
                if ((self.x_goal == self.x_true) and (self.y_goal == self.y_true)) else
                (
                self.y_goal
        ))))
        return

    def check_tick_condition(self):
        return (self.remaining_goals > 0)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.x_goal = serene_safe_assignment.x_goal(random.choice([0, 1]))
        self.y_goal = serene_safe_assignment.y_goal(random.choice([0, 1]))
        self.x_true = serene_safe_assignment.x_true(random.choice([0, 1]))
        self.y_true = serene_safe_assignment.y_true(random.choice([0, 1]))
        self.remaining_goals = serene_safe_assignment.remaining_goals(random.choice([1, 2, 3]))

    def x_too_small(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.x_true < self.x_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.x_true < self.x_goal)

    def x_too_big(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.x_true > self.x_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.x_true > self.x_goal)

    def y_too_small(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.y_true < self.y_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.y_true < self.y_goal)

    def y_too_big(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.y_true > self.y_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.y_true > self.y_goal)

    def go_x_func__0(self, node):
        self.x_true = serene_safe_assignment.x_true(max(0, min(1, (self.x_true + node.x_dir))))
        return

    def go_y_func__0(self, node):
        self.y_true = serene_safe_assignment.y_true(max(0, min(1, (self.y_true + node.y_dir))))
        return
