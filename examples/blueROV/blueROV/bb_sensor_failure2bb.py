#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures sensor failure
"""

##############################################################################
# Imports
##############################################################################

import py_trees
#import rospy
#import sensor_msgs.msg as sensor_msgs
#from std_msgs.msg import Bool
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
        * bb_sensor_failure: the raw message from topic /iver0/sensor_failure_rpm
        * bb_sensor_failure_warning (:obj:`bool`)
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
    """
    def __init__(self, 
                    name, 
                    topic_name="bb_sensor_failure"        
                ):
                
        super(ToBlackboard, self).__init__(name=name,
                                           #topic_name=topic_name,
                                           #topic_type=Bool,
                                           variable_name="bb_sensor_failure",
                                           variable_value=None
                                           #clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.serene_info_variable="BlueROV_Blackboard_Node"
        self.variable_type="Bool"

        #self.blackboard = py_trees.blackboard.Blackboard()
        
        #self.blackboard.bb_sensor_failure = Bool()
        
        #self.blackboard.bb_sensor_failure_warning = None

"""        
############<<USER INIT CODE BEGINS>>##############################
        self.blackboard.bb_sensor_failure.data = False
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
        if self.blackboard.bb_sensor_failure.data:
            self.blackboard.bb_sensor_failure_warning = True
            rospy.logwarn_throttle(1, "%s: Sensor Failure triggered!" % self.name)
        # Once failure occurs, warning remains true

        self.feedback_message = "bb_sensor_failure triggered" if self.blackboard.bb_sensor_failure_warning else "bb_sensor_failure not triggered"
############<<USER UPDATE CODE ENDS>>################################
"""
        #return status

"""        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################
"""