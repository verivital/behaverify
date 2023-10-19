import random
import serene_safe_assignment


class light_controller_environment():
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
        self.tunnel_state = serene_safe_assignment.tunnel_state((
            random.choice([self.tunnel_state, 'empty'])
            if (self.light == 'off') else
            (
            random.choice([self.light, 'empty'])
        )))
        self.west_cars = serene_safe_assignment.west_cars((
            random.choice([True, False])
            if (self.light == 'west_to_east') else
            (
            random.choice([True, self.west_cars])
        )))
        self.east_cars = serene_safe_assignment.east_cars((
            random.choice([True, False])
            if (self.light == 'east_to_west') else
            (
            random.choice([True, self.east_cars])
        )))
        return

    def check_tick_condition(self):
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []



        def west_and_east_cars():
            return (self.west_cars and self.east_cars)

        self.west_and_east_cars = west_and_east_cars
        self.tunnel_state = serene_safe_assignment.tunnel_state('empty')
        self.east_cars = serene_safe_assignment.east_cars(random.choice([True, False]))
        self.west_cars = serene_safe_assignment.west_cars(random.choice([True, False]))
        self.light = serene_safe_assignment.light('off')

    def check_tunnel_in_use(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        (self.tunnel_state != 'empty')
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return (self.tunnel_state != 'empty')

    def check_west_and_east_cars(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        self.west_and_east_cars()
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return self.west_and_east_cars()

    def check_west_cars(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        self.west_cars
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return self.west_cars

    def check_east_cars(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        self.east_cars
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return self.east_cars

    def light_signal_func__0(self, node):
        self.light = serene_safe_assignment.light((
            self.blackboard.direction
            if self.blackboard.signal else
            (
            'off'
        )))
        return
