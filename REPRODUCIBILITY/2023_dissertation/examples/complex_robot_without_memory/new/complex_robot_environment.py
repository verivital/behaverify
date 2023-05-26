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

    def between_tick_environment_update(self):
        if (self.tile_tracker == self.tile_progress):
            self.tile_progress = 0
        else:
            self.tile_progress = self.tile_progress
        self.tile_tracker = self.tile_progress
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.x = 0
        self.y = 0
        self.hole_1 = random.choice([0, 1, 2])
        self.hole_2 = random.choice([0, 1, 2])
        self.hole_3 = random.choice([0, 1, 2])
        self.hole_4 = random.choice([0, 1, 2])
        self.hole_5 = random.choice([0, 1, 2])
        self.hole_6 = random.choice([0, 1, 2])
        self.hole_7 = random.choice([0, 1, 2])
        self.hole_8 = random.choice([0, 1, 2])
        self.hole_9 = random.choice([0, 1, 2])
        self.flag_x = random.choice([15, 16, 17, 18])
        self.flag_y = random.choice([0, 1, 2])
        self.tile_progress = 0
        self.tile_tracker = 0

    def active_hole(self):
        if ((self.x + min(0, self.blackboard.forward())) == 4):
            _active_hole_value_to_return_ = self.hole_1
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 1)):
            _active_hole_value_to_return_ = self.hole_2
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 2)):
            _active_hole_value_to_return_ = self.hole_3
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 3)):
            _active_hole_value_to_return_ = self.hole_4
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 4)):
            _active_hole_value_to_return_ = self.hole_5
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 5)):
            _active_hole_value_to_return_ = self.hole_6
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 6)):
            _active_hole_value_to_return_ = self.hole_7
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 7)):
            _active_hole_value_to_return_ = self.hole_8
        elif ((self.x + min(0, self.blackboard.forward())) == (4 + 8)):
            _active_hole_value_to_return_ = self.hole_9
        else:
            _active_hole_value_to_return_ = -1
        return _active_hole_value_to_return_

    def flag_returned(self):
        _flag_returned_value_to_return_ = (self.blackboard.have_flag and (self.x <= 3))
        return _flag_returned_value_to_return_

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
        if (((self.blackboard.forward() + self.x) >= 0) and ((self.blackboard.forward() + self.x) <= 18) and ((self.active_hole() == -1) or (self.active_hole() == self.y))):
            update_val_x = (self.x + self.blackboard.forward())
        else:
            update_val_x = self.x
        self.x = serene_safe_assignment.x(update_val_x)
        return

    def go_side_func__0(self, node):
        if (((self.blackboard.side + self.y) >= 0) and ((self.blackboard.side + self.y) <= 2)):
            update_val_y = (self.y + self.blackboard.side)
        else:
            update_val_y = self.y
        self.y = serene_safe_assignment.y(update_val_y)
        return

    def search_tile_func__condition(self, node):
        if True:
            return True
        else:
            return False


    def search_tile_func__0(self, node):
        if (self.tile_progress == 2):
            to_return_tile_searched = True
        else:
            to_return_tile_searched = random.choice([True, False])
        return to_return_tile_searched

    def search_tile_func__1(self, node):
        if self.blackboard.have_flag:
            to_return_have_flag = True
        else:
            to_return_have_flag = (node.tile_searched and (self.x == self.flag_x) and (self.y == self.flag_y))
        return to_return_have_flag

    def update_search_func__0(self, node):
        if node.tile_searched:
            update_val_tile_progress = 2
        else:
            update_val_tile_progress = min(2, (1 + self.tile_progress))
        self.tile_progress = serene_safe_assignment.tile_progress(update_val_tile_progress)
        return

    def compute_zone_func__condition(self, node):
        if True:
            return True
        else:
            return False


    def compute_zone_func__0(self, node):
        if (self.x <= 3):
            to_return_zone = 'home'
        elif (self.x >= 15):
            to_return_zone = 'target'
        else:
            to_return_zone = 'maze'
        return to_return_zone
