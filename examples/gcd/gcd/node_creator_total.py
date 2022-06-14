import os

#-----------------------------------------------------------------
#common node parts kept here to increase reusage

def common_string(max_children_plus_one = 0):
    status_start = ("\tCONSTANTS" + os.linesep
                    + "\t\tsuccess, failure, running, invalid, error;" + os.linesep
                    + "\tDEFINE" + os.linesep 
                    + "\t\tstatus :=" + os.linesep 
                    + "\t\t\tcase" + os.linesep
                    + "\t\t\t\t!(active) : invalid;" + os.linesep #this should be the only invalid case.
    )
    status_end = ("\t\t\tesac;" + os.linesep)
    active = []
    for child in range(max_children_plus_one):
        active_start = ("\t\tchild_" + str(child) + ".active :=" + os.linesep 
                        + "\t\t\tcase" + os.linesep
                        + "\t\t\t\t!(active) : FALSE;" + os.linesep #if the node isn't active, then the children definitely aren't active 
        )
        active.append((active_start))
    
    active_end = ("\t\t\t\tTRUE : TRUE;" + os.linesep 
                  + "\t\t\tesac;" + os.linesep
    )
    children = ""
    for child in range(max_children_plus_one):
        children += ", child_" + str(child)
    return (status_start, status_end, active, active_end, children)


#-----------------------------------------------------------------
#Decorators

def create_decorator_condition(ignored_value):
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_condition(child_0, status)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t(child_0.status = status) : success;" + os.linesep  #it matches the status
                     + "\t\t\t\tTRUE : running;" + os.linesep  #it doesn't match the status
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
    )
    return return_string
def create_decorator_eternal_guard(ignored_value):
    pass
def create_decorator_inverter(ignored_value):    
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_inverter(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t(child_0.status = failure) : success;" + os.linesep  #failure becomes success
                     + "\t\t\t\t(child_0.status = success) : failure;" + os.linesep  #success becomes failure
                     + "\t\t\t\tTRUE : running;" + os.linesep #must have been running
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
    )
    return return_string
def create_decorator_one_shot(ignored_value):
    pass
    
    (status_start, status_end) = common_string(number_of_nodes, False, False)#this uses a custom child_0 direction. can't use the standard decorator
    return_string = ("MODULE decorator_one_shot(child_0,descendants, child_0_status, on_successful_completion_only)" + os.linesep
                      + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                      + "\t\tchild_0_completed : boolean;" + os.linesep #keep track of if the child_0 has completed yet
                      + "\t\tchild_0_final : {success, failure};" + os.linesep #keep track of the child_0's final result
                      + "\t\tinit(child_0_completed) := FALSE;" + os.linesep #uh...yeah doesn't start completed
                      + "\t\tinit(child_0_final) := failure;" + os.linesep #this included not because it needs to be, but because it should help limit the state space nuXmv has to cover
                      + "\t\tnext(child_0_completed) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(child_0.status = success) : TRUE;" + os.linesep#set to true if child_0 succeeded
                      + "\t\t\t\t(child_0.status = failure) & !(on_successful_completion_only) : TRUE;" + os.linesep#also set to true if child_0 failed, but that's ok
                      + "\t\t\t\tTRUE : child_0_completed;" + os.linesep#otherwise, hold
                      + "\t\t\tesac;" + os.linesep
                      + "\t\tnext(child_0_final) :=" + os.linesep
                      + "\t\t\tcase" + os.linesep
                      + "\t\t\t\t(child_0.status = success) : success;" + os.linesep#if we returned success, explicitly set it to success
                      + "\t\t\t\tTRUE : child_0_final;" + os.linesep #otherwise, keep it unchanging. If failure was a valid exit, that's what we were already on
                      + "\t\t\tesac;" + os.linesep
                      + "\t\t\t\t(child_0_completed) : child_0_final;" + os.linesep  #child_0 completed. we're done.
                      + "\t\t\t\t!(child_0_completed) : child_0.status;" +os.linesep
                      + status_end
                      + "\t\t\t\t(child_0_completed) : parent;" + os.linesep #child_0 already finished. time to leave
                      + "\t\t\t\t!(child_0_completed) & (child_0.status = invalid) : child_0;" + os.linesep #if the child_0 has not yet been ran, go run the child_0.
                      + "\t\t\t\t!(child_0_completed) & !(child_0.status = invalid) : parent;" + os.linesep # child_0 already ran. time to return to parent
                      + "\t\t\t\tTRUE : -1.." + str(number_of_nodes) + ";" + os.linesep #if this isn't the active node, allow it to bounce around
                      + "\t\t\tesac;" + os.linesep 
                      + os.linesep)
    return return_string
