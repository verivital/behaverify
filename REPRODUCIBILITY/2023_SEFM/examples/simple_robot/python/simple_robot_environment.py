import random
import serene_safe_assignment


class simple_robot_environment():
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
                random.choice([0, 1, 2, 3, 4, 5])
                if ((self.x_goal == self.x_true) and (self.y_goal == self.y_true)) else
                (
                self.x_goal
        ))))
        self.y_goal = serene_safe_assignment.y_goal((
            self.y_goal
            if (0 == self.remaining_goals) else
            (
                random.choice([0, 1, 2, 3, 4, 5])
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

        self.x_goal = serene_safe_assignment.x_goal(random.choice([0, 1, 2, 3, 4, 5]))
        self.y_goal = serene_safe_assignment.y_goal(random.choice([0, 1, 2, 3, 4, 5]))
        self.x_true = serene_safe_assignment.x_true(random.choice([0, 1, 2, 3, 4, 5]))
        self.y_true = serene_safe_assignment.y_true(random.choice([0, 1, 2, 3, 4, 5]))
        self.remaining_goals = serene_safe_assignment.remaining_goals(random.choice([0, 1, 2, 3]))

    def mission_func__condition(self, node):
        if True:
            return True
        else:
            return False


    def mission_func__0(self, node):
        return self.x_goal

    def mission_func__1(self, node):
        return self.y_goal

    def position_func__condition(self, node):
        if True:
            return True
        else:
            return False


    def position_func__0(self, node):
        return self.x_true

    def position_func__1(self, node):
        return self.y_true

    def right_func__0(self, node):
        self.x_true = serene_safe_assignment.x_true(min(5, (self.x_true + 1)))
        return

    def left_func__0(self, node):
        self.x_true = serene_safe_assignment.x_true(max(0, (self.x_true - 1)))
        return

    def up_func__0(self, node):
        self.y_true = serene_safe_assignment.y_true(min(5, (self.y_true + 1)))
        return

    def down_func__0(self, node):
        self.y_true = serene_safe_assignment.y_true(max(0, (self.y_true - 1)))
        return
