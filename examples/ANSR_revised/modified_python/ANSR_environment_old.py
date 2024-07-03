# from pathlib import Path # I don't know what this was, but it seems not relevant now.
import random # not used
# import onnxruntime # not used
import os
import adk_node.msg # for msg_types
import rclpy.qos # for setting QoS for pub/sub

import geometry_msgs # for creating the path that is published (it's a single point).
import nav_msgs # for odometry

# import airsim # probabl needs to be cut.
import numpy as np # for numpy calculations
from ebt.bt.obstacle_info import obs_info

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

    # def convert_to_adk(self, position_x, position_y):
    #     # intentionally swap coordinates, because of weirdness
    #     return (
    #         float((position_y * self.scale) + self.offset[1]),
    #         float((position_x * self.scale) + self.offset[0])
    #     )

    # # def convert_to_airsim(self, position_x, position_y, scale = 8, altitude = -10):
    # #     return airsim.Vector3r(
    # #         float(position_x * scale + self.offset[0]),
    # #         float(position_y * scale + self.offset[1]),
    # #         altitude)

    # # def convert_from_airsim(self, position, scale = 8):
    # #     return (round((position.x_val - self.offset[0]) / scale), round((position.y_val - self.offset[1]) / scale))

    # def convert_from_adk(self, position_x, position_y):
    #     # intentionally reverse x and y
    #     return (
    #         round(((position_y - self.offset[1]) / self.scale)),
    #         round(((position_x - self.offset[0]) / self.scale))
    #     )

    # def convert_from_planner(self, position_x, position_y):
    #     # adk_x = (position_x * self.planner_scale) + self.planner_offset[0]
    #     # adk_y = (position_y * self.planner_scale) + self.planner_offset[1]
    #     adk_x = (position_x + self.planner_offset[0]) * self.planner_scale
    #     adk_y = (position_y + self.planner_offset[1]) * self.planner_scale
    #     return self.convert_from_adk(adk_x, adk_y)

    def __init__(self, blackboard, serene_height):
        self.serene_points = True
        self.tick_count = 0
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.obstacles = None
        self.obstacle_sizes = None
        self.altitude = -1 * serene_height
        self.scale = 8 # for converting from serene grid to actual grid
        self.offset = (-200, -200) # for converting from serene grid to actual grid

        self.ros_node = None
        self.action_publisher = None
        self.planner_subscriber = None
        self.planner_position = None
        self.planner_position_x = None
        self.planner_position_y = None
        self.planner_position_z = None
        self.odometry_subscriber = None
        self.odometry_position = None
        self.odometry_position_x = None
        self.odometry_position_y = None
        self.odometry_position_z = None
        return

    def odometry_callback(self, msg):
        if msg is not None:
            self.odometry_position = msg.pose.pose.position

    def planner_callback(self, msg):
        if msg is not None:
            self.planner_position = msg.pose.position

    # def setup_planner_info(self, planner_scale, planner_offset):
    #     self.planner_scale = planner_scale
    #     self.planner_offset = planner_offset

    def setup_pub_sub(self, ros_node, planner_msg_type, planner_msg_topic, planner_qos_profile):
        self.ros_node = ros_node
        self.action_publisher = self.ros_node.create_publisher(
            msg_type = adk_node.msg.WaypointPath,
            topic = '/adk_node/input/waypoints',
            qos_profile = rclpy.qos.QoSProfile(
                reliability = rclpy.qos.QoSReliabilityPolicy.RELIABLE,
                durability = rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL,
                history = rclpy.qos.QoSHistoryPolicy.KEEP_LAST,
                depth = 1
            )
        )
        self.odometry_subscriber = self.ros_node.create_subscription(
            msg_type = nav_msgs.msg.Odometry,
            topic = '/adk_node/SimpleFlight/odom_local_ned',
            callback = self.odometry_callback,
            qos_profile = rclpy.qos.QoSProfile(
                reliability = rclpy.qos.QoSReliabilityPolicy.RELIABLE,
                durability = rclpy.qos.QoSDurabilityPolicy.VOLATILE,
                history = rclpy.qos.QoSHistoryPolicy.KEEP_LAST,
                depth = 1
            )
        )
        self.planner_subscriber  = self.ros_node.create_subscription(
            msg_type = planner_msg_type,
            topic = planner_msg_topic,
            callback = self.planner_callback,
            qos_profile = planner_qos_profile
        )
        # for publish
        # --> just action, I think. DONE?
        # for subscribe
        # --> planner destination
        # --> current location (look at task_update_subgoal for this. seems to process odometry data there).

    def initialize_environment(self):
        node = None
        (self.obstacles, self.obstacle_sizes) = obs_info(-1 * self.altitude)
        return


    def function_get_new_destination__condition(self, node):
        if self.planner_position is not None:
            self.planner_position_x = int(self.planner_position.x)
            self.planner_position_y = int(self.planner_position.y)
            self.planner_position_z = int(self.planner_position.z)
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('get new destination -> SUCCESS\n'
                                 + str((self.planner_position_x, self.planner_position_y, self.planner_position_z)) + '\n'
                                 )
            return True
        elif self.serene_points:
            self.planner_position_x = min(400, max(0, self.blackboard.drone_x + random.randint(-6, 6)))
            self.planner_position_y = min(400, max(0, self.blackboard.drone_y + random.randint(-6, 6)))
            return True
        else:
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('get new destination -> FAILED\n')
            return False


    def function_get_new_destination__0(self, node):
        return self.planner_position_x

    def function_get_new_destination__1(self, node):
        return self.planner_position_y

    def function_get_new_destination__2(self, node):
        return self.planner_position_z

    def function_get_position__condition(self, node):
        if self.odometry_position is not None:
            self.odometry_position_x = int(self.odometry_position.x)
            self.odometry_position_y = int(self.odometry_position.y)
            self.odometry_position_z = int(self.odometry_position.z)
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('update position -> SUCCESS\n'
                                 + str((self.odometry_position_x, self.odometry_position_y, self.odometry_position_z)) + '\n'
                                 )
            return True
        else:
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('update position -> FAILED\n')
            return False


    def function_get_position__0(self, node):
        if self.odometry_position is not None:
            return (
                (self.odometry_position_x != self.blackboard.drone_x)
                or
                (self.odometry_position_y != self.blackboard.drone_y)
                or
                (self.odometry_position_z != self.blackboard.drone_z)
            )
        else:
            return False

    def function_get_position__1(self, node):
        return self.odometry_position_x

    def function_get_position__2(self, node):
        return self.odometry_position_y

    def function_get_position__3(self, node):
        return self.odometry_position_z

    def function_send_action__0(self, node):
        # self.executing_action = self.blackboard.current_action
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('sent an action! ' + str(self.blackboard.current_action) + '\n')

        go_to_x = (
            max(0, (self.blackboard.drone_x - 1))
            if (self.blackboard.current_action == 'west') else
            (
                min(49, (self.blackboard.drone_x + 1))
                if (self.blackboard.current_action == 'east') else
                (
                self.blackboard.drone_x
        )))
        go_to_y = (
            max(0, (self.blackboard.drone_y - 1))
            if (self.blackboard.current_action == 'south') else
            (
                min(49, (self.blackboard.drone_y + 1))
                if (self.blackboard.current_action == 'north') else
                (
                self.blackboard.drone_y
        )))
        go_to_z = self.blackboard.drone_z if (self.blackboard.current_action in ('west', 'east', 'south', 'north', 'no_action')) else self.blackboard.current_action[1]

        # original
        # airsim_pos = self.convert_to_airsim(go_to_y, go_to_x)
        # self.client.moveOnPathAsync([airsim_pos], velocity=4, drivetrain=airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(False, 0), lookahead=-1, adaptive_lookahead=1).join()

        # new
        # (go_to_x_conv, go_to_y_conv) = self.convert_to_adk(go_to_x, go_to_y)
        go_to = geometry_msgs.msg.PoseStamped()
        go_to.pose.position.x = float(go_to_x)
        go_to.pose.position.y = float(go_to_y)
        go_to.pose.position.z = float(go_to_z * -1)
        go_to.pose.orientation.w = 1.0 # no idea what this does.
        go_to.header.frame_id = "map" # i assume this is relevant somehow.
        message_to_send = adk_node.msg.WaypointPath()
        # message_to_send.velocity = 2.0
        message_to_send.velocity = 4.0
        # message_to_send.velocity = 8.0
        message_to_send.lookahead = -1.0
        message_to_send.adaptive_lookahead = 1.0
        message_to_send.wait_on_last_task = True
        message_to_send.path = [go_to]
        self.action_publisher.publish(message_to_send)
        with open('/output/serene_parse.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write(
                '------------------------' + os.linesep
                + 'State after tick: ' + str(self.tick_count) + os.linesep
                + self.print_blackboard() + os.linesep
                + 'local' + os.linesep
                + self.print_environment() + os.linesep
            )
            self.tick_count += 1
        return

    def indent(self, n):
        return '  '*n

    def print_blackboard(self):
        ret_string = 'blackboard' + os.linesep
        ret_string += self.indent(1) + 'drone_x: ' + str(self.blackboard.drone_x) + os.linesep
        ret_string += self.indent(1) + 'drone_y: ' + str(self.blackboard.drone_y) + os.linesep
        ret_string += self.indent(1) + 'drone_z: ' + str(self.blackboard.drone_z) + os.linesep
        ret_string += self.indent(1) + 'destination_x: ' + str(self.blackboard.destination_x) + os.linesep
        ret_string += self.indent(1) + 'destination_y: ' + str(self.blackboard.destination_y) + os.linesep
        ret_string += self.indent(1) + 'destination_z: ' + str(self.blackboard.destination_z) + os.linesep
        ret_string += self.indent(1) + 'cell_changed_var: ' + str(self.blackboard.cell_changed_var) + os.linesep
        ret_string += self.indent(1) + 'current_action: ' + str(self.blackboard.current_action) + os.linesep
        ret_string += self.indent(1) + 'network: ' + str(self.blackboard.network) + os.linesep
        return ret_string


    def print_environment(self):
        return 'environment'
        # ret_string = 'environment' + os.linesep
        # ret_string += self.indent(1) + 'obstacles: ' + str(self.obstacles) + os.linesep
        # ret_string += self.indent(1) + 'obstacle_sizes: ' + str(self.obstacle_sizes) + os.linesep
        # # ret_string += self.indent(1) + 'executing_action: ' + str(self.executing_action) + os.linesep
        # return ret_string
