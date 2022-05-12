#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/py_trees/devel/LICENSE
#

##############################################################################
# Imports
##############################################################################

#import functools
import py_trees
#import py_trees_ros
import py_trees.console as console
#import py_trees_msgs.msg as py_trees_msgs
#import rospy
import sys
import operator
import copy

  
import bb_hsd_pipe2bb  
import bb_hsd_surface2bb  
import bb_hsd_rth2bb  
import bb_hsd_wp2bb  
import bb_fls2bb  
import bb_fls_warning2bb  
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
import bb_rtreach2bb  
import task_emergency_stop_task  
import task_surface_task  
import task_rth_task  
import task_loiter_task  
import task_obstacle_avoidance  
import task_mission_server  
import task_next_mission  
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

def create_root():
    BlueROV = py_trees.composites.Parallel("BlueROV")
    topics2bb = py_trees.composites.Parallel("topics2bb")
    dd_tasks = py_trees.composites.Selector("dd_tasks")
    priorities = py_trees.composites.Selector("priorities")
    emergency_stop_tasks = py_trees.composites.Sequence("emergency_stop_tasks")
    rth_par = py_trees.composites.Parallel("rth_par")
    track_pipe_mission = py_trees.composites.Sequence("track_pipe_mission")
    tracking = py_trees.composites.Parallel("tracking")
    lec2am_speed_cmd = py_trees.composites.Selector("lec2am_speed_cmd")
    lec2am_mapping_cmd = py_trees.composites.Selector("lec2am_mapping_cmd")
    track_pipe_mission_end = py_trees.composites.Sequence("track_pipe_mission_end")
    waypoint_mission = py_trees.composites.Sequence("waypoint_mission")
    waypoint_selector = py_trees.composites.Selector("waypoint_selector")
    waypoint_end = py_trees.composites.Sequence("waypoint_end")

    reallocate_check = py_trees.composites.Selector(name="reallocate_check")
    reallocate_check_SIF = py_trees.decorators.SuccessIsFailure(reallocate_check, name="reallocate_check_SIF")
    battery_check = py_trees.composites.Selector(name="battery_check")
    battery_check_SIF = py_trees.decorators.SuccessIsFailure(battery_check, name="battery_check_SIF")
    sensor_failure_selector = py_trees.composites.Selector(name="sensor_failure_selector")
    sensor_failure_selector_SIF = py_trees.decorators.SuccessIsFailure(sensor_failure_selector, name="sensor_failure_selector_SIF")
    emergency_stop_check = py_trees.composites.Selector(name="emergency_stop_check")
    emergency_stop_check_SIF = py_trees.decorators.SuccessIsFailure(emergency_stop_check, name="emergency_stop_check_SIF")
    home_reached_selector = py_trees.composites.Selector(name="home_reached_selector")
    home_reached_selector_SIF = py_trees.decorators.SuccessIsFailure(home_reached_selector, name="home_reached_selector_SIF")
    obstacle_standoff_check = py_trees.composites.Selector(name="obstacle_standoff_check")
    obstacle_standoff_check_SIF = py_trees.decorators.SuccessIsFailure(obstacle_standoff_check, name="obstacle_standoff_check_SIF")
    rth_selector = py_trees.composites.Selector(name="rth_selector")
    rth_selector_SIF = py_trees.decorators.SuccessIsFailure(rth_selector, name="rth_selector_SIF")
    geofence_selector = py_trees.composites.Selector(name="geofence_selector")
    geofence_selector_SIF = py_trees.decorators.SuccessIsFailure(geofence_selector, name="geofence_selector_SIF")
    pipe_lost_selector = py_trees.composites.Selector(name="pipe_lost_selector")
    pipe_lost_selector_SIF = py_trees.decorators.SuccessIsFailure(pipe_lost_selector, name="pipe_lost_selector_SIF")
    lec2am_l_speed_check = py_trees.composites.Selector(name="lec2am_l_speed_check")
    lec2am_l_speed_check_SIF = py_trees.decorators.SuccessIsFailure(lec2am_l_speed_check, name="lec2am_l_speed_check_SIF")
    lec2am_r_speed_check = py_trees.composites.Selector(name="lec2am_r_speed_check")
    lec2am_r_speed_check_SIF = py_trees.decorators.SuccessIsFailure(lec2am_r_speed_check, name="lec2am_r_speed_check_SIF")
    lec2am_l_mapping_check = py_trees.composites.Selector(name="lec2am_l_mapping_check")
    lec2am_l_mapping_check_SIF = py_trees.decorators.SuccessIsFailure(lec2am_l_mapping_check, name="lec2am_l_mapping_check_SIF")
    lec2am_r_mapping_check = py_trees.composites.Selector(name="lec2am_r_mapping_check")
    lec2am_r_mapping_check_SIF = py_trees.decorators.SuccessIsFailure(lec2am_r_mapping_check, name="lec2am_r_mapping_check_SIF")
    waypoints_sif = py_trees.composites.Selector(name="waypoints_sif")
    waypoints_sif_SIF = py_trees.decorators.SuccessIsFailure(waypoints_sif, name="waypoints_sif_SIF")


    hsd_pipe2bb = bb_hsd_pipe2bb.ToBlackboard(
        name="hsd_pipe2bb",
        topic_name="/iver0/hsd_pipeline_mapping" 
    )
    hsd_surface2bb = bb_hsd_surface2bb.ToBlackboard(
        name="hsd_surface2bb",
        topic_name="/iver0/hsd_to_surface" 
    )
    hsd_rth2bb = bb_hsd_rth2bb.ToBlackboard(
        name="hsd_rth2bb",
        topic_name="/iver0/hsd_to_rth" 
    )
    hsd_wp2bb = bb_hsd_wp2bb.ToBlackboard(
        name="hsd_wp2bb",
        topic_name="/iver0/hsd_to_waypoint" 
    )
    fls2bb = bb_fls2bb.ToBlackboard(
        name="fls2bb",
        topic_name="/iver0/fls_echosunder" 
    )
    fls_warning2bb = bb_fls_warning2bb.ToBlackboard(
        name="fls_warning2bb",
        topic_name="/iver0/obstacle_in_view", 
        fls_in_view_window = None,  
        fls_in_view_limit = None 
    )
    battery2bb = bb_battery2bb.ToBlackboard(
        name="battery2bb",
        topic_name="/iver0/pixhawk_hw", 
        failsafe_battery_low_threshold = None 
    )
    ddlecam2bb = bb_ddlecam2bb.ToBlackboard(
        name="ddlecam2bb",
        topic_name="/lec_dd_am/p_value" 
    )
    rth2bb = bb_rth2bb.ToBlackboard(
        name="rth2bb",
        topic_name="/iver0/bb_rth", 
        failsafe_rth_enable = None 
    )
    geofence2bb = bb_geofence2bb.ToBlackboard(
        name="geofence2bb",
        topic_name="/iver0/bb_geofence" 
    )
    lec2_am_l_2bb = bb_lec2_am_l_2bb.ToBlackboard(
        name="lec2_am_l_2bb",
        topic_name="/lec2_am/left/p_value", 
        pipe_estimation_good_log_val = None,  
        speed_good_log_val = None 
    )
    lec2_am_r_2bb = bb_lec2_am_r_2bb.ToBlackboard(
        name="lec2_am_r_2bb",
        topic_name="/lec2_am/right/p_value", 
        pipe_estimation_good_log_val = None,  
        speed_good_log_val = None 
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
        home_reached_threshold = None 
    )
    mission2bb = bb_mission2bb.ToBlackboard(
        name="mission2bb",
        topic_name="/iver0/bb_mission" 
    )
    ddlec2bb = bb_ddlec2bb.ToBlackboard(
        name="ddlec2bb",
        topic_name="/iver0/degradation_detector", 
        total_degradation_threshold = None,  
        num_classes = None,  
        enable_fault_detection = None,  
        decision_source = None 
    )
    rtreach2bb = bb_rtreach2bb.ToBlackboard(
        name="rtreach2bb",
        topic_name="/reachability_result", 
        enable_emergency_stop = None 
    )

    emergency_stop_fs = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "emergency_stop_fs",
        check = py_trees.common.ComparisonExpression(
            variable = 'emergency_stop_warning',
            value = False,
            operator = operator.eq
        )
    )
    obstacle_standoff_fs = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "obstacle_standoff_fs",
        check = py_trees.common.ComparisonExpression(
            variable = 'obstacle_standoff_warning',
            value = False,
            operator = operator.eq
        )
    )
    is_reallocation_requested = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "is_reallocation_requested",
        check = py_trees.common.ComparisonExpression(
            variable = 'dd_xy_axis_degradation',
            value = False,
            operator = operator.eq
        )
    )
    check_dd_am = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_dd_am",
        check = py_trees.common.ComparisonExpression(
            variable = 'lec_dd_am_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_lec2am_ls = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_lec2am_ls",
        check = py_trees.common.ComparisonExpression(
            variable = 'lec2_am_l_speed_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_lec2am_rs = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_lec2am_rs",
        check = py_trees.common.ComparisonExpression(
            variable = 'lec2_am_r_speed_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_lec2am_lp = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_lec2am_lp",
        check = py_trees.common.ComparisonExpression(
            variable = 'lec2_am_l_pipe_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_lec2am_rp = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_lec2am_rp",
        check = py_trees.common.ComparisonExpression(
            variable = 'lec2_am_r_pipe_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_geofence = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_geofence",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_geofence_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_rth = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_rth",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_rth_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_surface = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_surface",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_home_reached',
            value = False,
            operator = operator.eq
        )
    )
    check_pipe_post = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_pipe_post",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_pipe_lost_warning',
            value = False,
            operator = operator.eq
        )
    )
    check_waypoints_completed = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_waypoints_completed",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_waypoints_completed.data',
            value = False,
            operator = operator.eq
        )
    )
    check_sensor_failure = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "check_sensor_failure",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_sensor_failure_warning',
            value = False,
            operator = operator.eq
        )
    )
    battery_low_fs = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "battery_low_fs",
        check = py_trees.common.ComparisonExpression(
            variable = 'battery_low_warning',
            value = False,
            operator = operator.eq
        )
    )
    is_track_pipe_mission_requested = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "is_track_pipe_mission_requested",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_mission.data',
            value =  'pipe_following' ,
            operator = operator.eq
        )
    )
    is_waypoint_requested = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "is_waypoint_requested",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_mission.data',
            value =  'waypoint_following' ,
            operator = operator.eq
        )
    )
    is_snr_requested = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "is_snr_requested",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_mission.data',
            value =  'fdr' ,
            operator = operator.eq
        )
    )
    is_loiter_requested = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "is_loiter_requested",
        check = py_trees.common.ComparisonExpression(
            variable = 'bb_mission.data',
            value =  'loitering' ,
            operator = operator.eq
        )
    )
    dd_z_axis = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "dd_z_axis",
        check = py_trees.common.ComparisonExpression(
            variable = 'dd_z_axis_warning',
            value = False,
            operator = operator.eq
        )
    )
    dd_xy_axis = py_trees.behaviours.CheckBlackboardVariableValue(
        name = "dd_xy_axis",
        check = py_trees.common.ComparisonExpression(
            variable = 'dd_xy_axis_degradation',
            value = False,
            operator = operator.eq
        )
    )


    success_node = py_trees.behaviours.Success(
        name="success_node")
    failure_node = py_trees.behaviours.Failure(
        name="failure_node")
    running_node = py_trees.behaviours.Running(
        name="running_node")
    idle = py_trees.behaviours.Running(
        name="idle")

    emergency_stop_task =task_emergency_stop_task.TaskHandler(
        name="emergency_stop_task") 
            
    surface_task =task_surface_task.TaskHandler(
        name="surface_task") 
            
    rth_task =task_rth_task.TaskHandler(
        name="rth_task") 
            
    loiter_task =task_loiter_task.TaskHandler(
        name="loiter_task") 
            
    obstacle_avoidance =task_obstacle_avoidance.TaskHandler(
        name="obstacle_avoidance", 
        enable_obstacle_avoidance = None) 
            
    mission_server =task_mission_server.TaskHandler(
        name="mission_server", 
        uuv_max_speed = None,  
        mission_file = None) 
            
    next_mission =task_next_mission.TaskHandler(
        name="next_mission") 
            
    speed_max_task =task_speed_max_task.TaskHandler(
        name="speed_max_task", 
        uuv_max_speed = None) 
            
    speed_min_task =task_speed_min_task.TaskHandler(
        name="speed_min_task", 
        uuv_min_speed = None) 
            
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
        name="dd_lec_task", 
        num_classes = None,  
        ann_input_len = None,  
        ddlec_am_path = None,  
        ddlec_am_params = None) 
            
                                    

    evaluate =py_trees.timers.Timer(
        "evaluate",
        duration=0.5)

    clone_storage = {}
    if topics2bb in clone_storage:
        new_clone=copy.copy(clone_storage[topics2bb])
        BlueROV.add_child(new_clone)
    else:
        clone_storage[topics2bb]=copy.copy(topics2bb)
        BlueROV.add_child(topics2bb)

    if dd_tasks in clone_storage:
        new_clone=copy.copy(clone_storage[dd_tasks])
        BlueROV.add_child(new_clone)
    else:
        clone_storage[dd_tasks]=copy.copy(dd_tasks)
        BlueROV.add_child(dd_tasks)

    if mission_server in clone_storage:
        new_clone=copy.copy(clone_storage[mission_server])
        BlueROV.add_child(new_clone)
    else:
        clone_storage[mission_server]=copy.copy(mission_server)
        BlueROV.add_child(mission_server)

    if obstacle_avoidance in clone_storage:
        new_clone=copy.copy(clone_storage[obstacle_avoidance])
        BlueROV.add_child(new_clone)
    else:
        clone_storage[obstacle_avoidance]=copy.copy(obstacle_avoidance)
        BlueROV.add_child(obstacle_avoidance)

    if priorities in clone_storage:
        new_clone=copy.copy(clone_storage[priorities])
        BlueROV.add_child(new_clone)
    else:
        clone_storage[priorities]=copy.copy(priorities)
        BlueROV.add_child(priorities)


    if battery2bb in clone_storage:
        new_clone=copy.copy(clone_storage[battery2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[battery2bb]=copy.copy(battery2bb)
        topics2bb.add_child(battery2bb)

    if rth2bb in clone_storage:
        new_clone=copy.copy(clone_storage[rth2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[rth2bb]=copy.copy(rth2bb)
        topics2bb.add_child(rth2bb)

    if geofence2bb in clone_storage:
        new_clone=copy.copy(clone_storage[geofence2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[geofence2bb]=copy.copy(geofence2bb)
        topics2bb.add_child(geofence2bb)

    if lec2_am_r_2bb in clone_storage:
        new_clone=copy.copy(clone_storage[lec2_am_r_2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[lec2_am_r_2bb]=copy.copy(lec2_am_r_2bb)
        topics2bb.add_child(lec2_am_r_2bb)

    if lec2_am_l_2bb in clone_storage:
        new_clone=copy.copy(clone_storage[lec2_am_l_2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[lec2_am_l_2bb]=copy.copy(lec2_am_l_2bb)
        topics2bb.add_child(lec2_am_l_2bb)

    if pipe_lost2bb in clone_storage:
        new_clone=copy.copy(clone_storage[pipe_lost2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[pipe_lost2bb]=copy.copy(pipe_lost2bb)
        topics2bb.add_child(pipe_lost2bb)

    if sensor_failure2bb in clone_storage:
        new_clone=copy.copy(clone_storage[sensor_failure2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[sensor_failure2bb]=copy.copy(sensor_failure2bb)
        topics2bb.add_child(sensor_failure2bb)

    if waypoints_completed2bb in clone_storage:
        new_clone=copy.copy(clone_storage[waypoints_completed2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[waypoints_completed2bb]=copy.copy(waypoints_completed2bb)
        topics2bb.add_child(waypoints_completed2bb)

    if mission2bb in clone_storage:
        new_clone=copy.copy(clone_storage[mission2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[mission2bb]=copy.copy(mission2bb)
        topics2bb.add_child(mission2bb)

    if ddlec2bb in clone_storage:
        new_clone=copy.copy(clone_storage[ddlec2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[ddlec2bb]=copy.copy(ddlec2bb)
        topics2bb.add_child(ddlec2bb)

    if fls2bb in clone_storage:
        new_clone=copy.copy(clone_storage[fls2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[fls2bb]=copy.copy(fls2bb)
        topics2bb.add_child(fls2bb)

    if fls_warning2bb in clone_storage:
        new_clone=copy.copy(clone_storage[fls_warning2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[fls_warning2bb]=copy.copy(fls_warning2bb)
        topics2bb.add_child(fls_warning2bb)

    if hsd_pipe2bb in clone_storage:
        new_clone=copy.copy(clone_storage[hsd_pipe2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[hsd_pipe2bb]=copy.copy(hsd_pipe2bb)
        topics2bb.add_child(hsd_pipe2bb)

    if hsd_wp2bb in clone_storage:
        new_clone=copy.copy(clone_storage[hsd_wp2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[hsd_wp2bb]=copy.copy(hsd_wp2bb)
        topics2bb.add_child(hsd_wp2bb)

    if hsd_rth2bb in clone_storage:
        new_clone=copy.copy(clone_storage[hsd_rth2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[hsd_rth2bb]=copy.copy(hsd_rth2bb)
        topics2bb.add_child(hsd_rth2bb)

    if hsd_surface2bb in clone_storage:
        new_clone=copy.copy(clone_storage[hsd_surface2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[hsd_surface2bb]=copy.copy(hsd_surface2bb)
        topics2bb.add_child(hsd_surface2bb)

    if rtreach2bb in clone_storage:
        new_clone=copy.copy(clone_storage[rtreach2bb])
        topics2bb.add_child(new_clone)
    else:
        clone_storage[rtreach2bb]=copy.copy(rtreach2bb)
        topics2bb.add_child(rtreach2bb)


    if reallocate_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[reallocate_check_SIF])
        dd_tasks.add_child(new_clone)
    else:
        clone_storage[reallocate_check_SIF]=copy.copy(reallocate_check_SIF)
        dd_tasks.add_child(reallocate_check_SIF)

    if dd_lec_task in clone_storage:
        new_clone=copy.copy(clone_storage[dd_lec_task])
        dd_tasks.add_child(new_clone)
    else:
        clone_storage[dd_lec_task]=copy.copy(dd_lec_task)
        dd_tasks.add_child(dd_lec_task)


    if is_reallocation_requested in clone_storage:
        new_clone=copy.copy(clone_storage[is_reallocation_requested])
        reallocate_check.add_child(new_clone)
    else:
        clone_storage[is_reallocation_requested]=copy.copy(is_reallocation_requested)
        reallocate_check.add_child(is_reallocation_requested)

    if reallocate_task in clone_storage:
        new_clone=copy.copy(clone_storage[reallocate_task])
        reallocate_check.add_child(new_clone)
    else:
        clone_storage[reallocate_task]=copy.copy(reallocate_task)
        reallocate_check.add_child(reallocate_task)


    if battery_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[battery_check_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[battery_check_SIF]=copy.copy(battery_check_SIF)
        priorities.add_child(battery_check_SIF)

    if sensor_failure_selector_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[sensor_failure_selector_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[sensor_failure_selector_SIF]=copy.copy(sensor_failure_selector_SIF)
        priorities.add_child(sensor_failure_selector_SIF)

    if emergency_stop_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[emergency_stop_check_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[emergency_stop_check_SIF]=copy.copy(emergency_stop_check_SIF)
        priorities.add_child(emergency_stop_check_SIF)

    if home_reached_selector_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[home_reached_selector_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[home_reached_selector_SIF]=copy.copy(home_reached_selector_SIF)
        priorities.add_child(home_reached_selector_SIF)

    if obstacle_standoff_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[obstacle_standoff_check_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[obstacle_standoff_check_SIF]=copy.copy(obstacle_standoff_check_SIF)
        priorities.add_child(obstacle_standoff_check_SIF)

    if rth_selector_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[rth_selector_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[rth_selector_SIF]=copy.copy(rth_selector_SIF)
        priorities.add_child(rth_selector_SIF)

    if geofence_selector_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[geofence_selector_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[geofence_selector_SIF]=copy.copy(geofence_selector_SIF)
        priorities.add_child(geofence_selector_SIF)

    if pipe_lost_selector_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[pipe_lost_selector_SIF])
        priorities.add_child(new_clone)
    else:
        clone_storage[pipe_lost_selector_SIF]=copy.copy(pipe_lost_selector_SIF)
        priorities.add_child(pipe_lost_selector_SIF)

    if track_pipe_mission in clone_storage:
        new_clone=copy.copy(clone_storage[track_pipe_mission])
        priorities.add_child(new_clone)
    else:
        clone_storage[track_pipe_mission]=copy.copy(track_pipe_mission)
        priorities.add_child(track_pipe_mission)

    if waypoint_mission in clone_storage:
        new_clone=copy.copy(clone_storage[waypoint_mission])
        priorities.add_child(new_clone)
    else:
        clone_storage[waypoint_mission]=copy.copy(waypoint_mission)
        priorities.add_child(waypoint_mission)

    if loiter_task in clone_storage:
        new_clone=copy.copy(clone_storage[loiter_task])
        priorities.add_child(new_clone)
    else:
        clone_storage[loiter_task]=copy.copy(loiter_task)
        priorities.add_child(loiter_task)


    if battery_low_fs in clone_storage:
        new_clone=copy.copy(clone_storage[battery_low_fs])
        battery_check.add_child(new_clone)
    else:
        clone_storage[battery_low_fs]=copy.copy(battery_low_fs)
        battery_check.add_child(battery_low_fs)

    if surface_task in clone_storage:
        new_clone=copy.copy(clone_storage[surface_task])
        battery_check.add_child(new_clone)
    else:
        clone_storage[surface_task]=copy.copy(surface_task)
        battery_check.add_child(surface_task)


    if check_sensor_failure in clone_storage:
        new_clone=copy.copy(clone_storage[check_sensor_failure])
        sensor_failure_selector.add_child(new_clone)
    else:
        clone_storage[check_sensor_failure]=copy.copy(check_sensor_failure)
        sensor_failure_selector.add_child(check_sensor_failure)

    if surface_task in clone_storage:
        new_clone=copy.copy(clone_storage[surface_task])
        sensor_failure_selector.add_child(new_clone)
    else:
        clone_storage[surface_task]=copy.copy(surface_task)
        sensor_failure_selector.add_child(surface_task)


    if emergency_stop_fs in clone_storage:
        new_clone=copy.copy(clone_storage[emergency_stop_fs])
        emergency_stop_check.add_child(new_clone)
    else:
        clone_storage[emergency_stop_fs]=copy.copy(emergency_stop_fs)
        emergency_stop_check.add_child(emergency_stop_fs)

    if emergency_stop_tasks in clone_storage:
        new_clone=copy.copy(clone_storage[emergency_stop_tasks])
        emergency_stop_check.add_child(new_clone)
    else:
        clone_storage[emergency_stop_tasks]=copy.copy(emergency_stop_tasks)
        emergency_stop_check.add_child(emergency_stop_tasks)


    if emergency_stop_task in clone_storage:
        new_clone=copy.copy(clone_storage[emergency_stop_task])
        emergency_stop_tasks.add_child(new_clone)
    else:
        clone_storage[emergency_stop_task]=copy.copy(emergency_stop_task)
        emergency_stop_tasks.add_child(emergency_stop_task)

    if surface_task in clone_storage:
        new_clone=copy.copy(clone_storage[surface_task])
        emergency_stop_tasks.add_child(new_clone)
    else:
        clone_storage[surface_task]=copy.copy(surface_task)
        emergency_stop_tasks.add_child(surface_task)


    if check_surface in clone_storage:
        new_clone=copy.copy(clone_storage[check_surface])
        home_reached_selector.add_child(new_clone)
    else:
        clone_storage[check_surface]=copy.copy(check_surface)
        home_reached_selector.add_child(check_surface)

    if surface_task in clone_storage:
        new_clone=copy.copy(clone_storage[surface_task])
        home_reached_selector.add_child(new_clone)
    else:
        clone_storage[surface_task]=copy.copy(surface_task)
        home_reached_selector.add_child(surface_task)


    if obstacle_standoff_fs in clone_storage:
        new_clone=copy.copy(clone_storage[obstacle_standoff_fs])
        obstacle_standoff_check.add_child(new_clone)
    else:
        clone_storage[obstacle_standoff_fs]=copy.copy(obstacle_standoff_fs)
        obstacle_standoff_check.add_child(obstacle_standoff_fs)

    if surface_task in clone_storage:
        new_clone=copy.copy(clone_storage[surface_task])
        obstacle_standoff_check.add_child(new_clone)
    else:
        clone_storage[surface_task]=copy.copy(surface_task)
        obstacle_standoff_check.add_child(surface_task)


    if check_rth in clone_storage:
        new_clone=copy.copy(clone_storage[check_rth])
        rth_selector.add_child(new_clone)
    else:
        clone_storage[check_rth]=copy.copy(check_rth)
        rth_selector.add_child(check_rth)

    if rth_par in clone_storage:
        new_clone=copy.copy(clone_storage[rth_par])
        rth_selector.add_child(new_clone)
    else:
        clone_storage[rth_par]=copy.copy(rth_par)
        rth_selector.add_child(rth_par)


    if rth_task in clone_storage:
        new_clone=copy.copy(clone_storage[rth_task])
        rth_par.add_child(new_clone)
    else:
        clone_storage[rth_task]=copy.copy(rth_task)
        rth_par.add_child(rth_task)

    if home2bb in clone_storage:
        new_clone=copy.copy(clone_storage[home2bb])
        rth_par.add_child(new_clone)
    else:
        clone_storage[home2bb]=copy.copy(home2bb)
        rth_par.add_child(home2bb)


    if check_geofence in clone_storage:
        new_clone=copy.copy(clone_storage[check_geofence])
        geofence_selector.add_child(new_clone)
    else:
        clone_storage[check_geofence]=copy.copy(check_geofence)
        geofence_selector.add_child(check_geofence)

    if rth_par in clone_storage:
        new_clone=copy.copy(clone_storage[rth_par])
        geofence_selector.add_child(new_clone)
    else:
        clone_storage[rth_par]=copy.copy(rth_par)
        geofence_selector.add_child(rth_par)


    if check_pipe_post in clone_storage:
        new_clone=copy.copy(clone_storage[check_pipe_post])
        pipe_lost_selector.add_child(new_clone)
    else:
        clone_storage[check_pipe_post]=copy.copy(check_pipe_post)
        pipe_lost_selector.add_child(check_pipe_post)

    if loiter_task in clone_storage:
        new_clone=copy.copy(clone_storage[loiter_task])
        pipe_lost_selector.add_child(new_clone)
    else:
        clone_storage[loiter_task]=copy.copy(loiter_task)
        pipe_lost_selector.add_child(loiter_task)


    if is_track_pipe_mission_requested in clone_storage:
        new_clone=copy.copy(clone_storage[is_track_pipe_mission_requested])
        track_pipe_mission.add_child(new_clone)
    else:
        clone_storage[is_track_pipe_mission_requested]=copy.copy(is_track_pipe_mission_requested)
        track_pipe_mission.add_child(is_track_pipe_mission_requested)

    if tracking in clone_storage:
        new_clone=copy.copy(clone_storage[tracking])
        track_pipe_mission.add_child(new_clone)
    else:
        clone_storage[tracking]=copy.copy(tracking)
        track_pipe_mission.add_child(tracking)

    if track_pipe_mission_end in clone_storage:
        new_clone=copy.copy(clone_storage[track_pipe_mission_end])
        track_pipe_mission.add_child(new_clone)
    else:
        clone_storage[track_pipe_mission_end]=copy.copy(track_pipe_mission_end)
        track_pipe_mission.add_child(track_pipe_mission_end)


    if tracking_task in clone_storage:
        new_clone=copy.copy(clone_storage[tracking_task])
        tracking.add_child(new_clone)
    else:
        clone_storage[tracking_task]=copy.copy(tracking_task)
        tracking.add_child(tracking_task)

    if lec2am_speed_cmd in clone_storage:
        new_clone=copy.copy(clone_storage[lec2am_speed_cmd])
        tracking.add_child(new_clone)
    else:
        clone_storage[lec2am_speed_cmd]=copy.copy(lec2am_speed_cmd)
        tracking.add_child(lec2am_speed_cmd)

    if lec2am_mapping_cmd in clone_storage:
        new_clone=copy.copy(clone_storage[lec2am_mapping_cmd])
        tracking.add_child(new_clone)
    else:
        clone_storage[lec2am_mapping_cmd]=copy.copy(lec2am_mapping_cmd)
        tracking.add_child(lec2am_mapping_cmd)


    if lec2am_l_speed_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[lec2am_l_speed_check_SIF])
        lec2am_speed_cmd.add_child(new_clone)
    else:
        clone_storage[lec2am_l_speed_check_SIF]=copy.copy(lec2am_l_speed_check_SIF)
        lec2am_speed_cmd.add_child(lec2am_l_speed_check_SIF)

    if lec2am_r_speed_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[lec2am_r_speed_check_SIF])
        lec2am_speed_cmd.add_child(new_clone)
    else:
        clone_storage[lec2am_r_speed_check_SIF]=copy.copy(lec2am_r_speed_check_SIF)
        lec2am_speed_cmd.add_child(lec2am_r_speed_check_SIF)

    if speed_max_task in clone_storage:
        new_clone=copy.copy(clone_storage[speed_max_task])
        lec2am_speed_cmd.add_child(new_clone)
    else:
        clone_storage[speed_max_task]=copy.copy(speed_max_task)
        lec2am_speed_cmd.add_child(speed_max_task)


    if check_lec2am_ls in clone_storage:
        new_clone=copy.copy(clone_storage[check_lec2am_ls])
        lec2am_l_speed_check.add_child(new_clone)
    else:
        clone_storage[check_lec2am_ls]=copy.copy(check_lec2am_ls)
        lec2am_l_speed_check.add_child(check_lec2am_ls)

    if speed_min_task in clone_storage:
        new_clone=copy.copy(clone_storage[speed_min_task])
        lec2am_l_speed_check.add_child(new_clone)
    else:
        clone_storage[speed_min_task]=copy.copy(speed_min_task)
        lec2am_l_speed_check.add_child(speed_min_task)


    if check_lec2am_rs in clone_storage:
        new_clone=copy.copy(clone_storage[check_lec2am_rs])
        lec2am_r_speed_check.add_child(new_clone)
    else:
        clone_storage[check_lec2am_rs]=copy.copy(check_lec2am_rs)
        lec2am_r_speed_check.add_child(check_lec2am_rs)

    if speed_min_task in clone_storage:
        new_clone=copy.copy(clone_storage[speed_min_task])
        lec2am_r_speed_check.add_child(new_clone)
    else:
        clone_storage[speed_min_task]=copy.copy(speed_min_task)
        lec2am_r_speed_check.add_child(speed_min_task)


    if lec2am_l_mapping_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[lec2am_l_mapping_check_SIF])
        lec2am_mapping_cmd.add_child(new_clone)
    else:
        clone_storage[lec2am_l_mapping_check_SIF]=copy.copy(lec2am_l_mapping_check_SIF)
        lec2am_mapping_cmd.add_child(lec2am_l_mapping_check_SIF)

    if lec2am_r_mapping_check_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[lec2am_r_mapping_check_SIF])
        lec2am_mapping_cmd.add_child(new_clone)
    else:
        clone_storage[lec2am_r_mapping_check_SIF]=copy.copy(lec2am_r_mapping_check_SIF)
        lec2am_mapping_cmd.add_child(lec2am_r_mapping_check_SIF)

    if pipe_mapping_enable_task in clone_storage:
        new_clone=copy.copy(clone_storage[pipe_mapping_enable_task])
        lec2am_mapping_cmd.add_child(new_clone)
    else:
        clone_storage[pipe_mapping_enable_task]=copy.copy(pipe_mapping_enable_task)
        lec2am_mapping_cmd.add_child(pipe_mapping_enable_task)


    if check_lec2am_lp in clone_storage:
        new_clone=copy.copy(clone_storage[check_lec2am_lp])
        lec2am_l_mapping_check.add_child(new_clone)
    else:
        clone_storage[check_lec2am_lp]=copy.copy(check_lec2am_lp)
        lec2am_l_mapping_check.add_child(check_lec2am_lp)

    if pipe_mapping_disable_task in clone_storage:
        new_clone=copy.copy(clone_storage[pipe_mapping_disable_task])
        lec2am_l_mapping_check.add_child(new_clone)
    else:
        clone_storage[pipe_mapping_disable_task]=copy.copy(pipe_mapping_disable_task)
        lec2am_l_mapping_check.add_child(pipe_mapping_disable_task)


    if check_lec2am_rp in clone_storage:
        new_clone=copy.copy(clone_storage[check_lec2am_rp])
        lec2am_r_mapping_check.add_child(new_clone)
    else:
        clone_storage[check_lec2am_rp]=copy.copy(check_lec2am_rp)
        lec2am_r_mapping_check.add_child(check_lec2am_rp)

    if pipe_mapping_disable_task in clone_storage:
        new_clone=copy.copy(clone_storage[pipe_mapping_disable_task])
        lec2am_r_mapping_check.add_child(new_clone)
    else:
        clone_storage[pipe_mapping_disable_task]=copy.copy(pipe_mapping_disable_task)
        lec2am_r_mapping_check.add_child(pipe_mapping_disable_task)


    if evaluate in clone_storage:
        new_clone=copy.copy(clone_storage[evaluate])
        track_pipe_mission_end.add_child(new_clone)
    else:
        clone_storage[evaluate]=copy.copy(evaluate)
        track_pipe_mission_end.add_child(evaluate)


    if is_waypoint_requested in clone_storage:
        new_clone=copy.copy(clone_storage[is_waypoint_requested])
        waypoint_mission.add_child(new_clone)
    else:
        clone_storage[is_waypoint_requested]=copy.copy(is_waypoint_requested)
        waypoint_mission.add_child(is_waypoint_requested)

    if waypoint_selector in clone_storage:
        new_clone=copy.copy(clone_storage[waypoint_selector])
        waypoint_mission.add_child(new_clone)
    else:
        clone_storage[waypoint_selector]=copy.copy(waypoint_selector)
        waypoint_mission.add_child(waypoint_selector)


    if waypoints_sif_SIF in clone_storage:
        new_clone=copy.copy(clone_storage[waypoints_sif_SIF])
        waypoint_selector.add_child(new_clone)
    else:
        clone_storage[waypoints_sif_SIF]=copy.copy(waypoints_sif_SIF)
        waypoint_selector.add_child(waypoints_sif_SIF)

    if waypoint_task in clone_storage:
        new_clone=copy.copy(clone_storage[waypoint_task])
        waypoint_selector.add_child(new_clone)
    else:
        clone_storage[waypoint_task]=copy.copy(waypoint_task)
        waypoint_selector.add_child(waypoint_task)


    if check_waypoints_completed in clone_storage:
        new_clone=copy.copy(clone_storage[check_waypoints_completed])
        waypoints_sif.add_child(new_clone)
    else:
        clone_storage[check_waypoints_completed]=copy.copy(check_waypoints_completed)
        waypoints_sif.add_child(check_waypoints_completed)

    if waypoint_end in clone_storage:
        new_clone=copy.copy(clone_storage[waypoint_end])
        waypoints_sif.add_child(new_clone)
    else:
        clone_storage[waypoint_end]=copy.copy(waypoint_end)
        waypoints_sif.add_child(waypoint_end)


    if next_mission in clone_storage:
        new_clone=copy.copy(clone_storage[next_mission])
        waypoint_end.add_child(new_clone)
    else:
        clone_storage[next_mission]=copy.copy(next_mission)
        waypoint_end.add_child(next_mission)

    if loiter_task in clone_storage:
        new_clone=copy.copy(clone_storage[loiter_task])
        waypoint_end.add_child(new_clone)
    else:
        clone_storage[loiter_task]=copy.copy(loiter_task)
        waypoint_end.add_child(loiter_task)



#
#    BlueROV.add_children([
#        
#        topics2bb, 

#        
#        dd_tasks, 

#        
#        mission_server, 

#        
#        obstacle_avoidance, 

#        
#        priorities])

#
#
#    topics2bb.add_children([
#        
#        battery2bb, 

#        
#        rth2bb, 

#        
#        geofence2bb, 

#        
#        lec2_am_r_2bb, 

#        
#        lec2_am_l_2bb, 

#        
#        pipe_lost2bb, 

#        
#        sensor_failure2bb, 

#        
#        waypoints_completed2bb, 

#        
#        mission2bb, 

#        
#        ddlec2bb, 

#        
#        fls2bb, 

#        
#        fls_warning2bb, 

#        
#        hsd_pipe2bb, 

#        
#        hsd_wp2bb, 

#        
#        hsd_rth2bb, 

#        
#        hsd_surface2bb, 

#        
#        rtreach2bb])

#
#
#    dd_tasks.add_children([
#        
#        reallocate_check_SIF, 

#        
#        dd_lec_task])

#
#
#    reallocate_check.add_children([
#        
#        is_reallocation_requested, 

#        
#        reallocate_task])

#
#
#    priorities.add_children([
#        
#        battery_check_SIF, 

#        
#        sensor_failure_selector_SIF, 

#        
#        emergency_stop_check_SIF, 

#        
#        home_reached_selector_SIF, 

#        
#        obstacle_standoff_check_SIF, 

#        
#        rth_selector_SIF, 

#        
#        geofence_selector_SIF, 

#        
#        pipe_lost_selector_SIF, 

#        
#        track_pipe_mission, 

#        
#        waypoint_mission, 

#        
#        loiter_task])

#
#
#    battery_check.add_children([
#        
#        battery_low_fs, 

#        
#        surface_task])

#
#
#    sensor_failure_selector.add_children([
#        
#        check_sensor_failure, 

#        
#        surface_task])

#
#
#    emergency_stop_check.add_children([
#        
#        emergency_stop_fs, 

#        
#        emergency_stop_tasks])

#
#
#    emergency_stop_tasks.add_children([
#        
#        emergency_stop_task, 

#        
#        surface_task])

#
#
#    home_reached_selector.add_children([
#        
#        check_surface, 

#        
#        surface_task])

#
#
#    obstacle_standoff_check.add_children([
#        
#        obstacle_standoff_fs, 

#        
#        surface_task])

#
#
#    rth_selector.add_children([
#        
#        check_rth, 

#        
#        rth_par])

#
#
#    rth_par.add_children([
#        
#        rth_task, 

#        
#        home2bb])

#
#
#    geofence_selector.add_children([
#        
#        check_geofence, 

#        
#        rth_par])

#
#
#    pipe_lost_selector.add_children([
#        
#        check_pipe_post, 

#        
#        loiter_task])

#
#
#    track_pipe_mission.add_children([
#        
#        is_track_pipe_mission_requested, 

#        
#        tracking, 

#        
#        track_pipe_mission_end])

#
#
#    tracking.add_children([
#        
#        tracking_task, 

#        
#        lec2am_speed_cmd, 

#        
#        lec2am_mapping_cmd])

#
#
#    lec2am_speed_cmd.add_children([
#        
#        lec2am_l_speed_check_SIF, 

#        
#        lec2am_r_speed_check_SIF, 

#        
#        speed_max_task])

#
#
#    lec2am_l_speed_check.add_children([
#        
#        check_lec2am_ls, 

#        
#        speed_min_task])

#
#
#    lec2am_r_speed_check.add_children([
#        
#        check_lec2am_rs, 

#        
#        speed_min_task])

#
#
#    lec2am_mapping_cmd.add_children([
#        
#        lec2am_l_mapping_check_SIF, 

#        
#        lec2am_r_mapping_check_SIF, 

#        
#        pipe_mapping_enable_task])

#
#
#    lec2am_l_mapping_check.add_children([
#        
#        check_lec2am_lp, 

#        
#        pipe_mapping_disable_task])

#
#
#    lec2am_r_mapping_check.add_children([
#        
#        check_lec2am_rp, 

#        
#        pipe_mapping_disable_task])

#
#
#    track_pipe_mission_end.add_children([
#        
#        evaluate])

#
#
#    waypoint_mission.add_children([
#        
#        is_waypoint_requested, 

#        
#        waypoint_selector])

#
#
#    waypoint_selector.add_children([
#        
#        waypoints_sif_SIF, 

#        
#        waypoint_task])

#
#
#    waypoints_sif.add_children([
#        
#        check_waypoints_completed, 

#        
#        waypoint_end])

#
#
#    waypoint_end.add_children([
#        
#        next_mission, 

#        
#        loiter_task])

#
#
    return BlueROV

    