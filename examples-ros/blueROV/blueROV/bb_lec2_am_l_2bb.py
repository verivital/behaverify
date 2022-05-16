#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures the output of the lec2 assurance monitor left
"""

##############################################################################
# Imports
##############################################################################

import py_trees
import rospy
import sensor_msgs.msg as sensor_msgs
from ng_msgs.msg import LEC1OutputAssuredStamped
from py_trees_ros import subscribers
############<<USER IMPORT CODE BEGINS>>##############################
import numpy as np
############<<USER IMPORT CODE ENDS>>################################

##############################################################################
# Blackboard node
##############################################################################


class ToBlackboard(subscribers.ToBlackboard):
    """
    Subscribes to the battery message and writes battery data to the blackboard.
    Also adds a warning flag to the blackboard if the battery
    is low - note that it does some buffering against ping-pong problems so the warning
    doesn't trigger on/off rapidly when close to the threshold.

    When ticking, updates with :attr:`~py_trees.common.Status.RUNNING` if it got no data,
    :attr:`~py_trees.common.Status.SUCCESS` otherwise.

    Blackboard Variables:
        * lec2_am_l: the raw message from topic /lec2_am/left/p_value
        * lec2_am_l_speed_warning (:obj:`bool`)
        * lec2_am_l_pipe_warning (:obj:`bool`)
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
        pipe_estimation_good_log_val (:obj:`float`) : parameter        
        speed_good_log_val (:obj:`float`) : parameter        
    """
    def __init__(self, 
                    name, 
                    topic_name="lec2_left_am",         
                    pipe_estimation_good_log_val=5.0,         
                    speed_good_log_val=2.5        
                ):
                
        super(ToBlackboard, self).__init__(name=name,
                                           topic_name=topic_name,
                                           topic_type=LEC1OutputAssuredStamped,
                                           blackboard_variables={"lec2_am_l":None},
                                           clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.blackboard = py_trees.blackboard.Blackboard()
        
        self.blackboard.lec2_am_l = LEC1OutputAssuredStamped()
        
        self.blackboard.lec2_am_l_speed_warning = False
        self.blackboard.lec2_am_l_pipe_warning = False
        
        self.pipe_estimation_good_log_val=pipe_estimation_good_log_val        
        self.speed_good_log_val=speed_good_log_val        
############<<USER INIT CODE BEGINS>>##############################
############<<USER INIT CODE ENDS>>################################
    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
        """
        self.logger.debug("%s.update()" % self.__class__.__name__)
        status = super(ToBlackboard, self).update()
        if status == py_trees.common.Status.RUNNING:
            return status
############<<USER UPDATE CODE BEGINS>>##############################
        log_m = np.log(self.blackboard.lec2_am_l.confs[0].values[-2])
        if log_m > self.speed_good_log_val * 2 :
            self.blackboard.lec2_am_l_speed_warning = True
            rospy.logwarn_throttle(1, "%s: lec2_am_ls is high!" % self.name)
        elif log_m < self.speed_good_log_val:
        # else:       
            self.blackboard.lec2_am_l_speed_warning = False
        # else don't do anything in between - i.e. avoid the ping pong problems
        
        if log_m > self.pipe_estimation_good_log_val * 2 :
            self.blackboard.lec2_am_l_pipe_warning = True
            rospy.logwarn_throttle(1, "%s: lec2_am_lp is high!" % self.name)
        elif log_m < self.pipe_estimation_good_log_val:
        # else:
            self.blackboard.lec2_am_l_pipe_warning = False
        # else don't do anything in between - i.e. avoid the ping pong problems
        self.feedback_message = "lec2_am_l is high" if (self.blackboard.lec2_am_l_pipe_warning or self.blackboard.lec2_am_l_speed_warning) else "lec2_am_l is ok"
############<<USER UPDATE CODE ENDS>>################################
        return status
        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################