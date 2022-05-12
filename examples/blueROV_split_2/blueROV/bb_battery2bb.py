#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
This node captures the state of the battery
"""

##############################################################################
# Imports
##############################################################################

import py_trees
#import rospy
#import sensor_msgs.msg as sensor_msgs
#from vandy_bluerov.msg import PixhawkHW
#from py_trees_ros import subscribers

"""
############<<USER IMPORT CODE BEGINS>>##############################
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
        * battery: the raw message from topic /iver0/pixhawk_hw
        * battery_low_warning (:obj:`bool`)
    Args:
        name (:obj:`str`): name of the behaviour
        topic_name (:obj:`str`) : name of the input topic        
        failsafe_battery_low_threshold (:obj:`float`) : parameter        
    """
    def __init__(self, 
                    name, 
                    topic_name="pixhawk_hw",         
                    failsafe_battery_low_threshold=None,#0.1        
                ):

        super(ToBlackboard, self).__init__(name=name,
                                           #topic_name=topic_name,
                                           #topic_type=PixhawkHW,
                                           #blackboard_variables={"battery":None},
                                           variable_name="battery",
                                           variable_value=None
                                           #clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.serene_info_variable="BlueROV_Blackboard_Node"
        self.variable_type="PixhawkHW"
        #self.blackboard = py_trees.blackboard.Blackboard()
        
        #self.blackboard.battery = PixhawkHW()
        
        #self.blackboard.battery_low_warning = False
        
        #self.failsafe_battery_low_threshold=failsafe_battery_low_threshold
"""
############<<USER INIT CODE BEGINS>>##############################
        self.blackboard.battery.batt_charge_remaining = 0.0
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
        if self.blackboard.battery.batt_charge_remaining > self.failsafe_battery_low_threshold + 0.05:
            self.blackboard.battery_low_warning = False
        elif self.blackboard.battery.batt_charge_remaining < self.failsafe_battery_low_threshold:
            self.blackboard.battery_low_warning = True
            rospy.logwarn_throttle(60, "%s: battery level is low!" % self.name)
        # else don't do anything in between - i.e. avoid the ping pong problems

        self.feedback_message = "Battery level is low" if self.blackboard.battery_low_warning else "Battery level is ok"
############<<USER UPDATE CODE ENDS>>################################
"""
        #return status
"""        
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################
"""