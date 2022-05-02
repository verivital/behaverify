#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures the output of the DD LEC
"""

##############################################################################
# Imports
##############################################################################

import py_trees
#import rospy
#import sensor_msgs.msg as sensor_msgs
#from std_msgs.msg import Float32MultiArray
#from py_trees_ros import subscribers

"""
############<<USER IMPORT CODE BEGINS>>##############################
import numpy as np
############<<USER IMPORT CODE ENDS>>################################
"""

##############################################################################
# Blackboard node
##############################################################################


class ToBlackboard(py_trees.behaviours.SetBlackboardVariable):
    """
    Subscribes to the battery message and writes battery data to the blackboard.
    Also adds a warning flag to the blackboard if the battery
    is low - note that it does some buffering against ping-pong problems so the warning
    doesn't trigger on/off rapidly when close to the threshold.

    When ticking, updates with :attr:`~py_trees.common.Status.RUNNING` if it got no data,
    :attr:`~py_trees.common.Status.SUCCESS` otherwise.

    Blackboard Variables:
        * dd_output: the raw message from topic /iver0/degradation_detector
        * dd_z_axis_warning (:obj:`bool`)
        * dd_xy_axis_degradation (:obj:`bool`)
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
        total_degradation_threshold (:obj:`float`) : parameter        
        num_classes (:obj:`float`) : parameter        
        enable_fault_detection (:obj:`float`) : parameter        
        decision_source (:obj:`float`) : parameter        
    """
    def __init__(self, 
                    name, 
                    topic_name="degradation_detector",         
                    total_degradation_threshold=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea7faf0>,         
                    num_classes=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea7fc40>,         
                    enable_fault_detection=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea7fd90>,         
                    decision_source=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea7fee0>        
                ):
                
        super(ToBlackboard, self).__init__(name=name,
                                           #topic_name=topic_name,
                                           #topic_type=Float32MultiArray,
                                           variable_name="dd_output",
                                           variable_value=None
                                           #clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.serene_info_variable="BlueROV_Blackboard_Node"
        self.variable_type="Float32MultiArray"

        #self.blackboard = py_trees.blackboard.Blackboard()
        
        #self.blackboard.dd_output = Float32MultiArray()
        
        #self.blackboard.dd_z_axis_warning = None
        #self.blackboard.dd_xy_axis_degradation = None
        
        #self.total_degradation_threshold=total_degradation_threshold        
        #self.num_classes=num_classes        
        #self.enable_fault_detection=enable_fault_detection        
        #self.decision_source=decision_source
"""        
############<<USER INIT CODE BEGINS>>##############################
############<<USER INIT CODE ENDS>>################################
"""

    #def update(self):
"""
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
"""
        #self.logger.debug("%s.update()" % self.__class__.__name__)
        #status = super(ToBlackboard, self).update()
        #if status == py_trees.common.Status.RUNNING:
            #return status
            
"""
############<<USER UPDATE CODE BEGINS>>##############################
        [prediction, credibility, confidence, decision, degraded_id, efficiency] = np.array(self.blackboard.dd_output.data)
        
        # threshold = -0.145
        a = 0.9 # Magic numbers?
        b = -0.3 # Magic numbers?

        custom_decision = False
        if a * credibility + b * confidence >= self.blackboard.decision_threshold: # Can we make a decision?
            custom_decision = True
        if (
            prediction < self.num_classes-1 
            and custom_decision
            and self.blackboard.total_degradation <= self.total_degradation_threshold
        ):
            # degraded
            if prediction == self.num_classes-2:
                # Z axis
                self.blackboard.dd_z_axis_warning = True
                rospy.logwarn_throttle(1, "Z axis thruster degradation detected")
            else:
                # XY axis
                self.blackboard.dd_xy_axis_degradation = True
                rospy.logwarn_throttle(1, "XY axis thruster severe degradation detected")
        else:
            self.blackboard.dd_z_axis_warning = False
            self.blackboard.dd_xy_axis_degradation = False
############<<USER UPDATE CODE ENDS>>################################
"""
        #return status

"""        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################
"""