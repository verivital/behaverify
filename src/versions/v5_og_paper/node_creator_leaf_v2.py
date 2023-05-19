import os

#-----------------------------------------------------------------
#common node parts kept here to increase reusage
def common_string(number_of_nodes):
    status_define = ("\tCONSTANTS" + os.linesep
                     + "\t\tsuccess, failure, running, invalid;" + os.linesep
                     + "\tDEFINE" + os.linesep 
                     + "\t\tstatus :=" + os.linesep 
                     + "\t\t\tcase" + os.linesep)
    status_end = ("\t\t\t\tTRUE : invalid;" + os.linesep 
                  + "\t\t\tesac;" + os.linesep)
    return (status_define, status_end)

#-----------------------------------------------------------------
#decorators
def create_decorator_condition(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_condition(relevant_child, relevant_status, status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t(relevant_status = status) : success;" + os.linesep  #it matches the status
                      + "\t\t\t\t!(relevant_status = status) : running;" + os.linesep  #it doesn't match the status
                      + status_end)
    return return_string
def create_decorator_eternal_guard(number_of_nodes):
    pass
def create_decorator_inverter(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_inverter(relevant_child, relevant_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t((relevant_status = invalid) | (relevant_status = running)) : relevant_status;" + os.linesep  #child is either running or invalid. either way, that's what we are
                      + "\t\t\t\t(relevant_status = failure) : success;" + os.linesep  #failure becomes success
                      + "\t\t\t\t(relevant_status = success) : failure;" + os.linesep  #success becomes failure
                      + status_end)
    return return_string
def create_decorator_one_shot(number_of_nodes):
    pass
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes, False, False)#this uses a custom child direction. can't use the standard decorator
    return_string += ("MODULE decorator_one_shot(relevant_child, relevant_status,descendants, relevant_status, on_successful_completion_only)" + os.linesep
                      + status_define
                      + "\t\tchild_completed : boolean;" + os.linesep #keep track of if the child has completed yet
                      + "\t\tchild_final : {success, failure};" + os.linesep #keep track of the child's final result
                      + "\t\tinit(child_completed) := FALSE;" + os.linesep #uh...yeah doesn't start completed
                      + "\t\tinit(child_final) := failure;" + os.linesep #this included not because it needs to be, but because it should help limit the state space nuXmv has to cover
                      + "\t\tnext(child_completed) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(relevant_status = success) : TRUE;" + os.linesep#set to true if child succeeded
                      + "\t\t\t\t(relevant_status = failure) & !(on_successful_completion_only) : TRUE;" + os.linesep#also set to true if child failed, but that's ok
                      + "\t\t\t\tTRUE : child_completed;" + os.linesep#otherwise, hold
                      + "\t\t\tesac;" + os.linesep
                      + "\t\tnext(child_final) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(relevant_status = success) : success;" + os.linesep#if we returned success, explicitly set it to success
                      + "\t\t\t\tTRUE : child_final;" + os.linesep #otherwise, keep it unchanging. If failure was a valid exit, that's what we were already on
                      + "\t\t\tesac;" + os.linesep
                      + "\t\t\t\t(child_completed) : child_final;" + os.linesep  #child completed. we're done.
                      + "\t\t\t\t!(child_completed) : relevant_status;" +os.linesep
                      + status_end
                      + "\t\t\t\t(child_completed) : parent;" + os.linesep #child already finished. time to leave
                      + "\t\t\t\t!(child_completed) & (relevant_status = invalid) : child;" + os.linesep #if the child has not yet been ran, go run the child.
                      + "\t\t\t\t!(child_completed) & !(relevant_status = invalid) : parent;" + os.linesep # child already ran. time to return to parent
                      + "\t\t\t\tTRUE : -1.." + str(number_of_nodes) + ";" + os.linesep #if this isn't the active node, allow it to bounce around
                      + "\t\t\tesac;" + os.linesep 
                      + os.linesep)
    return return_string
def create_decorator_status_to_blackboard(number_of_nodes):
    pass
def create_decorator_timeout(number_of_nodes):
    pass
def create_decorator_failure_is_running(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_failure_is_running(relevant_child, relevant_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t!(relevant_status = failure) : relevant_status;" + os.linesep  #no matter what, we match the child
                      + "\t\t\t\t(relevant_status = failure) : running;" + os.linesep  #unless it failed. then we pretend it's still running
                      + status_end)
    return return_string
def create_decorator_failure_is_success(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_failure_is_success(relevant_child, relevant_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t!(relevant_status = failure) : relevant_status;" + os.linesep  #no matter what, we match the child
                      + "\t\t\t\t(relevant_status = failure) : success;" + os.linesep  #unless it failed. then we pretend it succeeded
                      + status_end)
    return return_string
def create_decorator_running_is_failure(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_running_is_failure(relevant_child, relevant_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t!(relevant_status = running) : relevant_status;" + os.linesep  #no matter what, we match the child
                      + "\t\t\t\t(relevant_status = running) : failure;" + os.linesep  #unless it's running. that's a fail
                      + status_end)
    return return_string
def create_decorator_running_is_success(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_running_is_success(relevant_child, relevant_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t!(relevant_status = running) : relevant_status;" + os.linesep  #no matter what, we match the child
                      + "\t\t\t\t(relevant_status = running) : success;" + os.linesep  #unless it running. that's a success
                      + status_end)
    return return_string
def create_decorator_success_is_failure(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_success_is_failure(relevant_child, relevant_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t!(relevant_status = success) : relevant_status;" + os.linesep  #no matter what, we match the child
                      + "\t\t\t\t(relevant_status = success) : failure;" + os.linesep  #we won't let you succeed
                      + status_end)
    return return_string
def create_decorator_success_is_running(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE decorator_success_is_running(relevant_child, relevant_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(relevant_child < 0) : invalid;" + os.linesep #must be considering the child.
                      + "\t\t\t\t!(relevant_status = success) : relevant_status;" + os.linesep  #no matter what, we match the child
                      + "\t\t\t\t(relevant_status = success) : running;" + os.linesep  #we won't let you succeed
                      + status_end)
    return return_string




#-----------------------------------------------------------------
#the blackboard
def create_names_module(variable_to_int, nodes):
    return_string=''
    if variable_to_int:
        return_string += ("MODULE define_variables" + os.linesep
                          + "\tDEFINE" + os.linesep)
        for variable in variable_to_int:
            return_string += ("\t\t" + variable + " := " + str(variable_to_int[variable]) + ";" + os.linesep)
    return_string += ("MODULE define_nodes" + os.linesep
                      + "\tDEFINE" + os.linesep)
    for i in range(len(nodes)):
        return_string += ("\t\t" + nodes[i][2] + " := " + str(i) + ";" + os.linesep)
                          
    return return_string
#def create_blackboard(variable_to_int, variable_access, nodes):
def create_blackboard(int_to_variable, variable_to_int, variable_access, nodes, no_seperate_modules, min_val = 0, max_val = 1):
    return_string=''
    return_string += ("MODULE blackboard_module(active_node, node_names, variable_names, random_status, statuses)" + os.linesep
                      + "\tCONSTANTS" + os.linesep
                      + "\t\tsuccess, failure, running, invalid;" + os.linesep
                      + "\tDEFINE" + os.linesep)
    #if variable_to_int:
    if int_to_variable and not no_seperate_modules:
        var_array_string = ("\t\tvariables := [")
        var_exist_string = ("\t\tvariable_exists := [")
        decl_string = ("\tVAR" + os.linesep)
        #for variable in variable_to_int:
        for i in range(len(int_to_variable)):
            variable = int_to_variable[i]
            var_array_string += (variable + "_SET." + variable + ", ")
            var_exist_string += (variable + "_SET." + variable + "_exists, ")
            set_string="{"
            if variable_to_int[variable] in variable_access:
                for node in variable_access[variable_to_int[variable]]:
                    set_string += str(node) + ", "
            else:
                set_string += "-1, "
            decl_string += ("\t\t" + variable + "_SET : " + variable + "_SET_module(active_node, " + set_string[0:-2] + "}, variables, variable_exists, node_names, variable_names, statuses);" + os.linesep)
        return_string += (var_array_string[0:-2] + "];" + os.linesep
                          + var_exist_string[0:-2] + "];" + os.linesep
                          + decl_string)
    elif int_to_variable:
        var_array_string = ("\t\tvariables := [")
        var_exist_string = ("\t\tvariable_exists := [")
        exist_define = ""
        decl_string = ("\tVAR" + os.linesep)
        assign_string = ("\tASSIGN" + os.linesep)
        poss_values="{"
        for i in range(min_val, max_val+1):
            poss_values = poss_values + str(i) + ", "
        poss_values = poss_values[0:-2] + "}"
        #for variable in variable_to_int:
        for i in range(len(int_to_variable)):
            variable = int_to_variable[i]
            var_array_string += (variable + ", ")
            var_exist_string += (variable + "_exists, ")
            set_string=""
            if variable_to_int[variable] in variable_access:
                for node in variable_access[variable_to_int[variable]]:
                    set_string += "node_names." + nodes[node][2] + ", "
            else:
                set_string += "-1, "
            exist_define += "\t\t" + variable + "_exists := TRUE;" + os.linesep
            decl_string += ("\t\t" + variable + " : " + str(min_val) + ".." + str(max_val) + ";" + os.linesep)
            assign_string += ("\t\tinit(" + variable + ") := " + str(min_val) +";" + os.linesep
                              + "\t\tnext(" + variable + ") := " + os.linesep
                              + "\t\t\tcase" + os.linesep
            )
            if variable_to_int[variable] in variable_access:
                for node in variable_access[variable_to_int[variable]]:
                    assign_string += "\t\t\t\t(active_node = node_names." + nodes[node][2] + ") & (statuses[relevant_child] = success) : " + poss_values + ";" + os.linesep
            assign_string +=(
                + "\t\t\t\tTRUE : " + variable + ";" + os.linesep
                + "\t\t\tesac;" + os.linesep
            )
        return_string += (var_array_string[0:-2] + "];" + os.linesep
                          + var_exist_string[0:-2] + "];" + os.linesep
                          + exist_define
                          + decl_string
                          + assign_string
        )
        
                          
    return return_string
#-----------------------------------------------------------------
#blackboard nodes
def create_node_blackboard_to_status(number_of_nodes, variable):
    pass
def create_node_check_blackboard_variable_exists(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_check_blackboard_variable_exists(active_node, id, blackboard, variable)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & (blackboard.variable_exists[variable]) : success;" + os.linesep  #the variable exists
                      + "\t\t\t\t(active_node = id) & !(blackboard.variable_exists[variable]) : failure;" + os.linesep  #it doesn't
                      + status_end)
    return return_string

def create_node_check_blackboard_variable_value(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_check_blackboard_variable_value(active_node, id, blackboard, variable, check)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & !(blackboard.variable_exists[variable]) : failure;" + os.linesep  #the variable doesn't exist
                      + "\t\t\t\t(active_node = id) & (blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                      + "\t\t\t\t(active_node = id) & (blackboard.variable_exists[variable]) & !(check.result) : failure;" + os.linesep  #fails the check
                      + status_end)
    return return_string
def create_node_check_blackboard_variable_values(number_of_nodes, variables, checks, operators):
    pass
    #NOT ACTUALLY DONE. OPERATORS CONFUSING.
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_check_blackboard_variable_values(active_node, id, variables_exist, checks)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & !(variables_exist) : failure;" + os.linesep  #at least some of the variables don't exist
                      + "\t\t\t\t(active_node = id) & (variables_exist) & (checks.result) : success;" + os.linesep  #passes the check
                      + "\t\t\t\t(active_node = id) & (variables_exist)) & !(checks.result) : failure;" + os.linesep  #fails the check
                      + status_end)
    return return_string
def create_node_set_blackboard_variable(number_of_nodes):
    pass
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_set_blackboard_variable(active_node, id, blackboard, variable, nodes_with_access, value_creator, overwrite)" + os.linesep
                      + status_define
                      + "\t\tblackboard_var : integer;" + os.linesep
                      + "\t\tblackboard_var_exists : boolean;" + os.linesep
                      + "\t\tfree_var : integer;" + os.linesep
                      + "\tINVAR" + os.linesep
                      + "\t\tfree_var = blackboard_var;" + os.linesep
                      + "\t\tnext(blackboard_var) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) & (overwrite) : value_creator.blackboard_var;" + os.linesep
                      + "\t\t\t\t(active_node = id) & !(blackboard_var_exists) : value_creator.blackboard_var;" + os.linesep
                      + "\t\t\t\t(active_node = id) & !(overwrite) & (blackboard_var_exists) : blackboard_var;" + os.linesep
                      #+ "\t\t\t\t!(active_node = id) & (active_node in nodes_with_access) : free_var;" + os.linesep
                      + "\t\t\t\t!(active_node = id) & (active_node in nodes_with_access) : next(free_var);" + os.linesep #so. the options are to use next(free_var), or remove the INVAR for free_var
                      + "\t\t\t\tTRUE : blackboard_var;" + os.linesep
                      + "\t\t\tesac;" + os.linesep
                      + "\t\tnext(blackboard_var_exists) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) : TRUE;" + os.linesep
                      + "\t\t\t\t!(active_node = id) & (active_node in nodes_with_access) : {FALSE, TRUE};" + os.linesep
                      + "\t\t\t\tTRUE : blackboard_var_exists;" + os.linesep
                      + "\t\t\tesac;" + os.linesep
                      + "\t\t\t\t(active_node = id) & (overwrite) : success;" + os.linesep  #success if it actually set the value
                      + "\t\t\t\t(active_node = id) & !(blackboard_var_exists) : success;" + os.linesep  #success if it actually set the value
                      + "\t\t\t\t(active_node = id) & !(overwrite) & (blackboard_var_exists) : failure;" + os.linesep #failure if it didn't set anything
                      + status_end)
    return return_string
def create_node_set_blackboard_variables(number_of_nodes):
    return_string=''
    return_string += ("MODULE node_set_blackboard_variables(active_node, id, status_module)" + os.linesep
                      + "\tDEFINE" + os.linesep
                      + "\t\tstatus := status_module.status;" + os.linesep)
    return return_string
def create_node_unset_blackboard_variable(number_of_nodes):
    pass
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_unset_blackboard_variable(active_node, id, variable, nodes_with_access)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) : success;" + os.linesep  #this always returns success
                      + status_end
                      + "\tVAR" + os.linesep
                      + "\t\tblackboard_var_exists : boolean;" + os.linesep #this is so we can set that the variable doesn't exist
                      + "\tASSIGN" + os.linesep
                      + "\t\tnext(blackboard_var_exists) :=" +os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) : FALSE;" + os.linesep #we just unset it
                      + "\t\t\t\t!(active_node = id) & (active_node in nodes_with_access) : {FALSE, TRUE};" + os.linesep #well, someone else with access might be setting or unsetting it.
                      + "\t\t\t\tTRUE : blackboard_var_exists;" + os.linesep #in a state with no access, so it won't change.
                      + "\t\t\tesac;" + os.linesep)
    return return_string
def create_node_wait_for_blackboard_variable(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_wait_for_blackboard_variable(active_node, id, variable, blackboard)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & (blackboard.variable_exists[variable]) : success;" + os.linesep  #variable exists
                      + "\t\t\t\t(active_node = id) & !(blackboard.variable_exists[variable]) : running;" + os.linesep  #variable does not yet exist
                      + status_end)
    return return_string
def create_node_wait_for_blackboard_variable_value(number_of_nodes, variable, value):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_wait_for_blackboard_variable_value(active_node, id, blackboard, variable, check)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & !(blackboard.variable_exists[variable]) : running;" + os.linesep  #the variable doesn't exist
                      + "\t\t\t\t(active_node = id) & (blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                      + "\t\t\t\t(active_node = id) & (blackboard.variable_exists[variable]) & !(check.result) : running;" + os.linesep  #fails the check
                      + status_end)
    return return_string
#-----------------------------------------------------------------
#basic example nodes
def create_node_count(number_of_nodes):
    pass
    #variables needed: fail_until, running_until, success_until, reset
    print('WARNING: reset currently resets whenever the root node ticks with success or failure. This does not match the behavior of py_trees')
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_count(active_node, id, fail_until, running_until, success_until, reset)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & (internal_node_count < fail_until) : failure;" + os.linesep  #internal_node_count <fail_until means we return failure
                      #if we reached this point, internal_node_count >= fail_until
                      + "\t\t\t\t(active_node = id) & (internal_node_count < running_until) : running;" + os.linesep #internal_node_count <running_until means we return running
                      #if we reached this point, internal_node_count >= fail_until and internal_node_count >= running_until
                      + "\t\t\t\t(active_node = id) & (internal_node_count < success_until) : success;" + os.linesep #internal_node_count <success_until means we return running
                      #if we reached this point, internal_node_count >= fail_until and internal_node_count >= running_until and internal_node_count >= success_until
                      + "\t\t\t\t(active_node = id) : failure;" + os.linesep #internal_node_count = max_internal at this point
                      + status_end
                      + "\t\tmax_internal := max(fail_until, max(running_until, success_until));" + os.linesep#define this so we don't have to have it copied everywhere.
                      + "\tVAR" + os.linesep 
                      + "\t\tinternal_node_count : 0..max_internal;" + os.linesep  #define the internal count
                      + "\tASSIGN" + os.linesep
                      + "\t\tinit(internal_node_count) := 0;" + os.linesep  #initiate the internal internal_node_count to 0
                      + "\t\tnext(internal_node_count) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = -1) & !(relevant_status[0] = running) & (reset) : 0;" + os.linesep #reset the internal_node_count if reset is true, and we invalidate the node
                      + "\t\t\t\t(active_node = id) : min(internal_node_count + 1, max_internal);" + os.linesep #update the internal node.
                      + "\t\t\t\tTRUE : internal_node_count;" + os.linesep #don't change the value otherwise
                      + "\t\t\tesac;" + os.linesep)
    return return_string

