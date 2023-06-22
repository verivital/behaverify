import emergency_stop_fs_file
import obstacle_standoff_fs_file
import is_reallocation_requested_file
import check_dd_am_file
import check_lec2am_ls_file
import check_lec2am_rs_file
import check_lec2am_lp_file
import check_lec2am_rp_file
import check_geofence_file
import check_rth_file
import check_surface_file
import check_pipe_lost_file
import check_sensor_failure_file
import battery_low_fs_file
import is_track_pipe_mission_requested_file
import is_waypoint_requested_file
import is_snr_requested_file
import is_loiter_requested_file
import dd_z_axis_file
import dd_xy_axis_file
import rtreach_check_file
import rtreach_obstacle_check_file
import rtreach_long_term_check_file
import obstacle_avoidance_required_file
import fls2bb_file
import fls_warning2bb_file
import battery2bb_file
import ddlecam2bb_file
import rth2bb_file
import geofence2bb_file
import lec2_am_l_2bb_file
import lec2_am_r_2bb_file
import pipe_lost2bb_file
import sensor_failure2bb_file
import waypoints_completed2bb_file
import home2bb_file
import rtreach2bb_file
import emergency_stop_task_file
import surface_task_file
import rth_task_file
import loiter_task_file
import obstacle_avoidance_file
import mission_server_file
import next_mission_node_file
import speed_max_task_file
import speed_min_task_file
import pipe_mapping_enable_task_file
import pipe_mapping_disable_task_file
import tracking_task_file
import waypoint_task_file
import reallocate_task_file
import dd_lec_task_file
import publish_HSD_command_file
import failure_node_file
import check_waypoints_completed_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'battery_low_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_fls_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_geofence_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_home_reached', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_mission', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_obstacle_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_pipe_lost_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_pipe_mapping_enable', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_rth_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'bb_sensor_failure_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'cm_hsd_input', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dd_xy_axis_degradation', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dd_z_axis_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'emergency_stop_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'HSD_out', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'lec_dd_am_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'lec2_am_l_speed_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'lec2_am_l_pipe_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'lec2_am_r_speed_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'lec2_am_r_pipe_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'next_mission', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'pipe_mapping_enable', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'obstacle_standoff_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'rtreach_long_term_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'rtreach_obstacle_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'rtreach_warning', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'finished_missions', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dd_output', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'BLUEROV_SURFACED', access = py_trees.common.Access.WRITE)
    blackboard_reader.battery_low_warning = serene_safe_assignment.battery_low_warning(False)
    blackboard_reader.bb_fls_warning = serene_safe_assignment.bb_fls_warning(False)
    blackboard_reader.bb_geofence_warning = serene_safe_assignment.bb_geofence_warning(False)
    blackboard_reader.bb_home_reached = serene_safe_assignment.bb_home_reached(False)
    blackboard_reader.bb_mission = serene_safe_assignment.bb_mission('waypoint_following')
    blackboard_reader.bb_obstacle_warning = serene_safe_assignment.bb_obstacle_warning(False)
    blackboard_reader.bb_pipe_lost_warning = serene_safe_assignment.bb_pipe_lost_warning(False)
    blackboard_reader.bb_pipe_mapping_enable = serene_safe_assignment.bb_pipe_mapping_enable(False)
    blackboard_reader.bb_rth_warning = serene_safe_assignment.bb_rth_warning(False)
    blackboard_reader.bb_sensor_failure_warning = serene_safe_assignment.bb_sensor_failure_warning(False)
    blackboard_reader.cm_hsd_input = serene_safe_assignment.cm_hsd_input('cm_loiter_task')
    blackboard_reader.dd_xy_axis_degradation = serene_safe_assignment.dd_xy_axis_degradation(False)
    blackboard_reader.dd_z_axis_warning = serene_safe_assignment.dd_z_axis_warning(False)
    blackboard_reader.emergency_stop_warning = serene_safe_assignment.emergency_stop_warning(False)
    blackboard_reader.HSD_out = serene_safe_assignment.HSD_out('uuv_max_speed')
    blackboard_reader.lec_dd_am_warning = serene_safe_assignment.lec_dd_am_warning(False)
    blackboard_reader.lec2_am_l_speed_warning = serene_safe_assignment.lec2_am_l_speed_warning(False)
    blackboard_reader.lec2_am_l_pipe_warning = serene_safe_assignment.lec2_am_l_pipe_warning(False)
    blackboard_reader.lec2_am_r_speed_warning = serene_safe_assignment.lec2_am_r_speed_warning(False)
    blackboard_reader.lec2_am_r_pipe_warning = serene_safe_assignment.lec2_am_r_pipe_warning(False)
    blackboard_reader.next_mission = serene_safe_assignment.next_mission(False)
    blackboard_reader.pipe_mapping_enable = serene_safe_assignment.pipe_mapping_enable(False)
    blackboard_reader.obstacle_standoff_warning = serene_safe_assignment.obstacle_standoff_warning(False)
    blackboard_reader.rtreach_long_term_warning = serene_safe_assignment.rtreach_long_term_warning(False)
    blackboard_reader.rtreach_obstacle_warning = serene_safe_assignment.rtreach_obstacle_warning(False)
    blackboard_reader.rtreach_warning = serene_safe_assignment.rtreach_warning(False)
    blackboard_reader.finished_missions = serene_safe_assignment.finished_missions(False)
    blackboard_reader.dd_output = serene_safe_assignment.dd_output('safe')
    blackboard_reader.BLUEROV_SURFACED = serene_safe_assignment.BLUEROV_SURFACED(False)
    return blackboard_reader


