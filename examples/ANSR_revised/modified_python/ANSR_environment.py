# from pathlib import Path
# import random
# Above BehaVerify generated. Modified to remove unused components
from collections import namedtuple # for faking points
import random # for faking points
import math # for floor
# import os # for formatting logging
import adk_node.msg # for msg_types
import rclpy.qos # for setting QoS for pub/sub
import geometry_msgs # for creating the path that is published (it's a single point)
import nav_msgs # for odometry
import std_msgs.msg # for things like string
#import map??? missing

from ebt.bt.advanced_a_star import a_star

from vanderbilt_utils.binvox_tools import convert_binvox # for handling the map
from vanderbilt_interfaces.msg import ObstacleMap

from vanderbilt_utils.interface_definitions import message_settings

import numpy

# for info about subscribing to topics: https://git.isis.vanderbilt.edu/ansr/ebt/-/blob/main/ebt/bt/composite_construction/topics_processing.py?ref_type=heads
# for info about converting the map: https://git.isis.vanderbilt.edu/ansr/ebt/-/blob/main/ebt/bt/behaviors/task_transform_obstacles.py?ref_type=heads
# for info about vanderbilt messages: https://git.isis.vanderbilt.edu/ansr/vanderbilt_utils/-/blob/master/vanderbilt_utils/interface_definitions/message_settings.py?ref_type=heads
# for more info about vanderbilt messages: https://git.isis.vanderbilt.edu/ansr/vanderbilt_interface/-/blob/master/msg/Camera.msg?ref_type=heads

FAKE_POINT = namedtuple('fake_point', ['x', 'y', 'z'])

