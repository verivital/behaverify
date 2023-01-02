#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures the state of the lec dd assurance monitor
"""

##############################################################################
# Imports
##############################################################################

import py_trees
#import rospy
#import sensor_msgs.msg as sensor_msgs
#from ng_msgs.msg import LEC1OutputAssuredStamped
#from py_trees_ros import subscribers

"""
############<<USER IMPORT CODE BEGINS>>##############################
import numpy as np
############<<USER IMPORT CODE ENDS>>################################
"""

##############################################################################
# Blackboard node
##############################################################################


#class ToBlackboard(subscribers.ToBlackboard):
class ToBlackboard(py_trees.behaviours.SetBlackboardVariable):
    """
    Subscribes to the battery message and writes battery data to the blackboard.
    Also adds a warning flag to the blackboard if the battery
    is low - note that it does some buffering against ping-pong problems so the warning
    doesn't trigger on/off rapidly when close to the threshold.

    When ticking, updates with :attr:`~py_trees.common.Status.RUNNING` if it got no data,
    :attr:`~py_trees.common.Status.SUCCESS` otherwise.

    Blackboard Variables:
        * lec_dd_am: the raw message from topic /lec_dd_am/p_value
        * lec_dd_am_warning (:obj:`bool`)
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
    """
    def __init__(self, 
                    name, 
                    topic_name="lec_dd_am"        
                ):

        super(ToBlackboard, self).__init__(name=name,
                                           #topic_name=topic_name,
                                           #topic_type=LEC1OutputAssuredStamped,
                                           #blackboard_variables={"lec_dd_am":None},
                                           variable_name="lec_dd_am",
                                           variable_value=None
                                           #clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.serene_info_variable="BlueROV_Blackboard_Node"
        self.variable_type="LEC1OutputAssuredStamped"
        #self.blackboard = py_trees.blackboard.Blackboard()
        
        #self.blackboard.lec_dd_am = LEC1OutputAssuredStamped()
        
        #self.blackboard.lec_dd_am_warning = False

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
        log_m = np.log(self.blackboard.lec_dd_am.confs[0].values[-2])
        if log_m > self.dd_threshold :
            self.blackboard.lec_dd_am_warning = True
            rospy.logwarn_throttle(5, "%s: lec_dd_am level is high!" % self.name)
        elif log_m < self.dd_threshold / 2:
            self.blackboard.lec_dd_am_warning = False
        # else don't do anything in between - i.e. avoid the ping pong problems

        self.feedback_message = "lec_dd_am level is high" if self.blackboard.lec_dd_am_speed_warning else "lec_dd_am level is ok"
############<<USER UPDATE CODE ENDS>>################################
"""
        #return status
"""        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################
"""