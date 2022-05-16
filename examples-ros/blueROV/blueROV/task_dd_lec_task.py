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

 
from std_msgs.msg import Float32MultiArray
############<<USER IMPORT CODE BEGINS>>##############################
#User code
import numpy as np
import math
import os
import rospkg
import tensorflow as tf
import tensorflow.keras as keras
import tf.transformations as trans
import collections
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, Activation
import json
########## Addition for compatability with ALC Toolchain ##########
# import pytorch_semseg_adapter
from std_msgs.msg import Float32, Bool
from ng_msgs.msg import LEC1OutputAssuredStamped, AssuranceMonitorConfidence
import torch
import alc_utils.common
import alc_utils.assurance_monitor
import alc_utils.network_interface
from alc_utils import config as alc_config
############<<USER IMPORT CODE ENDS>>################################

##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name ,  
                 num_classes=22, 
                 ann_input_len=13, 
                 ddlec_am_path="jupyter/admin_BlueROV/FDIR_ALC/SLModel", 
                 ddlec_am_params="{'user_choice':'override_threshold','am_s_threshold':0.5, 'am_threshold':0.5}"
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.task = name
        self.blackboard = py_trees.blackboard.Blackboard()
        
        self.num_classes=num_classes        
        self.ann_input_len=ann_input_len        
        self.ddlec_am_path=ddlec_am_path        
        self.ddlec_am_params=ddlec_am_params     
        self.lec_input__sub = rospy.Subscriber( '/iver0/thruster_cmd_logging',
                                            Float32MultiArray,
                                            self.lec_input__callback,
                                            queue_size =1)
        self.lec_input__msg =  Float32MultiArray()                   
        self.degradation_detector__pub = rospy.Publisher( '/iver0/degradation_detector',
                                            Float32MultiArray,
                                            queue_size=1)
        self.degradation_detector__msg =  Float32MultiArray()                   
        self.degradation_detector_am__pub = rospy.Publisher( '/iver0/degradation_detector_am/p_value',
                                            Float32MultiArray,
                                            queue_size=1)
        self.degradation_detector_am__msg =  Float32MultiArray()                   

############<<USER INIT CODE BEGINS>>##############################
        _ams = alc_utils.assurance_monitor.load_assurance_monitor("multi")
        # Should be an input arg
        if (not os.path.exists(ddlec_am_path)):
            ddlec_am_path = os.path.join(alc_config.WORKING_DIRECTORY, ddlec_am_path)
        if (os.path.exists(ddlec_am_path)):
            _ams.load([ddlec_am_path])
            self.am = _ams.assurance_monitors[0]
        else:
            self.am = None
############<<USER INIT CODE ENDS>>################################

    def setup(self, timeout):
############<<USER SETUP CODE BEGINS>>##############################
############<<USER SETUP CODE ENDS>>################################
        return True            

    def lec_input__callback(self, msg):
        self.lec_input__msg = msg
############<<USER SUB_lec_input_ CODE BEGINS>>##############################
############<<USER SUB_lec_input_ CODE ENDS>>################################        


    def degradation_detector__publish(self, data):
        self.degradation_detector__msg = data
############<<USER PUB_degradation_detector_ CODE BEGINS>>##############################
############<<USER PUB_degradation_detector_ CODE ENDS>>################################
        self.degradation_detector__pub.publish(data)        
    def degradation_detector_am__publish(self, data):
        self.degradation_detector_am__msg = data
############<<USER PUB_degradation_detector_am_ CODE BEGINS>>##############################
############<<USER PUB_degradation_detector_am_ CODE ENDS>>################################
        self.degradation_detector_am__pub.publish(data)        

    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
        """
        self.logger.debug("%s.update()" % self.__class__.__name__)
        
############<<USER UPDATE CODE BEGINS>>##############################

        # no assurance monitor loaded
        if (not self.am):
            rospy.loginfo(" No assurance monitor loaded in Btree [%s]" % (self.task))
 
         # if input is ready
        if (self.am and len(self.lec_input__msg.data[0:self.ann_input_len]) == self.ann_input_len):
            # Format LEC input
            model_input = np.reshape(self.lec_input__msg.data[0:self.ann_input_len], (1, -1))
 

            # print("\n\n\nModel input:\n"+str(model_input)+"\n\n\n")

            # Run LEC/AM prediction
            msg =  Float32MultiArray()
            msg.data = model_input
            INPUT_TOPIC = "/iver0/thruster_cmd_logging"
            model_input = {INPUT_TOPIC : msg}
            # Params must come from args
            #params = json.loads(self.ddlec_am_params.replace("'", "\""))
            params = self.ddlec_am_params
            [computed_p_values, prediction, credibility, confidence, decisions, am_output, softmax, combined_am_output] = self.am.evaluate(model_input, None, **params) 
            [degraded_id, efficiency] = self.get_fault_from_class(prediction, self.num_classes)            

            # Publishing LEC output
            msg =  Float32MultiArray()

            msg.data = [degraded_id, efficiency, prediction, credibility, confidence, decisions["snapshot"], decisions["comb"], am_output, softmax, combined_am_output]
            #self.degradation_detector__pub.publish(self.degradation_detector__msg)
            self.degradation_detector__publish(msg)
            # Publishing p values
            msg.data = computed_p_values   
            #self.degradation_detector_am__pub.publish(self.degradation_detector_am__msg)
            self.degradation_detector_am__publish(msg)

            if prediction == self.num_classes - 1:
                uuv_state_str = "\033[1;32m Nominal  \033[0m"
            else:
                uuv_state_str = "\033[1;31m Degraded \033[0m"                                 

            rospy.loginfo("[%s] %s class: %d (#%d, %0.2f), comb_am: %0.2f,\033[1;3%dm decision: %d\033[0m" % (
                self.task, uuv_state_str, prediction, degraded_id, efficiency, combined_am_output, 1+decisions["comb"], decisions["comb"]))
               
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
    def get_fault_from_class(self, class_val, num_classes):
        if class_val == num_classes - 1:
            # Nominal
            degraded_id = 6
            efficiency = 1.0
        elif class_val >= 20:
            # Z axis thruster degradation
            degraded_id =   class_val - 16
            efficiency = 0.9
        else:
            # XY axis thruster degradation
            slot = class_val % 5
            degraded_id = class_val // 5
        
            if slot == 0:
                efficiency = 0
            else:
                efficiency = 0.45 + slot * 0.1

        return [degraded_id, efficiency]
############<<USER CUSTOM CODE ENDS>>################################