def create_node_failure(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_failure(active_node, id)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) : failure;" + os.linesep  #this always returns failure
                      + status_end)
    return return_string

def create_node_periodic(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_periodic(active_node, id, period)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) : cycle;" + os.linesep  #this always returns cycle
                      + status_end
                      + "\tVAR" + os.linesep
                      + "\t\tcycle : {running, success, failure};" + os.linesep #keep track of where we are in the cycle
                      + "\t\tinternal_node_count : 1..period;" + os.linesep #keep track of where we are in the internal_node_count
                      + "\tASSIGN" + os.linesep
                      + "\t\tinit(cycle) := running;" + os.linesep #initiate cycle
                      + "\t\tinit(internal_node_count) := 1;" + os.linesep #initiate internal_node_count
                      + "\t\tnext(cycle) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) & (internal_node_count = period) & (cycle = running) : success;" + os.linesep #if we've internal_node_counted up, time to go to success
                      + "\t\t\t\t(active_node = id) & (internal_node_count = period) & (cycle = success) : failure;" + os.linesep #if we've internal_node_counted up, time to go to failure
                      + "\t\t\t\t(active_node = id) & (internal_node_count = period) & (cycle = failure) : running;" + os.linesep #if we've internal_node_counted up, time to go to running
                      + "\t\t\t\tTRUE : cycle;" + os.linesep
                      + "\t\t\tesac;" + os.linesep
                      + "\t\tnext(internal_node_count) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) & (internal_node_count = period) : 1;" + os.linesep #if we reached the max, then we need to reset.
                      + "\t\t\t\t(active_node = id) & (internal_node_count < period) : min(internal_node_count + 1, period);" + os.linesep #if we haven't reached it, internal_node_count up
                      + "\t\t\t\tTRUE : internal_node_count;" + os.linesep
                      + "\t\t\tesac;" + os.linesep)
    return return_string


