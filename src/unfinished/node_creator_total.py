import os

#-----------------------------------------------------------------
#common node parts kept here to increase reusage

def common_string(number_of_children = 0):
    status_start = ("\tCONSTANTS" + os.linesep
                    + "\t\tsuccess, failure, running, invalid, error;" + os.linesep
                    + "\tDEFINE" + os.linesep 
                    + "\t\tstatus :=" + os.linesep 
                    + "\t\t\tcase" + os.linesep
                    + "\t\t\t\t(active = FALSE) : invalid;" + os.linesep #this should be the only invalid case.
    )
    status_end = ("\t\t\tesac;" + os.linesep)
    active = []
    for child in range(number_of_children):
        active_start = ("\t\tactive_" + str(child) " :=" + os.linesep 
                        + "\t\t\tcase" + os.linesep
                        + "\t\t\t\t!(active) : FALSE;" + os.linesep #if the node isn't active, then the children definitely aren't active 
        )
        active.append((active_start))
    
    active_end = ("\t\t\t\tTRUE : TRUE;" + os.linesep 
                  + "\t\t\tesac;" + os.linesep
    )
    return (status_start, status_end, active, active_end)

#-----------------------------------------------------------------
#Decorators

def create_decorator_condition():
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_condition(active, child_status, status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t(child_status = status) : success;" + os.linesep  #it matches the status
                     + "\t\t\t\tTRUE : running;" + os.linesep  #it doesn't match the status
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string
def create_decorator_eternal_guard():
    pass
def create_decorator_inverter():    
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_inverter(active, child_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t(child_status = failure) : success;" + os.linesep  #failure becomes success
                     + "\t\t\t\t(child_status = success) : failure;" + os.linesep  #success becomes failure
                     + "\t\t\t\tTRUE : running;" + os.linesep #must have been running
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string
def create_decorator_one_shot():
    pass
    
    (status_start, status_end) = common_string(number_of_nodes, False, False)#this uses a custom child direction. can't use the standard decorator
    return_string = ("MODULE decorator_one_shot(active, child_status,descendants, child_status, on_successful_completion_only)" + os.linesep
                      + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                      + "\t\tchild_completed : boolean;" + os.linesep #keep track of if the child has completed yet
                      + "\t\tchild_final : {success, failure};" + os.linesep #keep track of the child's final result
                      + "\t\tinit(child_completed) := FALSE;" + os.linesep #uh...yeah doesn't start completed
                      + "\t\tinit(child_final) := failure;" + os.linesep #this included not because it needs to be, but because it should help limit the state space nuXmv has to cover
                      + "\t\tnext(child_completed) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(child_status = success) : TRUE;" + os.linesep#set to true if child succeeded
                      + "\t\t\t\t(child_status = failure) & !(on_successful_completion_only) : TRUE;" + os.linesep#also set to true if child failed, but that's ok
                      + "\t\t\t\tTRUE : child_completed;" + os.linesep#otherwise, hold
                      + "\t\t\tesac;" + os.linesep
                      + "\t\tnext(child_final) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(child_status = success) : success;" + os.linesep#if we returned success, explicitly set it to success
                      + "\t\t\t\tTRUE : child_final;" + os.linesep #otherwise, keep it unchanging. If failure was a valid exit, that's what we were already on
                      + "\t\t\tesac;" + os.linesep
                      + "\t\t\t\t(child_completed) : child_final;" + os.linesep  #child completed. we're done.
                      + "\t\t\t\t!(child_completed) : child_status;" +os.linesep
                      + status_end
                      + "\t\t\t\t(child_completed) : parent;" + os.linesep #child already finished. time to leave
                      + "\t\t\t\t!(child_completed) & (child_status = invalid) : child;" + os.linesep #if the child has not yet been ran, go run the child.
                      + "\t\t\t\t!(child_completed) & !(child_status = invalid) : parent;" + os.linesep # child already ran. time to return to parent
                      + "\t\t\t\tTRUE : -1.." + str(number_of_nodes) + ";" + os.linesep #if this isn't the active node, allow it to bounce around
                      + "\t\t\tesac;" + os.linesep 
                      + os.linesep)
    return return_string
def create_decorator_status_to_blackboard():
    pass
def create_decorator_timeout():
    pass
def create_decorator_failure_is_running():
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_failure_is_running(active, child_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_status = failure) : child_status;" + os.linesep  #no matter what, we match the child
                     + "\t\t\t\tTRUE : running;" + os.linesep  #unless it failed. then we pretend it's still running
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string
def create_decorator_failure_is_success():
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_failure_is_success(active, child_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_status = failure) : child_status;" + os.linesep  #no matter what, we match the child
                     + "\t\t\t\tTRUE : success;" + os.linesep  #unless it failed. then we pretend it success
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string
def create_decorator_running_is_failure():
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_running_is_failure(active, child_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_status = running) : child_status;" + os.linesep  #no matter what, we match the child
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #unless it's running. then we pretend it failed
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string
def create_decorator_running_is_success():
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_running_is_success(active, child_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_status = running) : child_status;" + os.linesep  #no matter what, we match the child
                     + "\t\t\t\tTRUE : success;" + os.linesep  #unless it's running. then we pretend it success
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string
def create_decorator_success_is_failure():
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_success_is_failure(active, child_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_status = success) : child_status;" + os.linesep  #no matter what, we match the child
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #unless it's success. then we pretend it failed
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string
def create_decorator_success_is_running():
    (status_start, status_end, active, active_end) = common_string(1)
    return_string = ("MODULE decorator_success_is_running(active, child_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_status = success) : child_status;" + os.linesep  #no matter what, we match the child
                     + "\t\t\t\tTRUE : running;" + os.linesep  #unless it's success. then we pretend it running
                     + status_end
                     + active[0]#handles (if this node not active, child not active)
                     + active_end#handle (otherwise, child active)
    )
    return return_string


#-----------------------------------------------------------------
#the blackboard

def create_names_module(variable_to_int, nodes):
    
    if variable_to_int:
        return_string = ("MODULE define_variables" + os.linesep
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
    
    return_string = ("MODULE blackboard_module(active_node, node_names, variable_names, random_status, statuses)" + os.linesep
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
def create_node_check_blackboard_variable_exists(): 
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_check_blackboard_variable_exists(active, blackboard, variable)" + os.linesep
                     + status_start
                     + "\t\t\t\t(blackboard.variable_exists[variable]) : success;" + os.linesep  #the variable exists
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #it doesn't
                     + status_end)
    return return_string

def create_node_check_blackboard_variable_value():
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_check_blackboard_variable_value(active, blackboard, variable, check)" + os.linesep
                     + status_start
                     + "\t\t\t\t(blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #the variable doesn't exist or fails the check
                     + status_end)
    return return_string

def create_node_check_blackboard_variable_values(number_of_nodes, variables, checks, operators):
    pass
    #NOT ACTUALLY DONE. OPERATORS CONFUSING.
    
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_check_blackboard_variable_values(active, variables_exist, checks)" + os.linesep
                      + status_start
                      + "\t\t\t\t!(variables_exist) : failure;" + os.linesep  #at least some of the variables don't exist
                      + "\t\t\t\t(variables_exist) & (checks.result) : success;" + os.linesep  #passes the check
                      + "\t\t\t\t(variables_exist)) & !(checks.result) : failure;" + os.linesep  #fails the check
                      + status_end)
    return return_string
def create_node_set_blackboard_variable():
    pass
    
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_set_blackboard_variable(active, blackboard, variable, nodes_with_access, value_creator, overwrite)" + os.linesep
                      + status_start
                      + "\t\tblackboard_var : integer;" + os.linesep
                      + "\t\tblackboard_var_exists : boolean;" + os.linesep
                      + "\t\tfree_var : integer;" + os.linesep
                      + "\tINVAR" + os.linesep
                      + "\t\tfree_var = blackboard_var;" + os.linesep
                      + "\t\tnext(blackboard_var) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(overwrite) : value_creator.blackboard_var;" + os.linesep
                      + "\t\t\t\t!(blackboard_var_exists) : value_creator.blackboard_var;" + os.linesep
                      + "\t\t\t\t!(overwrite) & (blackboard_var_exists) : blackboard_var;" + os.linesep
                      #+ "\t\t\t\t!(active_node in nodes_with_access) : free_var;" + os.linesep
                      + "\t\t\t\t!(active_node in nodes_with_access) : next(free_var);" + os.linesep #so. the options are to use next(free_var), or remove the INVAR for free_var
                      + "\t\t\t\tTRUE : blackboard_var;" + os.linesep
                      + "\t\t\tesac;" + os.linesep
                      + "\t\tnext(blackboard_var_exists) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) : TRUE;" + os.linesep
                      + "\t\t\t\t!(active_node in nodes_with_access) : {FALSE, TRUE};" + os.linesep
                      + "\t\t\t\tTRUE : blackboard_var_exists;" + os.linesep
                      + "\t\t\tesac;" + os.linesep
                      + "\t\t\t\t(overwrite) : success;" + os.linesep  #success if it actually set the value
                      + "\t\t\t\t!(blackboard_var_exists) : success;" + os.linesep  #success if it actually set the value
                      + "\t\t\t\t!(overwrite) & (blackboard_var_exists) : failure;" + os.linesep #failure if it didn't set anything
                      + status_end)
    return return_string
