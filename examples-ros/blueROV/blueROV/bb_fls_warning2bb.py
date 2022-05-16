#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures the FLS obstacle in view information
"""

##############################################################################
# Imports
##############################################################################

import py_trees
import rospy2 as rospy
import sensor_msgs.msg as sensor_msgs
from std_msgs.msg import Header
from py_trees_ros import subscribers
############<<USER IMPORT CODE BEGINS>>##############################
from collections import deque
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
        * obstacle_in_view: the raw message from topic /iver0/obstacle_in_view
        * bb_fls_warning (:obj:`bool`)
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
        fls_in_view_window (:obj:`float`) : parameter        
        fls_in_view_limit (:obj:`float`) : parameter        
    """
    def __init__(self, 
                    name, 
                    topic_name="obstacle_in_view",         
                    fls_in_view_window=20,         
                    fls_in_view_limit=10        
                ):
                
        super(ToBlackboard, self).__init__(name=name,
                                           topic_name=topic_name,
                                           topic_type=Header,
                                           blackboard_variables={"obstacle_in_view":None},
                                           clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.blackboard = py_trees.blackboard.Blackboard()
        
        self.blackboard.obstacle_in_view = Header()
        
        self.blackboard.bb_fls_warning = False
        
        self.fls_in_view_window=fls_in_view_window        
        self.fls_in_view_limit=fls_in_view_limit        
############<<USER INIT CODE BEGINS>>##############################
        self.obstacle_in_view_list = deque(maxlen=self.fls_in_view_window)
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
        # This runs with the tree update - 1 Hz, might be little slow
        if rospy.Time.now() - self.blackboard.obstacle_in_view.stamp < rospy.Duration.from_sec(1.0):
            # Obstacle was observed during the last update        
            self.obstacle_in_view_list.append(1)            
        else:
            self.obstacle_in_view_list.append(0)
        if np.sum(self.obstacle_in_view_list) > self.fls_in_view_limit:
            # Obstacle in view at least x seconds in the last n second window
            self.blackboard.bb_fls_warning = True
            rospy.logwarn_throttle(1, "%s: fls_warning triggered!" % self.name)
            # For now, trigger and do some e-stop
            self.blackboard.emergency_stop_warning = True
            rospy.logwarn_throttle(1, "%s: emergency_stop_warning!" % self.name)


############<<USER UPDATE CODE ENDS>>################################
        return status
        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################