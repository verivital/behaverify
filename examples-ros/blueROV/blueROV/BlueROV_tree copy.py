#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/py_trees/devel/LICENSE
#

##############################################################################
# Imports
##############################################################################

import functools
import py_trees
import py_trees_ros
import py_trees.console as console
import py_trees_msgs.msg as py_trees_msgs
import rospy2 as rospy
import sys

  
import bb_battery2bb  
import bb_ddlecam2bb  
import bb_rth2bb  
import bb_geofence2bb  
import bb_lec2_am_l_2bb  
import bb_lec2_am_r_2bb  
import bb_pipe_lost2bb  
import bb_sensor_failure2bb  
import bb_waypoints_completed2bb  
import bb_home2bb  
import bb_mission2bb  
import bb_ddlec2bb  
import task_surface_task  
import task_rth_task  
import task_loiter_task  
import task_obstacle_avoidance  
import task_speed_max_task  
import task_speed_min_task  
import task_pipe_mapping_enable_task  
import task_pipe_mapping_disable_task  
import task_tracking_task  
import task_waypoint_task
import task_reallocate_task
import task_dd_lec_task

##############################################################################
# Behaviour Tree output interface
##############################################################################


class BlueROV_BT(object):
    def __init__(self):
        self.failsafe_battery_low_threshold = rospy.get_param('~failsafe_battery_low_threshold', 0.1)         
        self.dd_threshold = rospy.get_param('~dd_threshold', 5.0)         
        self.failsafe_rth_enable = rospy.get_param('~failsafe_rth_enable', True)         
        self.pipe_estimation_good_log_val = rospy.get_param('~pipe_estimation_good_log_val', 5.0)         
        self.speed_good_log_val = rospy.get_param('~speed_good_log_val', 2.5)         
        self.pipe_estimation_good_log_val = rospy.get_param('~pipe_estimation_good_log_val', 5.0)         
        self.speed_good_log_val = rospy.get_param('~speed_good_log_val', 2.5)         
        self.home_reached_threshold = rospy.get_param('~home_reached_threshold', 15)         
        self.enable_waypoint_following = rospy.get_param('~enable_waypoint_following', False)         
        self.decision_threshold = rospy.get_param('~decision_threshold', 0.7)         
        self.total_degradation_threshold = rospy.get_param('~total_degradation_threshold', 0.0)         
        self.num_classes = rospy.get_param('~num_classes', 22)         
        self.ann_input_len = rospy.get_param('~ann_input_len', 13)         

        rospy.loginfo('[BT] Tree Params: ')
        rospy.loginfo('[BT] failsafe_battery_low_threshold: {0}'.format(self.failsafe_battery_low_threshold))
        rospy.loginfo('[BT] dd_threshold: {0}'.format(self.dd_threshold))
        rospy.loginfo('[BT] failsafe_rth_enable: {0}'.format(self.failsafe_rth_enable))
        rospy.loginfo('[BT] pipe_estimation_good_log_val: {0}'.format(self.pipe_estimation_good_log_val))
        rospy.loginfo('[BT] speed_good_log_val: {0}'.format(self.speed_good_log_val))
        rospy.loginfo('[BT] pipe_estimation_good_log_val: {0}'.format(self.pipe_estimation_good_log_val))
        rospy.loginfo('[BT] speed_good_log_val: {0}'.format(self.speed_good_log_val))
        rospy.loginfo('[BT] home_reached_threshold: {0}'.format(self.home_reached_threshold))
        rospy.loginfo('[BT] enable_waypoint_following: {0}'.format(self.enable_waypoint_following))
        rospy.loginfo('[BT] decision_threshold: {0}'.format(self.decision_threshold))
        rospy.loginfo('[BT] total_degradation_threshold: {0}'.format(self.total_degradation_threshold))
        rospy.loginfo('[BT] num_classes: {0}'.format(self.num_classes))
        rospy.loginfo('[BT] ann_input_len: {0}'.format(self.ann_input_len))

        root = self.create_root()
        behaviour_tree = py_trees_ros.trees.BehaviourTree(root)
        rospy.on_shutdown(functools.partial(self.shutdown, behaviour_tree))
        if not behaviour_tree.setup(timeout=15.0):
            console.logerror("failed to setup the tree, aborting.")
            sys.exit(1)
        behaviour_tree.tick_tock(500.0)

    def create_root(self):

        BlueROV = py_trees.composites.Parallel("BlueROV")
        topics2bb = py_trees.composites.Parallel("topics2bb")
        dd_tasks = py_trees.composites.Selector("dd_tasks")
        priorities = py_trees.composites.Selector("priorities")
        rth_par = py_trees.composites.Parallel("rth_par")
        track_pipe_mission = py_trees.composites.Sequence("track_pipe_mission")
        tracking = py_trees.composites.Parallel("tracking")
        lec2am_speed_cmd = py_trees.composites.Selector("lec2am_speed_cmd")
        lec2am_mapping_cmd = py_trees.composites.Selector("lec2am_mapping_cmd")
        track_pipe_mission_end = py_trees.composites.Sequence("track_pipe_mission_end")
        waypoint_mission = py_trees.composites.Sequence("waypoint_mission")
        waypoint_selector = py_trees.composites.Selector("waypoint_selector")
        waypoint_end = py_trees.composites.Sequence("waypoint_end")

        battery_check = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="battery_check")
        sensor_failure_selector = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="sensor_failure_selector")
        reallocate_check = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="reallocate_check")
        home_reached_selector = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="home_reached_selector")
        rth_selector = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="rth_selector")
        geofence_selector = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="geofence_selector")
        pipe_lost_selector = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="pipe_lost_selector")
        lec2am_l_speed_check = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="lec2am_l_speed_check")
        lec2am_r_speed_check = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="lec2am_r_speed_check")
        lec2am_l_mapping_check = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="lec2am_l_mapping_check")
        lec2am_r_mapping_check = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="lec2am_r_mapping_check")
        waypoints_sif = py_trees.meta.success_is_failure(py_trees.composites.Selector)(name="waypoints_sif")


        battery2bb = bb_battery2bb.ToBlackboard(
            name="battery2bb",
            topic_name="/iver0/pixhawk_hw", 
            failsafe_battery_low_threshold = self.failsafe_battery_low_threshold 
        )
        ddlecam2bb = bb_ddlecam2bb.ToBlackboard(
            name="ddlecam2bb",
            topic_name="/lec_dd_am/p_value", 
            dd_threshold = self.dd_threshold 
        )
        rth2bb = bb_rth2bb.ToBlackboard(
            name="rth2bb",
            topic_name="/iver0/bb_rth", 
            failsafe_rth_enable = self.failsafe_rth_enable 
        )
        geofence2bb = bb_geofence2bb.ToBlackboard(
            name="geofence2bb",
            topic_name="/iver0/bb_geofence" 
        )
        lec2_am_l_2bb = bb_lec2_am_l_2bb.ToBlackboard(
            name="lec2_am_l_2bb",
            topic_name="/lec2_am/left/p_value", 
            pipe_estimation_good_log_val = self.pipe_estimation_good_log_val,  
            speed_good_log_val = self.speed_good_log_val 
        )
        lec2_am_r_2bb = bb_lec2_am_r_2bb.ToBlackboard(
            name="lec2_am_r_2bb",
            topic_name="/lec2_am/right/p_value", 
            pipe_estimation_good_log_val = self.pipe_estimation_good_log_val,  
            speed_good_log_val = self.speed_good_log_val 
        )
        pipe_lost2bb = bb_pipe_lost2bb.ToBlackboard(
            name="pipe_lost2bb",
            topic_name="/iver0/bb_pipe_lost" 
        )
        sensor_failure2bb = bb_sensor_failure2bb.ToBlackboard(
            name="sensor_failure2bb",
            topic_name="/iver0/sensor_failure_rpm" 
        )
        waypoints_completed2bb = bb_waypoints_completed2bb.ToBlackboard(
            name="waypoints_completed2bb",
            topic_name="/iver0/waypoints_completed" 
        )
        home2bb = bb_home2bb.ToBlackboard(
            name="home2bb",
            topic_name="/iver0/bb_home_dist", 
            home_reached_threshold = self.home_reached_threshold 
        )
        mission2bb = bb_mission2bb.ToBlackboard(
            name="mission2bb",
            topic_name="/bb_mission",
            default_mission = 'waypoint' if self.enable_waypoint_following else 'pipe_track' 
        )
        ddlec2bb = bb_ddlec2bb.ToBlackboard(
            name="ddlec2bb",
            topic_name="/iver0/degradation_detector", 
            decision_threshold = self.decision_threshold,  
            total_degradation_threshold = self.total_degradation_threshold,  
            num_classes = self.num_classes,  
            ann_input_len = self.ann_input_len 
        )


        is_reallocation_requested = py_trees.blackboard.CheckBlackboardVariable(
            name="is_reallocation_requested",
            variable_name='dd_xy_axis_degradation',
            expected_value= False)
        check_dd_am = py_trees.blackboard.CheckBlackboardVariable(
            name="check_dd_am",
            variable_name='lec_dd_am_warning',
            expected_value= False)
        check_lec2am_ls = py_trees.blackboard.CheckBlackboardVariable(
            name="check_lec2am_ls",
            variable_name='lec2_am_l_speed_warning',
            expected_value= False)
        check_lec2am_rs = py_trees.blackboard.CheckBlackboardVariable(
            name="check_lec2am_rs",
            variable_name='lec2_am_r_speed_warning',
            expected_value= False)
        check_lec2am_lp = py_trees.blackboard.CheckBlackboardVariable(
            name="check_lec2am_lp",
            variable_name='lec2_am_l_pipe_warning',
            expected_value= False)
        check_lec2am_rp = py_trees.blackboard.CheckBlackboardVariable(
            name="check_lec2am_rp",
            variable_name='lec2_am_r_pipe_warning',
            expected_value= False)
        check_geofence = py_trees.blackboard.CheckBlackboardVariable(
            name="check_geofence",
            variable_name='bb_geofence_warning',
            expected_value= False)
        check_rth = py_trees.blackboard.CheckBlackboardVariable(
            name="check_rth",
            variable_name='bb_rth_warning',
            expected_value= False)
        check_surface = py_trees.blackboard.CheckBlackboardVariable(
            name="check_surface",
            variable_name='bb_home_reached',
            expected_value= False)
        check_pipe_post = py_trees.blackboard.CheckBlackboardVariable(
            name="check_pipe_post",
            variable_name='bb_pipe_lost_warning',
            expected_value= False)
        check_waypoints_completed = py_trees.blackboard.CheckBlackboardVariable(
            name="check_waypoints_completed",
            variable_name='bb_waypoints_completed.data',
            expected_value= True)
        check_sensor_failure = py_trees.blackboard.CheckBlackboardVariable(
            name="check_sensor_failure",
            variable_name='bb_sensor_failure_warning',
            expected_value= False)
        battery_low_fs = py_trees.blackboard.CheckBlackboardVariable(
            name="battery_low_fs",
            variable_name='battery_low_warning',
            expected_value= False)
        is_track_pipe_mission_requested = py_trees.blackboard.CheckBlackboardVariable(
            name="is_track_pipe_mission_requested",
            variable_name='bb_mission.data',
            expected_value=  'pipe_track' )
        is_waypoint_requested = py_trees.blackboard.CheckBlackboardVariable(
            name="is_waypoint_requested",
            variable_name='bb_mission.data',
            expected_value=  'waypoint' )
        is_snr_requested = py_trees.blackboard.CheckBlackboardVariable(
            name="is_snr_requested",
            variable_name='bb_mission.data',
            expected_value=  'fdr' )
        dd_z_axis = py_trees.blackboard.CheckBlackboardVariable(
            name="dd_z_axis",
            variable_name='dd_z_axis_warning',
            expected_value= False)
        dd_xy_axis = py_trees.blackboard.CheckBlackboardVariable(
            name="dd_xy_axis",
            variable_name='dd_xy_axis_degradation',
            expected_value= False)

        waypoints_condition =py_trees.meta.condition(
            py_trees.composites.Selector,
            status=py_trees.common.Status.FAILURE)(name="waypoints_condition")

        success_node = py_trees.behaviours.Success(name="success_node")
        failure_node = py_trees.behaviours.Failure(name="failure_node")
        running_node = py_trees.behaviours.Running(name="running_node")
        idle = py_trees.behaviours.Running(name="idle")
    

        surface_task =task_surface_task.TaskHandler(
            name="surface_task")
        rth_task =task_rth_task.TaskHandler(
            name="rth_task")
        loiter_task =task_loiter_task.TaskHandler(
            name="loiter_task")
        obstacle_avoidance =task_obstacle_avoidance.TaskHandler(
            name="obstacle_avoidance")
        speed_max_task =task_speed_max_task.TaskHandler(
            name="speed_max_task")
        speed_min_task =task_speed_min_task.TaskHandler(
            name="speed_min_task")
        pipe_mapping_enable_task =task_pipe_mapping_enable_task.TaskHandler(
            name="pipe_mapping_enable_task")
        pipe_mapping_disable_task =task_pipe_mapping_disable_task.TaskHandler(
            name="pipe_mapping_disable_task")
        tracking_task =task_tracking_task.TaskHandler(
            name="tracking_task")
        waypoint_task =task_waypoint_task.TaskHandler(
            name="waypoint_task")
        reallocate_task =task_reallocate_task.TaskHandler(
            name="reallocate_task")
        dd_lec_task =task_dd_lec_task.TaskHandler(
            name="dd_lec_task")                           


        evaluate =py_trees.timers.Timer(
            "evaluate",
            duration=0.5)


        BlueROV.add_children([                
            topics2bb,                 
            dd_tasks,                 
            obstacle_avoidance,                 
            priorities])

        topics2bb.add_children([                
            battery2bb,                 
            rth2bb,                 
            geofence2bb,                 
            lec2_am_r_2bb,                 
            lec2_am_l_2bb,                 
            pipe_lost2bb,                 
            sensor_failure2bb,                 
            waypoints_completed2bb,                 
            mission2bb,                 
            ddlec2bb])                 
            # home2bb])


        dd_tasks.add_children([                
            reallocate_check,                 
            dd_lec_task])

        priorities.add_children([                
            battery_check,                 
            sensor_failure_selector,                 
            home_reached_selector,                 
            rth_selector,                 
            geofence_selector,                 
            pipe_lost_selector,                 
            track_pipe_mission,                 
            waypoint_mission,                 
            idle])

        battery_check.add_children([                
            battery_low_fs,                 
            surface_task])

        sensor_failure_selector.add_children([                
            check_sensor_failure,                 
            surface_task])

        reallocate_check.add_children([                
            is_reallocation_requested,                 
            reallocate_task])

        home_reached_selector.add_children([                
            check_surface,                 
            surface_task])

        rth_selector.add_children([                
            check_rth,                 
            rth_par])

        rth_par.add_children([                
            rth_task,                 
            home2bb])

        geofence_selector.add_children([                
            check_geofence,                 
            rth_par])

        pipe_lost_selector.add_children([                
            check_pipe_post,                 
            loiter_task])

        track_pipe_mission.add_children([                
            is_track_pipe_mission_requested,                 
            tracking,                 
            track_pipe_mission_end])

        tracking.add_children([                
            tracking_task,                 
            lec2am_speed_cmd,                 
            lec2am_mapping_cmd])

        lec2am_speed_cmd.add_children([                
            lec2am_l_speed_check,                 
            lec2am_r_speed_check,                 
            speed_max_task])

        lec2am_l_speed_check.add_children([                
            check_lec2am_ls,                 
            speed_min_task])

        lec2am_r_speed_check.add_children([                
            check_lec2am_rs,                 
            speed_min_task])

        lec2am_mapping_cmd.add_children([                
            lec2am_l_mapping_check,                 
            lec2am_r_mapping_check,                 
            pipe_mapping_enable_task])

        lec2am_l_mapping_check.add_children([                
            check_lec2am_lp,                 
            pipe_mapping_disable_task])

        lec2am_r_mapping_check.add_children([                
            check_lec2am_rp,                 
            pipe_mapping_disable_task])

        track_pipe_mission_end.add_children([                
            evaluate])

        waypoint_mission.add_children([                
            is_waypoint_requested,                 
            waypoint_selector])

        waypoint_selector.add_children([                
            waypoints_condition,                 
            waypoint_end])

        waypoints_condition.add_children([                
            waypoints_sif])

        waypoints_sif.add_children([                
            check_waypoints_completed,                 
            waypoint_task])

        waypoint_end.add_children([                
            loiter_task])

        return BlueROV


    def shutdown(self, behaviour_tree):
        behaviour_tree.interrupt()

##############################################################################
# Main
##############################################################################


if __name__=='__main__':
    rospy.init_node('BlueROV', log_level=rospy.INFO)
    try:
        node = BlueROV_BT()
        rospy.spin()
    except rospy.ROSInterruptException:
        print('caught exception')

    