def create_node_set_blackboard_variables():
    return_string = ("MODULE node_set_blackboard_variables(active, status_module)" + os.linesep
                      + "\tDEFINE" + os.linesep
                      + "\t\tstatus := status_module.status;" + os.linesep)
    return return_string
def create_node_unset_blackboard_variable():
    pass
    
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_unset_blackboard_variable(active, variable, nodes_with_access)" + os.linesep
                      + status_start
                      + "\t\t\t\t(active_node = id) : success;" + os.linesep  #this always returns success
                      + status_end
                      + "\tVAR" + os.linesep
                      + "\t\tblackboard_var_exists : boolean;" + os.linesep #this is so we can set that the variable doesn't exist
                      + "\tASSIGN" + os.linesep
                      + "\t\tnext(blackboard_var_exists) :=" +os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(active_node = id) : FALSE;" + os.linesep #we just unset it
                      + "\t\t\t\t!(active_node in nodes_with_access) : {FALSE, TRUE};" + os.linesep #well, someone else with access might be setting or unsetting it.
                      + "\t\t\t\tTRUE : blackboard_var_exists;" + os.linesep #in a state with no access, so it won't change.
                      + "\t\t\tesac;" + os.linesep)
    return return_string
def create_node_wait_for_blackboard_variable():
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_wait_for_blackboard_variable(active, variable, blackboard)" + os.linesep
                      + status_start
                      + "\t\t\t\t(blackboard.variable_exists[variable]) : success;" + os.linesep  #variable exists
                      + "\t\t\t\tTRUE : running;" + os.linesep  #variable does not yet exist
                      + status_end)
    return return_string
