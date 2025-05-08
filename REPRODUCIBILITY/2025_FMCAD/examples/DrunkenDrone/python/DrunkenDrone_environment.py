from pathlib import Path
import random
import onnxruntime


class DrunkenDrone_environment():
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
        self.x_g = (
            self.blackboard.serene_randomizer.r_1(node)
            if self.blackboard.new else
            (
                self.x_g
        ))
        self.y_g = (
            self.blackboard.serene_randomizer.r_2(node)
            if self.blackboard.new else
            (
                self.y_g
        ))
        self.x_d = (
            max(0, (self.x_d - 1))
            if (self.blackboard.act == 'We') else
            (
                min(19, (self.x_d + 1))
                if (self.blackboard.act == 'Ea') else
                (
                    self.x_d
        )))
        self.y_d = (
            max(0, (self.y_d - 1))
            if (self.blackboard.act == 'So') else
            (
                min(19, (self.y_d + 1))
                if (self.blackboard.act == 'No') else
                (
                    self.y_d
        )))
        return

    def check_tick_condition(self):
        return (True)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.x_d = None
        self.y_d = None
        self.x_g = None
        self.y_g = None
        return

    def initialize_environment(self):
        node = None
        self.x_d = 0
        self.y_d = 0
        self.x_g = self.x_d
        self.y_g = self.y_d
        return


    def NeedNew(self, node):
        '''
        -- RETURN
        This method is expected to return True or False.
        This method is being modeled using the following behavior:
        ((self.x_g == self.x_d) and (self.y_g == self.y_d))
        -- SIDE EFFECTS
        This method is expected to have no side effects (for the tree).
        '''
        # below we include an auto generated attempt at implmenting this
        return ((self.x_g == self.x_d) and (self.y_g == self.y_d))