def create_decorator_status_to_blackboard(ignored_value):
    pass
def create_decorator_timeout(ignored_value):
    pass
def create_decorator_failure_is_running(ignored_value):
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_failure_is_running(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = failure) : child_0.status;" + os.linesep  #no matter what, we match the child_0
                     + "\t\t\t\tTRUE : running;" + os.linesep  #unless it failed. then we pretend it's still running
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
    )
    return return_string
def create_decorator_failure_is_success(ignored_value):
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_failure_is_success(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = failure) : child_0.status;" + os.linesep  #no matter what, we match the child_0
                     + "\t\t\t\tTRUE : success;" + os.linesep  #unless it failed. then we pretend it success
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
    )
    return return_string
def create_decorator_running_is_failure(ignored_value):
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_running_is_failure(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = running) : child_0.status;" + os.linesep  #no matter what, we match the child_0
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #unless it's running. then we pretend it failed
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
    )
    return return_string
def create_decorator_running_is_success(ignored_value):
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_running_is_success(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = running) : child_0.status;" + os.linesep  #no matter what, we match the child_0
                     + "\t\t\t\tTRUE : success;" + os.linesep  #unless it's running. then we pretend it success
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
    )
    return return_string
def create_decorator_success_is_failure(ignored_value):
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_success_is_failure(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = success) : child_0.status;" + os.linesep  #no matter what, we match the child_0
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #unless it's success. then we pretend it failed
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
    )
    return return_string
def create_decorator_success_is_running(ignored_value):
    (status_start, status_end, active, active_end, child_0ren) = common_string(1)
    return_string = ("MODULE decorator_success_is_running(child_0)" + os.linesep
                     + status_start
                     + "\t\t\t\t(child_0.status in {invalid, error}) : error;" + os.linesep  #we found an error
                     + "\t\t\t\t!(child_0.status = success) : child_0.status;" + os.linesep  #no matter what, we match the child_0
                     + "\t\t\t\tTRUE : running;" + os.linesep  #unless it's success. then we pretend it running
                     + status_end
                     + active[0]#handles (if this node not active, child_0 not active)
                     + active_end#handle (otherwise, child_0 active)
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
    else:
        return_string = ""
    return_string += ("MODULE define_nodes" + os.linesep
                      + "\tDEFINE" + os.linesep)
    for i in range(len(nodes)):
        return_string += ("\t\t" + nodes[i][2] + " := " + str(i) + ";" + os.linesep)
                          
    return return_string
#def create_blackboard(variable_to_int, variable_access, nodes):
def create_blackboard(int_to_variable, variable_to_int, variable_access, nodes, no_seperate_modules, min_val = 0, max_val = 1):
    
    return_string = ("MODULE blackboard_module(node_names, variable_names, statuses)" + os.linesep
                      + "\tCONSTANTS" + os.linesep
                      + "\t\tsuccess, failure, running, invalid, error;" + os.linesep
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
            decl_string += ("\t\t" + variable + "_SET : " + variable + "_SET_module(variables, variable_exists, node_names, variable_names, statuses);" + os.linesep)
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
            exist_define += "\t\t" + variable + "_exists := TRUE;" + os.linesep
            decl_string += ("\t\t" + variable + " : " + str(min_val) + ".." + str(max_val) + ";" + os.linesep)
            assign_string += ("\t\tinit(" + variable + ") := " + str(min_val) +";" + os.linesep
                              + "\t\tnext(" + variable + ") := " + os.linesep
                              + "\t\t\tcase" + os.linesep
            )
            if variable_to_int[variable] in variable_access:
                for node in variable_access[variable_to_int[variable]]:
                    assign_string += "\t\t\t\t(statuses[node_names." + nodes[node][2] + "] = success) : " + poss_values + ";" + os.linesep
            assign_string +=("\t\t\t\tTRUE : " + variable + ";" + os.linesep
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
def create_node_check_blackboard_variable_exists(ignored_value): 
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_check_blackboard_variable_exists(blackboard, variable)" + os.linesep
                     + status_start
                     + "\t\t\t\t(blackboard.variable_exists[variable]) : success;" + os.linesep  #the variable exists
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #it doesn't
                     + status_end)
    return return_string

def create_node_check_blackboard_variable_value(ignored_value):
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_check_blackboard_variable_value(blackboard, variable, check)" + os.linesep
                     + status_start
                     + "\t\t\t\t(blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #the variable doesn't exist or fails the check
                     + status_end)
    return return_string

def create_node_check_blackboard_variable_values(number_of_nodes, variables, checks, operators):
    pass
    #NOT ACTUALLY DONE. OPERATORS CONFUSING.
    
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_check_blackboard_variable_values(variables_exist, checks)" + os.linesep
                      + status_start
                      + "\t\t\t\t!(variables_exist) : failure;" + os.linesep  #at least some of the variables don't exist
                      + "\t\t\t\t(variables_exist) & (checks.result) : success;" + os.linesep  #passes the check
                      + "\t\t\t\t(variables_exist)) & !(checks.result) : failure;" + os.linesep  #fails the check
                      + status_end)
    return return_string