def create_node_wait_for_blackboard_variable_value(): 
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_wait_for_blackboard_variable_value(active, blackboard, variable, check)" + os.linesep
                      + status_start
                      + "\t\t\t\t(blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                      + "\t\t\t\tTRUE : running;" + os.linesep  #fails the check or doesn't exist
                      + status_end)
    return return_string

#-----------------------------------------------------------------
#basic example nodes

def create_node_count():
    pass
    #variables needed: fail_until, running_until, success_until, reset
    print('WARNING: reset currently resets whenever the root node ticks with success or failure. This does not match the behavior of py_trees')
    
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_count(active, fail_until, running_until, success_until, reset)" + os.linesep
                      + status_start
                      + "\t\t\t\t(internal_node_count < fail_until) : failure;" + os.linesep  #internal_node_count <fail_until means we return failure
                      #if we reached this point, internal_node_count >= fail_until
                      + "\t\t\t\t(internal_node_count < running_until) : running;" + os.linesep #internal_node_count <running_until means we return running
                      #if we reached this point, internal_node_count >= fail_until and internal_node_count >= running_until
                      + "\t\t\t\t(internal_node_count < success_until) : success;" + os.linesep #internal_node_count <success_until means we return running
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
                      + "\t\t\t\t(active_node = -1) & !(child_status[0] = running) & (reset) : 0;" + os.linesep #reset the internal_node_count if reset is true, and we invalidate the node
                      + "\t\t\t\t(active_node = id) : min(internal_node_count + 1, max_internal);" + os.linesep #update the internal node.
                      + "\t\t\t\tTRUE : internal_node_count;" + os.linesep #don't change the value otherwise
                      + "\t\t\tesac;" + os.linesep)
    return return_string

