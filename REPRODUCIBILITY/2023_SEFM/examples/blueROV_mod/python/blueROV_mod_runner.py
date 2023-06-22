import os
import py_trees
import blueROV_mod
import blueROV_mod_environment

blackboard_reader = blueROV_mod.create_blackboard()
environment = blueROV_mod_environment.blueROV_mod_environment(blackboard_reader)
root = blueROV_mod.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)
py_trees.display.render_dot_tree(root)


def full_tick():
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return


def print_blackboard():
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'battery_low_warning: ' + str(blackboard_reader.battery_low_warning) + os.linesep
    ret_string += indent(1) + 'bb_fls_warning: ' + str(blackboard_reader.bb_fls_warning) + os.linesep
    ret_string += indent(1) + 'bb_geofence_warning: ' + str(blackboard_reader.bb_geofence_warning) + os.linesep
    ret_string += indent(1) + 'bb_home_reached: ' + str(blackboard_reader.bb_home_reached) + os.linesep
    ret_string += indent(1) + 'bb_mission: ' + str(blackboard_reader.bb_mission) + os.linesep
    ret_string += indent(1) + 'bb_obstacle_warning: ' + str(blackboard_reader.bb_obstacle_warning) + os.linesep
    ret_string += indent(1) + 'bb_pipe_lost_warning: ' + str(blackboard_reader.bb_pipe_lost_warning) + os.linesep
    ret_string += indent(1) + 'bb_pipe_mapping_enable: ' + str(blackboard_reader.bb_pipe_mapping_enable) + os.linesep
    ret_string += indent(1) + 'bb_rth_warning: ' + str(blackboard_reader.bb_rth_warning) + os.linesep
    ret_string += indent(1) + 'bb_sensor_failure_warning: ' + str(blackboard_reader.bb_sensor_failure_warning) + os.linesep
    ret_string += indent(1) + 'cm_hsd_input: ' + str(blackboard_reader.cm_hsd_input) + os.linesep
    ret_string += indent(1) + 'dd_xy_axis_degradation: ' + str(blackboard_reader.dd_xy_axis_degradation) + os.linesep
    ret_string += indent(1) + 'dd_z_axis_warning: ' + str(blackboard_reader.dd_z_axis_warning) + os.linesep
    ret_string += indent(1) + 'emergency_stop_warning: ' + str(blackboard_reader.emergency_stop_warning) + os.linesep
    ret_string += indent(1) + 'HSD_out: ' + str(blackboard_reader.HSD_out) + os.linesep
    ret_string += indent(1) + 'lec_dd_am_warning: ' + str(blackboard_reader.lec_dd_am_warning) + os.linesep
    ret_string += indent(1) + 'lec2_am_l_speed_warning: ' + str(blackboard_reader.lec2_am_l_speed_warning) + os.linesep
    ret_string += indent(1) + 'lec2_am_l_pipe_warning: ' + str(blackboard_reader.lec2_am_l_pipe_warning) + os.linesep
    ret_string += indent(1) + 'lec2_am_r_speed_warning: ' + str(blackboard_reader.lec2_am_r_speed_warning) + os.linesep
    ret_string += indent(1) + 'lec2_am_r_pipe_warning: ' + str(blackboard_reader.lec2_am_r_pipe_warning) + os.linesep
    ret_string += indent(1) + 'next_mission: ' + str(blackboard_reader.next_mission) + os.linesep
    ret_string += indent(1) + 'pipe_mapping_enable: ' + str(blackboard_reader.pipe_mapping_enable) + os.linesep
    ret_string += indent(1) + 'obstacle_standoff_warning: ' + str(blackboard_reader.obstacle_standoff_warning) + os.linesep
    ret_string += indent(1) + 'rtreach_long_term_warning: ' + str(blackboard_reader.rtreach_long_term_warning) + os.linesep
    ret_string += indent(1) + 'rtreach_obstacle_warning: ' + str(blackboard_reader.rtreach_obstacle_warning) + os.linesep
    ret_string += indent(1) + 'rtreach_warning: ' + str(blackboard_reader.rtreach_warning) + os.linesep
    ret_string += indent(1) + 'finished_missions: ' + str(blackboard_reader.finished_missions) + os.linesep
    ret_string += indent(1) + 'dd_output: ' + str(blackboard_reader.dd_output) + os.linesep
    ret_string += indent(1) + 'BLUEROV_SURFACED: ' + str(blackboard_reader.BLUEROV_SURFACED) + os.linesep
    return ret_string