class ANSR_environment():
    def delay_this_action(self, action, node):
        # DONE!
        self.delayed_action_queue.append((action, node))

    def execute_delayed_action_queue(self):
        # DONE!
        for (delayed_action, node) in self.delayed_action_queue:
            delayed_action(node)
        self.delayed_action_queue = []
        return

    def pre_tick_environment_update(self):
        # DONE!
        node = None
        return

    def post_tick_environment_update(self):
        # DONE!
        node = None
        return

    def check_tick_condition(self):
        # DONE!
        return True

    def __init__(self, blackboard):
        # DONE!
        self.blackboard = blackboard
        self.delayed_action_queue = []

        self.map_x_size = None
        self.map_x_min = None
        self.map_x_max = None
        self.map_y_size = None
        self.map_y_min = None
        self.map_y_max = None
        self.map_z_vals = [] # slices at which we can fly.
        self.z_costs = {} # costs
        self.binvox_converter = None
        self.cost_graph = None
        self.obstacle_maps = None

        self.map_data = None
        self.path = []
        self.waypoint = None
        self.update_radius = None
        self.initial_goal = True
        self.fake_goals = False

        self.ros_node = None
        self.odometry_subscriber = None # for figuring out where the drone is
        self.odometry_position = None
        self.map_subscriber = None # for figuring out where obstacles are
        self.goal_subscriber = None # for figuring out where the drone needs to go
        self.goal_position = None
        self.goal_information_publisher = None # for responding to invalid locations
        self.waypoint_publisher = None
        return

    def calculate_cost(self, x1, y1, z1, x2, y2, z2):
        # DONE!
        try:
            height_multiplier = self.z_costs[z2]
        except:
            height_multiplier = 1 + len(self.map_z_vals)
        diff_val = (x2 - x1, y2 - y1, z2 - z1)
        base_val = 1 + (3 - diff_val.count(0))
        return base_val * height_multiplier

    def map_callback(self, msg):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('got: map\n')
        if msg is not None:
            self.map_data = msg.data

    def odometry_callback(self, msg):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('got: odometry\n')
        if msg is not None:
            self.odometry_position = msg.pose.pose.position

    def goal_callback(self, msg):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('got: goal\n')
        if msg is not None:
            self.goal_position = msg.pose.position

    def setup_pub_sub(self, ros_node):
        # DONE!
        self.ros_node = ros_node
        settings = message_settings.Messages()
        self.goal_information_publisher = self.ros_node.create_publisher(
            msg_type = settings.invalid_goal.msg_type,
            topic = settings.invalid_goal.topic,
            qos_profile = settings.invalid_goal.qos_profile
        )
        self.waypoint_publisher = self.ros_node.create_publisher(
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
        self.goal_subscriber = self.ros_node.create_subscription(
            msg_type = settings.goal.msg_type,
            topic = settings.goal.topic,
            callback = self.goal_callback,
            qos_profile = settings.goal.qos_profile
        )
        self.map_subscriber = self.ros_node.create_subscription(
            msg_type = settings.obstacle_map_raw.msg_type,
            topic = settings.obstacle_map_raw.topic,
            callback = self.map_callback,
            qos_profile = settings.obstacle_map_raw.qos_profile
        )

    def initialize_environment(self, map_x_size, map_y_size, map_z_vals, update_radius, fake_goals):
        # DONE!
        node = None
        self.map_x_size = map_x_size
        self.map_x_min = -1 * self.map_x_size // 2
        self.map_x_max = self.map_x_size // 2
        self.map_y_size = map_y_size
        self.map_y_min = -1 * self.map_y_size // 2
        self.map_y_max = self.map_y_size // 2
        self.map_z_vals = map_z_vals
        self.z_costs = {z : (index + 1) for (index, z) in enumerate(self.map_z_vals)}
        self.binvox_converter = convert_binvox.ConvertBinvox()
        self.update_radius = update_radius
        self.fake_goals = fake_goals
        return

    def read_position_function__condition(self, node):
        # DONE!
        if self.odometry_position is not None:
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('read: position\ndrone_true: ' + str((self.odometry_position.x, self.odometry_position.y, self.odometry_position.z)) + '\n')
            return True
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('read: position\nFAILED: position!\n')
        return False

    def read_position_function__0(self, node):
        # DONE!
        # note: x and y intentionally swapped for value, because odom is in NED but we're in ENU
        x = round(self.odometry_position.y)
        y = round(self.odometry_position.x)
        z = math.floor(self.odometry_position.z * (-1))
        prev_height = 0
        broke = False
        for height in self.map_z_vals:
            if z < height:
                z = prev_height
                broke = True
                break
            if z == height:
                z = height
                broke = True
                break
            prev_height = height
        if not broke:
            z = prev_height
        position = (x, y, z)
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('position : ' + str(position) + '\n')
        self.odometry_position = None
        return enumerate(position)

    def read_goal_function__condition(self, node):
        # DONE!
        if self.fake_goals and self.goal_position is None and self.blackboard.goal_requested:
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('CREATED A FAKE GOAL\n')
            self.goal_position = FAKE_POINT(random.randint(self.map_x_min, self.map_x_max), random.randint(self.map_y_min, self.map_y_max), random.choice(self.map_z_vals))
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write(
                'read: goal\n'
                + (
                    ('goal true: ' + str((self.goal_position.x, self.goal_position.y, self.goal_position.z)))
                    if self.goal_position is not None else
                    'FAILED: goal'
                )
                +'\n'
            )
        return self.goal_position is not None

    def read_goal_function__0(self, node):
        # DONE!
        x = round(self.goal_position.x)
        y = round(self.goal_position.y)
        z = round(self.goal_position.z)
        if z not in self.map_z_vals:
            height = 0
            for height in self.map_z_vals:
                if z <= height:
                    break
            z = height
        goal = (x, y, z)
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('goal : ' + str(goal) + '\n')
        self.goal_position = None
        return enumerate(goal)

    def read_goal_function__1(self, node):
        # updates goal requested
        return False

    def read_goal_function__2(self, node):
        # udpates valid goal
        return True

    def check_safety(self, x, y, z, check_cell_only = False):
        '''
        return True if safe, False if unsafe
        '''
        return (
            not (
                self.obstacle_maps[z][x + self.map_x_min][y + self.map_y_min]
                if check_cell_only else
                (
                    any(
                        self.obstacle_maps[z][x1 + self.map_x_min][y1 + self.map_y_min]
                        for x1 in range(max(self.map_x_min, x - 1), min(self.map_x_max + 1, x + 1))
                        for y1 in range(max(self.map_y_min, y - 1), min(self.map_y_max + 1, y + 1))
                    )
                )
            )
        )
        # return not(
        #     self.obstacle_maps[z][x][y] or
        #     self.obstacle_maps[z][max(-1 * self.map_x_size // 2, x - 1)][y] or
        #     self.obstacle_maps[z][min(self.map_x_size // 2, x + 1)][y] or
        #     self.obstacle_maps[z][x][max(-1 * self.map_y_size // 2, y - 1)] or
        #     self.obstacle_maps[z][x][min(self.map_y_size // 2, y + 1)]
        # )
        # return not self.obstacle_maps[z][x][y]

    def read_map_function__condition(self, node):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('read: map\n')
        return True

    def read_map_function__0(self, node):
        # DONE!
        if self.map_data is not None:
            self.obstacle_maps = {
                z : numpy.transpose(
                    self.binvox_converter.get_slice(
                        numpy.reshape(self.map_data, (self.map_y_size, self.map_x_size)),
                        altitude = float(z),
                        tolerance = 1.0,
                        debug = True
                    ),
                    (1, 0))
                for z in self.map_z_vals
            }
            if not self.blackboard.map_exists:
                # initial map creation goes here.
                self.cost_graph = {
                    (x, y, z) : [
                        ((x + dxo, y + dyo, zo), self.calculate_cost(x, y, z, x + dxo, y + dyo, zo))
                        for dxo in (-1, 0, 1)
                        for dyo in (-1, 0, 1)
                        for zo in self.map_z_vals
                        if (
                                (
                                    (zo != z and dxo == 0 and dyo == 0) or
                                    (zo == z and (dxo != 0 or dyo != 0))
                                ) and
                                # (dxo != 0 or dyo != 0) and
                                self.map_x_min <= x + dxo <= self.map_x_max and
                                self.map_y_min <= y + dyo <= self.map_y_max and
                                self.check_safety(x + dxo, y + dyo, zo)
                        )
                    ]
                    for x in range(self.map_x_min, self.map_x_max + 1)
                    for y in range(self.map_y_min, self.map_y_max + 1)
                    for z in self.map_z_vals
                }
                with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                    serene_log.write('created map!\n')
            elif self.blackboard.valid_position:
                # map update goes here.
                for x in range(max(self.map_x_min, self.blackboard.position[0] - self.update_radius), min(self.map_x_max + 1, self.blackboard.position[0] + self.update_radius)):
                    for y in range(max(self.map_y_min, self.blackboard.position[1] - self.update_radius), min(self.map_y_max + 1, self.blackboard.position[1] + self.update_radius)):
                        for z in self.map_z_vals:
                            if self.check_safety(x, y, z):
                                self.cost_graph[(x, y, z)] = [
                                    ((x + dxo, y + dyo, zo), self.calculate_cost(x, y, z, x + dxo, y + dyo, zo))
                                    for dxo in (-1, 0, 1)
                                    for dyo in (-1, 0, 1)
                                    for zo in self.map_z_vals
                                    if (
                                            (
                                                (zo != z and dxo == 0 and dyo == 0) or
                                                (zo == z and (dxo != 0 or dyo != 0))
                                            ) and
                                            # (dxo != 0 or dyo != 0) and
                                            self.map_x_min <= x + dxo <= self.map_x_max and
                                            self.map_y_max <= y + dyo <= self.map_y_max and
                                            self.check_safety(x + dxo, y + dyo, zo)
                                    )
                                ]
                            else:
                                self.cost_graph[(x, y, z)] = []
                with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                    serene_log.write('updated map!\n')
            else:
                with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                    serene_log.write('cannot update map, position unknown\n')
        self.map_data = None
        return self.cost_graph is not None

    def compute_waypoint_function__condition(self, node):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('Computing waypoint\n')
        if self.blackboard.position[2] == 0:
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('Elevating!\n')
            self.path = [(self.blackboard.position[0], self.blackboard.position[1], self.map_z_vals[0])]
        elif len(self.path) > 0:
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('Checking existing path\n')
            # path exists! Verify that it's still feasible.
            if (
                    abs(self.blackboard.position[0] - self.path[0][0]) <= 1 and
                    abs(self.blackboard.position[1] - self.path[0][1]) <= 1 and
                    self.blackboard.position[2] >= self.path[0][2]
            ):
                # all good, but update where we are in the path.
                self.path.pop(0)
            if any((not self.check_safety(x, y, z)) for (x, y, z) in self.path):
                # there's an unsafe point. force recalc.
                self.path = []
        if len(self.path) == 0: # need a new path.
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('Calling A*\n')
            for _ in range(5): # number of times to retry
                self.path = a_star(self.cost_graph, tuple(self.blackboard.position), tuple(self.blackboard.goal))
                if len(self.path) == 0:
                    with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                        serene_log.write('path impossible\n')
                        if len(self.cost_graph[tuple(self.blackboard.position)]) == 0:
                            serene_log.write('start is obstacle\n')
                            if self.blackboard.position[2] < self.map_z_vals[-1]:
                                self.cost_graph[tuple(self.blackboard.position)] = [
                                    ((self.blackboard.position[0], self.blackboard.position[1], self.map_z_vals[-1]), 1)
                                ]
                            if len(self.cost_graph[(self.blackboard.position[0], self.blackboard.position[1], self.map_z_vals[-1])]) == 0:
                                (x, y, z) = (self.blackboard.position[0], self.blackboard.position[1], self.map_z_vals[-1])
                                self.cost_graph[(x, y, z)] = [
                                    ((x + dxo, y + dyo, zo), self.calculate_cost(x, y, z, x + dxo, y + dyo, zo))
                                    for dxo in (-1, 0, 1)
                                    for dyo in (-1, 0, 1)
                                    for zo in self.map_z_vals
                                    if (
                                            (
                                                (zo != z and dxo == 0 and dyo == 0) or
                                                (zo == z and (dxo != 0 or dyo != 0))
                                            ) and
                                            # (dxo != 0 or dyo != 0) and
                                            self.map_x_min <= x + dxo <= self.map_x_max and
                                            self.map_y_max <= y + dyo <= self.map_y_max and
                                            self.check_safety(x + dxo, y + dyo, zo, True)
                                    )
                                ]
                            continue
                        if len(self.cost_graph[tuple(self.blackboard.goal)]) == 0:
                            serene_log.write('goal is obstacle\n')
                    return False # there's no possible path
                self.path.pop(0) # remove the first point, because we're already at the first point.
                # remove the point before we checke for validity; if we're in an obstacle than things are bad already.
                # path found, confirm it's valid.
                if any((not self.check_safety(x, y, z)) for (x, y, z) in self.path):
                    # there's an unsafe point. force recalc, but first, update the map
                    for (x, y, z) in self.path:
                        if (not self.check_safety(x, y, z)):
                            self.cost_graph[(x, y, z)] = []
                    self.path = []
                else:
                    break # found a reasonable path, time to exit
        if len(self.path) == 0:
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('Could not find a path\n')
            return False # retry attempt maxed out.
        self.waypoint = self.path[0]
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('next point is: ' + str(self.waypoint) + '\n')
        self.send_goal_found()
        return True


    def compute_waypoint_function__0(self, node):
        # DONE!
        return enumerate(self.waypoint)

    def send_invalid_goal_request_function__0(self, node):
        # DONE!
        self.path = []
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('sent: invalid goal request\n')
        to_send = std_msgs.msg.String()
        to_send.data = 'IG: ' + str(self.blackboard.goal[0]) + ' ' + str(self.blackboard.goal[1])
        self.goal_information_publisher.publish(to_send)
        return

    def send_goal_found(self):
        to_send = std_msgs.msg.String()
        to_send.data = 'GF: ' + str(self.blackboard.goal[0]) + ' ' + str(self.blackboard.goal[1])
        self.goal_information_publisher.publish(to_send)
        return

    def send_next_goal_request_function__0(self, node):
        # DONE!
        self.path = []
        to_send = std_msgs.msg.String()
        to_send.data = 'request_initial_goal' if self.initial_goal else 'request_new_goal'
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('sent: ' + to_send.data + '\n')
        if self.initial_goal:
            self.blackboard.goal_requested = False
            self.initial_goal = False
        self.goal_information_publisher.publish(to_send)
        return

    def send_waypoint_function__0(self, node):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('sent: waypoint\n')
        (go_to_x, go_to_y, go_to_z) = self.blackboard.waypoint
        go_to = geometry_msgs.msg.PoseStamped()
        # convert back to NED
        go_to.pose.position.x = float(go_to_y)
        go_to.pose.position.y = float(go_to_x)
        go_to.pose.position.z = float(go_to_z * -1) - 1.3 # make us fly higher than the threshold, just in case. also reduces ping ponging (we hope)
        go_to.pose.orientation.w = 1.0 # no idea what this does.
        go_to.header.frame_id = "map" # i assume this is relevant somehow.
        message_to_send = adk_node.msg.WaypointPath()
        # message_to_send.velocity = 2.0
        message_to_send.velocity = 5.0
        # message_to_send.velocity = 8.0
        message_to_send.lookahead = -1.0
        message_to_send.adaptive_lookahead = 1.0
        message_to_send.wait_on_last_task = True
        message_to_send.path = [go_to]
        self.waypoint_publisher.publish(message_to_send)
        return
