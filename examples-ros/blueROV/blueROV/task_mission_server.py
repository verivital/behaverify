#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

##############################################################################
# Imports
##############################################################################

import dynamic_reconfigure.client
import py_trees
import rospy            

 
from std_msgs.msg import String
############<<USER IMPORT CODE BEGINS>>##############################
import sys
import numpy as np
import os
import yaml
import rospkg
import navpy
import math

from uuv_control_msgs.srv import *
from std_msgs.msg import String, Time, Float64MultiArray, Float32MultiArray, Bool, Int32
from visualization_msgs.msg import Marker, MarkerArray
from nav_msgs.msg import Path, Odometry
from ng_msgs.msg import LatLonDepth
from geometry_msgs.msg import PoseStamped, Point

import sys, os
rp = rospkg.RosPack()
sys.path.append(os.path.join(rp.get_path("vandy_bluerov"),"nodes"))
import waypoint_actions
import heading
############<<USER IMPORT CODE ENDS>>################################

##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name ,  
                 uuv_max_speed=0.9, 
                 mission_file="mission_04.yaml"
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.task = name
        self.blackboard = py_trees.blackboard.Blackboard()
        self.blackboard.uuv_max_speed = uuv_max_speed
        self.blackboard.mission_file = mission_file
        self.blackboard.refLat = 38.971203
        self.blackboard.refLon = -76.398464
        
        self.uuv_max_speed=uuv_max_speed        
        self.mission_file=mission_file     
        self.bb_mission_pub = rospy.Publisher( '/iver0/bb_mission',
                                            String,
                                            queue_size=1)
        self.bb_mission_msg =  String()                   

############<<USER INIT CODE BEGINS>>##############################
        rospy.loginfo('%s __init__', self.task)
        self.waypoints = []
        self.markerArray = MarkerArray()
        self.wa = waypoint_actions.WaypointAction
        self.wp = waypoint_actions.WaypointParams
        self.hc = heading.HeadingCalculator()
        
        self.default_loiter_n = 3
        self.default_loiter_radius = 20
        self.default_rth_depth = 5
        
        self.lla = True

        self.mission_types= {
            "unknown": -1,
            "loitering": 0,
            "pipe_following": 1,
            "waypoint_following": 2,
            "path_following": 3,
            "collision_avoidance": 4,
            "assurance": 5,
            "terminal": 6,
            "e_stop": 7
        }

        self.mission_idx = -1

        # HOME position msg
        self.home_position_pub = rospy.Publisher(
            '/iver0/home_position', LatLonDepth, queue_size=1) 
        self.home_position_msg = LatLonDepth()

        self.waypoint_pub = rospy.Publisher(
            '/iver0/waypoints', Float64MultiArray, queue_size=1)   
            
        self.waypoint_marker_pub = rospy.Publisher(
            '/iver0/waypoint_markers', MarkerArray, queue_size=1) 

        self.fdr_location_sub = rospy.Subscriber(
            '/iver0/fdr_pos_est', Point, self.callback_fdr)
        
        self.next_wp_pub = rospy.Publisher(
            "/iver0/next_wp", Bool, queue_size = 1)
        
        self.new_wp_sub = rospy.Subscriber(
            '/iver0/new_waypoint', Point, self.callback_new_wp)  

        self.obstacle_near_wp_sub = rospy.Subscriber(
            "/iver0/obstacle_near_wp", Bool, self.callback_obstacle_near_wp, queue_size = 1)

        self.target_id_sub = rospy.Subscriber(
            '/iver0/target_waypoint_id', Int32, self.callback_target_wp_id, queue_size=1) 
        self.target_wp_id = -1

        self.odometry_sub = rospy.Subscriber(
             '/iver0/pose_gt_noisy_ned', Odometry, self.callback_odometry, queue_size=1) 
        self.uuv_position = [0,0,0]

        # Load mission file
        rp = rospkg.RosPack()

        # if rospy.has_param('~filename'):
        #     filename = rp.get_path("vandy_bluerov") + "/missions/" + rospy.get_param('~filename')
        #     rospy.loginfo(self.task + 'mission filename, file: ' + str(filename))
        # else:
        #     raise rospy.ROSException(self.task + 'No filename found')

        filename = rp.get_path("vandy_bluerov") + "/missions/" + self.mission_file
        rospy.loginfo(self.task + 'mission filename, file: ' + str(filename))

        self.read_mission_file(filename)
############<<USER INIT CODE ENDS>>################################

    def setup(self, timeout):
