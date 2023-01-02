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
                 failsafe_battery_low_threshold=0.1
                 ):
        super(ToBlackboard, self).__init__(name=name,
                                           topic_name=topic_name,
                                           topic_type='PixhawkHW',
                                           blackboard_variables={"battery" : None},
                                           clearing_policy=py_trees.common.ClearingPolicy.NEVER
                                           )
        self.blackboard = py_trees.blackboard.Blackboard()
        self.blackboard.battery23 = 12
        self.blackboard.battery23_low_warning = False
        self.failsafe_battery_low_threshold = failsafe_battery_low_threshold

    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check
        against the
        parameters to update the bb variable
        """
        if self.blackboard.battery23 < self.failsafe_battery_low_threshold:
            return py_trees.common.Status.FAILURE
        else:
            return py_trees.common.Status.SUCCESS
