#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures the current mission
"""

##############################################################################
# Imports
##############################################################################

import py_trees
import rospy2 as rospy
import sensor_msgs.msg as sensor_msgs
from std_msgs.msg import String
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
        * bb_mission: the raw message from topic /iver0/bb_mission
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
    """
    def __init__(self, 
                    name, 
                    topic_name="bb_mission"        
                ):
                
        super(ToBlackboard, self).__init__(name=name,
                                           topic_name=topic_name,
                                           topic_type=String,
                                           blackboard_variables={"bb_mission":None},
                                           clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.blackboard = py_trees.blackboard.Blackboard()
        
        self.blackboard.bb_mission = String()
        
        
############<<USER INIT CODE BEGINS>>##############################
        # default_mission = 'waypoint'
        # if (not self.enable_waypoint_following):
        #     default_mission = 'pipe_track'
        # self.blackboard.bb_mission.data = default_mission
        print("\n\n\n\nmission2bb: " + str(self.blackboard.bb_mission.data))
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
        # print("mission2bb: " + str(self.blackboard.bb_mission.data))
        self.feedback_message = self.blackboard.bb_mission.data
############<<USER UPDATE CODE ENDS>>################################
        return status
        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################