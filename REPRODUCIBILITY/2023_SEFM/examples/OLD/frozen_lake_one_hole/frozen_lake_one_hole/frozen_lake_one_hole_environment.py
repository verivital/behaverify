import random
import serene_safe_assignment


class frozen_lake_one_hole_environment():
    def delay_this_action(self, action, node):
        self.delayed_action_queue.append((action, node))

    def execute_delayed_action_queue(self):
        for (delayed_action, node) in self.delayed_action_queue:
            delayed_action(node)
        self.delayed_action_queue = []
        return

    def between_tick_environment_update(self):
        self.loc = serene_safe_assignment.loc((
            self.start_loc
            if (self.blackboard.action == -1) else
            (
                (self.x_loc() + (4 * max(0, (self.y_loc() - 1))))
                if (self.blackboard.action == 3) else
                (
                    (self.x_loc() + (4 * min(3, (self.y_loc() + 1))))
                    if (self.blackboard.action == 1) else
                    (
                        (max(0, (self.x_loc() - 1)) + (4 * self.y_loc()))
                        if (self.blackboard.action == 0) else
                        (
                            (min(3, (self.x_loc() + 1)) + (4 * self.y_loc()))
                            if (self.blackboard.action == 2) else
                            (
                            self.loc
        )))))))
        self.falls_remaining = serene_safe_assignment.falls_remaining((
            max(-1, (self.falls_remaining - 1))
            if (self.loc == self.hole_loc) else
            (
            self.falls_remaining
        )))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def x_loc():
            return (self.loc % 4)

        self.x_loc = x_loc


        def y_loc():
            return ((self.loc - self.x_loc()) // 4)

        self.y_loc = y_loc
        self.start_loc = serene_safe_assignment.start_loc(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))
        self.goal_loc = serene_safe_assignment.goal_loc(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))
        self.loc = serene_safe_assignment.loc(self.start_loc)
        self.hole_loc = serene_safe_assignment.hole_loc((
            random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
            if (self.start_loc == 0) else
            (
                random.choice([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
                if (self.start_loc == 1) else
                (
                    random.choice([0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
                    if (self.start_loc == 2) else
                    (
                        random.choice([0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
                        if (self.start_loc == 3) else
                        (
                            random.choice([0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
                            if (self.start_loc == 4) else
                            (
                                random.choice([0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
                                if (self.start_loc == 5) else
                                (
                                    random.choice([0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15])
                                    if (self.start_loc == 6) else
                                    (
                                        random.choice([0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15])
                                        if (self.start_loc == 7) else
                                        (
                                            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15])
                                            if (self.start_loc == 8) else
                                            (
                                                random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15])
                                                if (self.start_loc == 9) else
                                                (
                                                    random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15])
                                                    if (self.start_loc == 10) else
                                                    (
                                                        random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15])
                                                        if (self.start_loc == 11) else
                                                        (
                                                            random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15])
                                                            if (self.start_loc == 12) else
                                                            (
                                                                random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15])
                                                                if (self.start_loc == 13) else
                                                                (
                                                                    random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15])
                                                                    if (self.start_loc == 14) else
                                                                    (
                                                                        random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
                                                                        if (self.start_loc == 15) else
                                                                        (
                                                                        0
        ))))))))))))))))))
        self.falls_remaining = serene_safe_assignment.falls_remaining(1)

    def fell_in_hole(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.blackboard.tiles[self.loc] == 'hole')
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.blackboard.tiles[self.loc] == 'hole')

    def up_bad(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('hole' == self.blackboard.tiles[(self.x_loc() + (4 * max(0, (self.y_loc() - 1))))]) or (self.y_loc() == 0))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('hole' == self.blackboard.tiles[(self.x_loc() + (4 * max(0, (self.y_loc() - 1))))]) or (self.y_loc() == 0))

    def down_bad(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('hole' == self.blackboard.tiles[(self.x_loc() + (4 * min(3, (self.y_loc() + 1))))]) or (self.y_loc() == 3))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('hole' == self.blackboard.tiles[(self.x_loc() + (4 * min(3, (self.y_loc() + 1))))]) or (self.y_loc() == 3))

    def left_bad(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('hole' == self.blackboard.tiles[(max(0, (self.x_loc() - 1)) + (4 * self.y_loc()))]) or (self.x_loc() == 0))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('hole' == self.blackboard.tiles[(max(0, (self.x_loc() - 1)) + (4 * self.y_loc()))]) or (self.x_loc() == 0))

    def right_bad(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('hole' == self.blackboard.tiles[(min(3, (self.x_loc() + 1)) + (4 * self.y_loc()))]) or (self.x_loc() == 3))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('hole' == self.blackboard.tiles[(min(3, (self.x_loc() + 1)) + (4 * self.y_loc()))]) or (self.x_loc() == 3))

    def up_unknown(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('unknown' == self.blackboard.tiles[(self.x_loc() + (4 * max(0, (self.y_loc() - 1))))]) and (self.y_loc() != 0))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('unknown' == self.blackboard.tiles[(self.x_loc() + (4 * max(0, (self.y_loc() - 1))))]) and (self.y_loc() != 0))

    def down_unknown(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('unknown' == self.blackboard.tiles[(self.x_loc() + (4 * min(3, (self.y_loc() + 1))))]) and (self.y_loc() != 3))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('unknown' == self.blackboard.tiles[(self.x_loc() + (4 * min(3, (self.y_loc() + 1))))]) and (self.y_loc() != 3))

    def left_unknown(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('unknown' == self.blackboard.tiles[(max(0, (self.x_loc() - 1)) + (4 * self.y_loc()))]) and (self.x_loc() != 0))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('unknown' == self.blackboard.tiles[(max(0, (self.x_loc() - 1)) + (4 * self.y_loc()))]) and (self.x_loc() != 0))

    def right_unknown(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('unknown' == self.blackboard.tiles[(min(3, (self.x_loc() + 1)) + (4 * self.y_loc()))]) and (self.x_loc() != 3))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('unknown' == self.blackboard.tiles[(min(3, (self.x_loc() + 1)) + (4 * self.y_loc()))]) and (self.x_loc() != 3))

    def need_new_subgoal(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (('hole' == self.blackboard.tiles[(self.blackboard.x_subgoal() + (4 * self.blackboard.y_subgoal()))]) or (self.loc == self.blackboard.subgoal))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (('hole' == self.blackboard.tiles[(self.blackboard.x_subgoal() + (4 * self.blackboard.y_subgoal()))]) or (self.loc == self.blackboard.subgoal))

    def need_up(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.y_loc() > self.blackboard.y_subgoal())
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.y_loc() > self.blackboard.y_subgoal())

    def need_down(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.y_loc() < self.blackboard.y_subgoal())
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.y_loc() < self.blackboard.y_subgoal())

    def need_left(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.x_loc() > self.blackboard.x_subgoal())
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.x_loc() > self.blackboard.x_subgoal())

    def need_right(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.x_loc() < self.blackboard.x_subgoal())
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.x_loc() < self.blackboard.x_subgoal())

    def reached_goal(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        ('goal' == self.blackboard.tiles[self.loc])
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return ('goal' == self.blackboard.tiles[self.loc])

    def subgoal_unreachable(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        ('hole' == self.blackboard.tiles[self.blackboard.subgoal])
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return ('hole' == self.blackboard.tiles[self.blackboard.subgoal])

    def get_info_func__condition(self, node):
        if True:
            return True
        else:
            return False


    def get_info_func__0(self, node):
        return [(self.loc, (
            'goal'
            if (self.loc == self.goal_loc) else
            (
                'hole'
                if (self.loc == self.hole_loc) else
                (
                'safe'
        ))))]
