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


############<<USER IMPORT CODE BEGINS>>##############################
import numpy as np # USER CODE?
from vandy_bluerov.srv import TAM
from uuv_thruster_manager.srv import ThrusterManagerInfo
from uuv_control_msgs.srv import *
from std_msgs.msg import Float32MultiArray
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
        self.blackboard.total_degradation = 0
     

############<<USER INIT CODE BEGINS>>##############################
        self.thruster_pairs = [[0,1],
                              [2,3]]
        #self.total_degradation = 0.0
        self.reallocations = np.ones(6)

        self.thruster_reallocation_pub = rospy.Publisher(
            '/iver0/thruster_reallocation', Float32MultiArray, queue_size=1)
############<<USER INIT CODE ENDS>>################################

    def setup(self, timeout):
############<<USER SETUP CODE BEGINS>>##############################
############<<USER SETUP CODE ENDS>>################################
        return True            



    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
        """
        self.logger.debug("%s.update()" % self.__class__.__name__)
        
############<<USER UPDATE CODE BEGINS>>##############################
        rospy.loginfo_throttle(1, "\033[1;32m[BT] " + str(self.task)+" \033[0m")
        if len(self.blackboard.dd_output.data) > 0:
            [degraded_id, efficiency, _, _, _, _, _, _, _, _] = np.array(self.blackboard.dd_output.data)
    
            if (
                self.blackboard.dd_xy_axis_degradation 
                # and abs(self.blackboard.HSD_out.heading) < 10.0   
            ):
                # Publish reallocation info for evaluation
                msg = Float32MultiArray()             
                if (efficiency == 0):
                    # Efficiency is between 0.0 to 0.5, classified as 0.0 - severe degradation
                    # Turn off thruster and its pair
                    rospy.logwarn_throttle(1, "[%s] Severe degradation detected - Turning off faulty thrusters" % self.name)
                    self.reallocate(int(degraded_id), efficiency)   
                    pair_id = self.get_thruster_pair(degraded_id)
                    self.reallocate(int(pair_id), efficiency)   

                    msg.data = [rospy.Time.now().to_sec(), degraded_id, -1.0 ] # 200% loss (2 complete thruster)
                    self.thruster_reallocation_pub.publish(msg)                 
                else:
                    # Efficiency is between 0.5 to 0.9 - mild degradation
                    # Reallocate thruster's pair
                    rospy.logwarn_throttle(1, "[%s] Mild degradation detected - Reallocation" % self.name)
                    self.reallocate(int(degraded_id), efficiency)   
                    
                    msg.data = [rospy.Time.now().to_sec(), degraded_id, efficiency]
                    self.thruster_reallocation_pub.publish(msg) 
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
    def reallocate(self, thruster_id, efficiency):
        # There is a bug in thruster id set/get addressing in UUV sim 
        rospy.loginfo_throttle(1, "[%s] ============================ TAM REALLOCATION ============================" % self.name)
        _tam = self.get_TAM()
        _degraded_thruster_pair = thruster_id
        _tam[:, _degraded_thruster_pair] *= efficiency
        self.reallocations[thruster_id] = efficiency
        print(self.reallocations)
        self.blackboard.total_degradation = 6 - np.sum(self.reallocations)
        print("Total degradation: %0.2f" % self.blackboard.total_degradation)
        if not self.set_TAM(_tam):
            rospy.logerr("Reallocation failed") 
            return False
        return True
    
    def get_thruster_pair(self, degraded_id):
        return self.thruster_pairs[int(degraded_id // 2)][int(1 - degraded_id % 2)]

    def get_TAM(self):
        try:
            rospy.wait_for_service('/iver0/thruster_manager/get_thrusters_info', timeout=5)
        except rospy.ROSException:
            raise rospy.ROSException('/iver0/thruster_manager/get_thrusters_info Service not available!')

        try:
            ThrusterManagerInfo_srv = rospy.ServiceProxy(
                '/iver0/thruster_manager/get_thrusters_info',
                ThrusterManagerInfo)
        except rospy.ServiceException, e:
            raise rospy.ROSException('Service call failed, error=' + e)

        response = ThrusterManagerInfo_srv()
        if len(response.allocation_matrix) == 36:
            return np.reshape(response.allocation_matrix, (6, 6))
        else:
            return False

    def set_TAM(self, tam):
        try:
            rospy.wait_for_service('/iver0/thruster_manager/set_tam', timeout=5)
        except rospy.ROSException:
            raise rospy.ROSException('/iver0/thruster_manager/set_tam Service not available!')

        try:
            TAM_reallocation_srv = rospy.ServiceProxy(
                '/iver0/thruster_manager/set_tam',
                TAM)
        except rospy.ServiceException, e:
            raise rospy.ROSException('Service call failed, error=' + e)

        response = TAM_reallocation_srv(tam.flatten())
        print("TAM_reallocation_srv: " + str(response))

        return True



############<<USER CUSTOM CODE ENDS>>################################