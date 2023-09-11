import os
import py_trees
import t15
import t15_environment

blackboard_reader = t15.create_blackboard()
environment = t15_environment.t15_environment(blackboard_reader)
root = t15.create_tree(environment)
tree = py_trees.trees.BehaviourTree(root)


def full_tick():
    environment.pre_tick_environment_update()
    tree.tick()
    environment.execute_delayed_action_queue()
    environment.post_tick_environment_update()
    return


def print_blackboard():
    ret_string = 'blackboard' + os.linesep
    ret_string += indent(1) + 'blVAR0: ' + str(blackboard_reader.blVAR0) + os.linesep
    ret_string += indent(1) + 'blFROZENVAR3: ' + str(blackboard_reader.blFROZENVAR3) + os.linesep
    ret_string += indent(1) + 'blDEFINE4: ' + str([blackboard_reader.blDEFINE4(x) for x in range(2)]) + os.linesep
    return ret_string


def print_environment():
    ret_string = 'environment' + os.linesep
    ret_string += indent(1) + 'envVAR1: ' + str(environment.envVAR1) + os.linesep
    return ret_string


node_to_locals = {
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


def tree_printer(node, indent_level):
    return (
        indent(indent_level) + node.name + ' -> ' + node.__serene_print__ + os.linesep
        + ''.join(map(lambda child: tree_printer(child, indent_level + 1), node.children))
    )


def reset_serene_tree_print(node):
    node.__serene_print__ = 'INVALID'
    for child in node.children:
        reset_serene_tree_print(child)
    return


for count in range(10):
    print('------------------------')
    print('State after tick: ' + str(count + 1))
    if environment.check_tick_condition():
        reset_serene_tree_print(root)
        full_tick()
        print(tree_printer(root, 0))
        print(print_blackboard())
        print(print_local())
        print(print_environment())
    else:
        print('after ' + str(count) + ' ticks, tick_condition no longer holds. Printing blackboard and environment, then exiting')
        print(print_blackboard())
        print(print_local())
        print(print_environment())
        break
