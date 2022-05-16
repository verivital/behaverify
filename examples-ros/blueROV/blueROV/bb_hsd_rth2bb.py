#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures HSD input from rth node
"""

##############################################################################
# Imports
##############################################################################

import py_trees
import rospy2 as rospy
import sensor_msgs.msg as sensor_msgs
from ng_msgs.msg import HSDCommand
from py_trees_ros import subscribers
############<<USER IMPORT CODE BEGINS>>##############################
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
        * hsd_to_rth: the raw message from topic /iver0/hsd_to_rth
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
    """
    def __init__(self, 
                    name, 
                    topic_name="hsd_to_rth"        
                ):
                
        super(ToBlackboard, self).__init__(name=name,
                                           topic_name=topic_name,
                                           topic_type=HSDCommand,
                                           blackboard_variables={"hsd_to_rth":None},
                                           clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.blackboard = py_trees.blackboard.Blackboard()
        
        self.blackboard.hsd_to_rth = HSDCommand()
        
        
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
############<<USER UPDATE CODE ENDS>>################################
        return status
        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################