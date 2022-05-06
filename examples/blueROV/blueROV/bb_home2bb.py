#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures if the uuv is home
"""

##############################################################################
# Imports
##############################################################################

import py_trees
#import rospy
#import sensor_msgs.msg as sensor_msgs
#from std_msgs.msg import Float32
#from py_trees_ros import subscribers

"""
############<<USER IMPORT CODE BEGINS>>##############################
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
        * bb_home_dist: the raw message from topic /iver0/bb_home_dist
        * bb_home_reached (:obj:`bool`)
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
        home_reached_threshold (:obj:`float`) : parameter        
    """
    def __init__(self, 
                    name, 
                    topic_name="bb_home_dist",         
                    home_reached_threshold=None,#<textx:btree.DefaultBBType instance at 0x7f698ed8c5e0>        
                ):
                
        super(ToBlackboard, self).__init__(name=name,
                                           #topic_name=topic_name,
                                           #topic_type=Float32,
                                           variable_name="bb_home_dist",
                                           variable_value=None
                                           #clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.serene_info_variable="BlueROV_Blackboard_Node"
        self.variable_type="Float32"

        #self.blackboard = py_trees.blackboard.Blackboard()
        
        #self.blackboard.bb_home_dist = Float32()
        
        #self.blackboard.bb_home_reached = None
        
        #self.home_reached_threshold=home_reached_threshold
"""        
############<<USER INIT CODE BEGINS>>##############################
        self.blackboard.bb_home_dist.data = 0.0
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
        if self.blackboard.bb_home_dist.data < self.home_reached_threshold:
            self.blackboard.bb_home_reached = True
            rospy.logwarn_throttle(1, "%s: SURFACE triggered!" % self.name)
            # Just turn on, no turn off

        self.feedback_message = "bb_surface triggered" if self.blackboard.bb_home_reached else "bb_surface not triggered"
############<<USER UPDATE CODE ENDS>>################################
"""
        #return status

"""        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################
"""