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

    use_exist = False

    for variable_name_key in variables:
        # print(variable_name)
        variable = variables[variable_name_key]
        variable_name = variable['prefix'] + variable['name']
        # -----------------------------------
        # define are static.
        if variable['mode'].strip() == 'DEFINE':
            if len(variable['next_value']) > 0:
                cur_stage = 0
                for stage in variable['next_value']:
                    define_string += (
                        tab_indent(2) + variable_name + '_stage_' + str(cur_stage) + ' :=' + os.linesep
                        + tab_indent(3) + 'case' + os.linesep
                        + ''.join(
                            [
                                (tab_indent(4) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep)
                                for condition_pair in stage
                            ]
                        )
                        + tab_indent(3) + 'esac;' + os.linesep
                    )
                    cur_stage = cur_stage + 1
            # if variable['initial_value'] is None:
            #     if variable['custom_value_range'] is None:
            #         define_string += ('\t\t' + variable_name + ' := ' + str(variable['min_value']) + ';' + os.linesep)
            #     else:
            #         define_string += ('\t\t' + variable_name + ' := ' + variable['custom_value_range'].split(',')[0].replace('{', '').strip() + ";" + os.linesep)
            # else:
            #     define_string += ('\t\t' + variable_name + ' := ' + os.linesep
            #                       + '\t\t\tcase' + os.linesep
            #                       + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['initial_value']])
            #                       + '\t\t\tesac;' + os.linesep
            #                       )
            # if use_exist:
            #     define_string += "\t\t" + variable_name + "_exists := TRUE;" + os.linesep
        elif variable['mode'].strip() == 'FROZENVAR' or len(variable['next_value']) == 0:
            frozenvar_string += ('\t\t' + variable_name + ' : '
                                 + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                 + ';' + os.linesep)
            # if variable['initial_value'] is not None:
            #     init_string += ('\t\tinit(' + variable_name + ') := ' + os.linesep
            #                     + '\t\t\tcase' + os.linesep
            #                     + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['initial_value']])
            #                     + '\t\t\tesac;' + os.linesep
            #                     )
            init_string += (
                ('\t\tinit(' + variable_name + ') := ' + os.linesep
                 + '\t\t\tcase' + os.linesep
                 + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['initial_value']])
                 + '\t\t\tesac;' + os.linesep
                 )
                if variable['initial_value'] is not None else
                (tab_indent(2) + 'init(' + variable_name + ') := '
                 + (
                     str(variable['min_value']) if variable['custom_value_range'] is None else
                     variable['custom_value_range'].split(',')[0].replace('{', '').strip()
                 )
                 + ';' + os.linesep
                 )
            )
            if use_exist:
                define_string += "\t\t" + variable_name + "_exists := TRUE;" + os.linesep
        # --------------------------------
        # ok, so we've handled define and frozenvar, so all that's left
        # is actual variable.
        else:
            # if len(variable['next_value']) == 0:
            #     var_string += ('\t\t' + variable_name + ' : '
            #                    + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (
            #                        variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
            #                    + ';' + os.linesep)
            #     init_string += (
            #         ('' if variable['initial_value'] is None else (
            #             '\t\tinit(' + variable_name + ') := ' + os.linesep
            #             + '\t\t\tcase' + os.linesep
            #             + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['initial_value']])
            #             + '\t\t\tesac;' + os.linesep
            #         ))
            #     )
            #     next_string += ('\t\tnext(' + variable_name + ') := ' + os.linesep
            #                     + '\t\t\tcase' + os.linesep
            #                     + '\t\t\t\tnext(!(' + root_node_name + '.active)) : ' + variable_name + ';' + os.linesep
            #                     + '\t\t\t\tTRUE : ' + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (
            #                         variable['custom_value_range'])) + ';' + os.linesep
            #                     + '\t\t\tesac;' + os.linesep
            #                     )
            #     continue
            if variable['keep_stage_0']:
                var_string += ('\t\t' + variable_name + ' : '
                               + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                               + ';' + os.linesep)
                init_string += (
                    ('' if variable['initial_value'] is None else (
                        '\t\tinit(' + variable_name + ') := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['initial_value']])
                        + '\t\t\tesac;' + os.linesep
                    ))
                )
                next_string += '\t\tnext(' + variable_name + ') := ' + variable_name + '_stage_' + str(len(variable['next_value'])) + ';' + os.linesep

                previous_stage = variable_name
                if use_exist:
                    define_string += '\t\t' + variable_name + '_exists := TRUE;' + os.linesep
                start_location = 0
            else:
                define_string += '\t\t' + variable_name + ' := ' + variable_name + '_stage_1;' + os.linesep
                define_string += '\t\tLINK_TO_PREVIOUS_FINAL_' + variable_name + ' := ' + variable_name + '_stage_' + str(len(variable['next_value'])) + ';' + os.linesep
                var_string += ('\t\t' + variable_name + '_stage_1' + ' : '
                               + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                               + ';' + os.linesep)
                init_string += (
                    ('' if variable['initial_value'] is None else (
                        '\t\tinit(' + variable_name + '_stage_1) := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['initial_value']])
                        + '\t\t\tesac;' + os.linesep
                    ))
                )
                (node_name, non_determinism, stage) = variable['next_value'][0]
                node_name = root_node_name if node_name is None else node_name
                next_string += (
                    '\t\tnext(' + variable_name + '_stage_1) := ' + os.linesep
                    + '\t\t\tcase' + os.linesep
                    + '\t\t\t\tnext(!(' + node_name + '.active)) : LINK_TO_PREVIOUS_FINAL_' + variable_name + ';' + os.linesep
                    + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                    + '\t\t\tesac;' + os.linesep
                )

                previous_stage = variable_name + '_stage_1'
                if use_exist:
                    define_string += '\t\t' + variable_name + '_stage_1_exists := TRUE;' + os.linesep
                start_location = 1

            for index in range(start_location, len(variable['next_value'])):
                stage_num = str(index + 1)
                (node_name, non_determinism, stage) = variable['next_value'][index]
                node_name = root_node_name if node_name is None else node_name
                if non_determinism:
                    var_string += ('\t\t' + variable_name + '_stage_' + stage_num + ' : '
                                   + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                   + ';' + os.linesep)
                    next_string += (
                        '\t\t' + variable_name + '_stage_' + stage_num + ' := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + '\t\t\t\t!(' + node_name + '.active) : ' + previous_stage + ';' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                        + '\t\t\tesac;' + os.linesep
                    )
                else:
                    define_string += (
                        '\t\t' + variable_name + '_stage_' + stage_num + ' := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + '\t\t\t\t!(' + node_name + '.active) : ' + previous_stage + ';' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                        + '\t\t\tesac;' + os.linesep
                    )
                previous_stage = variable_name + '_stage_' + stage_num
                if use_exist:
                    define_string += '\t\t' + variable_name + '_stage_' + stage_num + '_exists := TRUE;' + os.linesep
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
                     + "\t\t\t\tchild_0.status = incoming_status : outgoing_status;" + os.linesep  # if we detect the incoming status, use outgoing_status
                     + "\t\t\t\tTRUE : child_0.status;" + os.linesep  # otherwise matcch the child
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_inverter(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_inverter(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\tchild_0.status = success : failure;" + os.linesep  # if we detect the incoming status, use outgoing_status
                     + "\t\t\t\tchild_0.status = failure : success;" + os.linesep  # if we detect the incoming status, use outgoing_status
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


def create_composite_selector_with_memory(number_of_children):
    return_string = ('MODULE composite_selector_with_memory(next_composite, child, skip_child)' + os.linesep
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
                     + 'MODULE composite_selector_with_memory_END' + os.linesep
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


def create_composite_sequence_with_memory(number_of_children):
    return_string = ('MODULE composite_sequence_with_memory(next_composite, child, skip_child)' + os.linesep
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
                     + 'MODULE composite_sequence_with_memory_END' + os.linesep
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


def create_composite_parallel_with_memory(number_of_children):
    return_string = ('MODULE composite_parallel_with_memory(next_composite, child, success_on_all, skip_child)' + os.linesep
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
                     + 'MODULE composite_parallel_with_memory_END(success_on_all)' + os.linesep
                     + tab_indent(1) + 'CONSTANTS' + os.linesep
                     + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
                     + tab_indent(1) + 'DEFINE' + os.linesep
                     + tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                     + tab_indent(2) + 'internal_status := success_on_all ? success : running;' + os.linesep
                     )
    return return_string

# -----------------------------------------------------------------