def create_node_running(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_running(active_node, id)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) : running;" + os.linesep  #this always returns failure
                      + status_end)
    return return_string

def create_node_status_sequence(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_status_sequence(active_node, id, sequence, sequence_length, eventually)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & (internal_node_count < sequence_length) : sequence[internal_node_count];" + os.linesep  #return where we are in the sequence
                      + "\t\t\t\t(active_node = id) : eventually;" + os.linesep  #return where we are in the sequence
                      + status_end
                      + "\tVAR" + os.linesep
                      + "\t\tinternal_node_count : 0..sequence_length;" + os.linesep
                      + "\tASSIGN" + os.linesep
                      + "\t\tinit(internal_node_count) := 0;" + os.linesep
                      + "\t\tnext(internal_node_count) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) & (eventually = invalid) & (internal_node_count+1 = sequence_length) : 0;" + os.linesep #if we reached the max and we don't have an eventuality, reset
                      + "\t\t\t\t(active_node = id) : min(internal_node_count + 1, sequence_length);" + os.linesep #if we aren't resetting, then increase
                      + "\t\t\t\tTRUE : internal_node_count;" + os.linesep
                      + "\t\t\tesac;" + os.linesep)
    return return_string

def create_node_success(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_success(active_node, id)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) : success;" + os.linesep  #this always returns success
                      + status_end)
    return return_string

