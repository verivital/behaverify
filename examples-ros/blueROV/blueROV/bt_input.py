#!/usr/bin/env python

# Description: contingency management a.k.a. mission controller 0.1


import rospy2 as rospy
import numpy as np
import math
import uuv_waypoints
import collections
import scipy as sp
import scipy.signal as signal

from std_srvs.srv import Empty
from nav_msgs.msg import Odometry
from std_msgs.msg import Header, Float64, Float32, Bool, String, Float32MultiArray, Int32
from ng_msgs.msg import LatLonDepth, HSDCommand, LEC1OutputAssuredStamped, AssuranceMonitorConfidence
from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped
from vandy_bluerov.msg import PixhawkHW
from message_filters import ApproximateTimeSynchronizer, Subscriber
import tf.transformations as trans
from vandy_bluerov.srv import GoToHSD
from uuv_control_interfaces.dp_controller_local_planner import Hold, ClearWaypoints
from enum import IntEnum

class Failsafe_states(IntEnum):
    UNKNOWN = -1
    NONE = 0
    BATTERY_LOW = 1
    RTH = 2
    SIGNAL_LOST = 3
    GEOFENCE = 4
    PIPE_LOST = 5
    MISSION_ABORT = 6
    SENSOR_FAILURE = 7
    THRUSTER_DEGRADATION = 8
    OTHER_FS = 9

##############################################################################
# Behaviour Tree blackboard input interface
##############################################################################

