import os
import py_trees
import simple_robot
import simple_robot_environment

blackboard_reader = simple_robot.create_blackboard()
environment = simple_robot_environment.simple_robot_environment(blackboard_reader)
root = simple_robot.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)


def full_tick():
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return


def print_blackboard():
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'x: ' + str(blackboard_reader.x) + os.linesep
    ret_string += indent(1) + 'y: ' + str(blackboard_reader.y) + os.linesep
    ret_string += indent(1) + 'target_x: ' + str(blackboard_reader.target_x) + os.linesep
    ret_string += indent(1) + 'target_y: ' + str(blackboard_reader.target_y) + os.linesep
    ret_string += indent(1) + 'mission: ' + str(blackboard_reader.mission) + os.linesep
    return ret_string


def print_environment():
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'x_goal: ' + str(environment.x_goal) + os.linesep
    ret_string += indent(1) + 'y_goal: ' + str(environment.y_goal) + os.linesep
    ret_string += indent(1) + 'x_true: ' + str(environment.x_true) + os.linesep
    ret_string += indent(1) + 'y_true: ' + str(environment.y_true) + os.linesep
    ret_string += indent(1) + 'remaining_goals: ' + str(environment.remaining_goals) + os.linesep
    return ret_string


node_to_locals = {
    'get_position' : [],
    'clear_mission' : [],
    'get_mission' : [],
    'go_right' : [],
    'go_left' : [],
    'go_up' : [],
    'go_down' : [],
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