def create_node_set_blackboard_variable(ignored_value):
    pass
    
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_set_blackboard_variable(blackboard, variable, nodes_with_access, value_creator, overwrite)" + os.linesep
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
def create_node_set_blackboard_variables(ignored_value):
    return_string = ("MODULE node_set_blackboard_variables(status_module)" + os.linesep
                     + "\tDEFINE" + os.linesep
                     + "\t\tstatus :=" + os.linesep
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : invalid;" + os.linesep
                     + "\t\t\t\tTRUE : status_module.status;" + os.linesep
                     + "\t\t\tesac;" + os.linesep
    )
    return return_string
def create_node_unset_blackboard_variable(ignored_value):
    pass
    
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_unset_blackboard_variable(variable, nodes_with_access)" + os.linesep
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
def create_node_wait_for_blackboard_variable(ignored_value):
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_wait_for_blackboard_variable(variable, blackboard)" + os.linesep
                      + status_start
                      + "\t\t\t\t(blackboard.variable_exists[variable]) : success;" + os.linesep  #variable exists
                      + "\t\t\t\tTRUE : running;" + os.linesep  #variable does not yet exist
                      + status_end)
    return return_string
def create_node_wait_for_blackboard_variable_value(ignored_value): 
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_wait_for_blackboard_variable_value(blackboard, variable, check)" + os.linesep
                      + status_start
                      + "\t\t\t\t(blackboard.variable_exists[variable]) & (check.result) : success;" + os.linesep  #passes the check
                      + "\t\t\t\tTRUE : running;" + os.linesep  #fails the check or doesn't exist
                      + status_end)
    return return_string


#-----------------------------------------------------------------
#basic example nodes

def create_node_count(ignored_value):
    pass
    #variables needed: fail_until, running_until, success_until, reset
    print('WARNING: reset currently resets whenever the root node ticks with success or failure. This does not match the behavior of py_trees')
    
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_count(fail_until, running_until, success_until, reset)" + os.linesep
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

def create_node_failure(ignored_value): 
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_failure()" + os.linesep
                     + status_start
                     + "\t\t\t\tTRUE : failure;" + os.linesep  #this always returns failure
                     + status_end)
    return return_string

def create_node_periodic(ignored_value): 
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_periodic(period)" + os.linesep
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

def create_node_running(ignored_value):
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_running()" + os.linesep
                     + status_start
                     + "\t\t\t\tTRUE : running;" + os.linesep  #this always returns failure
                     + status_end)
    return return_string

def create_node_status_sequence(ignored_value): 
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_status_sequence(sequence, sequence_length, eventually)" + os.linesep
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

def create_node_success(ignored_value): 
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_success()" + os.linesep
                      + status_start
                      + "\t\t\t\tTRUE : success;" + os.linesep  #this always returns success
                      + status_end)
    return return_string

def create_node_success_every_n(ignored_value):
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_success_every_n(n)" + os.linesep
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

def create_node_tick_counter(ignored_value):
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_tick_counter(duration, completion_status)" + os.linesep
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

def create_node_timer(ignored_value): 
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_timer()" + os.linesep
                     + "\tCONSTANTS" + os.linesep
                     + "\t\tsuccess, failure, running, invalid, error;" + os.linesep
                     + "\tIVAR" + os.linesep
                     + "\t\tinput_status : {success, running};" + os.linesep
                     + "\tDEFINE" + os.linesep 
                     + "\t\tstatus :=" + os.linesep 
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : invalid;" + os.linesep #this should be the only invalid case.
                     + "\t\t\t\tTRUE : input_status;" + os.linesep#success or running only.  
                     + status_end)
    return return_string


