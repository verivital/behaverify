import random # for generators
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




class ANSR_environment():

    def __init__(self):

        self.ros_node = None

        # these are values we store from subscribing, or we can generate them
        self.goals = None
        self.goals_index = None
        self.map_info = None
        self.obstacle_map = None
        self.position = None

        # our subscribers
        self.path_publisher = None
        self.goals_subscriber = None
        self.obstacle_map_subscriber = None
        self.position_subscriber = None

        # our generators. {'chance' : float, 'function' : takes no arguments, generates the output}
        self.goals_generator = None
        self.obstacle_map_generator = None
        self.position_generator = None

        # parameters that *must* be configured using initialize_environment
        self.height_modifier = None
        self.velocity = None
        return

    def initialize_environment(self, height_modifier, velocity, goals_generator = None, obstacle_map_generator = None, position_generator = None):
        self.height_modifier = height_modifier
        self.velocity = velocity
        self.goals_generator = goals_generator
        self.obstacle_map_generator = obstacle_map_generator
        self.position_generator = position_generator
        return

    def goals_callback(self, msg):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('got: goals\n')
        if msg is not None:
            # this will be filled in later!
            pass

    def obstacle_map_callback(self, msg):
        # DONE!
        with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
            serene_log.write('got: obstacle map\n')
        if msg is not None:
            # https://docs.ros2.org/foxy/api/nav_msgs/msg/OccupancyGrid.html
            self.obstacle_map = msg.data
            self.map_info = {
                'resolution' : msg.info.resolution,
                'x_size' : msg.info.width,
                'y_size' : msg.info.height,
                'origin_position' : (msg.info.origin.position.x, msg.info.origin.position.y, msg.info.origin.position.z), # z is radians in orientation
                'origin_orientation' : msg.info.origin.orientation
            }

    def position_callback(self, msg):
        # DONE!
        if msg is not None:
            self.position = msg.pose.pose.position
            with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                serene_log.write('got: position: ' + str((self.position.x, self.position.y, self.position.z)) + '\n')

    def setup_pub_sub(self, ros_node, pub_path_segment = True, sub_goal = True, sub_obstacle_map = True, sub_position = True):
        # DONE!
        self.ros_node = ros_node
        settings = message_settings.Messages()
        if pub_path_segment:
            self.path_publisher = self.ros_node.create_publisher(
                msg_type = adk_node.msg.WaypointPath,
                topic = '/adk_node/input/waypoints',
                qos_profile = rclpy.qos.QoSProfile(
                    reliability = rclpy.qos.QoSReliabilityPolicy.RELIABLE,
                    durability = rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL,
                    history = rclpy.qos.QoSHistoryPolicy.KEEP_LAST,
                    depth = 1
                )
            )
        if sub_goal:
            self.goals_subscriber = self.ros_node.create_subscription(
                msg_type = settings.goal.msg_type,
                topic = settings.goal.topic,
                callback = self.goals_callback,
                qos_profile = settings.goal.qos_profile
            )
        if sub_obstacle_map:
            self.obstacle_map_subscriber = self.ros_node.create_subscription(
                msg_type = settings.obstacle_map_raw.msg_type,
                topic = settings.obstacle_map_raw.topic,
                callback = self.obstacle_map_callback,
                qos_profile = settings.obstacle_map_raw.qos_profile
            )
        if sub_position:
            self.position_subscriber = self.ros_node.create_subscription(
                msg_type = nav_msgs.msg.Odometry,
                topic = '/adk_node/SimpleFlight/odom_local_ned',
                callback = self.position_callback,
                qos_profile = rclpy.qos.QoSProfile(
                    reliability = rclpy.qos.QoSReliabilityPolicy.RELIABLE,
                    durability = rclpy.qos.QoSDurabilityPolicy.VOLATILE,
                    history = rclpy.qos.QoSHistoryPolicy.KEEP_LAST,
                    depth = 1
                )
            )

    def read_goals_ready(self):
        if self.goals_subscriber is None and self.goals_generator is not None:
            if random.random() < self.goals_generator['chance']:
                with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                    serene_log.write('generated: goals\n')
                (self.goals_index, self.goals) = self.goals_generator['function']()
        return self.goals is not None

    def read_goals(self):
        to_return = (self.goals_index, self.goals)
        self.goals = None
        self.goals_index = None
        return to_return

    def read_obstacle_map_ready(self):
        if self.obstacle_map_subscriber is None and self.obstacle_map_generator is not None:
            if random.random() < self.obstacle_map_generator['chance']:
                with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                    serene_log.write('generated: obstacle map\n')
                self.obstacle_map = self.obstacle_map_generator['function']()
        return self.obstacle_map is not None

    def read_obstacle_map(self):
        to_return = (self.obstacle_map, self.map_info)
        self.obstacle_map = None
        self.map_info = None
        return to_return

    def read_position_ready(self):
        return self.position is not None

    def read_position(self):
        if self.position_subscriber is None and self.position_generator is not None:
            if random.random() < self.position_generator['chance']:
                with open('/output/serene.log', 'a', encoding = 'utf-8') as serene_log:
                    serene_log.write('generated: position\n')
                self.obstacle_map = self.position_generator['function']()
        to_return = self.position
        self.position = None
        return to_return

    def create_geometry_message(self, point, convert_bt_to_waypoint, map_info):
        go_to = geometry_msgs.msg.PoseStamped()
        (go_to.pose.position.x, go_to.pose.position.y, go_to.pose.position.z) = convert_bt_to_waypoint(map_info, point, self.height_modifier)
        go_to.pose.orientation.w = 1.0 # i think this instructs the drone to look forward.
        go_to.header.frame_id = 'map' # i assume this is relevant somehow.
        return go_to

    def send_path_segment_function(self, path_segment, convert_bt_to_waypoint, map_info):
        message_to_send = adk_node.msg.WaypointPath()
        message_to_send.velocity = self.velocity
        message_to_send.lookahead = -1.0
        message_to_send.adaptive_lookahead = 1.0
        message_to_send.wait_on_last_task = True
        message_to_send.path = [self.create_geometry_message(point, convert_bt_to_waypoint, map_info) for point in path_segment]
        self.path_publisher.publish(message_to_send)
