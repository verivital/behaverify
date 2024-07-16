import os
import py_trees
import ANSR
import ANSR_environment
import serene_randomizer as serene_randomizer_module


def full_tick(tree, environment):
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return

def print_blackboard(blackboard_reader):
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'goal: ' + str(blackboard_reader.goal) + os.linesep
    ret_string += indent(1) + 'goal_requested: ' + str(blackboard_reader.goal_requested) + os.linesep
    ret_string += indent(1) + 'map_exists: ' + str(blackboard_reader.map_exists) + os.linesep
    ret_string += indent(1) + 'position: ' + str(blackboard_reader.position) + os.linesep
    ret_string += indent(1) + 'valid_goal: ' + str(blackboard_reader.valid_goal) + os.linesep
    ret_string += indent(1) + 'valid_position: ' + str(blackboard_reader.valid_position) + os.linesep
    ret_string += indent(1) + 'waypoint: ' + str(blackboard_reader.waypoint) + os.linesep
    return ret_string


def print_environment(environment):
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'fake: ' + str(environment.fake) + os.linesep
    return ret_string


node_to_locals = {
    'read_position' : [],
    'read_goal' : [],
    'send_next_goal_request' : [],
    'read_map' : [{'name' : 'success_read', 'is_func' : False, 'array_size' : None}],
    'compute_waypoint' : [],
    'send_invalid_goal_request' : [],
    'send_waypoint' : [],
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


def print_local(root):
    return 'local' + os.linesep + _print_local_(root)


def indent(n):
    return '  '*n




def run_tree():
    serene_randomizer = serene_randomizer_module.serene_randomizer()
    blackboard_reader = ANSR.create_blackboard(serene_randomizer)
    environment = ANSR_environment.ANSR_environment(blackboard_reader)
    serene_randomizer.set_blackboard_and_environment(blackboard_reader, environment)
    ANSR.initialize_blackboard(blackboard_reader)
    environment.initialize_environment()
    root = ANSR.create_tree(environment)
    tree = py_trees.trees.BehaviourTree(root)
    print('------------------------')
    print('Initial State')
    print(print_blackboard(blackboard_reader))
    print(print_local(root))
    print(print_environment(environment))
    for count in range(100):
        print('------------------------')
        print('State after tick: ' + str(count + 1))
        if environment.check_tick_condition():
            full_tick(tree, environment)
            print(print_blackboard(blackboard_reader))
            print(print_local(root))
            print(print_environment(environment))
        else:
            print('after ' + str(count) + ' ticks, tick_condition no longer holds. Printing blackboard and environment, then exiting')
            print(print_blackboard(blackboard_reader))
            print(print_local(root))
            print(print_environment(environment))
            break


if __name__ == '__main__':
    run_tree()