#-----------------------------------------------------------------
#a default node

def create_node_default(ignored_value):
    (status_start, status_end, active, active_end, children) = common_string()
    return_string = ("MODULE node_default()" + os.linesep
                     + "\tCONSTANTS" + os.linesep
                     + "\t\tsuccess, failure, running, invalid, error;" + os.linesep
                     + "\tIVAR" + os.linesep
                     + "\t\tinput_status : {success, running, failure};" + os.linesep
                     + "\tDEFINE" + os.linesep 
                     + "\t\tstatus :=" + os.linesep 
                     + "\t\t\tcase" + os.linesep
                     + "\t\t\t\t!(active) : invalid;" + os.linesep #this should be the only invalid case.
                     + "\t\t\t\tTRUE : input_status;" + os.linesep#success, running, or failure  
                     + status_end)
    return return_string


#-----------------------------------------------------------------
#composite nodes

def create_node_selector(max_children_plus_one):
    (status_start, status_end, active, active_end, children) = common_string(max_children_plus_one)
    
    return_string = ("MODULE node_selector(last_child" + children + ")" + os.linesep 
                      + status_start
                      + "\t\t\t\t(last_child < 0) : failure;" + os.linesep#no children, return default
                      #at least one child exists. enter for loop
    )
    for child in range(max_children_plus_one):
        return_string += "\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = error) : error;" + os.linesep
        #if any of the children had an error, propagate it
    for child in range(max_children_plus_one):
        #we return on first success, first running, or if everything is failure
        #if none of these occur, it is an error.
        return_string += ("\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = success) : success;" + os.linesep
                          #we found success, therefore, return success
                          + "\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = running) : running;" + os.linesep
                          #we found running, therefore, return running
                          + "\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = invalid) : error;" + os.linesep
                          #we should not be able to encounter invalid in a child before we run out of children, encounter running, or encounter success
        )
    return_string += ("\t\t\t\tTRUE : failure;" + os.linesep
                      #none of our children returned success or running, which means either there was an error we caught, or we failed.
                      + status_end
    )
    for child in range(max_children_plus_one):
        return_string += (active[child]
                          + "\t\t\t\t(" + str(child) + " > last_child) : FALSE;" + os.linesep
                          #if this is beyond the last child, it is not active (note that if there are no children, none of them will be active)
        )
        if child == 0:
            #first child of an active selector with children is always active
            return_string += ("\t\t\t\tTRUE : TRUE;" + os.linesep
                              + "\t\t\t\tesac;" + os.linesep
            )
        else:
            return_string += ("\t\t\t\t!(child_" + str(child-1) + ".active) : FALSE;" + os.linesep
                              #if the child before this one was not active, then this one isn't active
                              + "\t\t\t\t!(child_" + str(child-1) + ".status = failure) : FALSE;" + os.linesep
                              #if the child before this did not return failure, than we are inactive
                              + "\t\t\t\tTRUE: TRUE;" + os.linesep
                              #in all other cases, this node is active
                              + "\t\t\tesac;" + os.linesep
            )
    return return_string

