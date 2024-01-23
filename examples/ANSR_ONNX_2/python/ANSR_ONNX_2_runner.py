import os
import py_trees
import ANSR_ONNX_2
import ANSR_ONNX_2_environment
import serene_randomizer as serene_randomizer_module


def full_tick(tree, environment):
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return

def print_blackboard(blackboard_reader):
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'prev_dest_x: ' + str(blackboard_reader.prev_dest_x) + os.linesep
    ret_string += indent(1) + 'cur_x: ' + str(blackboard_reader.cur_x) + os.linesep
    ret_string += indent(1) + 'cur_y: ' + str(blackboard_reader.cur_y) + os.linesep
    ret_string += indent(1) + 'x_mid: ' + str(blackboard_reader.x_mid()) + os.linesep
    ret_string += indent(1) + 'cur_x_bool: ' + str(blackboard_reader.cur_x_bool()) + os.linesep
    ret_string += indent(1) + 'dest_x: ' + str(blackboard_reader.dest_x) + os.linesep
    ret_string += indent(1) + 'dest_y: ' + str(blackboard_reader.dest_y) + os.linesep
    ret_string += indent(1) + 'dir: ' + str(blackboard_reader.dir) + os.linesep
    ret_string += indent(1) + 'dir_int: ' + str(blackboard_reader.dir_int()) + os.linesep
    ret_string += indent(1) + 'victory: ' + str(blackboard_reader.victory) + os.linesep
    ret_string += indent(1) + 'x_net: ' + str(blackboard_reader.x_net) + os.linesep
    ret_string += indent(1) + 'y_net: ' + str(blackboard_reader.y_net) + os.linesep
    return ret_string


def print_environment(environment):
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'tree_x: ' + str([environment.tree_x(x) for x in range(2)]) + os.linesep
    ret_string += indent(1) + 'tree_y: ' + str([environment.tree_y(x) for x in range(2)]) + os.linesep
    ret_string += indent(1) + 'tar_x: ' + str(environment.tar_x) + os.linesep
    ret_string += indent(1) + 'tar_y: ' + str(environment.tar_y) + os.linesep
    ret_string += indent(1) + 'timer: ' + str(environment.timer) + os.linesep
    return ret_string


node_to_locals = {
    'send_victory' : [],
    'update_direction' : [],
    'call_xy_net' : [],
    'update_previous_destination' : [],
    'go_up' : [],
    'go_down' : [],
    'go_left' : [],
    'go_right' : [],
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
    blackboard_reader = ANSR_ONNX_2.create_blackboard(serene_randomizer)
    environment = ANSR_ONNX_2_environment.ANSR_ONNX_2_environment(blackboard_reader)
    serene_randomizer.set_blackboard_and_environment(blackboard_reader, environment)
    ANSR_ONNX_2.initialize_blackboard(blackboard_reader)
    environment.initialize_environment()
    root = ANSR_ONNX_2.create_tree(environment)
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
