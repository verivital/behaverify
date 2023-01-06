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

"""
def create_decorator_failure_is_running(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_failure_is_running(child_0)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = failure) : child_0.status;" + os.linesep  # no matter what, we match the child_0
                     + "\t\t\t\tTRUE : running;" + os.linesep  # unless it failed. then we pretend it's still running
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_failure_is_success(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_failure_is_success(child_0)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  # we found an error
                     + "\t\t\t\t!(child_0.status = failure) : child_0.status;" + os.linesep  # no matter what, we match the child_0
                     + "\t\t\t\tTRUE : success;" + os.linesep  # unless it failed. then we pretend it success
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_running_is_failure(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_running_is_failure(child_0)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  # we found an error
                     + "\t\t\t\t!(child_0.status = running) : child_0.status;" + os.linesep  # no matter what, we match the child_0
                     + "\t\t\t\tTRUE : failure;" + os.linesep  # unless it's running. then we pretend it failed
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_running_is_success(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_running_is_success(child_0)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  # we found an error
                     + "\t\t\t\t!(child_0.status = running) : child_0.status;" + os.linesep  # no matter what, we match the child_0
                     + "\t\t\t\tTRUE : success;" + os.linesep  # unless it's running. then we pretend it success
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_success_is_failure(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_success_is_failure(child_0)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = success) : child_0.status;" + os.linesep  # no matter what, we match the child_0
                     + "\t\t\t\tTRUE : failure;" + os.linesep  # unless it's success. then we pretend it failed
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_success_is_running(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_success_is_running(child_0)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  # we found an error
                     + "\t\t\t\t!(child_0.status = success) : child_0.status;" + os.linesep  # no matter what, we match the child_0
                     + "\t\t\t\tTRUE : running;" + os.linesep  # unless it's success. then we pretend it running
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string




# -----------------------------------------------------------------
# blackboard nodes


def create_leaf_blackboard_to_status(number_of_nodes, variable):
    pass


def create_leaf_check_blackboard_variable_exists(ignored_value = 0):
    return
    # (status_start, status_end) = common_string_leaf()
    # return_string = ("MODULE leaf_check_blackboard_variable_exists(blackboard, variable_num)" + os.linesep
    #                  + status_start
    #                  + "\t\tinternal_status := blackboard.variable_exists[variable] ? success : failure;" + os.linesep
    #                  #+ "\t\t\t\t(blackboard.variable_exists[variable]) : success;" + os.linesep  #the variable exists
    #                  #+ "\t\t\t\tTRUE : failure;" + os.linesep  #it doesn't
    #                  #+ status_end
    #                  )
    # return return_string


def create_leaf_check_blackboard_variable_value(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_check_blackboard_variable_value(check)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := (check.result) ? success : failure;" + os.linesep  # passes the check
                     # + "\t\t\t\t(blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                     # + "\t\t\t\tTRUE : failure;" + os.linesep  #the variable doesn't exist or fails the check
                     # + status_end
                     )
    return return_string


def create_leaf_check_blackboard_variable_values(number_of_nodes, variables, checks, operators):
    pass
    # NOT ACTUALLY DONE. OPERATORS CONFUSING.
    # (status_start, status_end) = common_string_leaf()
    # return_string = ("MODULE leaf_check_blackboard_variable_values(variables_exist, checks)" + os.linesep
    #                   + status_start
    #                   + "\t\t\t\t!(variables_exist) : failure;" + os.linesep  #at least some of the variables don't exist
    #                   + "\t\t\t\t(variables_exist) & (checks.result) : success;" + os.linesep  #passes the check
    #                   + "\t\t\t\t(variables_exist)) & !(checks.result) : failure;" + os.linesep  #fails the check
    #                   + status_end)
    # return return_string


def create_leaf_set_blackboard_variable(ignored_value = 0):
    pass
    # (status_start, status_end) = common_string_leaf()
    # return_string = ("MODULE leaf_set_blackboard_variable(blackboard, variable, nodes_with_access, value_creator, overwrite)" + os.linesep
    #                   + status_start
    #                   + "\t\tblackboard_var : integer;" + os.linesep
    #                   + "\t\tblackboard_var_exists : boolean;" + os.linesep
    #                   + "\t\tfree_var : integer;" + os.linesep
    #                   + "\tINVAR" + os.linesep
    #                   + "\t\tfree_var = blackboard_var;" + os.linesep
    #                   + "\t\tnext(blackboard_var) :=" + os.linesep
    #                   + "\t\t\tcase" + os.linesep
    #                   + "\t\t\t\t(overwrite) : value_creator.blackboard_var;" + os.linesep
    #                   + "\t\t\t\t!(blackboard_var_exists) : value_creator.blackboard_var;" + os.linesep
    #                   + "\t\t\t\t!(overwrite) & (blackboard_var_exists) : blackboard_var;" + os.linesep
    #                   #+ "\t\t\t\t!(active_leaf in nodes_with_access) : free_var;" + os.linesep
    #                   + "\t\t\t\t!(active_node in nodes_with_access) : next(free_var);" + os.linesep #so. the options are to use next(free_var), or remove the INVAR for free_var
    #                   + "\t\t\t\tTRUE : blackboard_var;" + os.linesep
    #                   + "\t\t\tesac;" + os.linesep
    #                   + "\t\tnext(blackboard_var_exists) :=" + os.linesep
    #                   + "\t\t\tcase" + os.linesep
    #                   + "\t\t\t\t(active_node = id) : TRUE;" + os.linesep
    #                   + "\t\t\t\t!(active_node in nodes_with_access) : {FALSE, TRUE};" + os.linesep
    #                   + "\t\t\t\tTRUE : blackboard_var_exists;" + os.linesep
    #                   + "\t\t\tesac;" + os.linesep
    #                   + "\t\t\t\t(overwrite) : success;" + os.linesep  #success if it actually set the value
    #                   + "\t\t\t\t!(blackboard_var_exists) : success;" + os.linesep  #success if it actually set the value
    #                   + "\t\t\t\t!(overwrite) & (blackboard_var_exists) : failure;" + os.linesep #failure if it didn't set anything
    #                   + status_end)
    # return return_string


def create_leaf_set_blackboard_variables(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_set_blackboard_variables(status_module)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := status_module.status;" + os.linesep
                     # + "\tDEFINE" + os.linesep
                     # + "\t\tstatus :=" + os.linesep
                     # + "\t\t\tcase" + os.linesep
                     # + "\t\t\t\t!(active) : invalid;" + os.linesep
                     # + "\t\t\t\tTRUE : status_module.status;" + os.linesep
                     # + "\t\t\tesac;" + os.linesep
                     )
    return return_string


def create_leaf_unset_blackboard_variable(ignored_value = 0):
    pass
    # (status_start, status_end) = common_string_leaf()
    # return_string = ("MODULE leaf_unset_blackboard_variable(variable, nodes_with_access)" + os.linesep
    #                   + status_start
    #                   + "\t\t\t\t(active_node = id) : success;" + os.linesep  #this always returns success
    #                   + status_end
    #                   + "\tVAR" + os.linesep
    #                   + "\t\tblackboard_var_exists : boolean;" + os.linesep #this is so we can set that the variable doesn't exist
    #                   + "\tASSIGN" + os.linesep
    #                   + "\t\tnext(blackboard_var_exists) :=" +os.linesep
    #                   + "\t\t\tcase" + os.linesep
    #                   + "\t\t\t\t(active_node = id) : FALSE;" + os.linesep #we just unset it
    #                   + "\t\t\t\t!(active_node in nodes_with_access) : {FALSE, TRUE};" + os.linesep #well, someone else with access might be setting or unsetting it.
    #                   + "\t\t\t\tTRUE : blackboard_var_exists;" + os.linesep #in a state with no access, so it won't change.
    #                   + "\t\t\tesac;" + os.linesep)
    # return return_string


def create_leaf_wait_for_blackboard_variable(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_wait_for_blackboard_variable(variable, blackboard)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := blackboard.variable_exists[variable] ? success : running;" + os.linesep  # passes the check
                     # + "\t\t\t\t(blackboard.variable_exists[variable]) : success;" + os.linesep  #variable exists
                     # + "\t\t\t\tTRUE : running;" + os.linesep  #variable does not yet exist
                     # + status_end
                     )
    return return_string


def create_leaf_wait_for_blackboard_variable_value(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_wait_for_blackboard_variable_value(blackboard, variable, check)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := (blackboard.variable_exists[variable]) & (check.result) ? success : running;" + os.linesep  # passes the check
                     # + "\t\t\t\t(blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                     # + "\t\t\t\tTRUE : running;" + os.linesep  #fails the check or doesn't exist
                     # + status_end
                     )
    return return_string


# -----------------------------------------------------------------
# basic example nodes


def create_leaf_count(ignored_value = 0):
    pass
    # variables needed: fail_until, running_until, success_until, reset
    # print('WARNING: reset currently resets whenever the root node ticks with success or failure. This does not match the behavior of py_trees')
    # (status_start, status_end) = common_string_leaf()
    # return_string = ("MODULE leaf_count(fail_until, running_until, success_until, reset)" + os.linesep
    #                   + status_start
    #                   + "\t\t\t\t(internal_node_count < fail_until) : failure;" + os.linesep  #internal_node_count <fail_until means we return failure
    #                   #if we reached this point, internal_node_count >= fail_until
    #                   + "\t\t\t\t(internal_node_count < running_until) : running;" + os.linesep #internal_node_count <running_until means we return running
    #                   #if we reached this point, internal_node_count >= fail_until and internal_node_count >= running_until
    #                   + "\t\t\t\t(internal_node_count < success_until) : success;" + os.linesep #internal_node_count <success_until means we return running
    #                   #if we reached this point, internal_node_count >= fail_until and internal_node_count >= running_until and internal_node_count >= success_until
    #                   + "\t\t\t\t(active_node = id) : failure;" + os.linesep #internal_node_count = max_internal at this point
    #                   + status_end
    #                   + "\t\tmax_internal := max(fail_until, max(running_until, success_until));" + os.linesep#define this so we don't have to have it copied everywhere.
    #                   + "\tVAR" + os.linesep
    #                   + "\t\tinternal_node_count : 0..max_internal;" + os.linesep  #define the internal count
    #                   + "\tASSIGN" + os.linesep
    #                   + "\t\tinit(internal_node_count) := 0;" + os.linesep  #initiate the internal internal_node_count to 0
    #                   + "\t\tnext(internal_node_count) :=" + os.linesep
    #                   + "\t\t\tcase" + os.linesep
    #                   + "\t\t\t\t(active_node = -1) & !(child_status[0] = running) & (reset) : 0;" + os.linesep #reset the internal_node_count if reset is true, and we invalidate the node
    #                   + "\t\t\t\t(active_node = id) : min(internal_node_count + 1, max_internal);" + os.linesep #update the internal node.
    #                   + "\t\t\t\tTRUE : internal_node_count;" + os.linesep #don't change the value otherwise
    #                   + "\t\t\tesac;" + os.linesep)
    # return return_string


def create_leaf_failure(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_failure()" + os.linesep
                     + status_start
                     + "\t\tinternal_status := failure;" + os.linesep
                     # + "\t\t\t\tTRUE : failure;" + os.linesep  #this always returns failure
                     # + status_end
                     )
    return return_string


def create_leaf_periodic(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_periodic(period)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := cycle;" + os.linesep
                     # + "\t\t\t\tTRUE : cycle;" + os.linesep  #this always returns cycle
                     # + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tcycle : {running, success, failure};" + os.linesep  # keep track of where we are in the cycle
                     + "\t\tinternal_node_count : 1..period;" + os.linesep  # keep track of where we are in the internal_node_count
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(cycle) := running;" + os.linesep  # initiate cycle
                     + "\t\tinit(internal_node_count) := 1;" + os.linesep  # initiate internal_node_count
                     + "\t\tnext(cycle) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : cycle;" + os.linesep  # do nothing if not active
                     + "\t\t\t\t(internal_node_count = period) & (cycle = running) : success;" + os.linesep  # if we've internal_node_counted up, time to go to success
                     + "\t\t\t\t(internal_node_count = period) & (cycle = success) : failure;" + os.linesep  # if we've internal_node_counted up, time to go to failure
                     + "\t\t\t\t(internal_node_count = period) & (cycle = failure) : running;" + os.linesep  # if we've internal_node_counted up, time to go to running
                     + "\t\t\t\tTRUE : cycle;" + os.linesep
                     + "\t\t\tesac;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep  # do nothing if not active
                     + "\t\t\t\t(internal_node_count = period) : 1;" + os.linesep  # if we reached the max, then we need to reset.
                     + "\t\t\t\t(internal_node_count < period) : min(internal_node_count + 1, period);" + os.linesep  # if we haven't reached it, internal_node_count up
                     + "\t\t\t\tTRUE : internal_node_count;" + os.linesep
                     + "\t\t\tesac;" + os.linesep
                     )
    return return_string


def create_leaf_running(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_running()" + os.linesep
                     + status_start
                     + "\t\tinternal_status := running;" + os.linesep
                     # + "\t\t\t\tTRUE : running;" + os.linesep  #this always returns failure
                     # + status_end
                     )
    return return_string


def create_leaf_status_sequence(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_status_sequence(sequence, sequence_length, eventually)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := (internal_node_count < sequence_length) ? sequence[internal_node_count] : eventually;" + os.linesep
                     # + "\t\t\t\t(internal_node_count < sequence_length) : sequence[internal_node_count];" + os.linesep  #return where we are in the sequence
                     # + "\t\t\t\tTRUE : eventually;" + os.linesep  #return where we are in the sequence
                     # + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tinternal_node_count : 0..sequence_length;" + os.linesep
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(internal_node_count) := 0;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep  # do nothing if not active
                     + "\t\t\t\t(eventually = invalid) & (internal_node_count + 1 = sequence_length) : 0;" + os.linesep  # if we reached the max and we don't have an eventuality, reset
                     + "\t\t\t\tTRUE : min(internal_node_count + 1, sequence_length);" + os.linesep  # if we aren't resetting, then increase
                     + "\t\t\tesac;" + os.linesep
                     )
    return return_string


def create_leaf_success(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_success()" + os.linesep
                     + status_start
                     + "\t\tinternal_status := success;" + os.linesep
                     # + "\tCONSTANTS" + os.linesep
                     # + "\t\tsuccess, failure, running, invalid;" + os.linesep
                     # + "\tDEFINE" + os.linesep
                     # #+ "\t\tstatus := active ? success : invalid;" + os.linesep
                     # + "\t\tstatus := success;" + os.linesep
                     )
    return return_string


def create_leaf_success_every_n(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_success_every_n(n)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := (internal_node_count = n) ? success : failure;" + os.linesep
                     # + "\t\t\t\t(internal_node_count = n) : success;" + os.linesep  #return success every nth time
                     # + "\t\t\t\tTRUE : failure;" + os.linesep  #return failure otherwise
                     # + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tinternal_node_count : 1..n;" + os.linesep
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(internal_node_count) := 1;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep  # hold if not active
                     + "\t\t\t\t(internal_node_count = n) : 1;" + os.linesep  # if we reached the max, then we need to reset.
                     + "\t\t\t\tTRUE : min(internal_node_count + 1, n);" + os.linesep  # if we haven't reached it, internal_node_count up
                     + "\t\t\tesac;" + os.linesep)
    return return_string


def create_leaf_tick_counter(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_tick_counter(duration, completion_status)" + os.linesep
                     + status_start
                     + "\t\tinternal_status := (internal_node_count < duration) ? running : completion_status;" + os.linesep
                     # + "\t\t\t\t(internal_node_count < duration) : running;" + os.linesep  #return running until we internal_node_count up
                     # + "\t\t\t\tTRUE : completion_status;" + os.linesep  #return running until we internal_node_count up
                     # + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tinternal_node_count : 0..duration;" + os.linesep
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(internal_node_count) := 0;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep  # hold if not active
                     + "\t\t\t\tTRUE : min(internal_node_count + 1, duration);" + os.linesep  # if we haven't reached it, internal_node_count up
                     + "\t\t\tesac;" + os.linesep)
    return return_string


# -----------------------------------------------------------------


def create_leaf_non_blocking(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_non_blocking()" + os.linesep
                     + status_start
                     + "\t\tinternal_status := input_status;" + os.linesep
                     + "\tVAR" + os.linesep
                     + "\t\tinput_status : {success, failure};" + os.linesep
                     # + "\tASSIGN" + os.linesep
                     # + "\t\tinit(input_status) := success;" + os.linesep
                     # + "\tCONSTANTS" + os.linesep
                     # + "\t\tsuccess, failure, running, invalid;" + os.linesep
                     # + "\tVAR" + os.linesep
                     # + "\t\tinput_status : {success, failure};" + os.linesep
                     # + "\tDEFINE" + os.linesep
                     # #+ "\t\tstatus := active ? input_status : invalid;" + os.linesep
                     # + "\t\tstatus := input_status;" + os.linesep
                     )
    return return_string


# -----------------------------------------------------------------


def create_leaf_timer(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_timer()" + os.linesep
                     + status_start
                     + "\t\tinternal_status := input_status;" + os.linesep
                     + "\tVAR" + os.linesep
                     + "\t\tinput_status : {success, running};" + os.linesep
                     # + "\tASSIGN" + os.linesep
                     # + "\t\tinit(input_status) := success;" + os.linesep
                     # + "\tCONSTANTS" + os.linesep
                     # + "\t\tsuccess, failure, running, invalid;" + os.linesep
                     # + "\tVAR" + os.linesep
                     # + "\t\tinput_status : {success, running};" + os.linesep
                     # + "\tDEFINE" + os.linesep
                     # #+ "\t\tstatus := active ? input_status : invalid;" + os.linesep
                     # + "\t\tstatus := input_status;" + os.linesep
                     )
    return return_string


# -----------------------------------------------------------------
# a default node


def create_leaf_default(ignored_value = 0):
    (status_start, status_end) = common_string_leaf()
    return_string = ("MODULE leaf_default()" + os.linesep
                     + status_start
                     + "\t\tinternal_status := input_status;" + os.linesep
                     + "\tVAR" + os.linesep
                     + "\t\tinput_status : {success, running, failure};" + os.linesep
                     # + "\tASSIGN" + os.linesep
                     # + "\t\tinit(input_status) := success;" + os.linesep
                     # + "\tCONSTANTS" + os.linesep
                     # + "\t\tsuccess, failure, running, invalid;" + os.linesep
                     # + "\tVAR" + os.linesep
                     # + "\t\tinput_status : {success, running, failure};" + os.linesep
                     # + "\tDEFINE" + os.linesep
                     # #+ "\t\tstatus := active ? input_status : invalid;" + os.linesep
                     # + "\t\tstatus := input_status;" + os.linesep
                     )
    return return_string




def common_string_leaf():
    status_start = ("\tCONSTANTS" + os.linesep
                    + "\t\tsuccess, failure, running, invalid;" + os.linesep
                    + "\tDEFINE" + os.linesep
                    + "\t\tstatus := active ? internal_status : invalid;" + os.linesep
                    # + "\t\tstatus :=" + os.linesep
                    # + "\t\t\tcase" + os.linesep
                    # + "\t\t\t\t!(active) : invalid;" + os.linesep #this should be the only invalid case.
                    )
    status_end = ("\t\t\tesac;" + os.linesep)
    return (status_start, status_end)


# -----------------------------------------------------------------
# Decorators

def create_decorator_condition(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_condition(child_0, status)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t(child_0.status = status) : success;" + os.linesep  # it matches the status
                     + "\t\t\t\tTRUE : running;" + os.linesep  # it doesn't match the status
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_eternal_guard(ignored_value = 0):
    pass


def create_decorator_inverter(ignored_value = 0):
    (status_start, status_end, active, active_end, children) = common_string_decorator(1)
    return_string = ("MODULE decorator_inverter(child_0)" + os.linesep
                     + status_start
                     # + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t(child_0.status = failure) : success;" + os.linesep  # failure becomes success
                     + "\t\t\t\t(child_0.status = success) : failure;" + os.linesep  # success becomes failure
                     + "\t\t\t\tTRUE : running;" + os.linesep  # must have been running
                     + status_end
                     + active[0]  # handles (if this node not active, child_0 not active)
                     + active_end  # handle (otherwise, child_0 active)
                     )
    return return_string


def create_decorator_one_shot(ignored_value = 0):
    return
    # (status_start, status_end) = common_string(number_of_nodes, False, False)#this uses a custom child_0 direction. can't use the standard decorator
    # return_string = ("MODULE decorator_one_shot(child_0,descendants, child_0_status, on_successful_completion_only)" + os.linesep
    #                   + status_start
    #                  + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
    #                   + "\t\tchild_0_completed : boolean;" + os.linesep #keep track of if the child_0 has completed yet
    #                   + "\t\tchild_0_final : {success, failure};" + os.linesep #keep track of the child_0's final result
    #                   + "\t\tinit(child_0_completed) := FALSE;" + os.linesep #uh...yeah doesn't start completed
    #                   + "\t\tinit(child_0_final) := failure;" + os.linesep #this included not because it needs to be, but because it should help limit the state space nuXmv has to cover
    #                   + "\t\tnext(child_0_completed) :=" + os.linesep
    #                   + "\t\t\tcase" + os.linesep
    #                   + "\t\t\t\t(child_0.status = success) : TRUE;" + os.linesep#set to true if child_0 succeeded
    #                   + "\t\t\t\t(child_0.status = failure) & !(on_successful_completion_only) : TRUE;" + os.linesep#also set to true if child_0 failed, but that's ok
    #                   + "\t\t\t\tTRUE : child_0_completed;" + os.linesep#otherwise, hold
    #                   + "\t\t\tesac;" + os.linesep
    #                   + "\t\tnext(child_0_final) :=" + os.linesep
    #                   + "\t\t\tcase" + os.linesep
    #                   + "\t\t\t\t(child_0.status = success) : success;" + os.linesep#if we returned success, explicitly set it to success
    #                   + "\t\t\t\tTRUE : child_0_final;" + os.linesep #otherwise, keep it unchanging. If failure was a valid exit, that's what we were already on
    #                   + "\t\t\tesac;" + os.linesep
    #                   + "\t\t\t\t(child_0_completed) : child_0_final;" + os.linesep  #child_0 completed. we're done.
    #                   + "\t\t\t\t!(child_0_completed) : child_0.status;" +os.linesep
    #                   + status_end
    #                   + "\t\t\t\t(child_0_completed) : parent;" + os.linesep #child_0 already finished. time to leave
    #                   + "\t\t\t\t!(child_0_completed) & (child_0.status = invalid) : child_0;" + os.linesep #if the child_0 has not yet been ran, go run the child_0.
    #                   + "\t\t\t\t!(child_0_completed) & !(child_0.status = invalid) : parent;" + os.linesep # child_0 already ran. time to return to parent
    #                   + "\t\t\t\tTRUE : -1.." + str(number_of_nodes) + ";" + os.linesep #if this isn't the active node, allow it to bounce around
    #                   + "\t\t\tesac;" + os.linesep
    #                   + os.linesep)
    # return return_string


def create_decorator_status_to_blackboard(ignored_value = 0):
    pass


def create_decorator_timeout(ignored_value = 0):
    pass
"""
