import os
import queue


def indent(n):
    return ' '*(4*n)


def create_constants():
    return ('constants { } end_constants' + os.linesep)


def create_blackboard_variables():
    return ('blackboard_variables {} end_blackboard_variables' + os.linesep)


def create_local_variables():
    return ('local_variables {local_variable {randomizer VAR BOOLEAN initial_value { result { False } end_result } end_initial_value } end_local_variable} end_local_variables' + os.linesep)


def create_environment():
    return (
        'environment {environment_variables {} end_environment_variables update_values {} end_update_values} end_environment' + os.linesep
    )


def create_checks():
    return (
        'checks {' + os.linesep
        + '} end_checks' + os.linesep
    )


def create_environment_checks():
    return ('environment_checks {#comment# check environment nodes are defined here #end_comment#} end_environment_checks' + os.linesep)


def create_actions():
    return (
        'actions {' + os.linesep
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'success_node' + os.linesep
        + indent(2) + 'imports {} end_imports' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables {} end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'return_statement { result { success } end_result } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'success_failure_node' + os.linesep
        + indent(2) + 'imports {} end_imports' + os.linesep
        + indent(2) + 'local_variables {randomizer} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables {} end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { local randomizer result { True, False } end_result } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { case { local randomizer } end_case result { success } end_result result { failure } end_result } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        + '} end_actions' + os.linesep
    )


def create_subtree_parallel(mapping, x, indent_level):
    return (
        (
            indent(indent_level) + 'composite {' + os.linesep
            + indent(indent_level + 1) + 'parLink' + str(x) + os.linesep
            + indent(indent_level + 1) + 'parallel policy success_on_all' + os.linesep
            + indent(indent_level + 1) + 'children {' + os.linesep
            + create_subtree_parallel(mapping, mapping[x][0], indent_level + 2)
            + create_subtree_parallel(mapping, mapping[x][1], indent_level + 2)
            + indent(indent_level + 1) + '} end_children' + os.linesep
            + indent(indent_level) + '} end_composite' + os.linesep
        )
        if x > 0 else
        (
            indent(indent_level) + 'composite {' + os.linesep
            + indent(indent_level + 1) + 'sel' + str((-1)*x) + os.linesep
            + indent(indent_level + 1) + 'selector' + os.linesep
            + indent(indent_level + 1) + 'children {' + os.linesep
            + indent(indent_level + 2) + 'success_failure_node' + os.linesep
            + indent(indent_level + 2) + 'success_node' + os.linesep
            + indent(indent_level + 1) + '} end_children' + os.linesep
            + indent(indent_level) + '} end_composite' + os.linesep
        )
    )


def create_tree_parallel(mapping, root):
    return (
        'sub_trees {#comment# subtrees go here. #end_comment#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + create_subtree_parallel(mapping, root, 1)
        + '} end_tree' + os.linesep
    )


def create_subtree_selector(mapping, x, indent_level):
    return (
        (
            indent(indent_level) + 'composite {' + os.linesep
            + indent(indent_level + 1) + 'selLink' + str(x) + os.linesep
            + indent(indent_level + 1) + 'selector' + os.linesep
            + indent(indent_level + 1) + 'children {' + os.linesep
            + create_subtree_selector(mapping, mapping[x][0], indent_level + 2)
            + create_subtree_selector(mapping, mapping[x][1], indent_level + 2)
            + indent(indent_level + 1) + '} end_children' + os.linesep
            + indent(indent_level) + '} end_composite' + os.linesep
        )
        if x > 0 else
        (
            indent(indent_level) + 'composite {' + os.linesep
            + indent(indent_level + 1) + 'sel' + str((-1)*x) + os.linesep
            + indent(indent_level + 1) + 'selector' + os.linesep
            + indent(indent_level + 1) + 'children {' + os.linesep
            + indent(indent_level + 2) + 'success_failure_node' + os.linesep
            + indent(indent_level + 2) + 'success_node' + os.linesep
            + indent(indent_level + 1) + '} end_children' + os.linesep
            + indent(indent_level) + '} end_composite' + os.linesep
        )
    )


def create_tree_selector(mapping, root):
    return (
        'sub_trees {#comment# subtrees go here. #end_comment#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + create_subtree_selector(mapping, root, 1)
        + '} end_tree' + os.linesep
    )


def create_specifications(x):
    return (
        'specifications {' + os.linesep
        + ''.join(
            [
                (
                    indent(1) + 'LTLSPEC { (globally, (implies, (success, success_failure_node' + (('_' + str(i)) if i > 0 else '') + '), (success, success_node' + (('_' + str(i)) if i > 0 else '') + '))) } end_LTLSPEC' + os.linesep
                    + indent(1) + 'LTLSPEC { (globally, (implies, (success, success_failure_node' + (('_' + str(i)) if i > 0 else '') + '), (not, (success, success_node' + (('_' + str(i)) if i > 0 else '') + ')))) } end_LTLSPEC' + os.linesep
                    + indent(1) + 'CTLSPEC { (always_globally, (implies, (success, success_failure_node' + (('_' + str(i)) if i > 0 else '') + '), (success, success_node' + (('_' + str(i)) if i > 0 else '') + '))) } end_CTLSPEC' + os.linesep
                    + indent(1) + 'CTLSPEC { (always_globally, (implies, (success, success_failure_node' + (('_' + str(i)) if i > 0 else '') + '), (not, (success, success_node' + (('_' + str(i)) if i > 0 else '') + ')))) } end_CTLSPEC' + os.linesep
                    + indent(1) + 'INVARSPEC { (implies, (success, success_failure_node' + (('_' + str(i)) if i > 0 else '') + '), (success, success_node' + (('_' + str(i)) if i > 0 else '') + ')) } end_INVARSPEC' + os.linesep
                    + indent(1) + 'INVARSPEC { (implies, (success, success_failure_node' + (('_' + str(i)) if i > 0 else '') + '), (not, (success, success_node' + (('_' + str(i)) if i > 0 else '') + '))) } end_INVARSPEC' + os.linesep
                )
                for i in range(x)
            ]
        )
        + '} end_specifications'
    )


def create_mapping(x):
    to_create = queue.Queue(0)
    for i in range(x):
        to_create.put(-1 * i)
    mapping = {}
    count = 1
    while True:
        child1 = to_create.get()

        if to_create.empty():
            break

        child2 = to_create.get()

        mapping[count] = (child1, child2)
        to_create.put(count)
        count = count + 1
    return (mapping, child1)


def create_checklist_parallel(x):
    (mapping, root) = create_mapping(x)
    return (
        create_constants()
        + create_blackboard_variables()
        + create_local_variables()
        + create_environment()
        + create_checks()
        + create_environment_checks()
        + create_actions()
        + create_tree_parallel(mapping, root)
        + create_specifications(x)
        )


def create_checklist_selector(x):
    (mapping, root) = create_mapping(x)
    return (
        create_constants()
        + create_blackboard_variables()
        + create_local_variables()
        + create_environment()
        + create_checks()
        + create_environment_checks()
        + create_actions()
        + create_tree_selector(mapping, root)
        + create_specifications(x)
        )


def write_files():
    for y in range(1, 51):
        x = 20 * y
        with open('./checklist_parallel_' + str(x) + '.tree', 'w') as f:
            f.write(create_checklist_parallel(x))
        with open('./checklist_selector_' + str(x) + '.tree', 'w') as f:
            f.write(create_checklist_selector(x))


write_files()