def create_node_failure(): 
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_failure(active)" + os.linesep
                     + status_start
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #this always returns failure
                     + status_end)
    return return_string

def create_node_periodic(): 
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_periodic(active, period)" + os.linesep
                     + status_start
                     + "\t\t\t\tTRUE : cycle;" + os.linesep  #this always returns cycle
                     + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tcycle : {running, success, failure};" + os.linesep #keep track of where we are in the cycle
                     + "\t\tinternal_node_count : 1..period;" + os.linesep #keep track of where we are in the internal_node_count
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(cycle) := running;" + os.linesep #initiate cycle
                     + "\t\tinit(internal_node_count) := 1;" + os.linesep #initiate internal_node_count
                     + "\t\tnext(cycle) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : cycle;" + os.linesep #do nothing if not active
                     + "\t\t\t\t(internal_node_count = period) & (cycle = running) : success;" + os.linesep #if we've internal_node_counted up, time to go to success
                     + "\t\t\t\t(internal_node_count = period) & (cycle = success) : failure;" + os.linesep #if we've internal_node_counted up, time to go to failure
                     + "\t\t\t\t(internal_node_count = period) & (cycle = failure) : running;" + os.linesep #if we've internal_node_counted up, time to go to running
                     + "\t\t\t\tTRUE : cycle;" + os.linesep
                     + "\t\t\tesac;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep #do nothing if not active
                     + "\t\t\t\t(internal_node_count = period) : 1;" + os.linesep #if we reached the max, then we need to reset.
                     + "\t\t\t\t(internal_node_count < period) : min(internal_node_count + 1, period);" + os.linesep #if we haven't reached it, internal_node_count up
                     + "\t\t\t\tTRUE : internal_node_count;" + os.linesep
                     + "\t\t\tesac;" + os.linesep)
    return return_string

def create_node_running():
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_running(active)" + os.linesep
                     + status_start
                     + "\t\t\t\tTRUE : running;" + os.linesep  #this always returns failure
                     + status_end)
    return return_string

def create_node_status_sequence(): 
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_status_sequence(active, sequence, sequence_length, eventually)" + os.linesep
                     + status_start
                     + "\t\t\t\t(internal_node_count < sequence_length) : sequence[internal_node_count];" + os.linesep  #return where we are in the sequence
                     + "\t\t\t\tTRUE : eventually;" + os.linesep  #return where we are in the sequence
                     + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tinternal_node_count : 0..sequence_length;" + os.linesep
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(internal_node_count) := 0;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep #do nothing if not active
                     + "\t\t\t\t(eventually = invalid) & (internal_node_count + 1 = sequence_length) : 0;" + os.linesep #if we reached the max and we don't have an eventuality, reset
                     + "\t\t\t\tTRUE : min(internal_node_count + 1, sequence_length);" + os.linesep #if we aren't resetting, then increase
                     + "\t\t\tesac;" + os.linesep)
    return return_string

