import os
import py_trees
import complex_robot
import complex_robot_environment

blackboard_reader = complex_robot.create_blackboard()
environment = complex_robot_environment.complex_robot_environment(blackboard_reader)
root = complex_robot.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)


def full_tick():
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return


def print_blackboard():
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'zone: ' + str(blackboard_reader.zone) + os.linesep
    ret_string += indent(1) + 'side: ' + str(blackboard_reader.side) + os.linesep
    ret_string += indent(1) + 'have_flag: ' + str(blackboard_reader.have_flag) + os.linesep
    ret_string += indent(1) + 'need_side_reached: ' + str(blackboard_reader.need_side_reached) + os.linesep
    ret_string += indent(1) + 'forward: ' + str(blackboard_reader.forward()) + os.linesep
    return ret_string


def print_environment():
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'x: ' + str(environment.x) + os.linesep
    ret_string += indent(1) + 'y: ' + str(environment.y) + os.linesep
    ret_string += indent(1) + 'hole_1: ' + str(environment.hole_1) + os.linesep
    ret_string += indent(1) + 'hole_2: ' + str(environment.hole_2) + os.linesep
    ret_string += indent(1) + 'hole_3: ' + str(environment.hole_3) + os.linesep
    ret_string += indent(1) + 'hole_4: ' + str(environment.hole_4) + os.linesep
    ret_string += indent(1) + 'hole_5: ' + str(environment.hole_5) + os.linesep
    ret_string += indent(1) + 'hole_6: ' + str(environment.hole_6) + os.linesep
    ret_string += indent(1) + 'hole_7: ' + str(environment.hole_7) + os.linesep
    ret_string += indent(1) + 'hole_8: ' + str(environment.hole_8) + os.linesep
    ret_string += indent(1) + 'hole_9: ' + str(environment.hole_9) + os.linesep
    ret_string += indent(1) + 'active_hole: ' + str(environment.active_hole()) + os.linesep
    ret_string += indent(1) + 'flag_x: ' + str(environment.flag_x) + os.linesep
    ret_string += indent(1) + 'flag_y: ' + str(environment.flag_y) + os.linesep
    ret_string += indent(1) + 'flag_returned: ' + str(environment.flag_returned()) + os.linesep
    ret_string += indent(1) + 'tile_progress: ' + str(environment.tile_progress) + os.linesep
    ret_string += indent(1) + 'tile_tracker: ' + str(environment.tile_tracker) + os.linesep
    return ret_string


node_to_locals = {
    'set_zone' : [],
    'go_forward' : [],
    'go_side' : [],
    'change_side' : [],
    'go_forward_1' : [],
    'go_side_1' : [],
    'change_side_1' : [],
    'never_need_side' : [],
    'search_tile' : [{'name' : 'tile_searched', 'is_func' : False, 'array_size' : None}],
    'go_side_2' : [],
    'change_side_2' : [],
    'go_forward_2' : [],
}


def print_local_in_node(node, local_var):
    var_attr = getattr(node, local_var['name'])
    if not local_var['is_func']:
        return indent(1) + node.name + '_DOT_' + local_var['name'] + ' : ' + str(var_attr) + os.linesep
    if local_var['array_size'] is None:
        return indent(1) + node.name + '_DOT_' + local_var['name'] + ' : ' + str(var_attr()) + os.linesep
    return indent(1) + node.name + '_DOT_' + local_var['name'] + ' : [' + ', '.join(map(str, map(var_attr, range(local_var['array_size'] - 1)))) + ']' + os.linesep

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
