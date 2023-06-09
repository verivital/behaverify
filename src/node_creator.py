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

    def write_cases(active_node_name, previous_stage, condition_pairs, indent_level):
        return (
            tab_indent(indent_level) + 'case' + os.linesep
            + (
                ''
                if active_node_name is None
                else
                (tab_indent(indent_level + 1) + '!(' + active_node_name + ') : ' + previous_stage + ';' + os.linesep)
            )
            + ''.join([(tab_indent(indent_level + 1) + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in condition_pairs])
            + tab_indent(indent_level) + 'esac;' + os.linesep
        )

    def get_active_node_name(node_name):
        node_name = root_node_name if node_name is None else node_name
        if node_name in nodes:
            active_node_name = node_name + '.active'
            force_constant = False
        else:
            # this means we pruned a node, but it was updating a variable. since the node was unreachable, it was never going to update anything
            # therefore, we cna force constant.
            active_node_name = 'FALSE'
            force_constant = True
        return (active_node_name, force_constant)

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
                    for stage_num, (_, _, _, indexed_cond_pairs) in enumerate(variable['next_value']):
                        define_string += (tab_indent(2) + stage_name + str(stage_num) + ' := [' + ', '.join(map(lambda x: stage_name + str(stage_num) + '_index_' + str(x), range(variable['array_size']))) + '];' + os.linesep)
                        for (index, condition_pairs) in indexed_cond_pairs:
                            define_string += (
                                tab_indent(2) + stage_name + str(stage_num) + '_index_' + str(index) + ' :=' + os.linesep
                                + write_cases(None, None, condition_pairs, 3)
                            )
            elif variable['mode'] == 'FROZENVAR' or len(variable['next_value']) == 0:
                frozenvar_string += (tab_indent(2) + stage_name + '0 : array 0..' + str(variable['array_size']) + ' of '
                                     + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                     + ';' + os.linesep)
                (_, _, _, indexed_cond_pairs) = variable['initial_value']
                for (index, condition_pairs) in indexed_cond_pairs:
                    init_string += (
                        tab_indent(2) + 'init(' + stage_name + '0[' + str(index) + ']) := ' + os.linesep
                        + write_cases(None, None, condition_pairs, 3)
                    )
            # --------------------------------
            # ok, so we've handled define and frozenvar, so all that's left
            # is actual variable.
            else:
                define_string += (tab_indent(2) + stage_name + '0 := [' + ', '.join(map(lambda x: stage_name + '0_index_' + str(x), range(variable['array_size']))) + '];' + os.linesep)
                if variable['keep_stage_0']:
                    (_, _, _, indexed_cond_pairs) = variable['initial_value']
                    if variable['keep_last_stage']:
                        # we will keep the last stage, nothing to do here
                        pass
                    else:
                        print('removal of last stage for array variables not yet implemented.')
                    for (index, condition_pairs) in indexed_cond_pairs:
                        var_string += ('\t\t' + stage_name + '0_index_' + str(index) + ' : '
                                       + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                       + ';' + os.linesep)
                        init_string += (
                            '\t\tinit(' + stage_name + '0_index_' + str(index) + ') := ' + os.linesep
                            + write_cases(None, None, condition_pairs, 3)
                        )
                        # next string in for loop because we need to init each index
                        next_string += '\t\tnext(' + stage_name + '0_index_' + str(index) + ') := ' + stage_name + str(len(variable['next_value'])) + '_index_' + str(index) + ';' + os.linesep
                        # TODO: explain why this doesn't have the root condition.

                    previous_stage = stage_name + '0'
                    start_location = 0
                else:
                    define_string += (tab_indent(2) + stage_name + '1 := [' + ', '.join(map(lambda x: stage_name + '1_index_' + str(x), range(variable['array_size']))) + '];' + os.linesep)
                    (_, _, _, indexed_cond_pairs) = variable['initial_value']
                    for (index, condition_pairs) in indexed_cond_pairs:
                        define_string += tab_indent(2) + stage_name + '0_index_' + str(index) + ' := ' + stage_name + '1_index_' + str(index) + ';' + os.linesep
                        define_string += tab_indent(2) + 'LINK_TO_PREVIOUS_FINAL_' + variable_name + '_index_' + str(index) + ' := ' + stage_name + str(len(variable['next_value'])) + '_index_' + str(index) + ';' + os.linesep
                        var_string += ('\t\t' + stage_name + '1_index_' + str(index) + ' : '
                                       + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                       + ';' + os.linesep)
                        init_string += (
                            '\t\tinit(' + stage_name + '1_index_' + str(index) + ') := ' + os.linesep
                            + write_cases(None, None, condition_pairs, 3)
                        )
                        # link handled in next loop
                    (node_name, constant_index, non_determinism, indexed_cond_pairs) = variable['next_value'][0]
                    (active_node_name, _) = get_active_node_name(node_name)
                    if constant_index:
                        for (index, condition_pairs) in indexed_cond_pairs:
                            next_string += (
                                tab_indent(2) + 'next(' + stage_name + '1_index_' + str(index) + ') := ' + os.linesep
                                + write_cases(active_node_name, 'LINK_TO_PREVIOUS_FINAL_' + variable_name + '_index_' + str(index), condition_pairs, 3)
                            )
                    else:
                        for index in range(variable['array_size']):
                            next_string += (
                                tab_indent(2) + 'next(' + stage_name + '1_index_' + str(index) + ') := ' + os.linesep
                                + tab_indent(3) + 'case' + os.linesep
                                + tab_indent(4) + 'next(!(' + active_node_name + ')) : LINK_TO_PREVIOUS_FINAL_' + variable_name + '_index_' + str(index) + ';' + os.linesep
                            )
                            for (index_expression, condition_pairs) in indexed_cond_pairs:
                                next_string += (
                                    tab_indent(4) + str(index) + ' = ' + index_expression + ' :' + os.linesep
                                    + write_cases(None, None, condition_pairs, 5)
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
                    (node_name, constant_index, non_determinism, indexed_cond_pairs) = variable['next_value'][counter]
                    (active_node_name, force_constant) = get_active_node_name(node_name)
                    if constant_index:
                        indices_to_do = set(range(variable['array_size']))
                        for (index, condition_pairs) in indexed_cond_pairs:
                            indices_to_do.remove(index)
                            if non_determinism[index] and not force_constant:
                                var_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' : '
                                    + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                    + ';' + os.linesep)
                                next_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + os.linesep
                                    + write_cases(active_node_name, previous_stage + '_index_' + str(index), condition_pairs, 3)
                                )
                            else:
                                define_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + os.linesep
                                    + write_cases(active_node_name, previous_stage + '_index_' + str(index), condition_pairs, 3)
                                )
                        for index in indices_to_do:
                            define_string += tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                    else:
                        if non_determinism and not force_constant:
                            for index in range(variable['array_size']):
                                var_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' : '
                                    + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                    + ';' + os.linesep)
                                next_string += (
                                    tab_indent(2) + stage_name + stage_num + '_index_' + str(index) + ' := ' + os.linesep
                                    + tab_indent(3) + 'case' + os.linesep
                                    + tab_indent(4) + '!(' + active_node_name + ') : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                )

                                for (index_expression, condition_pairs) in indexed_cond_pairs:
                                    next_string += (
                                        tab_indent(4) + str(index) + ' = ' + index_expression + ' :' + os.linesep
                                        + write_cases(None, None, condition_pairs, 5)
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
                                    + tab_indent(4) + '!(' + active_node_name + ') : ' + previous_stage + '_index_' + str(index) + ';' + os.linesep
                                )

                                for (index_expression, condition_pairs) in indexed_cond_pairs:
                                    define_string += (
                                        tab_indent(4) + str(index) + ' = ' + index_expression + ' :' + os.linesep
                                        + write_cases(None, None, condition_pairs, 5)
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
                    for stage_num, (_, _, condition_pairs) in enumerate(variable['next_value']):
                        define_string += (
                            tab_indent(2) + stage_name + str(stage_num) + ' :=' + os.linesep
                            + write_cases(None, None, condition_pairs, 3)
                        )
            elif variable['mode'] == 'FROZENVAR' or len(variable['next_value']) == 0:
                frozenvar_string += ('\t\t' + stage_name + '0 : '
                                     + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                     + ';' + os.linesep)
                (_, _, condition_pairs) = variable['initial_value']
                init_string += (
                    '\t\tinit(' + stage_name + '0) := ' + os.linesep
                    + write_cases(None, None, condition_pairs, 3)
                )
            # --------------------------------
            # ok, so we've handled define and frozenvar, so all that's left
            # is actual variable.
            else:
                if variable['keep_stage_0']:
                    var_string += ('\t\t' + stage_name + '0 : '
                                   + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                   + ';' + os.linesep)
                    (_, _, condition_pairs) = variable['initial_value']
                    init_string += (
                        '\t\tinit(' + stage_name + '0) := ' + os.linesep
                        + write_cases(None, None, condition_pairs, 3)
                    )
                    if variable['keep_last_stage']:
                        next_string += tab_indent(2) + 'next(' + stage_name + '0) := ' + stage_name + str(len(variable['next_value'])) + ';' + os.linesep
                        # TODO: explain why this doesn't have the root condition.
                    else:
                        # print('removed last stage for: ' + variable_name)
                        # we are going to get rid of the last stage.
                        # this means the update for stage_0 will instead be the update that the last stage was going to use
                        (node_name, _, condition_pairs) = variable['next_value'].pop()
                        (active_node_name, _) = get_active_node_name(node_name)
                        next_string += (
                            tab_indent(2) + 'next(' + stage_name + '0) := '
                            + write_cases(active_node_name, stage_name + str(len(variable['next_value'])), condition_pairs, 3)
                            # note that we don't need to subtract one from len because pop decreased the len naturally.
                            # thus, if there was only 1 other stage, this would now be empty, and point to ourself, which is what we want.
                        )

                    previous_stage = stage_name + '0'
                    start_location = 0
                else:
                    define_string += '\t\t' + stage_name + '0 := ' + stage_name + '1;' + os.linesep
                    define_string += '\t\tLINK_TO_PREVIOUS_FINAL_' + variable_name + ' := ' + stage_name + str(len(variable['next_value'])) + ';' + os.linesep
                    var_string += ('\t\t' + stage_name + '1' + ' : '
                                   + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                   + ';' + os.linesep)
                    (_, _, condition_pairs) = variable['initial_value']
                    init_string += (
                        '\t\tinit(' + stage_name + '1) := ' + os.linesep
                        + write_cases(None, None, condition_pairs, 3)
                    )
                    (node_name, non_determinism, condition_pairs) = variable['next_value'][0]
                    (active_node_name, _) = get_active_node_name(node_name)
                    next_string += (
                        '\t\tnext(' + stage_name + '1) := ' + os.linesep
                        + write_cases(active_node_name, 'LINK_TO_PREVIOUS_FINAL_' + variable_name, condition_pairs, 3)
                    )

                    previous_stage = stage_name + '1'
                    start_location = 1

                for index in range(start_location, len(variable['next_value'])):
                    stage_num = str(index + 1)
                    (node_name, non_determinism, condition_pairs) = variable['next_value'][index]
                    (active_node_name, force_constant) = get_active_node_name(node_name)
                    if non_determinism and not force_constant:
                        var_string += ('\t\t' + stage_name + stage_num + ' : '
                                       + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                       + ';' + os.linesep)
                        next_string += (
                            '\t\t' + stage_name + stage_num + ' := ' + os.linesep
                            + write_cases(active_node_name, previous_stage, condition_pairs, 3)
                        )
                    else:
                        define_string += (
                            '\t\t' + stage_name + stage_num + ' := ' + os.linesep
                            + write_cases(active_node_name, previous_stage, condition_pairs, 3)
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
    status_module = (
        'MODULE ' + statuses + '_DEFAULT_module'
        + os.linesep
        + tab_indent(1) + 'CONSTANTS' + os.linesep
        + tab_indent(2) + 'success, failure, running, invalid;' + os.linesep
        + tab_indent(1) + 'DEFINE' + os.linesep
        + (
            (
                tab_indent(2) + 'status := invalid;' + os.linesep
                + tab_indent(2) + 'internal_status := invalid;' + os.linesep
            )
            if statuses == ''
            else
            (
                tab_indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                + (
                    (tab_indent(2) + 'internal_status := ' + statuses + ';' + os.linesep)
                    if '_' not in statuses else
                    (
                        tab_indent(1) + 'VAR' + os.linesep
                        + tab_indent(2) + 'internal_status : {' + statuses.replace('_', ', ') + '};' + os.linesep
                    )
                )
            )
        )
    )
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
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    # note that resume_point is an integer between 0 and last_child (inclusive)
    if number_of_children == 0:
        inject_string = "resume_point"
    else:
        inject_string = ", resume_point"
    return_string = ("MODULE composite_selector_with_partial_memory_" + str(number_of_children) + "(" + children + inject_string + ")" + os.linesep
                     + status_start
                     )
    for child in range(number_of_children):
        # we return on first success, first running, or if everything is failure, but we skip over stuff if resuming
        # if none of these occur, it is an error.
        return_string += ("\t\t\t\t(" + str(child) + " >= resume_point) & !(child_" + str(child) + ".internal_status = failure) : child_" + str(child) + ".internal_status;" + os.linesep
                          # we found something that wasn't failure, so return here.
                          )
    return_string += ("\t\t\t\tTRUE : failure;" + os.linesep
                      # none of our children returned success or running, which means either there was an error we caught, or we failed
                      + status_end
                      )
    for child in range(number_of_children):
        if child == 0:
            return_string += ("\t\tchild_0.active := active & (0 >= resume_point);" + os.linesep)
            # first child is active if we are active and didn't skip it via resume_point
        else:
            # --- original version.
            return_string += (tab_indent(2) + 'child_' + str(child) + '.active := active & ((' + str(child) + ' >= resume_point) & ((' + str(child) + ' = resume_point) | (child_' + str(child - 1) + '.status = failure)));' + os.linesep)

            # --- internal_status version.
            # return_string += (tab_indent(2) + 'child_' + str(child) + '.active := active & ((' + str(child) + ' >= resume_point) & ((' + str(child) + ' = resume_point) | ((child_' + str(child - 1) + '.internal_status = success) & (child_' + str(child - 1) + '.active))));' + os.linesep)

            # most recent change -> changed .status to .internal_status. wait. this might be correct for a while, but fuck up later. let's consider it.
            # start from child 1. child 1 returns success.
            # child 2: inactive, because it was not the resume_point and child 1 did not return failure. but it's internal_status is failure.
            # child 3: active, because it was after the resume_point but not the resume_point. child 2 is inactive, so it should be inactive, but it's only checking internal_status.
            # ok. so that's an error. But. we must now consider if we should use active and internal status as a pair of conditions, to more actively prune.
            # ------- end consideration. below notes on doing stuff.
            # ------- consideration 2. i think there was an error in the resume code using the old version actually. NVM. i thought the following situation could occur
            # child x is skipped. child x + 1 fails to activate because child x is inactive. howerer, in the non-parallel nodes, child x being skipped means either child x+1 is skipped, or the resume point. either way, we don't have a problem.

            # other children are active if we are active, we didn't skip it via resume_point, and the previous child returned failure or we're resuming from this child specifically
    return return_string


def create_composite_selector_without_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_selector_without_memory_" + str(number_of_children) + "(" + children + ")" + os.linesep
                     + status_start
                     )
    for child in range(number_of_children):
        # we return on first success, first running, or if everything is failure
        return_string += ("\t\t\t\t!(child_" + str(child) + ".internal_status = failure) : child_" + str(child) + ".internal_status;" + os.linesep
                          # we found something that wasn't failure, so we return here.
                          )
    return_string += ("\t\t\t\tTRUE : failure;" + os.linesep
                      # none of our children returned success or running, which means either there was an error we caught, or we failed.
                      + status_end
                      )
    for child in range(number_of_children):
        if child == 0:
            return_string += ("\t\tchild_0.active := active;" + os.linesep)
            # first child is just based on active status in a selector
        else:
            return_string += ("\t\tchild_" + str(child) + ".active := child_" + str(child-1) + ".status = failure;" + os.linesep)
            # if it's not the first child, then the only thing that matters is was did the child before this one return failure?

            # below we have the internal_status version. which checks the internal status and if the parent is active. wait. that's wrong. this could cause later nodes to restart.
            # we need to check if the previous node is active.
            # return_string += ("\t\tchild_" + str(child) + ".active := (child_" + str(child-1) + ".internal_status = failure) & (child_" + str(child-1) + ".active);" + os.linesep)
    return return_string


def create_composite_sequence_with_partial_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    # note that resume_point is an integer between 0 and last_child (inclusive)
    if number_of_children == 0:
        inject_string = "resume_point"
    else:
        inject_string = ", resume_point"
    return_string = ("MODULE composite_sequence_with_partial_memory_" + str(number_of_children) + "(" + children + inject_string + ")" + os.linesep
                     + status_start
                     )
    for child in range(number_of_children):
        # we return on first failure, first running, or if everything is success, but we skip over stuff if resuming
        # if none of these occur, it is an error.
        return_string += ("\t\t\t\t(" + str(child) + " >= resume_point) & !(child_" + str(child) + ".internal_status = success) : child_" + str(child) + ".internal_status;" + os.linesep
                          # we found something that wasn't success, so return here.
                          )
    return_string += ("\t\t\t\tTRUE : success;" + os.linesep
                      # none of our children returned failure or running, which means either there was an error we caught, or we succeeded
                      + status_end
                      )
    for child in range(number_of_children):
        if child == 0:
            return_string += ("\t\tchild_0.active := active & (0 >= resume_point);" + os.linesep)
            # first child is active if we are active and didn't skip it via resume_point
        else:
            # --- original version.
            return_string += (tab_indent(2) + 'child_' + str(child) + '.active := active & ((' + str(child) + ' >= resume_point) & ((' + str(child) + ' = resume_point) | (child_' + str(child - 1) + '.status = success)));' + os.linesep)

            # --- internal_status version.
            # return_string += (tab_indent(2) + 'child_' + str(child) + '.active := active & ((' + str(child) + ' >= resume_point) & ((' + str(child) + ' = resume_point) | ((child_' + str(child - 1) + '.internal_status = success) & (child_' + str(child - 1) + '.active))));' + os.linesep)
    return return_string


def create_composite_sequence_without_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_sequence_without_memory_" + str(number_of_children) + "(" + children + ")" + os.linesep
                     + status_start
                     )
    for child in range(number_of_children):
        # we return on first failure, first running, or if everything is success
        return_string += ("\t\t\t\t!(child_" + str(child) + ".internal_status = success) : child_" + str(child) + ".internal_status;" + os.linesep
                          # we found something that wasn't success, so we return here.
                          )
    return_string += ("\t\t\t\tTRUE : success;" + os.linesep
                      # none of our children returned failure or running, which means either there was an error we caught, or we Succeeded.
                      + status_end
                      )
    for child in range(number_of_children):
        if child == 0:
            return_string += ("\t\tchild_0.active := active;" + os.linesep)
            # first child is just based on active status in a sequence without memory
        else:
            return_string += ("\t\tchild_" + str(child) + ".active := child_" + str(child-1) + ".status = success;" + os.linesep)
            # if it's not the first child, then the only thing that matters is was did the child before this one return success?

            # below we have the internal_status version. which checks the internal status and if the parent is active. wait. that's wrong. this could cause later nodes to restart.
            # we need to check if the previous node is active.
            # return_string += ("\t\tchild_" + str(child) + ".active := (child_" + str(child-1) + ".internal_status = success) & (child_" + str(child-1) + ".active);" + os.linesep)
    return return_string


def create_composite_parallel_success_on_all_with_partial_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_parallel_success_on_all_with_partial_memory_" + str(number_of_children) + "(" + children + ", skip_child)" + os.linesep
                     + status_start
                     )
    for child in range(number_of_children):
        return_string += "\t\t\t\t(child_" + str(child) + ".internal_status = failure) & !(skip_child[" + str(child) + "] = -2) : failure;" + os.linesep
        # we found failure, therefore, return failure
    # at this point, no failures are possible. everything is success, running, or skipped.
    for child in range(number_of_children):
        # we return on first success if success_on_all is false, on first running if it's true, and otherwise we need to see them all
        return_string += ("\t\t\t\t!(child_" + str(child) + ".internal_status = success) & !(skip_child[" + str(child) + "] = -2) : child_" + str(child) + ".internal_status;" + os.linesep
                          # we found something other than success, return that.
                          )
    return_string += ("\t\t\t\tTRUE : success;" + os.linesep
                      + status_end
                      )
    for child in range(number_of_children):
        return_string += ("\t\tchild_" + str(child) + ".active := active & !(skip_child[" + str(child) + "] = -2);" + os.linesep)
        # all children are active if they are not skipped
    return return_string