def create_node_success(): 
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_success(active)" + os.linesep
                      + status_start
                      + "\t\t\t\tTRUE : success;" + os.linesep  #this always returns success
                      + status_end)
    return return_string

def create_node_success_every_n():
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_success_every_n(active, n)" + os.linesep
                     + status_start
                     + "\t\t\t\t(internal_node_count = n) : success;" + os.linesep  #return success every nth time
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #return failure otherwise
                     + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tinternal_node_count : 1..n;" + os.linesep
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(internal_node_count) := 1;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep #hold if not active
                     + "\t\t\t\t(internal_node_count = n) : 1;" + os.linesep #if we reached the max, then we need to reset.
                     + "\t\t\t\tTRUE : min(internal_node_count + 1, n);" + os.linesep #if we haven't reached it, internal_node_count up
                     + "\t\t\tesac;" + os.linesep)
    return return_string

def create_node_tick_counter():
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_tick_counter(active, duration, completion_status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(internal_node_count < duration) : running;" + os.linesep  #return running until we internal_node_count up
                     + "\t\t\t\tTRUE : completion_status;" + os.linesep  #return running until we internal_node_count up
                     + status_end
                     + "\tVAR" + os.linesep
                     + "\t\tinternal_node_count : 0..duration;" + os.linesep
                     + "\tASSIGN" + os.linesep
                     + "\t\tinit(internal_node_count) := 0;" + os.linesep
                     + "\t\tnext(internal_node_count) :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : internal_node_count;" + os.linesep #hold if not active
                     + "\t\t\t\tTRUE : min(internal_node_count + 1, duration);" + os.linesep #if we haven't reached it, internal_node_count up
                     + "\t\t\tesac;" + os.linesep)
    return return_string


#-----------------------------------------------------------------

def create_node_timer(): 
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_timer(active)" + os.linesep
                     + "\tCONSTANTS" + os.linesep
                     + "\t\tsuccess, failure, running, invalid, error;" + os.linesep
                     + "\tIVAR" + os.linesep
                     + "\t\tinput_status := {success, running};" + os.linesep
                     + "\tDEFINE" + os.linesep 
                     + "\t\tstatus :=" + os.linesep 
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t(active = FALSE) : invalid;" + os.linesep #this should be the only invalid case.
                     + "\t\t\t\tTRUE : input_status;" + os.linesep#success or running only.  
                     + status_end)
    return return_string


#-----------------------------------------------------------------
#a default node

def create_node_default():
    (status_start, status_end, active, active_end) = common_string()
    return_string = ("MODULE node_default(active)" + os.linesep
                     + "\tCONSTANTS" + os.linesep
                     + "\t\tsuccess, failure, running, invalid, error;" + os.linesep
                     + "\tIVAR" + os.linesep
                     + "\t\tinput_status := {success, running, failure};" + os.linesep
                     + "\tDEFINE" + os.linesep 
                     + "\t\tstatus :=" + os.linesep 
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t(active = FALSE) : invalid;" + os.linesep #this should be the only invalid case.
                     + "\t\t\t\tTRUE : input_status;" + os.linesep#success, running, or failure  
                     + status_end)
    return return_string


#-----------------------------------------------------------------
#composite nodes

