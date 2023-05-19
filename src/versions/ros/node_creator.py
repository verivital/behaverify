import os


# -----------------------------------------------------------------
# the blackboard

def create_names_module(node_name_to_number):
    return ('MODULE define_nodes' + os.linesep
            + '\tDEFINE' + os.linesep
            + ''.join([('\t\t' + node_name + ' := ' + str(node_name_to_number[node_name]) + ';' + os.linesep) for node_name in node_name_to_number])
            )


def create_blackboard(nodes, variables):

    # node_name_to_id = {nodes[node_id]['name'] : node_id for node_id in nodes}

    return_string = ('MODULE blackboard_module(node_names, active)' + os.linesep
                     + '\tCONSTANTS' + os.linesep
                     + '\t\tsuccess, failure, running, invalid;' + os.linesep
                     + '\tDEFINE' + os.linesep)
    exist_define = ''
    frozen_decl_string = '\tFROZENVAR' + os.linesep
    decl_string = ('\tVAR' + os.linesep)
    assign_string = ('\tASSIGN' + os.linesep)

    for variable_name in variables:
        variable = variables[variable_name]
        # -----------------------------------
        # define are static.
        if variable['mode'].strip() == 'DEFINE':
            # if variable['mode'].strip() == 'DEFINE' or (variable['custom_value_range'] is None and variable['environment_update'] is None and variable['min_value'] >= variable['max_value']):
            if variable['init_value'] is None:
                if variable['custom_value_range'] is None:
                    exist_define += ('\t\t' + variable_name + ' := ' + str(variable['min_value']) + ';' + os.linesep)
                else:
                    exist_define += ('\t\t' + variable_name + ' := ' + variable['custom_value_range'].split(',')[0].replace('{', '').strip() + ";" + os.linesep)
            else:
                exist_define += ('\t\t' + variable_name + ' := ' + os.linesep
                                 + '\t\t\tcase' + os.linesep
                                 + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['init_value']])
                                 + '\t\t\tesac;' + os.linesep
                                 )
            exist_define += "\t\t" + variable_name + "_exists := TRUE;" + os.linesep
        elif variable['mode'].strip() == 'FROZENVAR':
            # elif variable['mode'].strip() == 'FROZENVAR' or (len(variable['next_value']) == 0 and variable['environment_update'] is None):
            frozen_decl_string += ('\t\t' + variable_name + ' : '
                                   + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                   + ';' + os.linesep)
            if variable['init_value'] is not None:
                assign_string += ('\t\tinit(' + variable_name + ') := ' + os.linesep
                                  + '\t\t\tcase' + os.linesep
                                  + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['init_value']])
                                  + '\t\t\tesac;' + os.linesep
                                  )
            exist_define += "\t\t" + variable_name + "_exists := TRUE;" + os.linesep
        # --------------------------------
        # ok, so we've handled define and frozenvar, so all that's left
        # is actual variable.
        elif variable['environment_update'] is not None:
            decl_string += ('\t\t' + variable_name + ' : '
                            + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                            + ';' + os.linesep)
            assign_string += (
                ('' if variable['init_value'] is None else (
                    '\t\tinit(' + variable_name + ') := ' + os.linesep
                    + '\t\t\tcase' + os.linesep
                    + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['init_value']])
                    + '\t\t\tesac;' + os.linesep
                ))
                + '\t\tnext(' + variable_name + ') := ' + os.linesep
                + '\t\t\tcase' + os.linesep
                + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['environment_update']])
                + '\t\t\tesac;' + os.linesep
            )
        else:
            if len(variable['next_value']) == 0:
                exist_define += ('\t\t' + variable_name + ' := ' + variable_name + '_stage_' + str(len(variable['next_value'])) + ';' + os.linesep)
                decl_string += ('\t\t' + variable_name + ' : '
                                + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                + ';' + os.linesep)
                assign_string += (
                    ('' if variable['init_value'] is None else (
                        '\t\tinit(' + variable_name + ') := ' + os.linesep
                        + '\t\t\tcase' + os.linesep
                        + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['init_value']])
                        + '\t\t\tesac;' + os.linesep
                    ))
                )
                continue
            exist_define += ('\t\t' + variable_name + ' := ' + variable_name + '_stage_' + str(len(variable['next_value'])) + ';' + os.linesep
                             + '\t\t' + variable_name + '_exists := TRUE;' + os.linesep)
            previous_stage = variable_name
            # the base variable is just a macro for the last stage.
            index = 0
            stage_num = str(index + 1)
            (node_name, stage) = variable['next_value'][index]
            decl_string += ('\t\t' + variable_name + '_stage_' + stage_num + ' : '
                            + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                            + ';' + os.linesep)
            assign_string += (
                ('' if variable['init_value'] is None else (
                    '\t\tinit(' + variable_name + '_stage_' + stage_num + ') := ' + os.linesep
                    + '\t\t\tcase' + os.linesep
                    + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in variable['init_value']])
                    + '\t\t\tesac;' + os.linesep
                ))
                + '\t\tnext(' + variable_name + '_stage_' + stage_num + ') := ' + os.linesep
                + '\t\t\tcase' + os.linesep
                + '\t\t\t\t!(active[node_names.' + node_name + ']) : ' + previous_stage + ';' + os.linesep
                + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                + '\t\t\tesac;' + os.linesep
            )
            previous_stage = variable_name + '_stage_' + stage_num
            exist_define += '\t\t' + variable_name + '_stage_' + stage_num + '_exists := TRUE;' + os.linesep

            for index in range(1, len(variable['next_value'])):
                stage_num = str(index + 1)
                (node_name, stage) = variable['next_value'][index]
                decl_string += ('\t\t' + variable_name + '_stage_' + stage_num + ' : '
                                + ((str(variable['min_value']) + '..' + str(variable['max_value'])) if variable['custom_value_range'] is None else (variable['custom_value_range'].replace('{TRUE, FALSE}', 'boolean')))
                                + ';' + os.linesep)
                assign_string += (
                    '\t\tinit(' + variable_name + '_stage_' + stage_num + ') := ' + variable_name + '_stage_1;' + os.linesep
                    + '\t\tnext(' + variable_name + '_stage_' + stage_num + ') := ' + os.linesep
                    + '\t\t\tcase' + os.linesep
                    + '\t\t\t\t!(active[node_names.' + node_name + ']) : ' + previous_stage + ';' + os.linesep
                    + ''.join([('\t\t\t\t' + condition_pair[0] + ' : ' + condition_pair[1] + ';' + os.linesep) for condition_pair in stage])
                    + '\t\t\tesac;' + os.linesep
                )
                previous_stage = variable_name + '_stage_' + stage_num
                exist_define += '\t\t' + variable_name + '_stage_' + stage_num + '_exists := TRUE;' + os.linesep
    return_string += (exist_define
                      + frozen_decl_string
                      + decl_string
                      + assign_string
                      + os.linesep
                      )
    return return_string

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


