import os
from behaverify_common import tab_indent

# -----------------------------------------------------------------
# the blackboard


def create_names_module(node_name_to_number):
    return ('MODULE define_nodes' + os.linesep
            + '\tDEFINE' + os.linesep
            + ''.join([('\t\t' + node_name + ' := ' + str(node_name_to_number[node_name]) + ';' + os.linesep) for node_name in node_name_to_number])
            )


def create_blackboard(nodes, variables, root_node_name):
    define_string = ''
    frozenvar_string = ''
    var_string = ''
    init_string = ''
    next_string = ''

    for variable_name in variables:
        # print(variable_name)
        variable = variables[variable_name]
        stage_name = variable_name + '_stage_'
        # we are getting rid of the prefix system.
        # variable_name = variable['prefix'] + variable['name']
        # -----------------------------------
        if variable['array']:
            # array variables handled differently.
            # define are static.
            if variable['mode'] == 'DEFINE':
                if len(variable['next_value']) > 0:
                    for stage_num, (_, _, _, stage) in enumerate(variable['next_value']):
                        define_string += (tab_indent(2) + stage_name + str(stage_num) + ' := [' + ', '.join(map(lambda x: stage_name + str(stage_num) + '_index_' + str(x), range(variable['array_size']))) + '];' + os.linesep)
                        for (index, index_stage) in stage:
                            define_string += (
                                tab_indent(2) + stage_name + str(stage_num) + '_index_' + str(index) + ' :=' + os.linesep
                                + tab_indent(3) + 'case' + os.linesep
                                + ''.join(
                                    [
                                        (tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep)
                                        for condition_pair in index_stage
                                    ]
                                )
                                + tab_indent(3) + 'esac;' + os.linesep
                            )
            elif variable['mode'] == 'FROZENVAR' or len(variable['next_value']) == 0:
                frozenvar_string += (tab_indent(2) + stage_name + '0 : array 0..' + str(variable['array_size']) + ' of '
                                     + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                     + ';' + os.linesep)
                (_, _, _, stage) = variable['initial_value']
                for (index, index_initial) in stage:
                    init_string += (
                        tab_indent(2) + 'init(' + stage_name + '0[' + str(index) + ']) := ' + os.linesep
                        + tab_indent(3) + 'case' + os.linesep
                        + ''.join([(tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in index_initial])
                        + tab_indent(3) + 'esac;' + os.linesep
                    )
            # --------------------------------
            # ok, so we've handled define and frozenvar, so all that's left
            # is actual variable.
            else:
                define_string += (tab_indent(2) + stage_name + '0 := [' + ', '.join(map(lambda x: stage_name + '0_index_' + str(x), range(variable['array_size']))) + '];' + os.linesep)
                if variable['keep_stage_0']:
                    (_, _, _, stage) = variable['initial_value']
                    for (index, index_initial) in stage:
                        var_string += ('\t\t' + stage_name + '0_index_' + str(index) + ' : '
                                       + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                       + ';' + os.linesep)
                        init_string += (
                            '\t\tinit(' + stage_name + '0_index_' + str(index) + ') := ' + os.linesep
                            + '\t\t\tcase' + os.linesep
                            + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in index_initial])
                            + '\t\t\tesac;' + os.linesep
                        )
                        next_string += '\t\tnext(' + stage_name + '0_index_' + str(index) + ') := ' + stage_name + str(len(variable['next_value'])) + '_index_' + str(index) + ';' + os.linesep
                        # TODO: explain why this doesn't have the root condition.

                    previous_stage = stage_name + '0'
                    start_location = 0
                else:
                    define_string += (tab_indent(2) + stage_name + '1 := [' + ', '.join(map(lambda x: stage_name + '1_index_' + str(x), range(variable['array_size']))) + '];' + os.linesep)
                    (_, _, _, stage) = variable['initial_value']
                    for (index, index_initial) in stage:
                        define_string += tab_indent(2) + stage_name + '0_index_' + str(index) + ' := ' + stage_name + '1_index_' + str(index) + ';' + os.linesep
                        define_string += tab_indent(2) + 'LINK_TO_PREVIOUS_FINAL_' + variable_name + '_index_' + str(index) + ' := ' + stage_name + str(len(variable['next_value'])) + '_index_' + str(index) + ';' + os.linesep
                        var_string += ('\t\t' + stage_name + '1_index_' + str(index) + ' : '
                                       + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                       + ';' + os.linesep)
                        init_string += (
                            '\t\tinit(' + stage_name + '1_index_' + str(index) + ') := ' + os.linesep
                            + '\t\t\tcase' + os.linesep
                            + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in index_initial])
                            + '\t\t\tesac;' + os.linesep
                        )
                        # link handled in next loop
                    (node_name, constant_index, non_determinism, stage) = variable['next_value'][0]
                    node_name = root_node_name if node_name is None else node_name
                    if constant_index:
                        for (index, condition_pairs) in stage:
                            next_string += (
                                tab_indent(2) + 'next(' + stage_name + '1_index_' + str(index) + ') := ' + os.linesep
                                + tab_indent(3) + 'case' + os.linesep
                                + tab_indent(4) + 'next(!(' + node_name + '.active)) : LINK_TO_PREVIOUS_FINAL_' + variable_name + '_index_' + str(index) + ';' + os.linesep
                                + ''.join([(tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in condition_pairs])
                                + tab_indent(3) + 'esac;' + os.linesep
                            )
                    else:
                        for index in range(variable['array_size']):
                            next_string += (
                                tab_indent(2) + 'next(' + stage_name + '1_index_' + str(index) + ') := ' + os.linesep
                                + tab_indent(3) + 'case' + os.linesep
                                + tab_indent(4) + 'next(!(' + node_name + '.active)) : LINK_TO_PREVIOUS_FINAL_' + variable_name + '_index_' + str(index) + ';' + os.linesep
                            )
                            for (index_expression, condition_pairs) in stage:
                                next_string += (
                                    tab_indent(4) + str(index) + ' = ' + index_expression + ' :' + os.linesep
                                    + tab_indent(5) + 'case' + os.linesep
                                    + ''.join([(tab_indent(6) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in condition_pairs])
                                    + tab_indent(5) + 'esac;' + os.linesep
                                )
                            next_string += (
                                tab_indent(4) + 'TRUE : LINK_TO_PREVIOUS_FINAL_' + variable_name + '_index_' + str(index) + ';' + os.linesep
                                + tab_indent(3) + 'esac;' + os.linesep
                            )

                    previous_stage = stage_name + '1'
                    start_location = 1

                for counter in range(start_location, len(variable['next_value'])):
                    stage_num = str(counter + 1)
                    define_string += (tab_indent(2) + stage_name + stage_num + ' := [' + ', '.join(map(lambda x: stage_name + stage_num + '_index_' + str(x), range(variable['array_size']))) + '];' + os.linesep)
                    (node_name, constant_index, non_determinism, stage) = variable['next_value'][counter]
                    node_name = root_node_name if node_name is None else node_name
                    if constant_index:
                        indices_to_do = set(range(variable['array_size']))
                        for (index, condition_pairs) in stage:
                            indices_to_do.remove(index)
                            if non_determinism[index]:
                                var_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' : '
                                    + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                    + ';' + os.linesep)
                                next_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + os.linesep
                                    + tab_indent(3) + 'case' + os.linesep
                                    + tab_indent(4) + '!(' + node_name + '.active) : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                    + ''.join([(tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in condition_pairs])
                                    + tab_indent(3) + 'esac;' + os.linesep
                                )
                            else:
                                define_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + os.linesep
                                    + tab_indent(3) + 'case' + os.linesep
                                    + tab_indent(4) + '!(' + node_name + '.active) : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                    + ''.join([(tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in condition_pairs])
                                    + tab_indent(3) + 'esac;' + os.linesep
                                )
                        for index in indices_to_do:
                            define_string += tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                    else:
                        if non_determinism:
                            for index in range(variable['array_size']):
                                var_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' : '
                                    + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                    + ';' + os.linesep)
                                next_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + os.linesep
                                    + tab_indent(3) + 'case' + os.linesep
                                    + tab_indent(4) + '!(' + node_name + '.active) : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                )

                                for (index_expression, condition_pairs) in stage:
                                    next_string += (
                                        tab_indent(4) + str(index) + ' = ' + index_expression + ' :' + os.linesep
                                        + tab_indent(5) + 'case' + os.linesep
                                        + ''.join([(tab_indent(6) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in condition_pairs])
                                        + tab_indent(5) + 'esac;' + os.linesep
                                    )
                                next_string += (
                                    tab_indent(4) + 'TRUE : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                    + tab_indent(3) + 'esac;' + os.linesep
                                )
                        else:
                            for index in range(variable['array_size']):
                                define_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + os.linesep
                                    + tab_indent(3) + 'case' + os.linesep
                                    + tab_indent(4) + '!(' + node_name + '.active) : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                )

                                for (index_expression, condition_pairs) in stage:
                                    define_string += (
                                        tab_indent(4) + str(index) + ' = ' + index_expression + ' :' + os.linesep
                                        + tab_indent(5) + 'case' + os.linesep
                                        + ''.join([(tab_indent(6) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in condition_pairs])
                                        + tab_indent(5) + 'esac;' + os.linesep
                                    )
                                define_string += (
                                    tab_indent(4) + 'TRUE : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                    + tab_indent(3) + 'esac;' + os.linesep
                                )
                    previous_stage = stage_name + stage_num
        else:
            # NOT AN ARRAY
            # define are static.
            if variable['mode'] == 'DEFINE':
                if len(variable['next_value']) > 0:
                    for stage_num, (_, _, stage) in enumerate(variable['next_value']):
                        define_string += (
                            tab_indent(2) + stage_name + str(stage_num) + ' :=' + os.linesep
                            + tab_indent(3) + 'case' + os.linesep
                            + ''.join(
                                [
                                    (tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep)
                                    for condition_pair in stage
                                ]
                            )
                            + tab_indent(3) + 'esac;' + os.linesep
                        )
            elif variable['mode'] == 'FROZENVAR' or len(variable['next_value']) == 0:
                frozenvar_string += ('\t\t' + stage_name + '0 : '
                                     + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                     + ';' + os.linesep)
                (_, _, stage) = variable['initial_value']
                init_string += (
                    '\t\tinit(' + stage_name + '0) := ' + os.linesep
                    + '\t\t\tcase' + os.linesep
                    + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                    + '\t\t\tesac;' + os.linesep
                )
            # --------------------------------
            # ok, so we've handled define and frozenvar, so all that's left
            # is actual variable.
            else:
                if variable['keep_stage_0']:
                    var_string += ('\t\t' + stage_name + '0 : '
                                   + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                   + ';' + os.linesep)
                    (_, _, stage) = variable['initial_value']
                    init_string += (
                        '\t\tinit(' + stage_name + '0) := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                        + '\t\t\tesac;' + os.linesep
                    )
                    next_string += '\t\tnext(' + stage_name + '0) := ' + stage_name + str(len(variable['next_value'])) + ';' + os.linesep
                    # TODO: explain why this doesn't have the root condition.

                    previous_stage = stage_name + '0'
                    start_location = 0
                else:
                    define_string += '\t\t' + stage_name + '0 := ' + stage_name + '1;' + os.linesep
                    define_string += '\t\tLINK_TO_PREVIOUS_FINAL_' + variable_name + ' := ' + stage_name + str(len(variable['next_value'])) + ';' + os.linesep
                    var_string += ('\t\t' + stage_name + '1' + ' : '
                                   + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                   + ';' + os.linesep)
                    (_, _, stage) = variable['initial_value']
                    init_string += (
                        '\t\tinit(' + stage_name + '1) := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                        + '\t\t\tesac;' + os.linesep
                    )
                    (node_name, non_determinism, stage) = variable['next_value'][0]
                    node_name = root_node_name if node_name is None else node_name
                    next_string += (
                        '\t\tnext(' + stage_name + '1) := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + '\t\t\t\tnext(!(' + node_name + '.active)) : LINK_TO_PREVIOUS_FINAL_' + variable_name + ';' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                        + '\t\t\tesac;' + os.linesep
                    )

                    previous_stage = stage_name + '1'
                    start_location = 1

                for index in range(start_location, len(variable['next_value'])):
                    stage_num = str(index + 1)
                    (node_name, non_determinism, stage) = variable['next_value'][index]
                    node_name = root_node_name if node_name is None else node_name
                    if non_determinism:
                        var_string += ('\t\t' + stage_name + stage_num + ' : '
                                       + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                       + ';' + os.linesep)
                        next_string += (
                            '\t\t' + stage_name + stage_num + ' := ' + os.linesep
                            + '\t\t\tcase' + os.linesep
                            + '\t\t\t\t!(' + node_name + '.active) : ' + previous_stage + ';' + os.linesep
                            + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                            + '\t\t\tesac;' + os.linesep
                        )
                    else:
                        define_string += (
                            '\t\t' + stage_name + stage_num + ' := ' + os.linesep
                            + '\t\t\tcase' + os.linesep
                            + '\t\t\t\t!(' + node_name + '.active) : ' + previous_stage + ';' + os.linesep
                            + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                            + '\t\t\tesac;' + os.linesep
                        )
                    previous_stage = stage_name + stage_num
    return (define_string,
            frozenvar_string,
            var_string,
            init_string,
            next_string
            )

# -----------------------------------------------------------------
# status module


def create_status_module(statuses):
    status_module = ('MODULE ' + statuses + '_DEFAULT_module'
                     + os.linesep
                     + '\tCONSTANTS' + os.linesep
                     + '\t\tsuccess, failure, running, invalid;' + os.linesep
                     + '\tDEFINE' + os.linesep
                     + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                     + (('\t\tinternal_status := ' + statuses + ';' + os.linesep) if '_' not in statuses else (
                         '\tVAR' + os.linesep
                         + '\t\tinternal_status : {' + statuses.replace('_', ', ') + '};' + os.linesep
                          )))
    return status_module

# -----------------------------------------------------------------
# common node parts kept here to increase reusage


def common_string_decorator(number_of_children = 0):
    status_start = ("\tCONSTANTS" + os.linesep
                    + "\t\tsuccess, failure, running, invalid;" + os.linesep
                    + "\tDEFINE" + os.linesep
                    + "\t\tstatus := active ? internal_status : invalid;" + os.linesep
                    + "\t\tinternal_status :=" + os.linesep
                    + "\t\t\tcase" + os.linesep
                    # + "\t\t\t\t!(active) : invalid;" + os.linesep #this should be the only invalid case.
                    )
    status_end = ("\t\t\tesac;" + os.linesep)
    active = []
    for child in range(number_of_children):
        active_start = ("\t\tchild_" + str(child) + ".active :=" + os.linesep
                        + "\t\t\tcase" + os.linesep
                        + "\t\t\t\t!(active) : FALSE;" + os.linesep
                        # if the node isn't active, then the children definitely aren't active
                        )
        active.append((active_start))
    active_end = ("\t\t\t\tTRUE : TRUE;" + os.linesep
                  + "\t\t\tesac;" + os.linesep
                  )
    children = ""
    for child in range(number_of_children):
        children += ", child_" + str(child)
    if not children == "":
        children = children[2:]
    return (status_start, status_end, active, active_end, children)


def common_string_composite(number_of_children = 0):
    status_start = ("\tCONSTANTS" + os.linesep
                    + "\t\tsuccess, failure, running, invalid;" + os.linesep
                    + "\tDEFINE" + os.linesep
                    + "\t\tstatus := active ? internal_status : invalid;" + os.linesep
                    + "\t\tinternal_status :=" + os.linesep
                    + "\t\t\tcase" + os.linesep
                    # + "\t\t\t\t!(active) : invalid;" + os.linesep #this should be the only invalid case.
                    )
    status_end = ("\t\t\tesac;" + os.linesep)
    active = []
    for child in range(number_of_children):
        active_start = ("\t\tchild_" + str(child) + ".active :=" + os.linesep
                        + "\t\t\tcase" + os.linesep
                        + "\t\t\t\t!(active) : FALSE;" + os.linesep
                        # if the node isn't active, then the children definitely aren't active
                        )
        active.append((active_start))
    active_end = ("\t\t\t\tTRUE : TRUE;" + os.linesep
                  + "\t\t\tesac;" + os.linesep
                  )
    children = ""
    for child in range(number_of_children):
        children += ", child_" + str(child)
    if not children == "":
        children = children[2:]
    return (status_start, status_end, active, active_end, children)


def create_decorator_X_is_Y(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_X_is_Y(child_0, incoming_status, outgoing_status)" + os.linesep
                     + status_start
                     + "\t\t\t\tchild_0.internal_status = incoming_status : outgoing_status;" + os.linesep  # if we detect the incoming status, use outgoing_status
                     + "\t\t\t\tTRUE : child_0.internal_status;" + os.linesep  # otherwise matcch the child
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_inverter(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_inverter(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\tchild_0.internal_status = success : failure;" + os.linesep  # if we detect the incoming status, use outgoing_status
                     + "\t\t\t\tchild_0.internal_status = failure : success;" + os.linesep  # if we detect the incoming status, use outgoing_status
                     + "\t\t\t\tTRUE : child_0.status;" + os.linesep  # otherwise matcch the child
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


# def create_leaf():
#     return ('MODULE leaf_module(internal_status_module)' + os.linesep
#             + '\tCONSTANTS' + os.linesep
#             + '\t\tsuccess, failure, running, invalid;' + os.linesep
#             + '\tDEFINE' + os.linesep
#             + '\t\tstatus := active ? internal_status_module.internal_status : invalid;' + os.linesep
#             )

# -----------------------------------------------------------------
# composite nodes


def create_composite_selector_with_partial_memory(number_of_children):
    return_string = ('MODULE composite_selector_with_partial_memory(next_composite, child, skip_child)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status :=' + os.linesep
                     + tab_indent(3) + 'case' + os.linesep
                     + tab_indent(4) + 'child.internal_status = failure : next_composite.internal_status;' + os.linesep
                     + tab_indent(4) + 'TRUE : child.internal_status;' + os.linesep
                     + tab_indent(3) + 'esac;' + os.linesep
                     + tab_indent(2) + 'child.active := active & !(skip_child);' + os.linesep
                     + tab_indent(2) + 'next_composite.active := active & ((child.internal_status = failure) | skip_child);' + os.linesep
                     + os.linesep
                     + 'MODULE composite_selector_with_partial_memory_END' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? failure : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status := failure;' + os.linesep
                     )
    return return_string


def create_composite_selector_without_memory(number_of_children):
    return_string = ('MODULE composite_selector_without_memory(next_composite, child)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status :=' + os.linesep
                     + tab_indent(3) + 'case' + os.linesep
                     + tab_indent(4) + 'child.internal_status = failure : next_composite.internal_status;' + os.linesep
                     + tab_indent(4) + 'TRUE : child.internal_status;' + os.linesep
                     + tab_indent(3) + 'esac;' + os.linesep
                     + tab_indent(2) + 'child.active := active;' + os.linesep
                     + tab_indent(2) + 'next_composite.active := active & (child.internal_status = failure);' + os.linesep
                     + os.linesep
                     + 'MODULE composite_selector_without_memory_END' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? failure : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status := failure;' + os.linesep
                     )
    return return_string


def create_composite_sequence_with_partial_memory(number_of_children):
    return_string = ('MODULE composite_sequence_with_partial_memory(next_composite, child, skip_child)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status :=' + os.linesep
                     + tab_indent(3) + 'case' + os.linesep
                     + tab_indent(4) + 'child.internal_status = success : next_composite.internal_status;' + os.linesep
                     + tab_indent(4) + 'TRUE : child.internal_status;' + os.linesep
                     + tab_indent(3) + 'esac;' + os.linesep
                     + tab_indent(2) + 'child.active := active & !(skip_child);' + os.linesep
                     + tab_indent(2) + 'next_composite.active := active & ((child.internal_status = success) | skip_child);' + os.linesep
                     + os.linesep
                     + 'MODULE composite_sequence_with_partial_memory_END' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? success : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status := success;' + os.linesep
                     )
    return return_string


def create_composite_sequence_without_memory(number_of_children):
    return_string = ('MODULE composite_sequence_without_memory(next_composite, child)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status :=' + os.linesep
                     + tab_indent(3) + 'case' + os.linesep
                     + tab_indent(4) + 'child.internal_status = success : next_composite.internal_status;' + os.linesep
                     + tab_indent(4) + 'TRUE : child.internal_status;' + os.linesep
                     + tab_indent(3) + 'esac;' + os.linesep
                     + tab_indent(2) + 'child.active := active;' + os.linesep
                     + tab_indent(2) + 'next_composite.active := active & (child.internal_status = success);' + os.linesep
                     + os.linesep
                     + 'MODULE composite_sequence_without_memory_END' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? success : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status := success;' + os.linesep
                     )
    return return_string


# -------------The status of parallel nodes in this version is handled by the main module.


def create_composite_parallel_without_memory(number_of_children):
    return_string = ('MODULE composite_parallel_without_memory(next_composite, child, success_on_all)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status :=' + os.linesep
                     + tab_indent(3) + 'case' + os.linesep
                     + tab_indent(4) + 'child.internal_status = failure : failure;' + os.linesep
                     + tab_indent(4) + 'success_on_all & (child.internal_status = success) : next_composite.internal_status;' + os.linesep
                     + tab_indent(4) + 'success_on_all & (child.internal_status = running) : running;' + os.linesep
                     + tab_indent(4) + '(child.internal_status = success) : success;' + os.linesep
                     + tab_indent(4) + 'TRUE : next_composite.internal_status;' + os.linesep
                     + tab_indent(3) + 'esac;' + os.linesep
                     + tab_indent(2) + 'child.active := active;' + os.linesep
                     + tab_indent(2) + 'next_composite.active := active;' + os.linesep
                     + os.linesep
                     + 'MODULE composite_parallel_without_memory_END(success_on_all)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status := success_on_all ? success : running;' + os.linesep
                     )
    return return_string


def create_composite_parallel_with_partial_memory(number_of_children):
    return_string = ('MODULE composite_parallel_with_partial_memory(next_composite, child, success_on_all, skip_child)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status :=' + os.linesep
                     + tab_indent(3) + 'case' + os.linesep
                     + tab_indent(4) + 'skip_child : next_composite.internal_status' + os.linesep
                     + tab_indent(4) + 'child.internal_status = failure : failure;' + os.linesep
                     + tab_indent(4) + 'success_on_all & (child.internal_status = success) : next_composite.internal_status;' + os.linesep
                     + tab_indent(4) + 'success_on_all & (child.internal_status = running) : running;' + os.linesep
                     + tab_indent(4) + '(child.internal_status = success) : success;' + os.linesep
                     + tab_indent(4) + 'TRUE : next_composite.internal_status;' + os.linesep
                     + tab_indent(3) + 'esac;' + os.linesep
                     + tab_indent(2) + 'child.active := active & !(skip_child);' + os.linesep
                     + tab_indent(2) + 'next_composite.active := active;' + os.linesep
                     + os.linesep
                     + 'MODULE composite_parallel_with_partial_memory_END(success_on_all)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status := success_on_all ? success : running;' + os.linesep
                     )
    return return_string

# -----------------------------------------------------------------