def create_node_selector(number_of_children):
    (status_start, status_end, active, active_end) = common_string(number_of_children)
    return_string = ("MODULE node_selector(active, children_statuses, last_child)" + os.linesep 
                      + status_start
                      + "\t\t\t\t(active = FALSE) : invalid;" + os.linesep# if we're not active, we're invalid
                      + "\t\t\t\t(last_child < 0) : failure;" + os.linesep#no children, return default
                      #at least one child exists. enter for loop
    )
    for child in range(number_of_children):
        return_string += "\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = error) : error;" + os.linesep
        #if any of the children had an error, propagate it
    for child in range(number_of_children):
        #we return on first success, first running, or if everything is failure
        #if none of these occur, it is an error.
        return_string += ("\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = success) : success;" + os.linesep
                          #we found success, therefore, return success
                          + "\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = running) : running;" + os.linesep
                          #we found running, therefore, return running
                          + "\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = invalid) : error;" + os.linesep
                          #we should not be able to encounter invalid in a child before we run out of children, encounter running, or encounter success
        )
    return_string += ("\t\t\t\tTRUE : failure;" + os.linesep
                      #none of our children returned success or running, which means either there was an error we caught, or we failed.
                      + status_end
    )
    for child in range(number_of_children):
        return_string += (active[child]
                          + "\t\t\t\t(active = FALSE) : FALSE;" + os.linesep
                          #if this node is not active, then the children are not active
                          + "\t\t\t\t(" + str(child) + " > last_child) : FALSE;" + os.linesep
                          #if this is beyond the last child, it is not active (note that if there are no children, none of them will be active)
        )
        if child == 0:
            #first child of an active selector with children is always active
            return_string += ("\t\t\t\tTRUE : TRUE;" + os.linesep
                              + "\t\t\t\tesac;" + os.linesep
            )
        else:
            return_string += ("\t\t\t\t!(active_" + str(child-1) + ") : FALSE;" + os.linesep
                              #if the child before this one was not active, then this one isn't active
                              + "\t\t\t\t!(children_statuses[min(" + str(child-1) + ", max(last_child, 0))] = FAILURE) : FALSE;" + os.linesep
                              #if the child before this returned failure, running, invalid, or error, this node is not active.
                              + "\t\t\t\tTRUE: TRUE;" + os.linesep
                              #in all other cases, this node is active
                              + "\t\t\tesac;" + os.linesep
            )
    return return_string

def create_node_sequence(number_of_children):
    (status_start, status_end, active, active_end) = common_string(number_of_children)
    return_string = ("MODULE node_sequence(active, children_statuses, last_child, resume_point)" + os.linesep 
                      + status_start
                      + "\t\t\t\t(active = FALSE) : invalid;" + os.linesep# if we're not active, we're invalid
                      + "\t\t\t\t(last_child < 0) : success;" + os.linesep#no children, return default
                      #at least one child exists. enter for loop
    )
    for child in range(number_of_children):
        return_string += "\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = error) : error;" + os.linesep
        #if any of the children had an error, propagate it
    for child in range(number_of_children):
        #we return on first success, first running, or if everything is failure
        #if none of these occur, it is an error.
        return_string += ("\t\t\t\t(resume_point <= " + str(child) + ") & (children_statuses[min(" + str(child) + ", max(last_child, 0))] = failure) : failure;" + os.linesep
                          #we found failure, therefore, return failure. (resume_point must be less than or equal to child for us to care about the child)
                          + "\t\t\t\t(resume_point <= " + str(child) + ") & (children_statuses[min(" + str(child) + ", max(last_child, 0))] = running) : running;" + os.linesep
                          #we found running, therefore, return running. (resume_point must be less than or equal to child for us to care about the child)
                          + "\t\t\t\t(resume_point <= " + str(child) + ") & (children_statuses[min(" + str(child) + ", max(last_child, 0))] = invalid) : error;" + os.linesep
                          #we should not be able to encounter invalid in a child before we run out of children, encounter running, or encounter failure. (unless we're resuming, in which case we can ignore the children until they meet or exceed the resume point
        )
    return_string += ("\t\t\t\tTRUE : success;" + os.linesep
                      #none of our children returned failure or running, which means either there was an error we caught, or we succeeded.
                      + status_end
    )
    for child in range(number_of_children):
        return_string += (active[child]
                          + "\t\t\t\t(active = FALSE) : FALSE;" + os.linesep
                          #if this node is not active, then the children are not active
                          + "\t\t\t\t(" + str(child) + " > last_child) : FALSE;" + os.linesep
                          #if this is beyond the last child, it is not active (note that if there are no children, none of them will be active)
                          + "\t\t\t\t(" + str(child) + " < resume_point) : FALSE;" + os.linesep
                          #all children that we are skipping over because of resuming are not active
                          + "\t\t\t\t(" + str(child) + " = resume_point) : TRUE;" + os.linesep
                          #the child we are resuming from is active
        )
        if child == 0:
            #first child is active, unless we deactivated it for one of the above exceptions
            return_string += ("\t\t\t\tTRUE : TRUE;" + os.linesep
                              + "\t\t\t\tesac;" + os.linesep
            )
        else:
            return_string += ("\t\t\t\t!(active_" + str(child-1) + ") : FALSE;" + os.linesep
                              #if the child before this one was not active, then this one isn't active
                              + "\t\t\t\t!(children_statuses[min(" + str(child-1) + ", max(last_child, 0))] = success) : FALSE;" + os.linesep
                              #if the child before this returned failure, running, invalid, or error, this node is not active.
                              + "\t\t\t\tTRUE: TRUE;" + os.linesep
                              #in all other cases, this node is active
                              + "\t\t\tesac;" + os.linesep
            )
    return return_string

