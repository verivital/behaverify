import textx
import argparse
import pprint
import os
import sys
import itertools
import copy


def get_variables(model):
    variables = {}
    local_variables = {}
    for variable in model.variables:
        cur_variable = {
            'variable_name' : variable.name,
            'mode' : variable.model_as,
            'custom_value_range' : (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
            'min_value' : 0 if variable.domain.min_val is None else variable.domain.min_val,
            'max_value' : 1 if variable.domain.min_val is None else variable.domain.max_val,
            'init_value' : None,
            # 'always_exist' : True,
            # 'init_exist' : True,
            # 'auto_change' : False,
            'next_value' : [],
            # 'next_exist' : {},
            # 'use_separate_stages' : True,
            'read_by' : [],
            'read_by_init' : []
        }
        if variable.is_local:
            local_variables[variable.name] = cur_variable
        else:
            variables[variable.name] = cur_variable
    return (variables, local_variables)


def walk_tree(model, variables, local_variables):
    nodes = {}
    walk_tree_recursive(model.root, -1, 0, nodes, {}, variables, local_variables)
    return nodes


def walk_tree_recursive(current_node, parent_id, next_available_id, nodes, node_names, variables, local_variables):
    if not hasattr(current_node, 'name'):
        current_node = current_node.leaf
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
    if current_node.node_type == 'sequence':
        if current_node.memory:
            memory_string = 'sequence_with_memory'
        else:
            memory_string = 'sequence_without_memory'
        nodes[this_id] = {
            'node_id' : this_id,
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : memory_string,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            }
        }
    elif current_node.node_type == 'selector':
        if current_node.memory:
            memory_string = 'selector_with_memory'
        else:
            memory_string = 'selector_without_memory'
        nodes[this_id] = {
            'node_id' : this_id,
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : memory_string,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            }
        }
    elif current_node.node_type == 'parallel':
        cur_type = 'parallel'
        if current_node.memory:
            cur_type += '_with_memory_' + current_node.parallel_policy
        else:
            cur_type += '_without_memory_success_on_all'
        nodes[this_id] = {
            'node_id' : this_id,
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : cur_type,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            }
        }

    elif current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            print('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
            sys.exit()

        nodes[this_id] = {
            'node_id' : this_id,
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'return_arguments' : {
                'success' : not current_node.x == 'success',
                'running' : not current_node.x == 'running',
                'failure' : not current_node.x == 'failure'
            },
            'additional_arguments' : [current_node.x, current_node.y]
        }

    elif current_node.node_type == 'check':
        # NOT DONE.
        # need to go through variables
        current_variable_stage = {}
        if current_node.condition is not None:
            for fragment in itertools.chain(current_node.condition.left_hand_side.fragments, current_node.condition.right_hand_side.fragments):
                if fragment.variable is not None:
                    if fragment.variable.name not in current_variable_stage:
                        variables[fragment.variable.name]['read_by'].append((len(variables[fragment.variable.name]['next_value']), node_name))
                        current_variable_stage[fragment.variable.name] = ('' if len(variables[fragment.variable.name]['next_value']) == 0 else '_stage_' + str(len(variables[fragment.variable.name]['next_value'])))

        nodes[this_id] = {
            'node_id' : this_id,
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'check',
            'return_arguments' : {
                'success' : True,
                'running' : False,
                'failure' : True
            },
            'internal_status_module_name' : None if current_node.condition is None else current_node.name.replace(' ', '') + '_module',
            'internal_status_module_code' : None if current_node.condition is None else (
                'MODULE ' + current_node.name.replace(' ', '') + '_module(blackboard)'
                '\tDEFINE' + os.linesep
                + 'internal_status := ('
                + ' '.join([(('blackboard.' + x.variable.name + current_variable_stage[x.variable.name]) if x.code is None else
                             (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                             )
                            for x in current_node.condition.left_hand_side.fragments])
                + ' ' + current_node.condition.operator + ' '
                + ' '.join([(('blackboard.' + x.variable.name + current_variable_stage[x.variable.name]) if x.code is None else
                             (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                             )
                            for x in current_node.condition.right_hand_side.fragments])
                + ') ? success : failure;' + os.linesep
                )
        }
    elif current_node.node_type == 'action':
        # NOT DONE
        # need to walk through everything to determine which statuses can return
        # also need to recover variable information.
        success = current_node.return_statement.default_result.can_success
        running = current_node.return_statement.default_result.can_running
        failure = current_node.return_statement.default_result.can_failure
        for result in current_node.return_statement.case_results:
            success = success or result.can_success
            running = running or result.can_running
            failure = failure or result.can_failure
        if not (success or running or failure):
            print('no valid return type for action node!' + node_name)
            sys.exit()

        current_variable_stage = {}

        def handle_statements(statements, variable_statement = True, init_statement = False):
            for statement in statements:
                if variable_statement:
                    new_stage = []
                for case_result in statement.case_results:
                    for fragment in itertools.chain(case_result.condition.left_hand_side.fragments,
                                                    case_result.condition.right_hand_side.fragments,
                                                    [fragment for value in case_result.values for fragment in value.fragments] if variable_statement else []
                                                    ):
                        if fragment.variable is not None:
                            if fragment.variable.is_local:
                                variable_name = node_name + '_DOT_' + fragment.variable.name
                                if variable_name not in variables:
                                    variables[variable_name] = copy.deepcopy(local_variables[fragment.variable.name])
                                    variables[variable_name]['variable_name'] = variable_name
                            else:
                                variable_name = fragment.variable.name
                            if init_statement:
                                variables[variable_name]['read_by_init'].append(node_name)
                            else:
                                # if variable_name not in current_variable_stage:
                                if len(variables[variable_name]['read_by']) == 0 or variables[variable_name]['read_by'][-1] != (len(variables[variable_name]['next_value']), node_name):
                                    variables[variable_name]['read_by'].append((len(variables[variable_name]['next_value']), node_name))
                                    current_variable_stage[variable_name] = ('' if len(variables[variable_name]['next_value']) == 0 else '_stage_' + str(len(variables[variable_name]['next_value'])))

                    if variable_statement:
                        new_stage.append((
                            ' '.join([(((node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name + ('' if init_statement else current_variable_stage[(node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name])) if x.code is None else
                                       (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                                       )
                                      for x in case_result.condition.left_hand_side.fragments])
                            + ' ' + case_result.condition.operator + ' '
                            + ' '.join([(((node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name + ('' if init_statement else current_variable_stage[(node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name])) if x.code is None else
                                       (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                                       )
                                      for x in case_result.condition.right_hand_side.fragments])
                            ,
                            ('{' if len(case_result.values) > 1 else '')
                            + ', '.join(
                                [
                                    ' '.join([(((node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name + ('' if init_statement else current_variable_stage[(node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name])) if x.code is None else
                                               (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                                               )
                                              for x in value.fragments])
                                    for value in case_result.values
                                ]
                            )
                            + ('}' if len(case_result.values) > 1 else '')
                        ))
                # ok now we handle the default case
                if variable_statement:
                    for value in statement.default_result.values:
                        for fragment in value.fragments:
                            if fragment.variable is not None:
                                if fragment.variable.is_local:
                                    variable_name = node_name + '_DOT_' + fragment.variable.name
                                    if variable_name not in variables:
                                        variables[variable_name] = copy.deepcopy(local_variables[fragment.variable.name])
                                        variables[variable_name]['variable_name'] = variable_name
                                else:
                                    variable_name = fragment.variable.name
                                if init_statement:
                                    variables[variable_name]['read_by_init'].append(node_name)
                                else:
                                    # if variable_name not in current_variable_stage:
                                    if len(variables[variable_name]['read_by']) == 0 or variables[variable_name]['read_by'][-1] != (len(variables[variable_name]['next_value']), node_name):
                                        variables[variable_name]['read_by'].append((len(variables[variable_name]['next_value']), node_name))
                                        current_variable_stage[variable_name] = ('' if len(variables[variable_name]['next_value']) == 0 else '_stage_' + str(len(variables[variable_name]['next_value'])))
                    # ---------
                    # we've confirmed all current variable stages needed to add the condition value pair, so we add that now
                    new_stage.append((
                        'TRUE'
                        ,
                        ('{' if len(statement.default_result.values) > 1 else '')
                        + ', '.join(
                            [
                                ' '.join([(((node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name + ('' if init_statement else current_variable_stage[(node_name + '_DOT_' if x.variable.is_local else '') + x.variable.name])) if x.code is None else
                                           (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                                           )
                                          for x in value.fragments])
                                for value in statement.default_result.values
                            ]
                        )
                        + ('}' if len(statement.default_result.values) > 1 else '')
                    ))
                    variable_name = (node_name + '_DOT_' if statement.variable.is_local else '') + statement.variable.name
                    if variable_name not in variables:
                        variables[variable_name] = copy.deepcopy(local_variables[statement.variable.name])
                        variables[variable_name]['variable_name'] = variable_name
                    if init_statement:
                        variables[variable_name]['init_value'] = new_stage
                    else:
                        variables[variable_name]['next_value'].append((node_name, new_stage))
                        current_variable_stage[variable_name] = ('' if len(variables[variable_name]['next_value']) == 0 else '_stage_' + str(len(variables[variable_name]['next_value'])))
            return

        statuses = []
        if success:
            statuses.append('success')
        if running:
            statuses.append('running')
        if failure:
            statuses.append('failure')
        handle_statements(current_node.init_statements, True, True)
        handle_statements(current_node.pre_update_statements)
        handle_statements([current_node.return_statement], False)

        nodes[this_id] = {
            'node_id' : this_id,
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'action',
            'return_arguments' : {
                'success' : success,
                'running' : running,
                'failure' : failure
            },
            'internal_status_module_name' : None if (len(current_node.return_statement.case_results) == 0 or [success, running, failure].count(True) == 1) else node_name + '_module',
            'internal_status_module_code' : None if (len(current_node.return_statement.case_results) == 0 or [success, running, failure].count(True) == 1) else (
                'MODULE ' + node_name + '_module(blackboard)'
                + '\tVAR' + os.linesep
                + '\t\tinternal_status : {' + [', '].join(statuses) + '};' + os.linesep
                + '\tASSIGN' + os.linesep
                + '\t\tinit(internal_status) := ' + statuses[0] + ';' + os.linesep
                + '\t\tnext(internal_status) := ' + os.linesep
                + '\t\t\tcase' + os.linesep
                + (';' + os.linesep).join([('\t\t\t\t('
                                            + ' '.join([(('blackboard.' + x.variable.name + current_variable_stage[x.variable.name]) if x.code is None else
                                                         (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                                                         )
                                                        for x in case_result.condition.left_hand_side.fragments])
                                            + ') ' + case_result.condition.operator + ' ('
                                            + ' '.join([(('blackboard.' + x.variable.name + current_variable_stage[x.variable.name]) if x.code is None else
                                                         (str(x.code).upper() if isinstance(x.code, bool) else str(x.code))
                                                         )
                                                        for x in case_result.condition.right_hand_side.fragments])
                                            + ') : '
                                            + ('{' if [case_result.can_success, case_result.can_running, case_result.can_failure].count(True) > 1 else '')
                                            + str([status for (status, possible) in [('success', case_result.can_success), ('running', case_result.can_running), ('failure', case_result.can_failure)] if possible])[1:-1]
                                            + ('}' if [case_result.can_success, case_result.can_running, case_result.can_failure].count(True) > 1 else '')
                                            )
                                           for case_result in current_node.return_statement.case_results]
                                          )
                + '' if current_node.return_statement.case_results is None else (';' + os.linesep)
                + '\t\t\t\tTRUE : '
                + ('{' if [current_node.return_statement.default_result.can_success,
                           current_node.return_statement.default_result.can_running,
                           current_node.return_statement.default_result.can_failure].count(True) > 1 else '')
                + str([status for (status, possible) in [('success', current_node.return_statement.default_result.can_success),
                                                         ('running', current_node.return_statement.default_result.can_running),
                                                         ('failure', current_node.return_statement.default_result.can_failure)] if possible])[1:-1]
                + ('}' if [current_node.return_statement.default_result.can_success,
                           current_node.return_statement.default_result.can_running,
                           current_node.return_statement.default_result.can_failure].count(True) > 1 else '')
                + ';' + os.linesep
                + '\t\t\tesac;' + os.linesep
            )
        }
        handle_statements(current_node.post_update_statements)

    if nodes[this_id]['category'] == 'leaf':
        pass
    elif nodes[this_id]['category'] == 'decorator':
        # currently there are no decorators. not really.
        next_available_id = walk_tree_recursive(
            current_node.child,
            this_id, next_available_id,
            nodes, node_names,
            variables, local_variables
            )
    else:
        for child in current_node.children:
            next_available_id = walk_tree_recursive(
                child,
                this_id, next_available_id,
                nodes, node_names,
                variables, local_variables
            )

    return next_available_id


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('--output_file', default = None)
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    (variables, local_variables) = get_variables(model)
    nodes = walk_tree(model, variables, local_variables)

    if args.output_file is None:
        printer = pprint.PrettyPrinter(indent = 4)
        printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    return


if __name__ == '__main__':
    main()
