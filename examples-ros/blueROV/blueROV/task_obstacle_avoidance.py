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
import rospy2 as rospy            

 
from ng_msgs.msg import HSDCommand 
from std_msgs.msg import String

############<<USER IMPORT CODE BEGINS>>##############################
############<<USER IMPORT CODE ENDS>>################################

##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name ,  
                 enable_obstacle_avoidance=True
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.task = name
        self.blackboard = py_trees.blackboard.Blackboard()
        self.blackboard.HSD_out = HSDCommand()
        self.blackboard.bb_obstacle_warning = False
        self.blackboard.cm_hsd_input = String()
        
        self.enable_obstacle_avoidance=enable_obstacle_avoidance     
        self.hsd_obstacle_avoidance__sub = rospy.Subscriber( '/iver0/hsd_obstacle_avoidance',
                                            HSDCommand,
                                            self.hsd_obstacle_avoidance__callback,
                                            queue_size =1)
        self.hsd_obstacle_avoidance__msg =  HSDCommand()                   
        self.hsd_pipeline_mapping__sub = rospy.Subscriber( '/iver0/hsd_pipeline_mapping',
                                            HSDCommand,
                                            self.hsd_pipeline_mapping__callback,
                                            queue_size =1)
        self.hsd_pipeline_mapping__msg =  HSDCommand()                   
        self.hsd_waypoint__sub = rospy.Subscriber( '/iver0/hsd_to_waypoint',
                                            HSDCommand,
                                            self.hsd_waypoint__callback,
                                            queue_size =1)
        self.hsd_waypoint__msg =  HSDCommand()                   
        self.hsd_pub_pub = rospy.Publisher( '/iver0/hsd_command',
                                            HSDCommand,
                                            queue_size=1)
        self.hsd_pub_msg =  HSDCommand()                   

############<<USER INIT CODE BEGINS>>##############################
        self.blackboard.bb_obstacle_warning = False
        self.blackboard.HSD_out.heading = 0.0
        self.blackboard.HSD_out.speed = 0.9
        self.blackboard.HSD_out.depth = 45 #?
        self.obstacle_avoidance_margin = 10.0

############<<USER INIT CODE ENDS>>################################

    def setup(self, timeout):
############<<USER SETUP CODE BEGINS>>##############################
        self.feedback_message = "setup"
############<<USER SETUP CODE ENDS>>################################
        return True            

    def hsd_obstacle_avoidance__callback(self, msg):
        self.hsd_obstacle_avoidance__msg = msg
############<<USER SUB_hsd_obstacle_avoidance_ CODE BEGINS>>##############################
############<<USER SUB_hsd_obstacle_avoidance_ CODE ENDS>>################################        

    def hsd_pipeline_mapping__callback(self, msg):
        self.hsd_pipeline_mapping__msg = msg
############<<USER SUB_hsd_pipeline_mapping_ CODE BEGINS>>##############################
        if (
                self.blackboard.cm_hsd_input == 'tracking_task' 
                and abs(self.hsd_obstacle_avoidance__msg.heading) < self.obstacle_avoidance_margin
        ):
                # Set H+S+D, speed comes from task_speed_min/max via BB
                self.hsd_pub_msg.heading = self.hsd_pipeline_mapping__msg.heading
                self.hsd_pub_msg.speed = self.blackboard.HSD_out.speed
                self.hsd_pub_msg.depth = self.hsd_pipeline_mapping__msg.depth
                self.hsd_pub_publish(self.hsd_pub_msg)
############<<USER SUB_hsd_pipeline_mapping_ CODE ENDS>>################################        

    def hsd_waypoint__callback(self, msg):
        self.hsd_waypoint__msg = msg
############<<USER SUB_hsd_waypoint_ CODE BEGINS>>##############################
        if (
                self.blackboard.cm_hsd_input == 'waypoint_task' 
                and abs(self.hsd_obstacle_avoidance__msg.heading) < self.obstacle_avoidance_margin
        ):
                # Set H+S+D
                self.hsd_pub_msg = self.hsd_waypoint__msg
                self.hsd_pub_publish(self.hsd_pub_msg)
############<<USER SUB_hsd_waypoint_ CODE ENDS>>################################        


    def hsd_pub_publish(self, data):
        self.hsd_pub_msg = data
############<<USER PUB_hsd_pub CODE BEGINS>>##############################
        self.hsd_pub_msg.header.stamp = rospy.Time.now()   
        if rospy.Time.now() > rospy.Time(15):
                self.hsd_pub_pub.publish(data)
                return
############<<USER PUB_hsd_pub CODE ENDS>>################################
        self.hsd_pub_pub.publish(data)        

    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
        """
        self.logger.debug("%s.update()" % self.__class__.__name__)
        
############<<USER UPDATE CODE BEGINS>>##############################
        self.feedback_message = "task {0}".format(self.task)
        if (abs(self.hsd_obstacle_avoidance__msg.heading) >= self.obstacle_avoidance_margin
           and self.enable_obstacle_avoidance
        ):
                # Obstacle avoidance
                self.blackboard.bb_obstacle_warning = True
                self.hsd_pub_msg.heading = self.hsd_obstacle_avoidance__msg.heading
                self.hsd_pub_msg.depth = self.hsd_obstacle_avoidance__msg.depth

                self.hsd_pub_msg.speed = self.blackboard.HSD_out.speed
                self.hsd_pub_publish(self.hsd_pub_msg)
        else:
                # Obstacle free heading
                self.blackboard.bb_obstacle_warning = False
                # Using BB varibles for this is slow
                # self.hsd_pub_msg.heading = self.blackboard.HSD_out.heading
                # self.hsd_pub_msg.depth = self.blackboard.HSD_out.depth
                
                # Critical timing HSD commands: Waypoint and Pipe tracking mission HSD:
                # For these use the ROS Topic directly as data driven publisher
        
                # Not critical timing HSD commands: all other
                # For these use the BB:
                if self.blackboard.cm_hsd_input in [
                        'loiter_task',                                                
                        'rth_task',
                        'surface_task'
                ]:
                        self.hsd_pub_msg = self.blackboard.HSD_out
                        
                        self.hsd_pub_msg.speed = self.blackboard.HSD_out.speed
                        self.hsd_pub_publish(self.hsd_pub_msg)
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
        self.feedback_message = "cleared"
############<<USER TERMINATE CODE ENDS>>################################        

############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################