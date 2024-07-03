# from pathlib import Path
# import random
# Above BehaVerify generated. Modified to remove unused components
import os # for formatting logging
import adk_node.msg # for msg_types
import rclpy.qos # for setting QoS for pub/sub
import geometry_msgs # for creating the path that is published (it's a single point)
import nav_msgs # for odometry
#import map??? missing

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
        return True

    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.delayed_action_queue = []

        # self.fake = None
        # Above BehaVerify generated. Modified to remove unused components

        self.ros_node = None
        self.odometry_subscriber = None # for figuring out where the drone is
        self.odometry_position = None
        self.map_subscriber = None # for figuring out where obstacles are
        self.map_vals = None
        self.planner_subscriber = None # for figuring out where the drone needs to go
        self.planner_position = None
        self.planner_publisher = None # for responding to invalid locations
        self.action_publisher = None
        return

    def odometry_callback(self, msg):
        if msg is not None:
            self.odometry_position = msg.pose.pose.position

    def map_callback(self, msg):
        if msg is not None:
            self.odometry_position = msg.pose.pose.position

    def planner_callback(self, msg):
        if msg is not None:
            self.planner_position = msg.pose.position

    def initialize_environment(self):
        node = None
        # self.fake = 0
        # Above BehaVerify generated. Modified to remove unused components
        return


    def read_position_function__condition(self, node):
        if True:
            return True
        else:
            return False


    def read_position_function__0(self, node):
        return self.blackboard.serene_randomizer.r_0(node)

    def read_position_function__1(self, node):
        return self.blackboard.serene_randomizer.r_1(node)

    def read_position_function__2(self, node):
        return self.blackboard.serene_randomizer.r_2(node)

    def read_position_function__3(self, node):
        return (
            min(1, max((-1), (self.blackboard.drone_x - self.blackboard.previous_x)))
            if ((self.blackboard.drone_x != self.blackboard.previous_x) or (self.blackboard.drone_y != self.blackboard.previous_y) or (self.blackboard.drone_z != self.blackboard.previous_z)) else
            (
                self.blackboard.drone_x_delta
        ))

    def read_position_function__4(self, node):
        return (
            min(1, max((-1), (self.blackboard.drone_y - self.blackboard.previous_y)))
            if ((self.blackboard.drone_x != self.blackboard.previous_x) or (self.blackboard.drone_y != self.blackboard.previous_y) or (self.blackboard.drone_z != self.blackboard.previous_z)) else
            (
                self.blackboard.drone_y_delta
        ))

    def read_destination_function__condition(self, node):
        if True:
            return True
        else:
            return False


    def read_destination_function__0(self, node):
        return self.blackboard.serene_randomizer.r_3(node)

    def read_destination_function__1(self, node):
        return self.blackboard.serene_randomizer.r_4(node)

    def read_destination_function__2(self, node):
        return self.blackboard.serene_randomizer.r_5(node)

    def request_new_destination_function__0(self, node):
        # self.fake = 0
        # Above BehaVerify generated. Modified to remove unused components
        return

    def read_map_function__condition(self, node):
        if True:
            return True
        else:
            return False


    def read_map_function__0(self, node):
        return True

    def compute_path_function__condition(self, node):
        if True:
            return True
        else:
            return False


    def compute_path_function__0(self, node):
        return 0

    def compute_path_function__1(self, node):
        return 0

    def compute_path_function__2(self, node):
        return 0

    def send_path_function__0(self, node):
        # self.fake = 0
        # Above BehaVerify generated. Modified to remove unused components
        return
