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

 
#from std_msgs.msg import String 
#from std_msgs.msg import Bool
##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name  
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.serene_info_variable="BlueROV_Task_Node"



        #self.task = name
        #self.blackboard = py_trees.blackboard.Blackboard()
        #self.blackboard.next_mission = None
     
        #self.bb_mission_sub = rospy.Subscriber( '/iver0/bb_mission',
                                            #String,
                                            #self.bb_mission_callback,
                                            #queue_size =1)
        #self.bb_mission_msg =  String()                   
        #self.next_wp__pub = rospy.Publisher( '/iver0/next_wp',
                                            #Bool,
                                            #queue_size=1)
        #self.next_wp__msg =  Bool()                   
"""
############<<USER INIT CODE BEGINS>>##############################
############<<USER INIT CODE ENDS>>################################
"""
    #def setup(self, timeout):
"""
############<<USER SETUP CODE BEGINS>>##############################
############<<USER SETUP CODE ENDS>>################################
"""
        #return True            

    #def bb_mission_callback(self, msg):
        #self.bb_mission_msg = msg
"""
############<<USER SUB_bb_mission CODE BEGINS>>##############################
############<<USER SUB_bb_mission CODE ENDS>>################################        
"""


    #def next_wp__publish(self, data):
        #self.next_wp__msg = data
"""
############<<USER PUB_next_wp_ CODE BEGINS>>##############################
############<<USER PUB_next_wp_ CODE ENDS>>################################
"""
        #self.next_wp__pub.publish(data)        
    #def update(self):
"""
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
"""
        #self.logger.debug("%s.update()" % self.__class__.__name__)
"""        
############<<USER UPDATE CODE BEGINS>>##############################
        self.blackboard.next_mission = True
        self.next_wp__pub.publish(Bool(True))
        return py_trees.common.Status.SUCCESS
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
############<<USER TERMINATE CODE ENDS>>################################        
"""
"""
############<<USER CUSTOM CODE BEGINS>>##############################
############<<USER CUSTOM CODE ENDS>>################################
"""