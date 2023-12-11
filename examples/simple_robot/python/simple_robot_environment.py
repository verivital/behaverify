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
        self.goal_reached = serene_safe_assignment.goal_reached(((self.x_goal == self.blackboard.x_true) and (self.y_goal == self.blackboard.y_true)))
        self.remaining_goals = serene_safe_assignment.remaining_goals((
            max(0, (self.remaining_goals - 1))
            if self.goal_reached else
            (
            self.remaining_goals
        )))
        self.x_goal = serene_safe_assignment.x_goal((
            self.x_goal
            if (0 == self.remaining_goals) else
            (
                (0 if ((temp := random.randint(0, 20)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10 if temp == 10 else (11 if temp == 11 else (12 if temp == 12 else (13 if temp == 13 else (14 if temp == 14 else (15 if temp == 15 else (16 if temp == 16 else (17 if temp == 17 else (18 if temp == 18 else (19 if temp == 19 else (20)))))))))))))))))))))
                if self.goal_reached else
                (
                self.x_goal
        ))))
        self.y_goal = serene_safe_assignment.y_goal((
            self.y_goal
            if (0 == self.remaining_goals) else
            (
                (0 if ((temp := random.randint(0, 20)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10 if temp == 10 else (11 if temp == 11 else (12 if temp == 12 else (13 if temp == 13 else (14 if temp == 14 else (15 if temp == 15 else (16 if temp == 16 else (17 if temp == 17 else (18 if temp == 18 else (19 if temp == 19 else (20)))))))))))))))))))))
                if self.goal_reached else
                (
                self.y_goal
        ))))
        return

    def check_tick_condition(self):
        return (self.remaining_goals > 0)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.x_goal = serene_safe_assignment.x_goal((0 if ((temp := random.randint(0, 20)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10 if temp == 10 else (11 if temp == 11 else (12 if temp == 12 else (13 if temp == 13 else (14 if temp == 14 else (15 if temp == 15 else (16 if temp == 16 else (17 if temp == 17 else (18 if temp == 18 else (19 if temp == 19 else (20))))))))))))))))))))))
        self.y_goal = serene_safe_assignment.y_goal((0 if ((temp := random.randint(0, 20)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10 if temp == 10 else (11 if temp == 11 else (12 if temp == 12 else (13 if temp == 13 else (14 if temp == 14 else (15 if temp == 15 else (16 if temp == 16 else (17 if temp == 17 else (18 if temp == 18 else (19 if temp == 19 else (20))))))))))))))))))))))
        self.remaining_goals = serene_safe_assignment.remaining_goals(3)
        self.goal_reached = serene_safe_assignment.goal_reached(False)

    def x_too_small(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.blackboard.x_true < self.x_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.blackboard.x_true < self.x_goal)

    def x_too_big(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.blackboard.x_true > self.x_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.blackboard.x_true > self.x_goal)

    def y_too_small(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.blackboard.y_true < self.y_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.blackboard.y_true < self.y_goal)

    def y_too_big(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.blackboard.y_true > self.y_goal)
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.blackboard.y_true > self.y_goal)
