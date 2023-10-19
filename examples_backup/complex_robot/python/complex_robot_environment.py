import random
import serene_safe_assignment


class complex_robot_environment():
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
        self.tile_progress = serene_safe_assignment.tile_progress((
            0
            if (self.tile_tracker == self.tile_progress) else
            (
            self.tile_progress
        )))
        self.tile_tracker = serene_safe_assignment.tile_tracker(self.tile_progress)
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def active_hole():
            return (
                self.hole_1
                if ((self.x + min(0, self.blackboard.forward())) == 4) else
                (
                    self.hole_2
                    if ((self.x + min(0, self.blackboard.forward())) == (4 + 1)) else
                    (
                        self.hole_3
                        if ((self.x + min(0, self.blackboard.forward())) == (4 + 2)) else
                        (
                            self.hole_4
                            if ((self.x + min(0, self.blackboard.forward())) == (4 + 3)) else
                            (
                                self.hole_5
                                if ((self.x + min(0, self.blackboard.forward())) == (4 + 4)) else
                                (
                                    self.hole_6
                                    if ((self.x + min(0, self.blackboard.forward())) == (4 + 5)) else
                                    (
                                        self.hole_7
                                        if ((self.x + min(0, self.blackboard.forward())) == (4 + 6)) else
                                        (
                                            self.hole_8
                                            if ((self.x + min(0, self.blackboard.forward())) == (4 + 7)) else
                                            (
                                                self.hole_9
                                                if ((self.x + min(0, self.blackboard.forward())) == (4 + 8)) else
                                                (
                                                -1
            ))))))))))

        self.active_hole = active_hole


        def flag_returned():
            return (self.blackboard.have_flag and (self.x <= 3))

        self.flag_returned = flag_returned
        self.x = serene_safe_assignment.x(0)
        self.y = serene_safe_assignment.y(0)
        self.hole_1 = serene_safe_assignment.hole_1(random.choice([0, 1, 2]))
        self.hole_2 = serene_safe_assignment.hole_2(random.choice([0, 1, 2]))
        self.hole_3 = serene_safe_assignment.hole_3(random.choice([0, 1, 2]))
        self.hole_4 = serene_safe_assignment.hole_4(random.choice([0, 1, 2]))
        self.hole_5 = serene_safe_assignment.hole_5(random.choice([0, 1, 2]))
        self.hole_6 = serene_safe_assignment.hole_6(random.choice([0, 1, 2]))
        self.hole_7 = serene_safe_assignment.hole_7(random.choice([0, 1, 2]))
        self.hole_8 = serene_safe_assignment.hole_8(random.choice([0, 1, 2]))
        self.hole_9 = serene_safe_assignment.hole_9(random.choice([0, 1, 2]))
        self.flag_x = serene_safe_assignment.flag_x(random.choice([15, 16, 17, 18]))
        self.flag_y = serene_safe_assignment.flag_y(random.choice([0, 1, 2]))
        self.tile_progress = serene_safe_assignment.tile_progress(0)
        self.tile_tracker = serene_safe_assignment.tile_tracker(0)

    def flag_not_returned(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        not (self.flag_returned())
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return not (self.flag_returned())

    def can_move_forward(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (((self.blackboard.forward() + self.x) >= 0) and ((self.blackboard.forward() + self.x) <= 18) and ((self.active_hole() == -1) or (self.active_hole() == self.y)))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (((self.blackboard.forward() + self.x) >= 0) and ((self.blackboard.forward() + self.x) <= 18) and ((self.active_hole() == -1) or (self.active_hole() == self.y)))

    def can_move_side(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (((self.blackboard.side + self.y) >= 0) and ((self.blackboard.side + self.y) <= 2))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (((self.blackboard.side + self.y) >= 0) and ((self.blackboard.side + self.y) <= 2))

    def go_forward_func__0(self, node):
        self.x = serene_safe_assignment.x((
            (self.x + self.blackboard.forward())
            if (((self.blackboard.forward() + self.x) >= 0) and ((self.blackboard.forward() + self.x) <= 18) and ((self.active_hole() == -1) or (self.active_hole() == self.y))) else
            (
            self.x
        )))
        return

    def go_side_func__0(self, node):
        self.y = serene_safe_assignment.y((
            (self.y + self.blackboard.side)
            if (((self.blackboard.side + self.y) >= 0) and ((self.blackboard.side + self.y) <= 2)) else
            (
            self.y
        )))
        return

    def search_tile_func__condition(self, node):
        if True:
            return True
        else:
            return False


    def search_tile_func__0(self, node):
        return (
            True
            if (self.tile_progress == 2) else
            (
            random.choice([True, False])
        ))

    def search_tile_func__1(self, node):
        return (
            True
            if self.blackboard.have_flag else
            (
            (node.tile_searched and (self.x == self.flag_x) and (self.y == self.flag_y))
        ))

    def update_search_func__0(self, node):
        self.tile_progress = serene_safe_assignment.tile_progress((
            2
            if node.tile_searched else
            (
            min(2, (1 + self.tile_progress))
        )))
        return

    def compute_zone_func__condition(self, node):
        if True:
            return True
        else:
            return False


    def compute_zone_func__0(self, node):
        return (
            'home'
            if (self.x <= 3) else
            (
                'target'
                if (self.x >= 15) else
                (
                'maze'
        )))