def create_node_success_every_n(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_success_every_n(active_node, id, n)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & (internal_node_count = n) : success;" + os.linesep  #return success every nth time
                      + "\t\t\t\t(active_node = id) & !(internal_node_count = n) : failure;" + os.linesep  #return failure otherwise
                      + status_end
                      + "\tVAR" + os.linesep
                      + "\t\tinternal_node_count : 1..n;" + os.linesep
                      + "\tASSIGN" + os.linesep
                      + "\t\tinit(internal_node_count) := 1;" + os.linesep
                      + "\t\tnext(internal_node_count) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) & (internal_node_count = n) : 1;" + os.linesep #if we reached the max, then we need to reset.
                      + "\t\t\t\t(active_node = id) : min(internal_node_count + 1, n);" + os.linesep #if we haven't reached it, internal_node_count up
                      + "\t\t\t\tTRUE : internal_node_count;" + os.linesep
                      + "\t\t\tesac;" + os.linesep)
    return return_string

def create_node_tick_counter(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_tick_counter(active_node, id, duration, completion_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & (internal_node_count < duration) : running;" + os.linesep  #return running until we internal_node_count up
                      + "\t\t\t\t(active_node = id) & (internal_node_count = duration) : completion_status;" + os.linesep  #return running until we internal_node_count up
                      + status_end
                      + "\tVAR" + os.linesep
                      + "\t\tinternal_node_count : 0..duration;" + os.linesep
                      + "\tASSIGN" + os.linesep
                      + "\t\tinit(internal_node_count) := 0;" + os.linesep
                      + "\t\tnext(internal_node_count) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) & (internal_node_count < duration) : internal_node_count + 1;" + os.linesep #if we haven't reached it, internal_node_count up
                      + "\t\t\t\tTRUE : internal_node_count;" + os.linesep #in all othercases, stay the same.
                      + "\t\t\tesac;" + os.linesep)
    return return_string


#-----------------------------------------------------------------

def create_node_timer(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_timer(active_node, id, random_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) & (random_status = success) : success;" + os.linesep  #return any status, just not failure
                      + "\t\t\t\t(active_node = id) : running;" + os.linesep  #return any status
                      + status_end)
    return return_string


#-----------------------------------------------------------------
#a default node
def create_node_default(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_default(active_node, id, random_status)" + os.linesep
                      + status_define
                      + "\t\t\t\t(active_node = id) : random_status;" + os.linesep #return any status
                      + status_end)
    return return_string

#-----------------------------------------------------------------
#composite nodes
def create_node_selector(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_selector(relevant_child, relevant_status, last_child)" + os.linesep 
                      + status_define
                      + "\t\t\t\t(last_child = -2) : failure;" + os.linesep#no children, return default
                      + "\t\t\t\t(relevant_child <= 0) : invalid;" + os.linesep#current node is not our descendant, we're invalid
                      + "\t\t\t\t(relevant_status = running) : running;" + os.linesep#a child returned running. therefore, we are running
                      + "\t\t\t\t(relevant_status = success) : success;" + os.linesep#a child returned success. therefore, we are success
                      + "\t\t\t\t(last_child = relevant_child) & (relevant_status = failure) : failure;" + os.linesep#if it's the last child, we have failure
                      + status_end)
    return return_string

def create_node_sequence(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_sequence(relevant_child, relevant_status, last_child)" + os.linesep 
                      + status_define
                      + "\t\t\t\t(last_child = -2) : success;" + os.linesep#no children, return default
                      + "\t\t\t\t(relevant_child <= 0) : invalid;" + os.linesep#current node is not our descendant, we're invalid
                      + "\t\t\t\t(relevant_status = running) : running;" + os.linesep#a child returned running. therefore, we are running
                      + "\t\t\t\t(relevant_status = failure) : failure;" + os.linesep#a child returned failure, therefore, we are failure
                      + "\t\t\t\t(last_child = relevant_child) & (relevant_status = success) : success;" + os.linesep#if it's the last child, we have success
                      + status_end)
    return return_string


def create_node_parallel(number_of_nodes):
    return_string=''
    (status_define, status_end) = common_string(number_of_nodes)
    return_string += ("MODULE node_parallel(relevant_child, relevant_status, last_child, reset, synchronized, parallel_policy_all)" + os.linesep
                      + status_define
                      + "\t\t\t\t(last_child = -2) : success;" + os.linesep#no children, return default
                      + "\t\t\t\t(relevant_child <= 0) : invalid;" + os.linesep#current node is not our descendant, we're invalid
                      + "\t\t\t\t!(relevant_child = last_child) : invalid;" + os.linesep#are we on the last child
                      #we are now on the last child
                      + "\t\t\t\t(relevant_status = invalid) : invalid;" + os.linesep#if child is invalid, then we are invalid (this is handled by default case in sel, seq)
                      + "\t\t\t\t((cur_status = failure) | (relevant_status = failure)) : failure;" + os.linesep#if we had any failures, return failure
                      #at this point, on last child, all children success or running
                      + "\t\t\t\t(cur_status = running) & (relevant_status = running) : running;" + os.linesep #we were going to return running, and the last status was running, return running
                      #at this point, on last child, no failure, at least one not running (means success)
                      + "\t\t\t\t!(parallel_policy_all) : success;" + os.linesep#since at least one success, and not all needed, success
                      #at this point, on last child, no failure, at least one success, need all for success
                      + "\t\t\t\t(cur_status = success) & (relevant_status = success) : success;" + os.linesep#all success
                      #at this point, on last child, at least one success, and one running, all needed for success
                      + "\t\t\t\tTRUE : running;" + os.linesep#the last option.
                      + "\t\t\tesac;" + os.linesep
                      + "\tVAR" + os.linesep
                      + "\t\tcur_status : {failure, running, success};" + os.linesep
                      + "\tASSIGN" + os.linesep
                      + "\t\tinit(cur_status) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(parallel_policy_all) : success;" + os.linesep
                      + "\t\t\t\tTRUE : running;" + os.linesep
                      + "\t\t\tesac;" + os.linesep
                      + "\t\tnext(cur_status) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      #reset
                      + "\t\t\t\treset & (parallel_policy_all) : success;" + os.linesep#reset only if we're not still running.
                      + "\t\t\t\treset & !(parallel_policy_all) : running;" + os.linesep#reset only if we're not still running. (reset calculated elsewhere)
                      + "\t\t\t\t(relevant_child < 0) : cur_status;" + os.linesep #not currently our child. hold value
                      
                      + "\t\t\t\t((relevant_status = failure) | (cur_status = failure)) : failure;" + os.linesep#if a failure is present, stay on failure.
                      + "\t\t\t\t(parallel_policy_all) & (relevant_status = success) : cur_status;" + os.linesep#if a success is present, continue with w/e we have
                      + "\t\t\t\t(parallel_policy_all) & (relevant_status = running) : running;" + os.linesep#if a runnign is present, set to running
                      + "\t\t\t\t!(parallel_policy_all) & (relevant_status = success) : success;" + os.linesep#if a success is present, set to success
                      + "\t\t\t\t!(parallel_policy_all) & (relevant_status = running) : cur_status;" + os.linesep#if a runnign is present, continue with w/e we have
                      + "\t\t\t\tTRUE : cur_status;" + os.linesep#don't change.
                      + "\t\t\tesac;" + os.linesep)
    return return_string


#-----------------------------------------------------------------