def create_node_parallel(number_of_children):
    (status_start, status_end, active, active_end) = common_string(number_of_children)
    return_string = ("MODULE node_parallel(active, children_statuses, last_child, skip_child, parallel_policy_all)" + os.linesep 
                      + status_start
                      + "\t\t\t\t(active = FALSE) : invalid;" + os.linesep# if we're not active, we're invalid
                      + "\t\t\t\t(last_child < 0) : success;" + os.linesep#no children, return default
                      #at least one child exists. enter for loop
    )
    for child in range(number_of_children):
        return_string += ("\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = error) : error;" + os.linesep
                          + "\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = invalid) & !(skip_child[min(" + str(child) + ", max(last_child, 0))]) : error;" + os.linesep
        )
        #if any of the children had an error, propagate it
        #note that encountering an invalid child that was not skip_childped is an error.
    for child in range(number_of_children):
        return_string += ("\t\t\t\t(children_statuses[min(" + str(child) + ", max(last_child, 0))] = failure) : failure;" + os.linesep
                          #we found failure, therefore, return failure.
        )
    for child in range(number_of_children):
        #we return on first success, first running, or if everything is failure
        #if none of these occur, it is an error.
        return_string += ("\t\t\t\t(parallel_policy_all) & (children_statuses[min(" + str(child) + ", max(last_child, 0))] = running) : running;" + os.linesep
                          #we found running, therefore, return running. (only happens if we need all to be success for success)
                          + "\t\t\t\t!(parallel_policy_all) & (children_statuses[min(" + str(child) + ", max(last_child, 0))] = success) : success;" + os.linesep
                          #we found success, therefore, return success. (only happens if we only need one success for success)
        )
    return_string += ("\t\t\t\t(parallel_policy_all) : success;" + os.linesep
                      #we need all to be success. if we had encountered a running, failure, invalid, or error, we would not reach this point. thus all are success.
                      + "\t\t\t\tTRUE : running;" + os.linesep
                      #we only need one for success. since we reached this point, none of the children are success, failure, invalid, or error. Thus all are running.
                      + status_end
    )
    for child in range(number_of_children):
        return_string += (active[child]
                          + "\t\t\t\t(active = FALSE) : FALSE;" + os.linesep
                          #if this node is not active, then the children are not active
                          + "\t\t\t\t(" + str(child) + " > last_child) : FALSE;" + os.linesep
                          #if this is beyond the last child, it is not active (note that if there are no children, none of them will be active)
                          + "\t\t\t\t(skip_child[" + str(child) + "]) : FALSE;" + os.linesep
                          #all children that we are skipping are not active
                          + "\t\t\t\tTRUE : TRUE;" + os.linesep
                          #all other children are active
                          + "\t\t\tesac;" + os.linesep
        )
    return return_string

#-----------------------------------------------------------------