# this is basically a fake thing. if you're success_on_one, then you're basically unsynchronized


"""
def create_composite_parallel_with_partial_memory_success_on_one(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_parallel_with_partial_memory_success_on_one_" + str(number_of_children) + "(" + children + ", skip_child)" + os.linesep
                      + status_start
    )
    for child in range(number_of_children):
        return_string += "\t\t\t\t(child_" + str(child) + ".internal_status = failure) : failure;" + os.linesep
        #we found failure, therefore, return failure
    #at this point, no failures are possible. everything is success, running, or skipped.
    for child in range(number_of_children):
        #we return on first success if success_on_all is false, on first running if it's true, and otherwise we need to see them all
        return_string += ("\t\t\t\t!(child_" + str(child) + ".internal_status = running) : child_" + str(child) + ".internal_status;" + os.linesep
                          #we found something other than running, so return that.
        )
    return_string += ("\t\t\t\tTRUE : running;" + os.linesep
                      + status_end
    )
    for child in range(number_of_children):
        return_string += ("\t\tchild_" + str(child) + ".active := active & !(skip_child[" + str(child) + "] = -2);" + os.linesep)
        #all children are active if they are not skipped
    return return_string
"""

# no skipping in the below


def create_composite_parallel_success_on_all_without_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_parallel_success_on_all_without_memory_" + str(number_of_children) + "(" + children + ")" + os.linesep
                     + status_start
                     )
    for child in range(number_of_children):
        return_string += "\t\t\t\t(child_" + str(child) + ".internal_status = failure) : failure;" + os.linesep
        # we found failure, therefore, return failure
    # at this point, no failures are possible. everything is success, running,
    for child in range(number_of_children):
        # we return on first success if success_on_all is false, on first running if it's true, and otherwise we need to see them all
        return_string += ("\t\t\t\t!(child_" + str(child) + ".internal_status = success) : child_" + str(child) + ".internal_status;" + os.linesep
                          # we found something other than success, return that.
                          )
    return_string += ("\t\t\t\tTRUE : success;" + os.linesep
                      + status_end
                      )
    for child in range(number_of_children):
        return_string += ("\t\tchild_" + str(child) + ".active := active;" + os.linesep)
        # all children are active
    return return_string


def create_composite_parallel_success_on_one_without_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_parallel_success_on_one_without_memory_" + str(number_of_children) + "(" + children + ")" + os.linesep
                     + status_start
                     )
    for child in range(number_of_children):
        return_string += "\t\t\t\t(child_" + str(child) + ".internal_status = failure) : failure;" + os.linesep
        # we found failure, therefore, return failure
    # at this point, no failures are possible. everything is success, running.
    for child in range(number_of_children):
        # we return on first success if success_on_all is false, on first running if it's true, and otherwise we need to see them all
        return_string += ("\t\t\t\t!(child_" + str(child) + ".internal_status = running) : child_" + str(child) + ".internal_status;" + os.linesep
                          # we found something other than running, so return that.
                          )
    return_string += ("\t\t\t\tTRUE : running;" + os.linesep
                      + status_end
                      )
    for child in range(number_of_children):
        return_string += ("\t\tchild_" + str(child) + ".active := active;" + os.linesep)
        # all children are active if they are not skipped
    return return_string

# -----------------------------------------------------------------
