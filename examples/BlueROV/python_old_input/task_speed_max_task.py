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

#import dynamic_reconfigure.client
import py_trees
#import rospy            

 
#from ng_msgs.msg import HSDCommand

##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name ,  
                 uuv_max_speed=None,#<textx:btree.DefaultBBType instance at 0x7fcb5b5f2c10>
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.serene_info_variable="BlueROV_Task_Node"



        #self.task = name
        #self.blackboard = py_trees.blackboard.Blackboard()
        #self.blackboard.HSD_out = HSDCommand()
        
        #self.uuv_max_speed=uuv_max_speed     
"""
############<<USER INIT CODE BEGINS>>##############################
        self.blackboard.uuv_max_speed = uuv_max_speed
        self.blackboard.HSD_out.heading = 0.0
        self.blackboard.HSD_out.speed = uuv_max_speed
        self.blackboard.HSD_out.depth = 45 #?
############<<USER INIT CODE ENDS>>################################
"""
    #def setup(self, timeout):
"""
############<<USER SETUP CODE BEGINS>>##############################
        self.feedback_message = "setup"        
############<<USER SETUP CODE ENDS>>################################
"""
        #return True            


    #def update(self):
"""
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
"""
        #self.logger.debug("%s.update()" % self.__class__.__name__)
"""        
############<<USER UPDATE CODE BEGINS>>##############################
        self.blackboard.HSD_out.speed = self.uuv_max_speed
############<<USER UPDATE CODE ENDS>>################################
"""
         # Return always running                
        #return py_trees.common.Status.RUNNING

    #def terminate(self, new_status):
"""
        Shoot off a clearing command.

        Args:
            new_status (:class:`~py_trees.common.Status`): the behaviour is transitioning to this new status
"""
"""
############<<USER TERMINATE CODE BEGINS>>##############################
        self.feedback_message = "cleared"
############<<USER TERMINATE CODE ENDS>>################################        
"""
"""
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################
"""