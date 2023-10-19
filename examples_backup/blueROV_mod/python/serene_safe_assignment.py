class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def battery(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable battery expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 1:
        return new_value
    else:
        raise SereneAssignmentException('variable battery expected value between 0 and 1 inclusive but received value ' + str(new_value))


def battery_low_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable battery_low_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_fls_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_fls_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_geofence(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_geofence expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_geofence_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_geofence_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_home_dist(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable bb_home_dist expected type int but received type ' + str(type(new_value)))
    if new_value in [10, 100]:
        return new_value
    else:
        raise SereneAssignmentException("variable bb_home_dist expected value in [10, 100] but received value '" + new_value + "'")


def bb_home_reached(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_home_reached expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_mission(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable bb_mission expected type str but received type ' + str(type(new_value)))
    if new_value in ['waypoint_following', 'e_stop', 'pipe_following']:
        return new_value
    else:
        raise SereneAssignmentException("variable bb_mission expected value in ['waypoint_following', 'e_stop', 'pipe_following'] but received value '" + new_value + "'")


def bb_obstacle_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_obstacle_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_pipelost(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_pipelost expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_pipe_lost_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_pipe_lost_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_pipe_mapping_enable(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_pipe_mapping_enable expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_rth(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_rth expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_rth_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_rth_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_sensor_failure(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_sensor_failure expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_sensor_failure_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_sensor_failure_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def bb_waypoints_completed(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable bb_waypoints_completed expected type bool but received type ' + str(type(new_value)))
    return new_value


def cm_hsd_input(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable cm_hsd_input expected type str but received type ' + str(type(new_value)))
    if new_value in ['cm_surface_task', 'cm_rth_task', 'cm_loiter_task', 'cm_obstacle_avoidance_task', 'cm_tracking_task', 'cm_waypoint_task']:
        return new_value
    else:
        raise SereneAssignmentException("variable cm_hsd_input expected value in ['cm_surface_task', 'cm_rth_task', 'cm_loiter_task', 'cm_obstacle_avoidance_task', 'cm_tracking_task', 'cm_waypoint_task'] but received value '" + new_value + "'")


def dd_xy_axis_degradation(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable dd_xy_axis_degradation expected type bool but received type ' + str(type(new_value)))
    return new_value


def dd_z_axis_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable dd_z_axis_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def emergency_stop_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable emergency_stop_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def fls_range(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable fls_range expected type str but received type ' + str(type(new_value)))
    if new_value in ['danger_zone', 'safe']:
        return new_value
    else:
        raise SereneAssignmentException("variable fls_range expected value in ['danger_zone', 'safe'] but received value '" + new_value + "'")


def HSD_out(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable HSD_out expected type str but received type ' + str(type(new_value)))
    if new_value in ['uuv_min_speed', 'uuv_max_speed']:
        return new_value
    else:
        raise SereneAssignmentException("variable HSD_out expected value in ['uuv_min_speed', 'uuv_max_speed'] but received value '" + new_value + "'")


def lec_dd_am(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable lec_dd_am expected type bool but received type ' + str(type(new_value)))
    return new_value


def lec_dd_am_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable lec_dd_am_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def lec2_am_l(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable lec2_am_l expected type str but received type ' + str(type(new_value)))
    if new_value in ['safe', 'speed', 'pipe', 'speed_pipe']:
        return new_value
    else:
        raise SereneAssignmentException("variable lec2_am_l expected value in ['safe', 'speed', 'pipe', 'speed_pipe'] but received value '" + new_value + "'")


def lec2_am_l_speed_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable lec2_am_l_speed_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def lec2_am_l_pipe_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable lec2_am_l_pipe_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def lec2_am_r(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable lec2_am_r expected type str but received type ' + str(type(new_value)))
    if new_value in ['safe', 'speed', 'pipe', 'speed_pipe']:
        return new_value
    else:
        raise SereneAssignmentException("variable lec2_am_r expected value in ['safe', 'speed', 'pipe', 'speed_pipe'] but received value '" + new_value + "'")


def lec2_am_r_speed_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable lec2_am_r_speed_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def lec2_am_r_pipe_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable lec2_am_r_pipe_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def next_mission(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable next_mission expected type bool but received type ' + str(type(new_value)))
    return new_value


def pipe_mapping_enable(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable pipe_mapping_enable expected type bool but received type ' + str(type(new_value)))
    return new_value


def obstacle_in_view(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable obstacle_in_view expected type bool but received type ' + str(type(new_value)))
    return new_value


def obstacle_standoff_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable obstacle_standoff_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def rtreach_long_term_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable rtreach_long_term_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def rtreach_obstacle_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable rtreach_obstacle_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def rtreach_result(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable rtreach_result expected type str but received type ' + str(type(new_value)))
    if new_value in ['safe', 'short', 'long', 'short_long']:
        return new_value
    else:
        raise SereneAssignmentException("variable rtreach_result expected value in ['safe', 'short', 'long', 'short_long'] but received value '" + new_value + "'")


def rtreach_warning(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable rtreach_warning expected type bool but received type ' + str(type(new_value)))
    return new_value


def finished_missions(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable finished_missions expected type bool but received type ' + str(type(new_value)))
    return new_value


def dd_output(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable dd_output expected type str but received type ' + str(type(new_value)))
    if new_value in ['safe', 'xy_warn', 'z_warn']:
        return new_value
    else:
        raise SereneAssignmentException("variable dd_output expected value in ['safe', 'xy_warn', 'z_warn'] but received value '" + new_value + "'")


def BLUEROV_SURFACED(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable BLUEROV_SURFACED expected type bool but received type ' + str(type(new_value)))
    return new_value


def read_success(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable read_success expected type bool but received type ' + str(type(new_value)))
    return new_value