def print_environment():
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'battery: ' + str(environment.battery) + os.linesep
    ret_string += indent(1) + 'bb_geofence: ' + str(environment.bb_geofence) + os.linesep
    ret_string += indent(1) + 'bb_home_dist: ' + str(environment.bb_home_dist) + os.linesep
    ret_string += indent(1) + 'bb_pipelost: ' + str(environment.bb_pipelost) + os.linesep
    ret_string += indent(1) + 'bb_rth: ' + str(environment.bb_rth) + os.linesep
    ret_string += indent(1) + 'bb_sensor_failure: ' + str(environment.bb_sensor_failure) + os.linesep
    ret_string += indent(1) + 'bb_waypoints_completed: ' + str(environment.bb_waypoints_completed) + os.linesep
    ret_string += indent(1) + 'fls_range: ' + str(environment.fls_range) + os.linesep
    ret_string += indent(1) + 'lec_dd_am: ' + str(environment.lec_dd_am) + os.linesep
    ret_string += indent(1) + 'lec2_am_l: ' + str(environment.lec2_am_l) + os.linesep
    ret_string += indent(1) + 'lec2_am_r: ' + str(environment.lec2_am_r) + os.linesep
    ret_string += indent(1) + 'obstacle_in_view: ' + str(environment.obstacle_in_view) + os.linesep
    ret_string += indent(1) + 'rtreach_result: ' + str(environment.rtreach_result) + os.linesep
    return ret_string


node_to_locals = {
    'battery2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'rth2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'geofence2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'lec2_am_r_2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'lec2_am_l_2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'pipe_lost2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'sensor_failure2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'waypoints_completed2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'fls2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'fls_warning2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'rtreach2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'home2bb' : [{'name' : 'read_success', 'is_func' : False, 'array_size' : None}],
    'dd_lec_task' : [],
    'reallocate_task' : [],
    'failure_node' : [],
    'next_mission_node' : [],
    'mission_server' : [],
    'obstacle_avoidance' : [],
    'emergency_stop_task' : [],
    'surface_task' : [],
    'surface_task_1' : [],
    'rth_task' : [],
    'loiter_task' : [],
    'tracking_task' : [],
    'speed_min_task' : [],
    'speed_max_task' : [],
    'waypoint_task' : [],
    'loiter_task_1' : [],
    'publish_HSD_command' : [],
}


def print_local_in_node(node, local_var):
    var_attr = getattr(node, local_var['name'])
    if not local_var['is_func']:
        return indent(1) + node.name + '_DOT_' + local_var['name'] + ' : ' + str(var_attr) + os.linesep
    if local_var['array_size'] is None:
        return indent(1) + node.name + '_DOT_' + local_var['name'] + ' : ' + str(var_attr()) + os.linesep
    return indent(1) + node.name + '_DOT_' + local_var['name'] + ' : [' + ', '.join(map(var_attr, range(local_var['array_size'] - 1))) + ']'

def print_locals_in_node(node, local_vars):
    return ''.join(map(lambda var: print_local_in_node(node, var), local_vars))


def _print_local_(node):
    if node.name in node_to_locals:
        return print_locals_in_node(node, node_to_locals[node.name])
    return ''.join(map(_print_local_, node.children))


def print_local():
    return 'local' + os.linesep + _print_local_(root)


def indent(n):
    return '  '*n




for count in range(100):
    print('------------------------')
    print('State after tick: ' + str(count + 1))
    if environment.check_tick_condition():
        full_tick()
        print(print_blackboard())
        print(print_local())
        print(print_environment())
    else:
        print('after ' + str(count) + ' ticks, tick_condition no longer holds. Printing blackboard and environment, then exiting')
        print(print_blackboard())
        print(print_local())
        print(print_environment())
        break
