import textx
import argparse
import pprint
# import modified_pretty_print
import os


def get_variables(model):
    variables = {}

    for variable in model.modeling_variables.variables:
        variable_name = variable.name.variable_name
        cur_variable = {}
        for internal_value in variable.internal_values:
            if internal_value.keyword == 'access':
                access_set = set()
                for access_node in internal_value.value:
                    if access_node.node_name == 'None':
                        access_set.add(None)
                    else:
                        access_set.add(access_node.node_name)
                cur_variable[internal_value.keyword] = access_set
            elif internal_value.keyword == 'next_exist':
                next_exist_dict = {}
                for next_exist in internal_value.value:
                    if next_exist.variable_name.variable_name == 'None':
                        cur_key = None
                    else:
                        cur_key = next_exist.variable_name.variable_name
                    if next_exist.exist_val == 'None':
                        cur_val = None
                    else:
                        cur_val = next_exist.exist_val
                    next_exist_dict[cur_key] = cur_val
                cur_variable[internal_value.keyword] = next_exist_dict
            elif internal_value.keyword == 'stages':
                cur_variable[internal_value.keyword] = internal_value.value
            elif internal_value.keyword == 'next_value':
                if internal_value.value[0] == 'None':
                    cur_variable[internal_value.keyword] = None
                else:
                    pairs = []
                    for condition_pair in internal_value.value:
                        pairs.append((''.join([str(temp) for temp in condition_pair.left_hand_side]), ''.join([str(temp) for temp in condition_pair.right_hand_side])))
                    cur_variable[internal_value.keyword] = pairs
            else:
                if hasattr(internal_value.value, 'index') and len(internal_value.value) > 1:
                    combined_string = ''
                    for value in internal_value.value:
                        combined_string += value.replace('\\n', '\n').replace('\\t', '\t')
                    cur_variable[internal_value.keyword] = combined_string
                else:
                    if hasattr(internal_value.value[0], 'variable_name'):
                        if internal_value.value[0].variable_name == 'None':
                            cur_variable[internal_value.keyword] = None
                        else:
                            cur_variable[internal_value.keyword] = internal_value.value[0].variable_name
                    else:
                        if internal_value.value[0] == 'None':
                            cur_variable[internal_value.keyword] = None
                        else:
                            cur_variable[internal_value.keyword] = internal_value.value[0]
        variables[variable_name] = cur_variable
    return variables


def walk_tree(metamodel, model):
    nodes = {}
    walk_tree_recursive_dsl(metamodel, model.tree.btree, -1, 0, nodes, {})
    return nodes