def create_leaf():
    return ('MODULE leaf_module(internal_status_module)' + os.linesep
            + '\tCONSTANTS' + os.linesep
            + '\t\tsuccess, failure, running, invalid;' + os.linesep
            + '\tDEFINE' + os.linesep
            + '\t\tstatus := active ? internal_status_module.internal_status : invalid;' + os.linesep
            )

# -----------------------------------------------------------------
# composite nodes


def create_composite_selector_with_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    # note that resume_point is an integer between 0 and last_child (inclusive)
    if number_of_children == 0:
        inject_string = "resume_point"
    else:
        inject_string = ", resume_point"
    return_string = ("MODULE composite_selector_with_memory_" + str(number_of_children) + "(" + children + inject_string + ")" + os.linesep
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
            # NEW MODIFICATION?
            return_string += ("\t\tchild_" + str(child) + ".active := (" + str(child) + " >= resume_point) & ((" + str(child) + " = resume_point) | (child_" + str(child-1) + ".status = failure));" + os.linesep)
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
    return return_string


def create_composite_sequence_with_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    # note that resume_point is an integer between 0 and last_child (inclusive)
    if number_of_children == 0:
        inject_string = "resume_point"
    else:
        inject_string = ", resume_point"
    return_string = ("MODULE composite_sequence_with_memory_" + str(number_of_children) + "(" + children + inject_string + ")" + os.linesep
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
            return_string += ("\t\tchild_" + str(child) + ".active := (" + str(child) + " >= resume_point) & ((" + str(child) + " = resume_point) | (child_" + str(child-1) + ".status = success));" + os.linesep)
            # other children are active if we are active, we didn't skip it via resume_point, and the previous child returned success or we're resuming from this child specifically
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
            # if it's not the first child, then the only thing that matters is was did the child before this one return success (is parent active also matters)
    return return_string


def create_composite_parallel_success_on_all_with_memory(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_parallel_success_on_all_with_memory_" + str(number_of_children) + "(" + children + ", skip_child)" + os.linesep
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
def create_composite_parallel_with_memory_success_on_one(number_of_children):
    (status_start, status_end, active, active_end, children) = common_string_composite(number_of_children)
    return_string = ("MODULE composite_parallel_with_memory_success_on_one_" + str(number_of_children) + "(" + children + ", skip_child)" + os.linesep
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
