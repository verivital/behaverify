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

 
from ng_msgs.msg import HSDCommand 
from std_msgs.msg import Bool 
from std_msgs.msg import String
############<<USER IMPORT CODE BEGINS>>##############################
############<<USER IMPORT CODE ENDS>>################################

##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name  
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.task = name
        self.blackboard = py_trees.blackboard.Blackboard()
        self.blackboard.HSD_out = HSDCommand()
        self.blackboard.cm_hsd_input = String()
     
        self.hsd_waypoint__sub = rospy.Subscriber( '/iver0/hsd_to_waypoint',
                                            HSDCommand,
                                            self.hsd_waypoint__callback,
                                            queue_size =1)
        self.hsd_waypoint__msg =  HSDCommand()                   
        self.hsd_waypoint_completed__sub = rospy.Subscriber( '/iver0/waypoints_completed',
                                            Bool,
                                            self.hsd_waypoint_completed__callback,
                                            queue_size =1)
        self.hsd_waypoint_completed__msg =  Bool()                   
        self.cm_hsd_input__pub = rospy.Publisher( '/iver0/cm_hsd_input',
                                            String,
                                            queue_size=1)
        self.cm_hsd_input__msg =  String()                   
        self.next_wp__pub = rospy.Publisher( '/iver0/next_wp',
                                            Bool,
                                            queue_size=1)
        self.next_wp__msg =  Bool()                   

############<<USER INIT CODE BEGINS>>##############################
        self.blackboard.HSD_out.heading = 0.0
        self.blackboard.HSD_out.speed = 0.9
        self.blackboard.HSD_out.depth = 45 #?
        self.waypoint_completed = False
############<<USER INIT CODE ENDS>>################################

    def setup(self, timeout):
############<<USER SETUP CODE BEGINS>>##############################
        self.feedback_message = "setup"
############<<USER SETUP CODE ENDS>>################################
        return True            

    def hsd_waypoint__callback(self, msg):
        self.hsd_waypoint__msg = msg
############<<USER SUB_hsd_waypoint_ CODE BEGINS>>##############################
############<<USER SUB_hsd_waypoint_ CODE ENDS>>################################        

    def hsd_waypoint_completed__callback(self, msg):
        self.hsd_waypoint_completed__msg = msg
############<<USER SUB_hsd_waypoint_completed_ CODE BEGINS>>##############################
############<<USER SUB_hsd_waypoint_completed_ CODE ENDS>>################################        


    def cm_hsd_input__publish(self, data):
        self.cm_hsd_input__msg = data
############<<USER PUB_cm_hsd_input_ CODE BEGINS>>##############################
############<<USER PUB_cm_hsd_input_ CODE ENDS>>################################
        self.cm_hsd_input__pub.publish(data)        
    def next_wp__publish(self, data):
        self.next_wp__msg = data
############<<USER PUB_next_wp_ CODE BEGINS>>##############################
############<<USER PUB_next_wp_ CODE ENDS>>################################
        self.next_wp__pub.publish(data)        

    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
        """
        self.logger.debug("%s.update()" % self.__class__.__name__)
        
############<<USER UPDATE CODE BEGINS>>##############################
        self.blackboard.cm_hsd_input = self.name
        self.blackboard.HSD_out.heading = self.hsd_waypoint__msg.heading
        self.blackboard.HSD_out.depth = self.hsd_waypoint__msg.depth
        # print('\t\t\t\t\t\tHSD 2BB:     ' + str(rospy.get_time()) + ' ' +  str(self.hsd_waypoint__msg.heading) + ' ' +  str(self.hsd_waypoint__msg.header.seq))

        rospy.loginfo("\033[1;32m[BT] " + str(self.task)+" \033[0m")
        #rospy.loginfo_throttle(1, "\033[1;32m[BT] " + str(self.task)+" \033[0m")
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