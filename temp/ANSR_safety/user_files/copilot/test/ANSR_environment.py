from pathlib import Path
import random
import ctypes

monitor_lib = ctypes.CDLL('./monitor.so')
# monitor_lib.step.argtypes = []
# monitor_lib.step.restypes = None
# drone_x = ctypes.c_int32.in_dll(monitor_lib, 'drone_x')
# drone_y = ctypes.c_int32.in_dll(monitor_lib, 'drone_y')
# delta_x = ctypes.c_int32.in_dll(monitor_lib, 'delta_x')
# delta_y = ctypes.c_int32.in_dll(monitor_lib, 'delta_y')
# slow_down = ctypes.c_bool.in_dll(monitor_lib, 'slow_down')
monitor_lib.driver.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
monitor_lib.driver.restypes = ctypes.c_bool

class ANSR_environment():
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
        return

    def check_tick_condition(self):
        return (True)

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.obstacles = None
        self.obstacle_sizes = None
        self.executing_action = None
        return

    def initialize_environment(self):
        node = None
        self.obstacles = [None for _ in range(4)]
        self.obstacles[0] = 3
        self.obstacles[1] = 3
        self.obstacles[2] = 0
        self.obstacles[3] = 4
        self.obstacle_sizes = [None for _ in range(2)]
        self.obstacle_sizes[0] = 1
        self.obstacle_sizes[1] = 0
        self.executing_action = 'no_action'
        return


    def function_get_new_destination__condition(self, node):
        if True:
            return True
        else:
            return False


    def function_get_new_destination__0(self, node):
        return self.blackboard.serene_randomizer.r_0(node)

    def function_get_new_destination__1(self, node):
        return self.blackboard.serene_randomizer.r_1(node)

    def function_get_velocity__condition(self, node):
        if True:
            return True
        else:
            return False

    convert_action = {
        'left' : (-1, 0),
        'right' : (1, 0),
        'up' : (0, 1),
        'down' : (0, -1),
        'no_action' : (0, 0)
    }

    def function_get_velocity__0(self, node):
        (dx, dy) = self.convert_action[self.blackboard.current_action]
        slow_down = monitor_lib.driver(self.blackboard.drone_x, self.blackboard.drone_y, dx, dy)
        if slow_down:
            return 1
        print('----------------------------------------------------------------------------------------------')
        return 2

    def function_get_position__condition(self, node):
        if True:
            return True
        else:
            return False


    def function_get_position__0(self, node):
        return True

    def function_get_position__1(self, node):
        return (
            max(0, (self.blackboard.drone_x - self.blackboard.drone_speed))
            if (self.blackboard.current_action == 'left') else
            (
                min(6, (self.blackboard.drone_x + self.blackboard.drone_speed))
                if (self.blackboard.current_action == 'right') else
                (
                self.blackboard.drone_x
        )))

    def function_get_position__2(self, node):
        return (
            max(0, (self.blackboard.drone_y - self.blackboard.drone_speed))
            if (self.blackboard.current_action == 'down') else
            (
                min(6, (self.blackboard.drone_y + self.blackboard.drone_speed))
                if (self.blackboard.current_action == 'up') else
                (
                self.blackboard.drone_y
        )))

    def function_send_action__0(self, node):
        self.executing_action = self.blackboard.current_action
        return
