import os
import py_trees
import light_controller
import light_controller_environment

blackboard_reader = light_controller.create_blackboard()
environment = light_controller_environment.light_controller_environment(blackboard_reader)
root = light_controller.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)


def full_tick():
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return


def print_blackboard():
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'fairness_counter: ' + str(blackboard_reader.fairness_counter) + os.linesep
    ret_string += indent(1) + 'direction: ' + str(blackboard_reader.direction) + os.linesep
    return ret_string


def print_environment():
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'tunnel_state: ' + str(environment.tunnel_state) + os.linesep
    ret_string += indent(1) + 'east_cars: ' + str(environment.east_cars) + os.linesep
    ret_string += indent(1) + 'west_cars: ' + str(environment.west_cars) + os.linesep
    ret_string += indent(1) + 'west_and_east_cars: ' + str(environment.west_and_east_cars()) + os.linesep
    ret_string += indent(1) + 'west_light: ' + str(environment.west_light) + os.linesep
    ret_string += indent(1) + 'east_light: ' + str(environment.east_light) + os.linesep
    return ret_string


node_to_locals = {
    'swap_direction' : [],
    'set_west' : [],
    'set_east' : [],
    'send_light_signal' : [],
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
