import os
import py_trees
import frozen_lake
import frozen_lake_environment

blackboard_reader = frozen_lake.create_blackboard()
environment = frozen_lake_environment.frozen_lake_environment(blackboard_reader)
root = frozen_lake.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)


def full_tick():
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return


def print_blackboard():
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'tiles: ' + str(blackboard_reader.tiles) + os.linesep
    ret_string += indent(1) + 'action: ' + str(blackboard_reader.action) + os.linesep
    ret_string += indent(1) + 'sometimes: ' + str(blackboard_reader.sometimes) + os.linesep
    ret_string += indent(1) + 'strategy: ' + str(blackboard_reader.strategy) + os.linesep
    ret_string += indent(1) + 'subgoal: ' + str(blackboard_reader.subgoal) + os.linesep
    ret_string += indent(1) + 'x_subgoal: ' + str(blackboard_reader.x_subgoal()) + os.linesep
    ret_string += indent(1) + 'y_subgoal: ' + str(blackboard_reader.y_subgoal()) + os.linesep
    return ret_string


def print_environment():
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'start_loc: ' + str(environment.start_loc) + os.linesep
    ret_string += indent(1) + 'goal_loc: ' + str(environment.goal_loc) + os.linesep
    ret_string += indent(1) + 'loc: ' + str(environment.loc) + os.linesep
    ret_string += indent(1) + 'x_loc: ' + str(environment.x_loc()) + os.linesep
    ret_string += indent(1) + 'y_loc: ' + str(environment.y_loc()) + os.linesep
    ret_string += indent(1) + 'hole_loc: ' + str(environment.hole_loc) + os.linesep
    ret_string += indent(1) + 'falls_remaining: ' + str(environment.falls_remaining) + os.linesep
    return ret_string


node_to_locals = {
    'get_info' : [],
    'request_hold' : [],
    'request_reset' : [],
    'request_up' : [],
    'request_down' : [],
    'request_left' : [],
    'request_right' : [],
    'set_new_subgoal' : [],
    'request_left_1' : [],
    'request_right_1' : [],
    'request_up_1' : [],
    'request_down_1' : [],
    'request_left_2' : [],
    'request_right_2' : [],
    'request_up_2' : [],
    'request_down_2' : [],
    'request_hold_1' : [],
    'request_up_3' : [],
    'sometimes_change_strategy' : [],
    'request_down_3' : [],
    'sometimes_change_strategy_1' : [],
    'request_left_3' : [],
    'sometimes_change_strategy_2' : [],
    'request_right_3' : [],
    'sometimes_change_strategy_3' : [],
    'request_hold_2' : [],
    'change_strategy' : [],
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
