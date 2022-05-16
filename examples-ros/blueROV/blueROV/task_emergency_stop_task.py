#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/py_trees_ros/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

##############################################################################
# Imports
##############################################################################

import dynamic_reconfigure.client
import py_trees
import rospy            


############<<USER IMPORT CODE BEGINS>>##############################
import rospkg
import sys, os
rp = rospkg.RosPack()
sys.path.append(os.path.join(rp.get_path("vandy_bluerov"),"nodes"))
from thruster_functions import ThrusterFunction
############<<USER IMPORT CODE ENDS>>################################

##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name  
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.task = name
        self.blackboard = py_trees.blackboard.Blackboard()
     

############<<USER INIT CODE BEGINS>>##############################
############<<USER INIT CODE ENDS>>################################

    def setup(self, timeout):
############<<USER SETUP CODE BEGINS>>##############################
############<<USER SETUP CODE ENDS>>################################
        return True            



    def update(self):
        """
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
        """
        self.logger.debug("%s.update()" % self.__class__.__name__)
        
############<<USER UPDATE CODE BEGINS>>##############################
        tfunc = ThrusterFunction() 
        tfunc.emergency_stop()        
        return py_trees.common.Status.SUCCESS
############<<USER UPDATE CODE ENDS>>################################

         # Return always running                
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        """
        Shoot off a clearing command.

        Args:
            new_status (:class:`~py_trees.common.Status`): the behaviour is transitioning to this new status
        """
############<<USER TERMINATE CODE BEGINS>>##############################
############<<USER TERMINATE CODE ENDS>>################################        

############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################