def create_node_sequence(max_children_plus_one):
    (status_start, status_end, active, active_end, children) = common_string(max_children_plus_one)
    #note that resume_point is an integer between 0 and last_child (inclusive)
    return_string = ("MODULE node_sequence(last_child" + children + ", resume_point)" + os.linesep 
                      + status_start
                      + "\t\t\t\t(last_child < 0) : success;" + os.linesep#no children, return default
                      #at least one child exists. enter for loop
    )
    for child in range(max_children_plus_one):
        return_string += "\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = error) : error;" + os.linesep
        #if any of the children had an error, propagate it
    for child in range(max_children_plus_one):
        #we return on first failure, first running, or if everything is success, but we skip over stuff if resuming
        #if none of these occur, it is an error.
        return_string += ("\t\t\t\t(" + str(child) + " >= resume_point) & (" + str(child) + " <= last_child) & (child_" + str(child) + ".status = failure) : failure;" + os.linesep
                          #we found success, therefore, return success
                          + "\t\t\t\t(" + str(child) + " >= resume_point) & (" + str(child) + " <= last_child) & (child_" + str(child) + ".status = running) : running;" + os.linesep
                          #we found running, therefore, return running
                          + "\t\t\t\t(" + str(child) + " >= resume_point) & (" + str(child) + " <= last_child) & (child_" + str(child) + ".status = invalid) : error;" + os.linesep
                          #we should not be able to encounter invalid in a child before we run out of children, encounter running, or encounter success
                          #note that in all of these cases, we ignore the status if str(child) < resume_point, as that means we resumed from after it, so it doesn't really matter what that node was doing (unless it was in an error state, which we would have caught earlier).
        )
    return_string += ("\t\t\t\tTRUE : success;" + os.linesep
                      #none of our children returned failure or running, which means either there was an error we caught, or we succeeded
                      + status_end
    )
    for child in range(max_children_plus_one):
        return_string += (active[child]
                          + "\t\t\t\t(" + str(child) + " > last_child) : FALSE;" + os.linesep
                          #if this is beyond the last child, it is not active (note that if there are no children, none of them will be active)
                          + "\t\t\t\t(" + str(child) + " < resume_point) : FALSE;" + os.linesep
                          #all children that we are skipping over because of resuming are not active
                          + "\t\t\t\t(" + str(child) + " = resume_point) : TRUE;" + os.linesep
                          #the child we are resuming from is active
        )
        if child == 0:
            #first child of an active selector with children is always active
            return_string += ("\t\t\t\tTRUE : TRUE;" + os.linesep
                              + "\t\t\t\tesac;" + os.linesep
            )
        else:
            return_string += ("\t\t\t\t!(child_" + str(child-1) + ".active) : FALSE;" + os.linesep
                              #if the child before this one was not active, then this one isn't active
                              + "\t\t\t\t!(child_" + str(child-1) + ".status = success) : FALSE;" + os.linesep
                              #if the child before this did not return success, we are inactive
                              + "\t\t\t\tTRUE: TRUE;" + os.linesep
                              #in all other cases, this node is active
                              + "\t\t\tesac;" + os.linesep
            )
    return return_string

def create_node_parallel(max_children_plus_one):
    (status_start, status_end, active, active_end, children) = common_string(max_children_plus_one)
    
    return_string = ("MODULE node_parallel(last_child" + children + ", skip_child, parallel_policy_all)" + os.linesep
                      + status_start
                      + "\t\t\t\t(last_child < 0) : success;" + os.linesep#no children, return default
                      #at least one child exists. enter for loop
    )
    for child in range(max_children_plus_one):
        return_string += ("\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = error) : error;" + os.linesep
                          + "\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = invalid) & !(skip_child[min(" + str(child) + ", max(last_child, 0))] = -2) : error;" + os.linesep
        )
        #if any of the children had an error, propagate it
        #note that an invalid child when this node is active is an error, unless it was skipped
        #note that skipped is indicated by being = -2
    #note that at this point, every node has returned success, failure, running, or was skipped.
    #skipped nodes indicate success was returned previously. no need to check them again.
    for child in range(max_children_plus_one):
        return_string += "\t\t\t\t(" + str(child) + " <= last_child) & (child_" + str(child) + ".status = failure) : failure;" + os.linesep
        #we found failure, therefore, return failure
    #at this point, no failures are possible. everything is success, running, or skipped.
    for child in range(max_children_plus_one):
        #we return on first success if success_on_all is false, on first running if it's true, and otherwise we need to see them all
        return_string += ("\t\t\t\t(" + str(child) + " <= last_child) & (parallel_policy_all) & (child_" + str(child) + ".status = running) : running;" + os.linesep
                          #we found running and need all to succeed, therefore running
                          + "\t\t\t\t(" + str(child) + " <= last_child) & !(parallel_policy_all) & (child_" + str(child) + ".status = success) : success;" + os.linesep
                          #we found success and need only one success, therefore, return success
        )
    return_string += ("\t\t\t\t(parallel_policy_all) : success;" + os.linesep
                      #we failed to encounter a running, which means everything was success (or skipped). therefore, success
                      + "\t\t\t\tTRUE : running;" + os.linesep
                      #we failed to encounter a success, which means we are running.
                      + status_end
    )
    for child in range(max_children_plus_one):
        return_string += (active[child]
                          + "\t\t\t\t(" + str(child) + " > last_child) : FALSE;" + os.linesep
                          #if this is beyond the last child, it is not active (note that if there are no children, none of them will be active)
                          + "\t\t\t\t(skip_child[min(" + str(child) + ", max(last_child, 0))] = -2) : FALSE;" + os.linesep
                          #all children that we are skipping are not active
                          + "\t\t\t\tTRUE : TRUE;" + os.linesep
                          #all other children are active
                          + "\t\t\tesac;" + os.linesep
        )
    return return_string

#-----------------------------------------------------------------
