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

 
#from std_msgs.msg import Float32MultiArray
##############################################################################
# Behaviours
##############################################################################


class TaskHandler(py_trees.behaviour.Behaviour):
    
    def __init__(self, 
                 name ,  
                 num_classes=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea8abe0>, 
                 ann_input_len=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea8ad30>, 
                 ddlec_am_path=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea8ae80>, 
                 ddlec_am_params=None,#<textx:btree.DefaultBBType instance at 0x7f9b3ea8afd0>
                ):                 
        super(TaskHandler, self).__init__(name=name)
        self.serene_info_variable="BlueROV_Task_Node"



        #self.task = name
        #self.blackboard = py_trees.blackboard.Blackboard()
        
        #self.num_classes=num_classes        
        #self.ann_input_len=ann_input_len        
        #self.ddlec_am_path=ddlec_am_path        
        #self.ddlec_am_params=ddlec_am_params     
        #self.lec_input__sub = rospy.Subscriber( '/iver0/thruster_cmd_logging',
                                            #Float32MultiArray,
                                            #self.lec_input__callback,
                                            #queue_size =1)
        #self.lec_input__msg =  Float32MultiArray()                   
        #self.degradation_detector__pub = rospy.Publisher( '/iver0/degradation_detector',
                                            #Float32MultiArray,
                                            #queue_size=1)
        #self.degradation_detector__msg =  Float32MultiArray()                   
        #self.degradation_detector_am__pub = rospy.Publisher( '/iver0/degradation_detector_am/p_value',
                                            #Float32MultiArray,
                                            #queue_size=1)
        #self.degradation_detector_am__msg =  Float32MultiArray()                   
"""
############<<USER INIT CODE BEGINS>>##############################
 
        # Tensorflow config
        tf_config = tf.ConfigProto(log_device_placement=False)
        tf_config.gpu_options.allow_growth = True
        # Keep track of TF Session and Graph in case LibraryAdapter instance is called across multiple threads
        self.session = tf.Session(config=tf_config)
        self.tf_graph = tf.get_default_graph()
        keras.backend.set_session(self.session)
        normalizer = [1000, 1000, 1000, 1000, 1000, 1000, 6000, 6000, 6000, 6000, 6000, 6000, 30]
        # try:
        self.ddv2 = DegradationDetectorLEC(self.normalizer, self.decision_threshold, self.num_classes)
        rospy.loginfo(" \033[1;32m>>>>>>>>>>>>>>>>>>> DD LEC LOADED <<<<<<<<<<<<<<<<<<<<<<<<<\033[0m ")
        # except:
            # rospy.logerr("DD LEC loading failed")

        am_topic = rospy.get_param('~am_topic', "/iver0/degradation_detector_am_vae/p_value")
        # am_model_dir = rospy.get_param('~am_model_dir', "jupyter/admin_BlueROV/LEC_DD_VAE/1607884132228/SLModel")
        am_model_dir = rospy.get_param('~am_model_dir', "jupyter/admin_BlueROV/LEC_DD_VAE/1623219226455/SLModel")

        model_dir = os.path.join(alc_config.WORKING_DIRECTORY, am_model_dir)

        self._assurance_monitor_paths = [model_dir]
        rospy.loginfo(model_dir)
        self._ams = alc_utils.assurance_monitor.load_assurance_monitor("multi")
        rospy.loginfo(" \033[1;32m>>>>>>>>>>>>>>>>>>> DD ASSURANCE MONITOR <<<<<<<<<<<<<<<<<<<<<<<<<\033[0m ")
        if (os.path.exists(model_dir)):
            self._ams.load(self._assurance_monitor_paths)
            rospy.loginfo("[DD TASK] am done")
        else:
            rospy.logerr("[DD TASK] am path/load error")
        if (self._ams and self._ams.assurance_monitors):
            rospy.loginfo("[DD TASK] am loaded")
        else:
            rospy.logerr("[DD TASK] am load error")
        rospy.loginfo("Publishing on Assurance monitor topic: " + str(am_topic))
        self.dd_am_vae_pub = rospy.Publisher(am_topic, Float32MultiArray, queue_size=1)


############<<USER INIT CODE ENDS>>################################
"""
    #def setup(self, timeout):
"""
############<<USER SETUP CODE BEGINS>>##############################
############<<USER SETUP CODE ENDS>>################################
"""
        #return True            

    #def lec_input__callback(self, msg):
        #self.lec_input__msg = msg
"""
############<<USER SUB_lec_input_ CODE BEGINS>>##############################
############<<USER SUB_lec_input_ CODE ENDS>>################################        
"""


    #def degradation_detector__publish(self, data):
        #self.degradation_detector__msg = data
"""
############<<USER PUB_degradation_detector_ CODE BEGINS>>##############################
############<<USER PUB_degradation_detector_ CODE ENDS>>################################
"""
        #self.degradation_detector__pub.publish(data)        
    #def degradation_detector_am__publish(self, data):
        #self.degradation_detector_am__msg = data
"""
############<<USER PUB_degradation_detector_am_ CODE BEGINS>>##############################
############<<USER PUB_degradation_detector_am_ CODE ENDS>>################################
"""
        #self.degradation_detector_am__pub.publish(data)        
    #def update(self):
"""
        Call the parent to write the raw data to the blackboard and then check against the
        parameters to update the bb variable
"""
        #self.logger.debug("%s.update()" % self.__class__.__name__)
"""        
############<<USER UPDATE CODE BEGINS>>##############################
 
         # if input is ready
        if len(self.lec_input__msg.data[0:self.ann_input_len]) == self.ann_input_len:
            # Format LEC input
            model_input = np.reshape(self.lec_input__msg.data[0:self.ann_input_len], (1, -1))

            # print("\n\n\nModel input:\n"+str(model_input)+"\n\n\n")

            # Run LEC prediction
            [prediction, credibility, confidence, decision] = self.ddv2.predict(self.ddv2.normalize(model_input)) 
            [degraded_id, efficiency] = self.ddv2.get_fault_from_class(prediction)
            p_values = self.ddv2.get_p_values()

            # Publishing LEC output
            msg =  Float32MultiArray()

            msg.data = [prediction, credibility, confidence, decision, degraded_id, efficiency]
            #self.degradation_detector__pub.publish(self.degradation_detector__msg)
            self.degradation_detector__publish(msg)
            # Publishing p values
            msg.data = p_values   
            #self.degradation_detector_am__pub.publish(self.degradation_detector_am__msg)
            self.degradation_detector_am__publish(msg)

            if prediction == self.num_classes - 1:
                uuv_state_str = "\033[1;32m Nominal  \033[0m"
            else:
                uuv_state_str = "\033[1;31m Degraded \033[0m"                                 

            rospy.loginfo("[%s] %s class: %d (#%d, %0.2f), credibility: %0.2f, confidence: %0.2f,\033[1;3%dm decision: %d\033[0m" % (
                self.task, uuv_state_str, prediction, degraded_id, efficiency, credibility, confidence, 1+decision, decision))

            # ASSURANCE MONITOR
            resas = []
            confidence_msg = None
            if self._ams and self._ams.assurance_monitors:
                topics_data = {}
                topics_data['/iver0/thruster_cmd_logging'] = self.lec_input__msg
                resas = self._ams.evaluate(topics_data, [])
            if resas:
                msg.data = [math.log(resas[0][-3]), resas[0][-1]] # log(m), detector
                self.dd_am_vae_pub.publish(msg)
                
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