############<<USER SETUP CODE BEGINS>>##############################
############<<USER SETUP CODE ENDS>>################################
        return True            


    def bb_mission_publish(self, data):
        self.bb_mission_msg = data
############<<USER PUB_bb_mission CODE BEGINS>>##############################
############<<USER PUB_bb_mission CODE ENDS>>################################
        self.bb_mission_pub.publish(data)        

    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
        """
        self.logger.debug("%s.update()" % self.__class__.__name__)
        
############<<USER UPDATE CODE BEGINS>>##############################
        if (self.blackboard.next_mission):
            self.next_mission()
            self.blackboard.next_mission = False

        self.waypoint_pub.publish(Float64MultiArray(data = np.array(self.waypoints).flatten()))         
        self.waypoint_marker_pub.publish(self.markerArray)
############<<USER UPDATE CODE ENDS>>################################

         # Return always running                
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        """
        Shoot off a clearing command.

        Args:
            new_status (:class:`~py_trees.common.Status`): the behaviour is transitioning to this new status
        """
############<<USER TERMINATE CODE BEGINS>>##############################
############<<USER TERMINATE CODE ENDS>>################################        

############<<USER CUSTOM CODE BEGINS>>##############################
    def read_mission_file(self, filename):
        if not os.path.isfile(filename):
            rospy.logerr(self.task + 'Invalid mission filename, file: ' + str(filename))
        try:
            with open(filename, 'r') as mission_file:
                self.mission = yaml.load(mission_file)

                print('\n===================[ Mission Home: ]===================\n')
                assert(self.mission['home'])
                if (self.mission['home'][0] == 0 and self.mission['home'][1] == 0):
                    self.lla = False
                    print('[ Using local coordiants (NED) ]')
                else:    
                    self.lla = True
                    self.blackboard.refLat = self.mission['home'][0]
                    self.blackboard.refLon = self.mission['home'][1]
                    print('[ Using lat/lon/alt coodrinates (LLA) ]')
                self.home_position_msg.latitude = 0
                self.home_position_msg.longitude = 0
                self.home_position_msg.depth = self.default_rth_depth
                print(self.home_position_msg)
                self.home_position_pub.publish(self.home_position_msg)

                print('\n===================[ Mission Contents: ]===================\n')
                assert(self.mission['missions'])
                print('Missions: ' + str(len(self.mission['missions'])))
                for mission_data in self.mission['missions']:
                    print('- ' + str(mission_data['type']))
                self.next_mission()
                print('\n===================[ Mission Started ]===================\n')

        except Exception, e:
            rospy.logerr(self.task + 'Error while loading the file')
            rospy.logerr(e)
            self.actual_mission = self.mission_types['loitering']
    
    
    def process_mission(self, mission_data):
        print('\n===================[ Loading Mission Part #' + str(self.mission_idx) + ']===================\n')
        if (mission_data['type'] == 'path_following'):
            # mission_entry = [
            #     mission_data['type'],
            #     mission_data['avoidance_operating_depth'],
            #     mission_data['avoidance_learning'],
            #     mission_data['segments'],
            #     mission_data['loiter_box_size']/2,
            #     mission_data['assurance_technologies'],
            #     mission_data['termination_conditions'],
            #     mission_data['waypoint_reached_distance'],
            #     ]
            print'Mission type: ' + (str(mission_data['type']))
            # print("Segments:")
            self.init_waypoints()
            for idx, segments in enumerate(mission_data['segments']):
                self.add_waypoint_from_segment(idx, segments)
                print(np.array(segments, dtype = float))
            # Set mission type to waypoint after conversion
            mission_data['type'] = 'waypoint_following'

        elif (mission_data['type'] == 'waypoint_following'):
            # mission_entry = [
            #     mission_data['type'],
            #     mission_data['avoidance_operating_depth'],
            #     mission_data['avoidance_learning'],
            #     mission_data['waypoints'],
            #     mission_data['loiter_box_size']/2,
            #     mission_data['assurance_technologies'],
            #     mission_data['termination_conditions'],
            #     mission_data['waypoint_reached_distance'],
            #     ]
            print'Mission type: ' + (str(mission_data['type']))
            # print("Waypoints:")
            self.init_waypoints()
            for waypoint in mission_data['waypoints']:
                # print(np.array(waypoint, dtype = float))
                self.add_waypoint_from_mission(waypoint)

        elif (mission_data['type'] == 'e_stop'):           
            print'Mission type: ' + (str(mission_data['type']))
            self.blackboard.emergency_stop_warning = True
            rospy.logwarn_throttle(1, "%s: emergency_stop_warning!" % self.name)

        elif (mission_data['type'] == 'pipe_following'):
            # mission_entry = [
            #     mission_data['type'],
            #     mission_data['avoidance_operating_depth'],
            #     mission_data['avoidance_learning'],
            #     mission_data['loiter_box_size']/2,
            #     mission_data['assurance_technologies'],
            #     mission_data['termination_conditions'],
            #     mission_data['waypoint_reached_distance'],
            #     ]
            print'Mission type: ' + (str(mission_data['type']))
        else:
            return False
        print("------------------------------------------------------\n")
        rospy.loginfo(self.task + ' Total waypoints: %d' %len(self.waypoints))
        print("    X     Y  Depth   Speed Type   P0    P1")
        print(np.round(self.waypoints,1))
        rospy.loginfo('%s Next mission loaded: %s' %(self.task, mission_data['type']))
        
        print("Termination Condition - min_obstacle_standoff: ")
        for termination_conditions in mission_data['termination_conditions']:
            if termination_conditions['type'] == 'min_obstacle_standoff':
                print termination_conditions['distance']
                self.blackboard.obstacle_min_standoff = termination_conditions['distance']
        
        print("Assurance Technologies - DDv2 Credibility decision threshold: ")
        for assurance in mission_data['assurance_technologies']:
            if assurance['topic'] == '/degradation_detector':
                print assurance['decision_threshold']
                self.blackboard.decision_threshold = assurance['decision_threshold']

        self.set_mission(mission_data['type'])
        self.blackboard.bb_mission.data = mission_data['type'] #Why?
        return True
        
    def next_mission(self):
        self.mission_idx += 1
        if (self.mission_idx < len(self.mission['missions'])):
            # Process mission
            if not self.process_mission(self.mission['missions'][self.mission_idx]):
                rospy.logerr('%sError processing next mission', self.task)
        else:
            rospy.loginfo('%sMission finished', self.task)
            # self.set_mission('loitering')
            # Activating RTH as a failsafe action:
            self.blackboard.bb_rth_warning = True
    
    def set_mission(self, mission):
        self.actual_mission = self.mission_types[mission]
        self.bb_mission_pub.publish(String(mission))

    def clear_waypoints(self):
        self.set_mission('loitering')
        self.waypoints = []        

    def add_waypoint_from_mission(self, mission_waypoint):
        # TODO: Coordinate conversion
        if (not self.lla):
            wp = np.array([
                mission_waypoint[0], # X
                mission_waypoint[1], # Y
                mission_waypoint[2], # Depth
                max(self.blackboard.uuv_max_speed, mission_waypoint[3]), # Speed
                self.wa.PASS, # Default action
                0,            # Skip param for PASS
                0             # Skip param for PASS
                ], dtype = float)
        else:
            [lat, lon, _] = navpy.lla2ned(mission_waypoint[0], mission_waypoint[1], 0, self.blackboard.refLat, self.blackboard.refLon, 0)
            wp = np.array([
                lat,
                lon,
                -mission_waypoint[2], # Depth
                max(self.blackboard.uuv_max_speed, mission_waypoint[3]), # Speed
                self.wa.PASS, # Default action
                0,            # Skip param for PASS
                0             # Skip param for PASS
                ], dtype = float)
            print("lla2ned: " + str(lat) +', '+ str(lon))
        self.add_waypoint(wp)

    def add_waypoint_from_segment(self, idx, segment):
        # Segment: heading (in degrees), range (in meters), depth (in meters), speed (in knots) 
        if idx == 0:
            # self.init_waypoints()
            prev_pos = [self.uuv_position[1], self.uuv_position[0]]
        else:
            prev_pos = self.waypoints[-1][0:2]
        [x, y] = self.get_position_from_heading(prev_pos,  segment[0], segment[1])
        # print('\n  prev_pos ' + str(np.round(prev_pos,1)))
        # print('  next_pos ' + str(np.round([x, y], 0)))
        wp = np.array([
                x,
                y,
                segment[2], # Depth
                max(self.uuv_max_speed, segment[3]), # Speed
                self.wa.PASS, # Default action
                0,            # Skip param for PASS
                0             # Skip param for PASS
                ], dtype = float)
        self.add_waypoint(wp)        

    def init_waypoints(self):
        # initial position
        # use this for the 0th waypoint
        '''
        # UUV needs this for cross track error minimalization
        wp = np.array([
                0,
                0,
                0, # Depth
                self.uuv_max_speed, # Speed
                self.wa.PASS, # Default action
                0,            # Skip param for PASS
                0             # Skip param for PASS
                ], dtype = float)
        self.add_waypoint(wp)     
        '''

        # For new missions - acts as an initial WP
        # UUV needs this for cross track error minimalization
        wp = np.array([
                self.uuv_position[1],
                self.uuv_position[0],
                0, # Depth
                self.uuv_max_speed, # Speed
                self.wa.PASS, # Default action
                0,            # Skip param for PASS
                0             # Skip param for PASS
                ], dtype = float)
        self.add_waypoint(wp)     


    def add_waypoint(self, waypoint):
        marker = Marker(type=Marker.SPHERE, action=Marker.ADD)
        marker.header.frame_id = "/world"
        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = waypoint[0]
        marker.pose.position.y = waypoint[1]
        marker.pose.position.z = -waypoint[2]
        marker.id=len(self.waypoints)
        self.markerArray.markers.append(marker)

        if len(self.waypoints) == 0:
            self.waypoints = [waypoint]
        else:
            self.waypoints = np.append(self.waypoints, [waypoint], axis = 0)
        return True

    def callback_fdr(self, p):
        # Params:
        # FDR X and Y
        # Z depth
        # UUV Speed
        # Waypoint Action, N=3, D= 10: Loiter 3 times around FDR in 30 diameter circle
        wp = np.array([p.x,
                       p.y, 
                       45, # TODO
                       1, 
                       self.wa.LOINTER_N, 
                       self.default_loiter_n, 
                       self.default_loiter_radius], 
                       dtype = float)
        self.add_waypoint(wp)

    def callback_new_wp(self, p):
        # Used for testing: Random waypoint generator
        # Params:
        # New Waypoint X and Y
        # Z depth
        wp = np.array([p.x,
                       p.y, 
                       45, #TODO
                       1, 
                       self.wa.PASS, 
                       0,
                       0], 
                       dtype = float)
        self.add_waypoint(wp)

    def get_position_from_heading(self, start,  heading, distance):
        x = start[0] + distance * math.sin(math.radians(float(heading)))
        y = start[1] + distance * math.cos(math.radians(float(heading)))
        return [x, y]
    
    def callback_odometry(self, msg):
        pos = [msg.pose.pose.position.x,
               msg.pose.pose.position.y,
               msg.pose.pose.position.z]

        # Calculate the position, position, and time of message
        p = self.vector_to_np(msg.pose.pose.position)
        self.uuv_position = p

    def vector_to_np(self, v):
        return np.array([v.x, v.y, v.z])

    def callback_obstacle_near_wp(self, msg):
        if (msg.data
            and self.target_wp_id >= 0
            and len(self.waypoints) > self.target_wp_id
        ):
            next_heading = self.hc.get_wp_heading(
                self.waypoints[self.target_wp_id][self.wp.X:2], 
                self.waypoints[self.target_wp_id + 1][self.wp.X:2]
            )
            next_distance = self.hc.planar_distance(
                self.waypoints[self.target_wp_id][self.wp.X:2], 
                self.waypoints[self.target_wp_id + 1][self.wp.X:2]
            )
            # print(self.waypoints[self.target_wp_id])
            # print(self.waypoints[self.target_wp_id + 1])
            # print(next_heading)
            new_wp_distance = 25

            if next_distance <= new_wp_distance:
                self.next_wp_pub.publish(Bool(True))
            else:
                self.waypoints[self.target_wp_id][self.wp.X] = self.waypoints[self.target_wp_id][self.wp.X] + new_wp_distance * math.sin(math.radians(next_heading))
                self.waypoints[self.target_wp_id][self.wp.Y] = self.waypoints[self.target_wp_id][self.wp.Y] + new_wp_distance * math.cos(math.radians(next_heading))

                print(self.waypoints[self.target_wp_id])

                self.waypoint_pub.publish(Float64MultiArray(data = np.array(self.waypoints).flatten()))     

                self.markerArray.markers[self.target_wp_id].pose.position.x = self.waypoints[self.target_wp_id][self.wp.X]
                self.markerArray.markers[self.target_wp_id].pose.position.y = self.waypoints[self.target_wp_id][self.wp.Y]
                
                self.waypoint_marker_pub.publish(self.markerArray)

            rospy.logwarn('--- Waypoint Altered due to obstacle---')

    def callback_target_wp_id(self, msg):
        self.target_wp_id = msg.data

if __name__=='__main__':
    print('Starting BT MissionServer')
    rospy.init_node('Mission_Server', log_level=rospy.INFO)
    try:
        node = TaskHandler("Mission_Server")
        rospy.spin()
    except rospy.ROSInterruptException:
        print('caught exception')

############<<USER CUSTOM CODE ENDS>>################################