def create_tree(environment):
    battery2bb = battery2bb_file.battery2bb('battery2bb', environment)
    rth2bb = rth2bb_file.rth2bb('rth2bb', environment)
    geofence2bb = geofence2bb_file.geofence2bb('geofence2bb', environment)
    lec2_am_r_2bb = lec2_am_r_2bb_file.lec2_am_r_2bb('lec2_am_r_2bb', environment)
    lec2_am_l_2bb = lec2_am_l_2bb_file.lec2_am_l_2bb('lec2_am_l_2bb', environment)
    pipe_lost2bb = pipe_lost2bb_file.pipe_lost2bb('pipe_lost2bb', environment)
    sensor_failure2bb = sensor_failure2bb_file.sensor_failure2bb('sensor_failure2bb', environment)
    waypoints_completed2bb = waypoints_completed2bb_file.waypoints_completed2bb('waypoints_completed2bb', environment)
    fls2bb = fls2bb_file.fls2bb('fls2bb', environment)
    fls_warning2bb = fls_warning2bb_file.fls_warning2bb('fls_warning2bb', environment)
    rtreach2bb = rtreach2bb_file.rtreach2bb('rtreach2bb', environment)
    home2bb = home2bb_file.home2bb('home2bb', environment)
    topics2bb = py_trees.composites.Parallel(name = 'topics2bb', policy = py_trees.common.ParallelPolicy.SuccessOnAll(False), children = [battery2bb, rth2bb, geofence2bb, lec2_am_r_2bb, lec2_am_l_2bb, pipe_lost2bb, sensor_failure2bb, waypoints_completed2bb, fls2bb, fls_warning2bb, rtreach2bb, home2bb])
    dd_lec_task = dd_lec_task_file.dd_lec_task('dd_lec_task', environment)
    is_reallocation_requested = is_reallocation_requested_file.is_reallocation_requested('is_reallocation_requested')
    reallocate_task = reallocate_task_file.reallocate_task('reallocate_task', environment)
    emergency_stop_check = py_trees.composites.Selector(name = 'emergency_stop_check', memory = False, children = [is_reallocation_requested, reallocate_task])
    emergency_stop_check_SIF = py_trees.decorators.SuccessIsFailure(name = 'emergency_stop_check_SIF', child = emergency_stop_check)
    dd_tasks = py_trees.composites.Selector(name = 'dd_tasks', memory = False, children = [dd_lec_task, emergency_stop_check_SIF])
    is_waypoint_requested = is_waypoint_requested_file.is_waypoint_requested('is_waypoint_requested')
    check_waypoints_completed = check_waypoints_completed_file.check_waypoints_completed('check_waypoints_completed', environment)
    waypoint_mission_end = py_trees.composites.Sequence(name = 'waypoint_mission_end', memory = False, children = [is_waypoint_requested, check_waypoints_completed])
    is_track_pipe_mission_requested = is_track_pipe_mission_requested_file.is_track_pipe_mission_requested('is_track_pipe_mission_requested')
    failure_node = failure_node_file.failure_node('failure_node', environment)
    pipe_tracking_misison_end = py_trees.composites.Sequence(name = 'pipe_tracking_misison_end', memory = False, children = [is_track_pipe_mission_requested, failure_node])
    confirm_mission_ended = py_trees.composites.Selector(name = 'confirm_mission_ended', memory = False, children = [waypoint_mission_end, pipe_tracking_misison_end])
    next_mission_node = next_mission_node_file.next_mission_node('next_mission_node', environment)
    mission_end = py_trees.composites.Sequence(name = 'mission_end', memory = False, children = [confirm_mission_ended, next_mission_node])
    mission_server = mission_server_file.mission_server('mission_server', environment)
    obstacle_avoidance = obstacle_avoidance_file.obstacle_avoidance('obstacle_avoidance', environment)
    emergency_stop_fs = emergency_stop_fs_file.emergency_stop_fs('emergency_stop_fs')
    emergency_stop_task = emergency_stop_task_file.emergency_stop_task('emergency_stop_task', environment)
    surface_task = surface_task_file.surface_task('surface_task', environment)
    emergency_stop_tasks = py_trees.composites.Sequence(name = 'emergency_stop_tasks', memory = False, children = [emergency_stop_task, surface_task])
    emergency_stop_check_1 = py_trees.composites.Selector(name = 'emergency_stop_check_1', memory = False, children = [emergency_stop_fs, emergency_stop_tasks])
    emergency_stop_check_SIF_1 = py_trees.decorators.SuccessIsFailure(name = 'emergency_stop_check_SIF_1', child = emergency_stop_check_1)
    obstacle_avoidance_required = obstacle_avoidance_required_file.obstacle_avoidance_required('obstacle_avoidance_required')
    battery_low_fs = battery_low_fs_file.battery_low_fs('battery_low_fs')
    check_sensor_failure = check_sensor_failure_file.check_sensor_failure('check_sensor_failure')
    obstacle_standoff_fs = obstacle_standoff_fs_file.obstacle_standoff_fs('obstacle_standoff_fs')
    check_rth = check_rth_file.check_rth('check_rth')
    check_geofence = check_geofence_file.check_geofence('check_geofence')
    rth_needed = py_trees.composites.Selector(name = 'rth_needed', memory = False, children = [check_rth, check_geofence])
    check_surface = check_surface_file.check_surface('check_surface')
    rth_surface = py_trees.composites.Sequence(name = 'rth_surface', memory = False, children = [rth_needed, check_surface])
    failsafe_triggered = py_trees.composites.Selector(name = 'failsafe_triggered', memory = False, children = [battery_low_fs, check_sensor_failure, obstacle_standoff_fs, rth_surface])
    surface_task_1 = surface_task_file.surface_task('surface_task_1', environment)
    failsafe_surface = py_trees.composites.Sequence(name = 'failsafe_surface', memory = False, children = [failsafe_triggered, surface_task_1])
    check_rth_1 = check_rth_file.check_rth('check_rth_1')
    check_geofence_1 = check_geofence_file.check_geofence('check_geofence_1')
    rth_needed_1 = py_trees.composites.Selector(name = 'rth_needed_1', memory = False, children = [check_rth_1, check_geofence_1])
    rth_task = rth_task_file.rth_task('rth_task', environment)
    rth = py_trees.composites.Sequence(name = 'rth', memory = False, children = [rth_needed_1, rth_task])
    check_pipe_lost = check_pipe_lost_file.check_pipe_lost('check_pipe_lost')
    loiter_task = loiter_task_file.loiter_task('loiter_task', environment)
    pipe_lost_selector = py_trees.composites.Selector(name = 'pipe_lost_selector', memory = False, children = [check_pipe_lost, loiter_task])
    pipe_lost_selector_SIF = py_trees.decorators.SuccessIsFailure(name = 'pipe_lost_selector_SIF', child = pipe_lost_selector)
    is_track_pipe_mission_requested_1 = is_track_pipe_mission_requested_file.is_track_pipe_mission_requested('is_track_pipe_mission_requested_1')
    tracking_task = tracking_task_file.tracking_task('tracking_task', environment)
    check_lec2am_ls = check_lec2am_ls_file.check_lec2am_ls('check_lec2am_ls')
    check_lec2am_rs = check_lec2am_rs_file.check_lec2am_rs('check_lec2am_rs')
    speed_warning = py_trees.composites.Selector(name = 'speed_warning', memory = False, children = [check_lec2am_ls, check_lec2am_rs])
    speed_min_task = speed_min_task_file.speed_min_task('speed_min_task', environment)
    speed_min = py_trees.composites.Sequence(name = 'speed_min', memory = False, children = [speed_warning, speed_min_task])
    speed_max_task = speed_max_task_file.speed_max_task('speed_max_task', environment)
    lec2am_speed_cmd = py_trees.composites.Selector(name = 'lec2am_speed_cmd', memory = False, children = [speed_min, speed_max_task])
    track_pipe_mission = py_trees.composites.Sequence(name = 'track_pipe_mission', memory = False, children = [is_track_pipe_mission_requested_1, tracking_task, lec2am_speed_cmd])
    is_waypoint_requested_1 = is_waypoint_requested_file.is_waypoint_requested('is_waypoint_requested_1')
    waypoint_task = waypoint_task_file.waypoint_task('waypoint_task', environment)
    waypoint_mission = py_trees.composites.Sequence(name = 'waypoint_mission', memory = False, children = [is_waypoint_requested_1, waypoint_task])
    loiter_task_1 = loiter_task_file.loiter_task('loiter_task_1', environment)
    priorities = py_trees.composites.Selector(name = 'priorities', memory = False, children = [emergency_stop_check_SIF_1, obstacle_avoidance_required, failsafe_surface, rth, pipe_lost_selector_SIF, track_pipe_mission, waypoint_mission, loiter_task_1])
    publish_HSD_command = publish_HSD_command_file.publish_HSD_command('publish_HSD_command', environment)
    blueROV = py_trees.composites.Parallel(name = 'blueROV', policy = py_trees.common.ParallelPolicy.SuccessOnAll(False), children = [topics2bb, dd_tasks, mission_end, mission_server, obstacle_avoidance, priorities, publish_HSD_command])
    return blueROV