class BB_input(object):
    def __init__(self):
        self.namespace = rospy.get_namespace().replace('/', '')
        self.travel_cost = rospy.get_param('~travel_cost', 0.0013) # 1m distance travel charge cost
        self.failsafe_battery_low_threshold = rospy.get_param('~failsafe_battery_low_threshold', 0.1) # 
        self.failsafe_rth_enable = rospy.get_param('~failsafe_rth_enable', True) # %
        self.failsafe_signal_lost_threshold = rospy.get_param('~failsafe_signal_lost_threshold', 10) # sec
        self.failsafe_tracking_lost_threshold = rospy.get_param('~failsafe_tracking_lost_threshold', 120) # sec
        self.failsafe_geofence_threshold = rospy.get_param('~geofence_threshold', 500) # % m from Home
        self.home_radius = rospy.get_param('~home_radius', 15) #m 
        self.sum_thrust_loss_threshold = float(rospy.get_param('~sum_thrust_loss_threshold', '1.00'))
        # self.pipe_estimation_bad_log_val = rospy.get_param('~pipe_estimation_bad_log_val', 10)
        # self.pipe_estimation_good_log_val = rospy.get_param('~pipe_estimation_good_log_val', 5)  
        # self.speed_bad_log_val = rospy.get_param('~speed_bad_log_val', 5)
        # self.speed_good_log_val = rospy.get_param('~speed_good_log_val', 2.5)  
        # self.uuv_min_speed = rospy.get_param('~uuv_min_speed', 0.9)  
        # self.uuv_max_speed = rospy.get_param('~uuv_max_speed', 0.4)  
        # self.enable_waypoint_following = rospy.get_param('~enable_waypoint_following', False)
        self.uuv_degradation_mode = rospy.get_param('~uuv_degradation_mode', 'x') # NGC degradation modes OR thruster degradation
        self.enable_rpm_sensor_check = rospy.get_param('~enable_rpm_sensor_check', False)
        self.enable_training_data_collection = rospy.get_param('~enable_training_data_collection', False)
        self.thruster_thrust_force_efficiency = rospy.get_param('~thruster_thrust_force_efficiency', 0.81)
        self.thruster_motor_fail_duration = rospy.get_param('~thruster_motor_fail_duration', 65535)
        self.thruster_motor_fail_starting_time = rospy.get_param('~thruster_motor_fail_starting_time', 50)
        self.thruster_motor_failure = rospy.get_param('~thruster_motor_failure', False)

        # self.pipe_tracking_speed = self.uuv_min_speed # default

        rospy.loginfo('[BT_IN] Params: ')
        rospy.loginfo('[BT_IN] travel_cost: %0.5f' % self.travel_cost)
        rospy.loginfo('[BT_IN] failsafe_battery_low_threshold: %0.2f' % self.failsafe_battery_low_threshold)
        rospy.loginfo('[BT_IN] failsafe_rth_enable: %s' % self.failsafe_rth_enable)
        rospy.loginfo('[BT_IN] failsafe_signal_lost_threshold: %d' % self.failsafe_signal_lost_threshold)
        rospy.loginfo('[BT_IN] failsafe_tracking_lost_threshold: %d' % self.failsafe_tracking_lost_threshold)
        rospy.loginfo('[BT_IN] failsafe_geofence_threshold: %d' % self.failsafe_geofence_threshold)
        rospy.loginfo('[BT_IN] home_radius: %d' % self.home_radius)
        # rospy.loginfo('[BT_IN] pipe_estimation_bad_log_val: %0.2f' % self.pipe_estimation_bad_log_val)
        # rospy.loginfo('[BT_IN] pipe_estimation_good_log_val: %0.2f' % self.pipe_estimation_good_log_val)
        # rospy.loginfo('[BT_IN] speed_bad_log_val: %0.2f' % self.speed_bad_log_val)
        # rospy.loginfo('[BT_IN] speed_good_log_val: %0.2f' % self.speed_good_log_val)
        # rospy.loginfo('[BT_IN] uuv_min_speed: %0.2f' % self.uuv_min_speed)
        rospy.loginfo('[BT_IN] sum_thrust_loss_threshold: %0.2f' % self.sum_thrust_loss_threshold)
        # rospy.loginfo('[BT_IN] speed_bad_log_val: %0.2f' % self.speed_bad_log_val)
        # rospy.loginfo('[BT_IN] speed_good_log_val: %0.2f' % self.speed_good_log_val)  
        # rospy.loginfo('[BT_IN] uuv_min_speed: %0.2f' % self.uuv_min_speed)  
        # rospy.loginfo('[BT_IN] uuv_max_speed: %0.2f' % self.uuv_max_speed)  
        # rospy.loginfo('[BT_IN] enable_waypoint_following: %0.2f' % self.enable_waypoint_following)
        rospy.loginfo('[BT_IN] uuv_degradation_mode: %s' % self.uuv_degradation_mode) 
        rospy.loginfo('[BT_IN] enable_rpm_sensor_check: %0.2f' % self.enable_rpm_sensor_check)
        rospy.loginfo('[BT_IN] enable_training_data_collection: %0.2f' % self.enable_training_data_collection)
        rospy.loginfo('[BT_IN] thruster_thrust_force_efficiency: %0.2f' % self.thruster_thrust_force_efficiency)
        rospy.loginfo('[BT_IN] thruster_motor_fail_duration: %0.2f' % self.thruster_motor_fail_duration)
        rospy.loginfo('[BT_IN] thruster_motor_fail_starting_time: %0.2f' % self.thruster_motor_fail_starting_time)
        rospy.loginfo('[BT_IN] thruster_motor_failure: %s' % self.thruster_motor_failure)
     
        self.total_distance = 0.0
        self.distance_to_home = 0.0
        self.safe_RTH = False
               
        # Subscribe to Waypoint Completed msg
        self.hsd_waypoint_completed_sub = rospy.Subscriber(
            '/iver0/waypoints_completed', Bool, self.waypoint_completed_callback, queue_size=1)
        self.waypoint_completed = False

        self.odometry_sub = rospy.Subscriber(
             '/iver0/pose_gt_noisy_ned', Odometry, self.odometry_callback, queue_size=1)    

        # Subscribe to Pipeline in view    
        self.pipeline_in_view_sub = rospy.Subscriber(
            "/iver0/pipeline_in_view", Header, self.pipeline_in_view_callback)
        self.pipeline_in_view_msg = Header()
        #self.pipeline_last_seen_limit = 120 #sec

        #  # Subscribe to PixhawkHW battery/power data
        self.pixhawk_data_sub = rospy.Subscriber(
            "/iver0/pixhawk_hw", PixhawkHW, self.pixhawk_data_callback)
        self.pixhawk_data = PixhawkHW()

        self.cm_am_left_pub= rospy.Publisher(
            "/iver0/cm_am/left", AssuranceMonitorConfidence, queue_size=1)
        self.cm_am_left = AssuranceMonitorConfidence()
        self.cm_am_left.type = AssuranceMonitorConfidence.TYPE_SVDD
        self.cm_am_right_pub= rospy.Publisher(
            "/iver0/cm_am/right", AssuranceMonitorConfidence, queue_size=1)
        self.cm_am_right = AssuranceMonitorConfidence()
        self.cm_am_right.type = AssuranceMonitorConfidence.TYPE_SVDD

        # For Plotting only - BTree computes log(martingale)
        # Subscribe to LEC2 AM
        self.lec2_am_left_sub = rospy.Subscriber(
            '/lec2_am/left/p_value', LEC1OutputAssuredStamped, self.lec2_am_left_callback, queue_size=1)
        self.lec2_am_right_sub = rospy.Subscriber(
            '/lec2_am/right/p_value', LEC1OutputAssuredStamped, self.lec2_am_right_callback, queue_size=1)
        self.lec2_am_left_confidence = [0,0]
        self.lec2_am_right_confidence = [0,0]
        self.lec2_am_confidence = 0

        # HOME position msg
        self.home_position_pub = rospy.Publisher(
            '/iver0/home_position', LatLonDepth, queue_size=1) 
        self.home_position_msg = LatLonDepth()   

        # Subscribe to Surface HSD
        self.hsd_surface_sub = rospy.Subscriber(
            '/iver0/hsd_command', HSDCommand, self.HSD_command_callback, queue_size=1)
        self.hsd_output_msg = HSDCommand()

        # self.am_pub = rospy.Publisher(
        #     '/iver0/am_values', Float32MultiArray, queue_size=1) 

        self.thruster_cmd_logging = rospy.Publisher(
            '/iver0/thruster_cmd_logging', Float32MultiArray, queue_size=1) 

        self.degradation_gt_pub = rospy.Publisher(
            '/iver0/degradation_gt', Float32MultiArray, queue_size=1) 

        self.sensor_failure_rpm_pub = rospy.Publisher(
            '/iver0/sensor_failure_rpm', Bool, queue_size=1)
        self.sensor_failure_rpm = False

        # Subscribe to Is Submerged msg
        self.is_submerged_sub = rospy.Subscriber(
            '/iver0/is_submerged', Bool, self.is_submerged_callback, queue_size=1)
        self.is_submerged = True

        self.uuv_yaw = 0
        self.uuv_yaw_pipe_tracking = 0
        self.uuv_position = [-1,-1,-1]
        self.home_position = [-1,-1,-1]

        self.bb_rth_pub = rospy.Publisher(
            '/iver0/bb_rth', Bool, queue_size=1)
        
        self.bb_pipe_lost_pub = rospy.Publisher(
            '/iver0/bb_pipe_lost', Bool, queue_size=1)

        self.bb_geofence_pub = rospy.Publisher(
            '/iver0/bb_geofence', Bool, queue_size=1)

        self.bb_home_dist_pub = rospy.Publisher(
            '/iver0/bb_home_dist', Float32, queue_size=1)

        # Estimated esc power difference, indicating possible RPM sensor issue
        self.power_sum_input = collections.deque(maxlen = 100)
        self.power_estimation_difference = collections.deque(maxlen = 10)

        self.thruster_0_sub = Subscriber('thrusters/0/input', FloatStamped)
        self.thruster_1_sub = Subscriber('thrusters/1/input', FloatStamped)
        self.thruster_2_sub = Subscriber('thrusters/2/input', FloatStamped)
        self.thruster_3_sub = Subscriber('thrusters/3/input', FloatStamped)
        self.thruster_4_sub = Subscriber('thrusters/4/input', FloatStamped)
        self.thruster_5_sub = Subscriber('thrusters/5/input', FloatStamped)
        approxTimeSync=ApproximateTimeSynchronizer([self.thruster_0_sub,
                                                    self.thruster_1_sub,
                                                    self.thruster_2_sub,
                                                    self.thruster_3_sub,
                                                    self.thruster_4_sub,
                                                    self.thruster_5_sub], queue_size=1, slop=0.1)

        approxTimeSync.registerCallback(self.thruster_callback)
        self.thruster_callback_msg = []

        #Wait for other nodes
        rospy.sleep(10.0)

        rate = rospy.Rate(1)
        while not rospy.is_shutdown():            
            self.cm_am_right_pub.publish(self.cm_am_right)
            self.cm_am_left_pub.publish(self.cm_am_left)
            # Check LEC2 AM and deny process of semseg output if AM tells its bad
            
            rospy.loginfo('[BT_IN] Travel: %dm, Home: %dm, Batt: %0.2f' % 
                (self.total_distance,
                self.distance_to_home,
                self.pixhawk_data.batt_charge_remaining ))

            self.create_thruster_log_msg(self.enable_training_data_collection, self.thruster_thrust_force_efficiency)

            # Check sensors                    
            if rospy.Time.now() > rospy.Time(15) and self.enable_rpm_sensor_check:
                self.check_rpm_sensor()
            
            # Check failsafes
            self.check_failsafes()
                                    
            
            # Execute Autonomous task
            rospy.loginfo('[BT_IN] Power: %0.2fA, pos: %s'%(self.pixhawk_data.thrusters_power, self.uuv_position ))

            rate.sleep()
    
    
    def waypoint_completed_callback(self, msg):
        self.waypoint_completed = msg.data

    def is_submerged_callback(self, msg):
        self.is_submerged = msg.data
        if self.is_submerged == False:
            rospy.signal_shutdown('Surface reached - simulation shutdown')

    def pipeline_in_view_callback(self, msg):
        self.pipeline_in_view_msg = msg

    @staticmethod
    def unwrap_angle(t):
        return math.atan2(math.sin(t),math.cos(t))

    @staticmethod
    def vector_to_np(v):
        return np.array([v.x, v.y, v.z])

    @staticmethod
    def quaternion_to_np(q):
        return np.array([q.x, q.y, q.z, q.w])

    @staticmethod
    def vector_to_mag(v):
        return np.linalg.norm(np.array([v.x, v.y, v.z]))

    @staticmethod
    def degree_to_rad(ang):
        return ang*np.pi/180.

    def odometry_callback(self, msg):
        pos = [msg.pose.pose.position.x,
               msg.pose.pose.position.y,
               msg.pose.pose.position.z]

        quat = [msg.pose.pose.orientation.x,
                msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z,
                msg.pose.pose.orientation.w]

        # Calculate the position, position, and time of message
        p = self.vector_to_np(msg.pose.pose.position)
        self.total_distance += self.dist(p)
        self.uuv_position = p
        # if np.array_equal(self.home_position,[-1,-1,-1]):
        #     self.home_position = self.uuv_position
        #     rospy.loginfo('[BT_IN]    #####   Home position set to %0.2f %0.2f %0.2f #####' % 
        #         (self.home_position[0],
        #         self.home_position[1],
        #         self.home_position[2]))
        #     self.home_position_msg.latitude = self.home_position[0]
        #     self.home_position_msg.longitude = self.home_position[1]
        #     self.home_position_msg.depth = self.home_position[2]
        #     self.home_position_pub.publish(self.home_position_msg)

        self.distance_to_home = self.dist(self.home_position)

        vel = self.vector_to_mag(msg.twist.twist.linear)

        q = self.quaternion_to_np(msg.pose.pose.orientation)
        rpy = trans.euler_from_quaternion(q, axes='sxyz')
        self.uuv_yaw = math.degrees(rpy[2])

    def pixhawk_data_callback(self, msg):
        self.pixhawk_data = msg

    def thruster_callback(self,*args):
        self.thruster_callback_msg = args

        _power = 0
        for thruser_input in self.thruster_callback_msg:               
            _power += abs(thruser_input.data)
        self.power_sum_input.append(_power)

    def check_rpm_sensor(self):
        fs = 20
        ny = fs / 2 
        cutoff = 0.999
        b,a = signal.butter(5,cutoff,btype='lowpass')
        # sos = signal.butter(5,cutoff,btype='lowpass', output='sos')

        # if power consumption is within normal range
        if 5.0 < self.pixhawk_data.thrusters_power < 80.0:
            if rospy.Time.now() > rospy.Time(20):
                _power = signal.filtfilt(b,a,np.array(self.power_sum_input))
                # _power = signal.sosfilt(sos,np.array(self.power_sum_input))
                _power = max(0.0335 * np.average(_power[-21:-1]) - 47.2404, 0)
                self.power_estimation_difference.append( abs(1 -_power/self.pixhawk_data.thrusters_power) )
                # rospy.loginfo("e/m: [ %0.2f ]/[ %0.2f ] diff: [ %0.2f, \033[1;31m %0.2f \033[0m]" %(_power, self.pixhawk_data.thrusters_power, self.power_estimation_difference[-1], np.average(self.power_estimation_difference)))
                if np.average(self.power_estimation_difference) > 0.50: # huge difference of total power            
                    self.sensor_failure_rpm = True
                    rospy.loginfo("\033[1;31m === [ SENSOR FAILURE DETECTED ] === \033[0m")
                    # self.active_diagnostics_pub.publish(Bool(True))
                # else:
                #     self.sensor_failure_rpm = False   
                    # self.active_diagnostics_pub.publish(Bool(False))

                self.sensor_failure_rpm_pub.publish(Bool(self.sensor_failure_rpm))

    
    def create_thruster_log_msg(self, training, efficiency):
        thruster_cmd = []
        degradation_gt = []
        for thruser_input in self.thruster_callback_msg:               
            thruster_cmd.append(thruser_input.data)
        for rpm in self.pixhawk_data.rpm:            
            thruster_cmd.append(rpm)
        thruster_cmd.append(self.hsd_output_msg.heading)
        # thruster_cmd.append(self.hsd_output_msg.speed)
        
        if (efficiency > 0.99
            or self.uuv_degradation_mode == 'x'):
            if training:
                thruster_cmd.append(6) # Nominal class
                thruster_cmd.append(1.0) # Nominal efficiency
            degradation_gt.append(6)
        else:
            if training:
                thruster_cmd.append(self.uuv_degradation_mode) # Degraded thruster
                thruster_cmd.append(efficiency) # Degraded efficiency
            if (
                rospy.Time(self.thruster_motor_fail_starting_time) < rospy.Time.now() < rospy.Time(self.thruster_motor_fail_starting_time + self.thruster_motor_fail_duration)
                and self.thruster_motor_failure
                ):
                degradation_gt.append(self.uuv_degradation_mode)
            else:
                degradation_gt.append(6)
        
        if (
            rospy.Time(self.thruster_motor_fail_starting_time) < rospy.Time.now() < rospy.Time(self.thruster_motor_fail_starting_time + self.thruster_motor_fail_duration)
            and self.thruster_motor_failure
            ):
            degradation_gt.append(self.thruster_thrust_force_efficiency)
        else:
            degradation_gt.append(1.0)

        msg =  Float32MultiArray()
        msg.data = thruster_cmd
        self.thruster_cmd_logging.publish(msg)   

        msg.data = degradation_gt
        self.degradation_gt_pub.publish(msg)   

        # rospy.loginfo(msg)  

    def dist(self, pos):
        return np.sqrt((self.uuv_position[0] - pos[0])**2 +
                       (self.uuv_position[1] - pos[1])**2)

    def get_safe_rth_cost(self, backup_batt):
        return self.distance_to_home * self.travel_cost + backup_batt 
        
    def check_failsafes(self):
        # Check for sensor failure
        if self.sensor_failure_rpm == True:
            rospy.loginfo('[BT_IN] RPM sensor failure')

        # # Check if battery is critical
        # if self.pixhawk_data.batt_charge_remaining < self.failsafe_battery_low_threshold:
        #     self.failsafe_sate = Failsafe_states.BATTERY_LOW        
        #     rospy.loginfo('[BT_IN] Battery low failsafe: %0.2f' %self.pixhawk_data.batt_charge_remaining)

        # Check if battery is low, but safe to RTH if RTH enabled
        if self.pixhawk_data.batt_charge_remaining - self.get_safe_rth_cost(0.20) < 0.01:                    
            self.bb_rth_pub.publish(Bool(True))
            rospy.loginfo('[BT_IN] RTH failsafe at %0.2f battery, RTH cost: %0.2f ' %(self.pixhawk_data.batt_charge_remaining, self.get_safe_rth_cost(0)))
        else:
            self.bb_rth_pub.publish(Bool(False))
        
        # Check when was the pipe last seen
        # Trigger Pipe lost if threshold elapsed
        if (rospy.Time.now() - self.pipeline_in_view_msg.stamp) > rospy.Duration(secs = self.failsafe_tracking_lost_threshold):
            self.bb_pipe_lost_pub.publish(Bool(True))
            rospy.loginfo('[BT_IN] Lost the pipeline failsafe. Limit was %d s' %self.failsafe_tracking_lost_threshold)
        else:
            self.bb_pipe_lost_pub.publish(Bool(False))
        
        # Check geofence
        if self.failsafe_geofence_threshold <= self.distance_to_home:       
            self.bb_geofence_pub.publish(Bool(True))
            rospy.loginfo('[BT_IN] Geofence failsafe. Limit was %d m' %self.failsafe_geofence_threshold)
        else:
            self.bb_geofence_pub.publish(Bool(False))

        # Publish home distance for surface task
        self.bb_home_dist_pub.publish(Float32(self.distance_to_home))
        # if (self.distance_to_home <= self.home_radius): 
        #     rospy.loginfo('[BT_IN] home positon reached ') 
        #     self.bb_check_home_pub.Publish(Bool(True))
        # else:
        #     self.bb_check_home_pub.Publish(Bool(False))
    
    # def set_safe_hsd_output(self, input_hsd, target_speed):
    #     if (abs(self.hsd_obstacle_avoidance_msg.heading) > 10):
    #         print("\033[1;34m AIS HSD INJECTION \033[0m")
    #         self.hsd_output_msg.heading = self.hsd_obstacle_avoidance_msg.heading
    #         self.hsd_output_msg.depth = self.hsd_obstacle_avoidance_msg.depth
    #         # self.hsd_output_msg.speed = self.hsd_obstacle_avoidance_msg.speed
    #         rospy.logdebug('[BT_IN] !!! Obstacle avoidance: %0.2f' % self.hsd_obstacle_avoidance_msg.heading)
    #     else:
    #         self.hsd_output_msg.heading = input_hsd.heading
    #         self.hsd_output_msg.depth = input_hsd.depth
    #     self.hsd_output_msg.speed = target_speed
    #     self.hsd_output_msg.header.stamp = rospy.Time.now()    
    
    def dd_callback(self, msg):
        self.msg = np.array(msg.data)
    
    def HSD_command_callback(self, msg):
        self.hsd_output_msg = msg

    def lec2_am_left_callback(self, msg):
        self.lec2_am_left_confidence[0] = np.log(msg.confs[0].values[-2])
        self.lec2_am_left_confidence[1] = msg.confs[0].values[-1]
        # self.lec2_am_left_confidence = msg.confs[0].values[-2:]
        self.cm_am_left.values = self.lec2_am_left_confidence

    def lec2_am_right_callback(self, msg):        
        self.lec2_am_right_confidence[0] = np.log(msg.confs[0].values[-2])
        self.lec2_am_right_confidence[1] = msg.confs[0].values[-1]
        # self.lec2_am_right_confidence = msg.confs[0].values[-2:]
        self.cm_am_right.values = self.lec2_am_right_confidence

if __name__=='__main__':
    print('Starting BlackBoard_input')
    rospy.init_node('BlackBoard_input', log_level=rospy.INFO)
    try:
        node = BB_input()
        rospy.spin()
    except rospy.ROSInterruptException:
        print('caught exception')