def walk_tree_recursive_dsl(metamodel, current_node, parent_id, next_available_id, nodes,
                            node_names):

    # for w.e reason, checks, tasks, and monitors are combined into a single 'node'
    # if the current node has the attribute name, it's a real 'node'
    # if it doesn't, then it stores a bunch of real nodes (checks, tasks, or monitors).
    # in that case, we will handlen this below.
    if hasattr(current_node, 'name'):
        this_id = next_available_id
        next_available_id = next_available_id + 1
        # increment what is available
        if parent_id >= 0:
            nodes[parent_id]['children'].append(this_id)
            # update parent's list of children
        # next, we get the name of this node, and correct for duplication
        node_name = current_node.name.replace(' ', '')
        if node_name in node_names:
            node_names[node_name] = node_names[node_name] + 1
            node_name = node_name + str(node_names[node_name])
        else:
            node_names[node_name] = 0

    # ----------------------------------------------------------------------------------
    # start of massive if statements, starting with composites
    # -----------------------------------------------------------------------------------
    # start of composite nodes
    if textx.textx_isinstance(current_node, metamodel['SeqBTNode']):
        if (hasattr(current_node, 'memory') and (not current_node.memory)):
            memory_string = 'sequence_without_memory'
        else:
            memory_string = 'sequence_with_memory'
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : memory_string,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : {}
        }
    elif textx.textx_isinstance(current_node, metamodel['SelBTNode']):
        if (hasattr(current_node, 'memory') and current_node.memory):
            memory_string = 'selector_with_memory'
        else:
            memory_string = 'selector_without_memory'
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : memory_string,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : {}
        }
    elif textx.textx_isinstance(current_node, metamodel['ParBTNode']):
        cur_type = 'parallel'
        if (hasattr(current_node, 'synchronized') and current_node.synchronized):
            cur_type += '_synchronized_success_on_all'
        else:
            cur_type += '_unsynchronized'
            if hasattr(current_node, 'ParallelPolicy'):
                cur_type += current_node.ParallelPolicy
            else:
                cur_type += '_success_on_all'
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : cur_type,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : {}
        }
    # -----------------------------------------------------------------------------------
    # start of decorators

    elif textx.textx_isinstance(current_node, metamodel['SIFBTNode']):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'return_arguments' : {
                'success' : False,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : ['success', 'failure'],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : {}
        }

        # ok, we've added the decorator. now we add in the selector node
        parent_id = this_id
        this_id = next_available_id
        next_available_id = next_available_id + 1
        # increment what is available
        if parent_id >= 0:
            nodes[parent_id]['children'].append(this_id)
            # update parent's list of children
        # next, we get the name of this node, and correct for duplication
        node_name = current_node.name.replace(' ', '')
        if node_name in node_names:
            node_names[node_name] = node_names[node_name] + 1
            node_name = node_name + str(node_names[node_name])
        else:
            node_names[node_name] = 0

        if (hasattr(current_node, 'memory') and current_node.memory):
            memory_string = 'selector_with_memory'
        else:
            memory_string = 'selector_without_memory'

        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : memory_string,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : {}
        }
        selector_id = this_id  # store this. we will restore it after adding the checks in
        decorator_id = parent_id
        parent_id = selector_id
        # ok, now we add all the checks, which are here for some reason.
        for check in current_node.checks:
            this_id = next_available_id
            next_available_id = next_available_id + 1
            # increment what is available
            if parent_id >= 0:
                nodes[parent_id]['children'].append(this_id)
                # update parent's list of children
            # next, we get the name of this node, and correct for duplication
            node_name = check.name.replace(' ', '')
            if node_name in node_names:
                node_names[node_name] = node_names[node_name] + 1
                node_name = node_name + str(node_names[node_name])
            else:
                node_names[node_name] = 0

            variable_name = check.bbvar.name

            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'leaf',
                'type' : 'check_blackboard_variable_value',
                'return_arguments' : {
                    'success' : True,
                    'running' : False,
                    'failure' : True
                },
                'additional_arguments' : [node_name + '_CHECK_' + variable_name],
                'additional_definitions' : [],
                'additional_declarations' : [
                    '\t\t' + node_name + '_CHECK_' + variable_name
                    + ' : '
                    + node_name + '_CHECK_' + variable_name + '_module(blackboard, node_names);'
                    + os.linesep
                ],
                'additional_initializations' : [],
                'additional_modules' : {
                    'check' : {
                        'name' : node_name + '_CHECK_' + variable_name + '_module',
                        'type' : 'check',
                        'args' : ['blackboard', 'node_names'],
                        'use_next' : False,
                        'left_hand_side' : None,
                        'operator' : '=',
                        'right_hand_side' : check.right_hand_side,
                        'variable_name' : variable_name
                    }
                }
            }
        # all checks added in, so now we restore back up to the selector
        this_id = selector_id
        parent_id = decorator_id
    # -----------------------------------------------------------------------------------
    # start of leaf nodes.
    # -----------------------------------------------------------------------------------
    # start of blackboard action nodes
    elif textx.textx_isinstance(current_node, metamodel['CheckBTNode']):
        for check in current_node.check:
            this_id = next_available_id
            next_available_id = next_available_id + 1
            # increment what is available
            if parent_id >= 0:
                nodes[parent_id]['children'].append(this_id)
                # update parent's list of children
            # next, we get the name of this node, and correct for duplication
            node_name = check.name.replace(' ', '')
            if node_name in node_names:
                node_names[node_name] = node_names[node_name] + 1
                node_name = node_name + str(node_names[node_name])
            else:
                node_names[node_name] = 0

            variable_name = check.bbvar.name

            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'leaf',
                'type' : 'check_blackboard_variable_value',
                'return_arguments' : {
                    'success' : True,
                    'running' : False,
                    'failure' : True
                },
                'additional_arguments' : [node_name + '_CHECK_' + variable_name],
                'additional_definitions' : [],
                'additional_declarations' : [
                    '\t\t' + node_name + '_CHECK_' + variable_name
                    + ' : '
                    + node_name + '_CHECK_' + variable_name + '_module(blackboard, node_names);'
                    + os.linesep
                ],
                'additional_initializations' : [],
                'additional_modules' : {
                    'check' : {
                        'name' : node_name + '_CHECK_' + variable_name + '_module',
                        'type' : 'check',
                        'args' : ['blackboard', 'node_names'],
                        'use_next' : False,
                        'left_hand_side' : None,
                        'operator' : '=',
                        'right_hand_side' : check.right_hand_side,
                        'variable_name' : variable_name
                    }
                }
            }
    elif textx.textx_isinstance(current_node, metamodel['TaskBTNode']):
        for check in current_node.task:
            this_id = next_available_id
            next_available_id = next_available_id + 1
            # increment what is available
            if parent_id >= 0:
                nodes[parent_id]['children'].append(this_id)
                # update parent's list of children
            # next, we get the name of this node, and correct for duplication
            node_name = check.name.replace(' ', '')
            if node_name in node_names:
                node_names[node_name] = node_names[node_name] + 1
                node_name = node_name + str(node_names[node_name])
            else:
                node_names[node_name] = 0

            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'leaf',
                'type' : 'set_blackboard_variables',
                'return_arguments' : {
                    'success' : True,
                    'running' : True,
                    'failure' : True
                },
                'additional_arguments' : [node_name + "_STATUS"],
                'additional_definitions' : [],
                'additional_declarations' : [
                    '\t\t' + node_name + '_STATUS : '
                    + node_name
                    + '_STATUS_module(blackboard, node_names);'
                    + os.linesep],
                'additional_initializations' : [],
                'additional_modules' : {
                    'status' : {
                        'name' : node_name + '_STATUS_module',
                        'type' : 'status',
                        'args' : ['blackboard', 'node_names'],
                        # 'possible_values' : ['success', 'failure', 'running'],
                        'initial_value' : None,
                        'current_value' : None,
                        'next_value' : None
                    }
                }
            }
    elif textx.textx_isinstance(current_node, metamodel['MonBTNode']):
        for check in current_node.mon:
            this_id = next_available_id
            next_available_id = next_available_id + 1
            # increment what is available
            if parent_id >= 0:
                nodes[parent_id]['children'].append(this_id)
                # update parent's list of children
            # next, we get the name of this node, and correct for duplication
            node_name = check.name.replace(' ', '')
            if node_name in node_names:
                node_names[node_name] = node_names[node_name] + 1
                node_name = node_name + str(node_names[node_name])
            else:
                node_names[node_name] = 0

            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'leaf',
                'type' : 'set_blackboard_variables',
                'return_arguments' : {
                    'success' : True,
                    'running' : True,
                    'failure' : True
                },
                'additional_arguments' : [node_name + "_STATUS"],
                'additional_definitions' : [],
                'additional_declarations' : [
                    '\t\t' + node_name + '_STATUS : '
                    + node_name
                    + '_STATUS_module(blackboard, node_names);'
                    + os.linesep],
                'additional_initializations' : [],
                'additional_modules' : {
                    'status' : {
                        'name' : node_name + '_STATUS_module',
                        'type' : 'status',
                        'args' : ['blackboard', 'node_names'],
                        # 'possible_values' : ['success', 'failure', 'running'],
                        'initial_value' : None,
                        'current_value' : None,
                        'next_value' : None
                    }
                }
            }
    elif textx.textx_isinstance(current_node, metamodel['TimerBTNode']):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'timer',
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : False
            },
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : {}
        }

    if nodes[this_id]['category'] == 'leaf':
        pass
    elif nodes[this_id]['category'] == 'decorator':
        # currently there are no decorators. not really.
        pass
    else:
        for child in current_node.nodes:
            next_available_id = walk_tree_recursive_dsl(
                metamodel, child, this_id, next_available_id,
                nodes, node_names
            )

    return next_available_id


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('--output_file', default = None)
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file)
    model = metamodel.model_from_file(args.model_file)

    nodes = walk_tree(metamodel, model)
    variables = get_variables(model)

    if args.output_file is None:
        printer = pprint.PrettyPrinter(indent = 4)
        # printer = modified_pretty_print.modified_pprinter(indent = 4)
        printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, stream = f)
            # printer = modified_pretty_print.modified_pprinter(indent = 4, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    return


if __name__ == '__main__':
    main()
