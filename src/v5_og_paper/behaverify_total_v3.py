#FORMERLY _internal_status

#python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 



#anyways

#each node has an 'active' macro, which is set based on parent
#the root is always 'active'
#each node has a 'status' macro, which is set based on children
#the leaf nodes either use an IVAR or some other method to set their status if they are 'active'. if they are not 'active', their status is 'invalid'.
#thus the only variables that are needed are the 'resume' variables and anything leaf nodes need to operate (and blackboard).


#the current flaw with this is that there is no real way to make it modular. actually wait. nuXmv might have count
#nvm

#solution: there are a finite number of nodes. therefore, there exists a node n with the most children (or ties it).
#therefore, each node has |n| or less children.
#therefore, we can just write the status macro to utilize this is a max, and call it a day.

#that solves the 'status' problem

#now we need to consider the 'active' problem

#here, children depend on the parent and on their left neighbor.

#solution:
#parent defines their child's active macro, which is passed to them. they use it without actually controlling it
#root node is passed a TRUE active macro.

#at this point, logic has primarily moved back into the node_creator file, i think. time to make a new one.

#things to still implement: new resume structure

#each local root tracks it's possible resume locations. unchanged from previous versions
#if anywhere upstream returns success/failure, indicate no resume
#if local root returns failure, indicate no resume
#if local root returns success, indicate SKIP or NO RESUME, depending on if parent it parallel_synch
#if local root returns running, track running based on macros from children.

#note here that we might need two propagations
#propagation 1 -> resume_child_ID is what we currently have built
#propagation 2 -> running_child_ID......wait what do we use this for? oh right. cuz we don't have active node? no.....we can just list through all the options? well. propagation might be cleaner?

#well, we're gonna try it


#----------------------------------------------------------------------------------------------------------------
import argparse
import py_trees
import sys
import time
import os
import re
import inspect
#----------------------------------------------------------------------------------------------------------------
import py_trees.console as console
import node_creator_total_v3 as node_creator
#----------------------------------------------------------------------------------------------------------------
blackboard_needed = False
#----------------------------------------------------------------------------------------------------------------
#regex stuff
blackboard_name_pattern = re.compile(r"#*(?P<blackboard_name>[^\s=]+)\s*=\s*py_trees\.blackboard\.Blackboard\(\s*\)")
#----------------------------------------------------------------------------------------------------------------
        
#-----------------------------------------------------------------------------------------------------------------------

def walk_tree(t, parent_id, next_available_id, children, nodes, additional_arguments, needed_nodes, node_names, variable_access, variable_check, variable_name_to_int, external_status_req, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, parallel_policies, parallel_unsynch = False):
    global blackboard_needed
    this_id=next_available_id
    next_available_id = next_available_id + 1
    children[parent_id].append(this_id)

    node_name=t.name
    if node_name in node_names:
        node_names[node_name]=node_names[node_name]+1
        node_name=node_name+str(node_names[node_name])
    else:
        node_names[node_name]=0

    leaf_set.add(this_id)

    try:
        #this is to overwrite the later checks in order to directly create a specific type of node.
        if t.serene_info_variable == "BlueROV_Blackboard_Node" or t.serene_info_variable == "BlueROV_Task_Node":
            external_status_req.append(node_name)
            nodes[this_id]=('node_set_blackboard_variables', parent_id, node_name)
            needed_nodes.add('node_set_blackboard_variables')
            blackboard_needed=True

            try:
                file_name=inspect.getfile(t.__class__)
                with open(file_name, 'r') as f:
                    code=f.read()
            except:
                code=inspect.getsource(t.__class__)
            blackboard_match=blackboard_name_pattern.search(code)
            invar_string = ""
            decl_string = ""
            if blackboard_match:
                blackboard_name=blackboard_match.groupdict()['blackboard_name'].strip()
                #variable_name_pattern=re.compile(r"#*\s*" + blackboard_name + "\.(?P<variable_name>[^\s=]+)\s*([+\-*/%&|^]?=|//=|\*\*=|>>=|<<=)\s*")
                variable_name_pattern=re.compile(r"#*\s*" + blackboard_name + "\.(?P<variable_name>[_a-zA-Z][\w\.]+)")
                start_loc=0
                done=False
                local_variable_list={}
                while not done:
                    variable_match=variable_name_pattern.search(code, start_loc)
                    if variable_match:
                        start_loc=variable_match.span()[1]
                        variable_name=variable_match.groupdict()['variable_name'].strip()
                        variable_name=variable_name.replace('.', '_dot_')
                        if variable_name in local_variable_list:
                            continue
                        else:
                            local_variable_list[variable_name]=True
                        if variable_name in variable_name_to_int:
                            var_num=variable_name_to_int[variable_name]
                        else:
                            var_num=len(variable_name_to_int)
                            variable_name_to_int[variable_name]=var_num
                        if var_num in variable_access:
                            variable_access[var_num].append(this_id)
                        else:
                            variable_access[var_num]=[this_id]
                    else:
                        done=True
            else:
                variable_name=t.variable_name
                variable_name=variable_name.replace('.', '_dot_')
                if variable_name in variable_name_to_int:
                    var_num=variable_name_to_int[variable_name]
                else:
                    var_num=len(variable_name_to_int)
                    variable_name_to_int[variable_name]=var_num
                if var_num in variable_access:
                    variable_access[var_num].append(this_id)
                else:
                    variable_access[var_num]=[this_id]
            decl_string = ("\t\t" + node_name + "_SET_status : " + node_name + "_SET_status_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);" + os.linesep)
            additional_arguments[this_id]=[{'arg': node_name + "_SET_status", 'decl' : decl_string},]
            #leaf_node_exit(this_id)
            return next_available_id
        elif t.serene_info_variable == "BlueROV_Task_Node":
            #currently this is beign used in the same way as the one above.
            pass
        elif t.serene_info_variable == "non_blocking":
            nodes[this_id]=('node_non_blocking', parent_id, node_name)
            needed_nodes.add('node_non_blocking')
            return next_available_id
    except AttributeError as e:
        #print(e)
        #print(node_name+ " ERROR?")
        pass

    is_decorator = True
    if isinstance(t, py_trees.composites.Sequence):
        #children[this_id]=[]
        nodes[this_id]=('node_sequence', parent_id, node_name)
        #needed_nodes.add('node_sequence')
        sequence_set.add(this_id)
        is_decorator = False
    elif isinstance(t, py_trees.composites.Selector):
        #resume_node=this_id
        #children[this_id]=[]
        nodes[this_id]=('node_selector', parent_id, node_name)
        #needed_nodes.add('node_selector')
        selector_set.add(this_id)
        is_decorator = False
    elif isinstance(t, py_trees.composites.Parallel):
        is_decorator = False
        #resume_node=this_id
        #children[this_id]=[]
        if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
            parallel_policies[this_id] = True
        else:
            parallel_policies[this_id] = False
        if t.policy.synchronise and (not parallel_unsynch):
            parallel_synch_set.add(this_id)
            #nodes[this_id]=('node_parallel_synchronised', parent_id, node_name)
            nodes[this_id]=('node_parallel', parent_id, node_name)
            #needed_nodes.add('node_parallel_synchronised')
            #needed_nodes.add('node_parallel')
            if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                #additional_arguments[this_id]=[{'arg' : "TRUE, TRUE"}]
                #additional_arguments[this_id]=[{'arg' : "TRUE"}]
                pass
            elif isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                #additional_arguments[this_id]=[{'arg' : "TRUE, FALSE"}]
                #additional_arguments[this_id]=[{'arg' : "FALSE"}]
                pass
            else:
                print('ERROR: the following parallel policy is not supported: ' + str(t.policy))
                sys.exit('Unsupported Parallel Policy')
        else:
            parallel_unsynch_set.add(this_id)
            #nodes[this_id]=('node_parallel_unsynchronised', parent_id, node_name)
            nodes[this_id]=('node_parallel', parent_id, node_name)
            #needed_nodes.add('node_parallel_unsynchronised')
            #needed_nodes.add('node_parallel')
            if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                #additional_arguments[this_id]=[{'arg' : "FALSE, TRUE"}]
                #additional_arguments[this_id]=[{'arg' : "TRUE"}]
                pass
            elif isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                #additional_arguments[this_id]=[{'arg' : "FALSE, FALSE"}]
                #additional_arguments[this_id]=[{'arg' : "FALSE"}]
                pass
            else:
                print('ERROR: the following parallel policy is not supported: ' + str(t.policy))
                sys.exit('Unsupported Parallel Policy')
    
            
    elif isinstance(t, py_trees.decorators.Condition):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_condition', parent_id, node_name)
        needed_nodes.add('decorator_condition')
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}, {'arg' : t.succeed_status.name.lower()}]
    elif isinstance(t, py_trees.decorators.Inverter):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_inverter', parent_id, node_name)
        needed_nodes.add('decorator_inverter')
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}]
    elif isinstance(t, py_trees.decorators.OneShot):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_one_shot', parent_id, node_name)
        needed_nodes.add('decorator_one_shot')
        if t.policy.name == "ON_SUCCESSFUL_COMPLETION":
            policy='TRUE'
        else:
            policy='FALSE'
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}, {'arg' : policy}]
    #there's a solid argument for combining all the X is Y types into one module, and just having 2 additional arguments for that module.
    elif isinstance(t, py_trees.decorators.FailureIsRunning):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_failure_is_running', parent_id, node_name)
        needed_nodes.add('decorator_failure_is_running')
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}]
    elif isinstance(t, py_trees.decorators.FailureIsSuccess):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_failure_is_success', parent_id, node_name)
        needed_nodes.add('decorator_failure_is_success')
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}]
    elif isinstance(t, py_trees.decorators.RunningIsFailure):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_running_is_failure', parent_id, node_name)
        needed_nodes.add('decorator_running_is_failure')
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}]
    elif isinstance(t, py_trees.decorators.RunningIsSuccess):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_running_is_success', parent_id, node_name)
        needed_nodes.add('decorator_running_is_success')
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}]
    elif isinstance(t, py_trees.decorators.SuccessIsFailure):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_success_is_failure', parent_id, node_name)
        needed_nodes.add('decorator_success_is_failure')
        #additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}]
    elif isinstance(t, py_trees.decorators.SuccessIsRunning):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_success_is_running', parent_id, node_name)
        needed_nodes.add('decorator_success_is_running')
        additional_arguments[this_id]=[{'arg' : str(next_available_id+1)}]
    elif isinstance(t, py_trees.behaviours.CheckBlackboardVariableExists):
        nodes[this_id]=('node_check_blackboard_variable_exists', parent_id, node_name)
        needed_nodes.add('node_check_blackboard_variable_exists')
        blackboard_needed=True
        variable_name=t.variable_name
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_name_to_int:
            var_num=variable_name_to_int[variable_name]
        else:
            var_num=len(variable_name_to_int)
            variable_name_to_int[variable_name]=var_num
        additional_arguments[this_id]=[{'arg' : 'blackboard'}, {'arg' : str(var_num)}]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.CheckBlackboardVariableValue):
        #(statuses, active_node, id, parent, blackboard, variable, check)" + os.linesep
        nodes[this_id]=('node_check_blackboard_variable_value', parent_id, node_name)
        needed_nodes.add('node_check_blackboard_variable_value')
        blackboard_needed=True
        variable_name=t.check.variable
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_name_to_int:
            var_num=variable_name_to_int[variable_name]
        else:
            var_num=len(variable_name_to_int)
            variable_name_to_int[variable_name]=var_num
        if variable_name in variable_check:
            variable_check[variable_name].append(this_id)
        else:
            variable_check[variable_name] = [this_id]
        additional_arguments[this_id]=[{'arg' : 'blackboard'},
                                       {'arg' : str(var_num)},
                                       {
                                           'arg' : node_name+'_CHECK_'+variable_name,
                                           'decl' : ('\t\t' + node_name + '_CHECK_' + variable_name
                                                     + ' : '+ node_name + '_CHECK_' + variable_name + '_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep)
                                       }]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.CheckBlackboardVariableValues):
        #leaf_node_exit(this_id)
        return next_available_id #not doing the below right now. it's way too much of a pain. don't know how to deal with operator
    elif isinstance(t, py_trees.behaviours.SetBlackboardVariable):
        external_status_req.append(node_name)
        nodes[this_id]=('node_set_blackboard_variables', parent_id, node_name)
        needed_nodes.add('node_set_blackboard_variables')
        blackboard_needed=True
        variable_name=t.variable_name
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_name_to_int:
            var_num=variable_name_to_int[variable_name]
        else:
            var_num=len(variable_name_to_int)
            variable_name_to_int[variable_name]=var_num
        if var_num in variable_access:
            variable_access[var_num].append(this_id)
        else:
            variable_access[var_num]=[this_id]
        decl_string = ("\t\t" + node_name + "_SET_status : " + node_name + "_SET_status_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);" + os.linesep)
        additional_arguments[this_id]=[{'arg': node_name + "_SET_status", 'decl' : decl_string},]
        #leaf_node_exit(this_id)
        return next_available_id
    
    elif isinstance(t, py_trees.behaviours.UnsetBlackboardVariable):
        #statuses, id, parent, variable, nodes_with_access)" + os.linesep
        nodes[this_id]=('node_unset_blackboard_variable', parent_id, node_name)
        needed_nodes.add('node_unset_blackboard_variable')
        blackboard_needed=True
        variable_name=t.key
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_name_to_int:
            var_num=variable_name_to_int[variable_name]
        else:
            var_num=len(variable_name_to_int)
            variable_name_to_int[variable_name]=var_num
        if var_num in variable_access:
            variable_access[var_num].append(this_id)
        else:
            variable_access[var_num]=[this_id]
        additional_arguments[this_id]=[{'arg' : str(var_num)},
                                       {'nodes_with_access_to' : var_num},
                                       {
                                           'invar' : ("\tINVAR" + os.linesep
                                                      + "\t\tblackboard.variable_exists[" + str(var_num) + "] = " + node_name + ".blackboard_var_exists;" + os.linesep)
                                       }]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.WaitForBlackboardVariable):
        nodes[this_id]=('node_wait_for_blackboard_variable', parent_id, node_name)
        needed_nodes.add('node_wait_for_blackboard_variable_exists')
        blackboard_needed=True
        variable_name=t.variable_name
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_name_to_int:
            var_num=variable_name_to_int[variable_name]
        else:
            var_num=len(variable_name_to_int)
            variable_name_to_int[variable_name]=var_num
        additional_arguments[this_id]=[{'arg' : 'blackboard'}, {'arg' : str(var_num)}]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.WaitForBlackboardVariableValue):
        nodes[this_id]=('node_wait_for_blackboard_variable_value', parent_id, node_name)
        needed_nodes.add('node_wait_for_blackboard_variable_value')
        blackboard_needed=True
        variable_name=t.check.variable
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_name_to_int:
            var_num=variable_name_to_int[variable_name]
        else:
            var_num=len(variable_name_to_int)
            variable_name_to_int[variable_name]=var_num
            
        if variable_name in variable_check:
            variable_check[variable_name].append(this_id)
        else:
            variable_check[variable_name] = [this_id]
        additional_arguments[this_id]=[{'arg' : 'blackboard'},
                                       {'arg' : str(var_num)},
                                       {
                                           'arg' : node_name+'_CHECK_'+variable_name,
                                           'decl' : ('\t\t' + node_name + '_CHECK_' + variable_name
                                                     + ' : '+ node_name + '_CHECK_' + variable_name + '_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep)
                                       }]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.Count):
        nodes[this_id]=('next_available_id', parent_id, node_name)
        needed_nodes.add('next_available_id')
        additional_arguments[this_id]=[{'arg' : str(t.fail_until)}, {'arg' : str(t.running_until)}, {'arg' : str(t.success_until)}, {'arg' : str(t.reset).upper()}]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.Failure):
        nodes[this_id]=('node_failure', parent_id, node_name)
        needed_nodes.add('node_failure')
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.Periodic):
        nodes[this_id]=('node_periodic', parent_id, node_name)
        needed_nodes.add('node_periodic')
        additional_arguments[this_id]=({'arg':str(t.period)}, )
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.Running):
        nodes[this_id]=('node_running', parent_id, node_name)
        needed_nodes.add('node_running')
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.StatusSequence):
        nodes[this_id]=('node_status_sequence', parent_id, node_name)
        needed_nodes.add('node_status_sequence')
        sequence_declaration="\t\tnode_status_sequence__sequence" + str(this_id) + " : array 0.." + str(len(t.sequence)-1) + " of {success, failure, running};" + os.linesep
        sequence_init=""
        for i in range(0, len(t.sequence)):
            sequence_init = (sequence_init
                             + "\t\tinit(node_status_sequence__sequence" + str(this_id) + "[" + str(i) + "]) := " + t.sequence[i].name.lower() + ";" + os.linesep)

        sequence_next="\t\tnext(node_status_sequence__sequence" + str(this_id) + ") := node_status_sequence__sequence" + str(this_id) + ";" + os.linesep
        if t.eventually is None:
            eventually='invalid'
        else:
            eventually=t.eventually.name.lower()
        additional_arguments[this_id]=[{'arg':'node_status_sequence__sequence'+str(this_id), 'decl' : sequence_declaration, 'init' : sequence_init, 'next' : sequence_next}, {'arg' : str(len(t.sequence))}, {'arg' : eventually}]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.Success):
        nodes[this_id]=('node_success', parent_id, node_name)
        needed_nodes.add('node_success')
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.SuccessEveryN):
        nodes[this_id]=('node_success_every_n', parent_id, node_name)
        needed_nodes.add('node_success_every_n')
        additional_arguments[this_id]=[{'arg' : str(t.every_n)}, ]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.behaviours.TickCounter):
        nodes[this_id]=('node_tick_counter', parent_id, node_name)
        needed_nodes.add('node_tick_counter')
        additional_arguments[this_id]=[{'arg' : str(t.duration)}, {'arg' : t.completion_status.name.lower()}]
        #leaf_node_exit(this_id)
        return next_available_id
    elif isinstance(t, py_trees.timers.Timer):
        nodes[this_id]=('node_timer', parent_id, node_name)
        needed_nodes.add('node_timer')
        #additional_arguments[this_id] = [{'arg' : 'random_status'}]
        #leaf_node_exit(this_id)
        return next_available_id
    else:#currently defaulting to default. will rework this later probably
        nodes[this_id]=('node_default', parent_id, node_name)
        needed_nodes.add('node_default')
        #additional_arguments[this_id] = [{'arg' : 'random_status'}]
        #leaf_node_exit(this_id)
        return next_available_id

    leaf_set.remove(this_id)
    if is_decorator:
        decorator_set.add(this_id)
    children[this_id] = []#if we've reached this point, then this node has children, and we are going to set up an empty list for it.
    for child in t.children:
        next_available_id = walk_tree(child, this_id, next_available_id, children, nodes, additional_arguments, needed_nodes, node_names, variable_access, variable_check, variable_name_to_int, external_status_req, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, parallel_policies, parallel_unsynch)
    return next_available_id


#-----------------------------------------------------------------------------------------------------------------------

#fixes some _dot_ variable nesting problems
def variable_name_cleanup(variable_name_to_int, variable_access):
    #this segment is to detect and create sub-variables
    #i.e., if a variable in the original was just "meh = Object"
    #but other places use meh.val1, meh.val2, etc, then the original "meh" needs to handle those.
    for variable in variable_name_to_int:
        variable_regex=re.compile(r""+variable+"_dot_")#if out variable is meh, we are now matching meh_dot_
        for child_variable in variable_name_to_int:
            if variable_regex.match(child_variable):#if this is true, then is means we are looking at meh_dot_something
                for access_node in variable_access[variable_name_to_int[variable]]:#we are now going to tell everything that can change meh, that it can change meh_dot_something
                    if variable_name_to_int[child_variable] in variable_access:#confirm that meh_dot_something is even being modified by something
                        pass
                    else:#don't think this should really happen, but w/e. i think this was more common in an older version.
                        variable_access[variable_name_to_int[child_variable]]=[]
                    if access_node in variable_access[variable_name_to_int[child_variable]]:#check if the node that has access to meh has access to meh_dot_something 
                        pass#if it does, do nothing
                    else:#otherwise, add it.
                        variable_access[variable_name_to_int[child_variable]].append(access_node)

#return node_to_local_root_map
def create_node_to_local_root_map(nodes, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
    node_to_local_root_map = {0: 0}# a map from node_id to the local root for that node_id
    #local_roots = {0}
    for node_id in range(1, len(nodes)):
        if nodes[node_id][1] in parallel_unsynch_set or nodes[node_id][1] in parallel_synch_set:
            node_to_local_root_map[node_id] = node_id
            #local_roots.add(node_id)
        else:
            node_to_local_root_map[node_id] = node_to_local_root_map[nodes[node_id][1]]
    #return (node_to_local_root_map, local_roots)
    return node_to_local_root_map

#returns Bool
def can_create_running(nodes, node_id, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
    if node_id in sequence_set:
        return False#even if it has no children, it will not create running
    elif node_id in decorator_set:
        #this needs to encompass all cases where a decorator can return Running
        if 'is_running' in nodes[node_id][0]:
            return True
        else:
            return False
    elif node_id in leaf_set:
        return True
    else:
        return True#selector and parallel can, everything else covered above

def map_can_return_running(nodes, node_id, running_map, children, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
    #print(running_map)
    if node_id in leaf_set:
        #this needs to encompass all cases where a leaf node can return Running
        if nodes[node_id][0] == "node_success":
            running_map[node_id] = False
            return False
        elif nodes[node_id][0] == "node_failure":
            running_map[node_id] = False
            return False
        elif nodes[node_id][0] == "node_non_blocking":
            running_map[node_id] = False
            return False
        elif nodes[node_id][0] == "node_check_blackboard_variable_exists":
            running_map[node_id] = False
            return False
        elif nodes[node_id][0] == "node_check_blackboard_variable_value":
            running_map[node_id] = False
            return False
        else:
            running_map[node_id] = True
            return True#currently being lazy, and just going to assume they can all return Running, even though this is not the case
    elif node_id in decorator_set:
        if 'running_is' in nodes[node_id][0]:
            map_can_return_running(nodes, children[node_id][0], running_map, children, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
            running_map[node_id] = False
            return False
        elif 'is_running' in nodes[node_id][0]:
            map_can_return_running(nodes, children[node_id][0], running_map, children, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
            running_map[node_id] = True
            return True
        else:
            running_map[node_id] = map_can_return_running(nodes, children[node_id][0], running_map, children, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
            return running_map[node_id]
    else:
        #it's a parallel, selector, or sequence node
        running = False
        for child in children[node_id]:
            running = map_can_return_running(nodes, child, running_map, children, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set) or running
            #print(child)
            #print(running_map)
        if len(children[node_id]) == 0:
            if node_id in parallel_synch_set or node_id in parallel_unsynch_set:
                running_map[node_id] = True
                return True
            else:
                running_map[node_id] = False
                return False
        running_map[node_id] = running
        return running
        
#return (local_root_to_relevant_list_map, sequence_to_relevant_descendants_map)
def create_local_root_to_relevant_list_map(nodes, children, node_to_local_root_map, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
    running_map = {}
    map_can_return_running(nodes, 0, running_map, children, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
    #print(running_map)
    local_root_to_relevant_list_map = {} # a map from local_root to the list of relevant things to track in terms of running
    sequence_to_relevant_descendants_map = {} # a map from each sequence to the set of relevant descendants
    for node_id in range(len(nodes)):
        if node_id == node_to_local_root_map[node_id]:
            #this is a local_root
            if nodes[node_id][1] in parallel_synch_set:
                #the local root's parent is a parallel_synch node, so we have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = [-2]
            else:
                #the local root's parent is not a parallel_synch node, so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = []
        elif running_map[node_id] and can_create_running(nodes, node_id, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
            cur_id = node_id
            #encountered_sequences = []
            first_child = True
            done = False
            true_done = False
            end_target=nodes[node_to_local_root_map[node_id]][1]#we end at the parent of the local root.
            sequences_found = []
            to_add = False
            while not done:
                previous_id=cur_id
                cur_id=nodes[cur_id][1]#get the parent
                if cur_id == end_target:
                    done = True
                    true_done = True
                elif cur_id in decorator_set:
                    if "running_is" in nodes[cur_id][0]:#if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
                        done = True
                        true_done = True
                        to_add=False
                        #if node_id in local_root_to_relevant_list_map[node_to_local_root_map[node_id]]:#check if we added it in
                            #local_root_to_relevant_list_map[node_to_local_root_map[node_id]].pop()#if we added it in, it must be at the end.
                        for sequence in sequences_found:#this sequence cannot resume. indicate as such.
                            sequence_to_relevant_descendants_map[sequence] = set()
                elif cur_id in selector_set or cur_id in parallel_synch_set or cur_id in parallel_unsynch_set:
                    done = True#nothing above us will care. they will track the selector or nothing.
                elif cur_id in sequence_set:
                    sequences_found.append(cur_id)
                    if cur_id not in sequence_to_relevant_descendants_map:
                       sequence_to_relevant_descendants_map[cur_id] = set()
                    if children[cur_id][0] == previous_id:
                        pass
                    else:
                        #we encountered proof that this node is relevant. add it to the sequence
                        first_child = False#keep running. there might be sequences above us that care though.
                        to_add = True
                        #local_root_to_relevant_list_map[node_to_local_root_map[node_id]].append(node_id)#this is a valid resume point. tell the local root about it.
                    if not first_child:
                        sequence_to_relevant_descendants_map[cur_id].add(node_id)
            #make sure there's not a decorator above the end point that invalidates our need to track running.
            while not true_done:
                previous_id = cur_id
                cur_id = nodes[cur_id][1]
                if cur_id == end_target:
                    true_done = True
                elif cur_id in decorator_set:
                    if "running_is" in nodes[cur_id][0]:#if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
                        true_done = True
                        to_add = False
                        #if node_id in local_root_to_relevant_list_map[node_to_local_root_map[node_id]]:#check if we added it in
                            #local_root_to_relevant_list_map[node_to_local_root_map[node_id]].pop()#if we added it in, it must be at the end. 
                        for sequence in sequences_found:#this sequence cannot resume. indicate as such.
                            sequence_to_relevant_descendants_map[sequence] = set()
            if to_add:
                local_root_to_relevant_list_map[node_to_local_root_map[node_id]].append(node_id)#this is a valid resume point. tell the local root about it. 

    return (local_root_to_relevant_list_map, sequence_to_relevant_descendants_map)

#return node_to_descendants_map. this maps each node to the set of all of it's descendants. leaf nodes map to an empty set. a node is not it's own descendant
def create_node_to_descendants_map(nodes, children, leaf_set):
    node_to_descendants_map={}
    for node_id in range(len(nodes)):
        node_to_descendants_map[node_id] = set()
        if node_id in leaf_set or node_id not in children or len(children[node_id]) == 0:
            #this is a terminus point
            cur_id = nodes[node_id][1]
            while not cur_id == -1:
                node_to_descendants_map[cur_id].add(node_id)
                cur_id=nodes[cur_id][1]
    return node_to_descendants_map


#-----------------------------------------------------------------------------------------------------------------------

#creates the strings necessary for initialization stuff
def create_nodes(nodes, children, additional_arguments, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, parallel_policies):
    define_string = ""
    init_string = ""
    next_string = ""
    var_string = ""
    for node_id in range(0, len(nodes)):
        #print(node_id)
        if node_id == 0:
            define_string += "\t\t" + nodes[node_id][2] + ".active := TRUE;" + os.linesep
        """
        if node_id == 0:
            active_val = "TRUE"
        else:
            active_val = nodes[nodes[node_id][1]][2] + ".active_" + str(children[nodes[node_id][1]].index(node_id))
        """
        if node_id in selector_set or node_id in sequence_set or node_id in parallel_synch_set or node_id in parallel_unsynch_set:
            if node_id not in children or len(children[node_id]) == 0:
                #this node has no children
                children_string = ""
            else:
                children_string = ""
                for child in children[node_id]:
                    children_string += ", " + nodes[child][2]
                children_string = children_string[2:]
        #---------------------------------
        if node_id in leaf_set:
            var_string += "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + "("
        elif node_id in selector_set:
            var_string += "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + str(len(children[node_id])) + "(" + children_string
        elif node_id in sequence_set:
            if node_id not in children or len(children[node_id]) < 2:
                resume_point = "-2"
            else:
                resume_point = "resume_point_" + str(node_id)
            if children_string == "":
                pass
            else:
                children_string = children_string + ', '
            var_string += "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + str(len(children[node_id])) + "(" + children_string + resume_point
        elif node_id in decorator_set:
            var_string += "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + "(" + nodes[children[node_id][0]][2]
        elif node_id in parallel_synch_set or node_id in parallel_unsynch_set:
            if node_id not in children or len(children[node_id]) == 0:
                skip_string = "[-2]"
            else:
                skip_string = "["
                for child in children[node_id]:
                    skip_string += "resume_from_node_" + str(child) + ", "
                skip_string = skip_string[0:-2] + "]"
            define_string += "\t\tparallel_skip_" + str(node_id) + " := " + skip_string + ";" + os.linesep
            if parallel_policies[node_id] == True:
                inject_string = "_success_on_all"
            else:
                inject_string = "_success_on_one"
                
            if children_string == "":
                pass
            else:
                children_string = children_string + ', '
            var_string += "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + inject_string + str(len(children[node_id])) + "(" + children_string + " parallel_skip_" + str(node_id)
        else:
            print('ERROR: node is not leaf, selector, sequence, decorator, or parallel. This should not be possible. Node information follows')
            print(nodes[node_id])
            var_string += "0"
        #---------------------------------
        if node_id in leaf_set:
            first = True
        else:
            first = False
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'arg' in additional_arguments[node_id][i]:
                    if first:
                        first = False
                        var_string = (var_string + additional_arguments[node_id][i]['arg'])
                    else:
                        var_string = (var_string + ", " + additional_arguments[node_id][i]['arg'])
                if 'nodes_with_access_to' in additional_arguments[node_id][i]:
                    set_string='{'
                    for node_with_access in variable_access[additional_arguments[node_id][i]['nodes_with_access_to']]:
                        set_string = set_string + str(node_with_access) + ', '
                    set_string=set_string[0:-2]+'}'#replace the last comma with a }
                    if first:
                        first = False
                        var_string = (var_string + set_string)
                    else:
                        var_string = (var_string + ", " + set_string)
                if 'range_placeholder' in additional_arguments[node_id][i]:
                    if first:
                        first = False
                        var_string = (var_string + str(len(children[node_id])-1))
                    else:
                        var_string = (var_string + ", " + str(len(children[node_id])-1))
                    
            var_string = var_string + ");" + os.linesep
            for i in range(0, len(additional_arguments[node_id])):
                if 'decl' in additional_arguments[node_id][i]:
                    var_string = var_string + additional_arguments[node_id][i]['decl']       
        else:#does not have  additional arguments
            var_string = (var_string + ");" + os.linesep)

    return (define_string, var_string, init_string, next_string)

#runs through any additional arguments
def create_additional_arguments(nodes, additional_arguments):
    var_string = ""
    define_string = ""
    init_string = ""
    next_string =  ""
    for node_id in range(len(nodes)):
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'invar' in additional_arguments[node_id][i]:
                    var_string = (var_string + additional_arguments[node_id][i]['invar'])
    for node_id in range(len(nodes)):
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'init' in additional_arguments[node_id][i]:
                    init_string = init_string + additional_arguments[node_id][i]['init']
    for node_id in range(len(nodes)):
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'next' in additional_arguments[node_id][i]:
                    next_string = next_string + additional_arguments[node_id][i]['next']
    return(var_string, define_string, init_string, next_string)

#responsible for creating the resume structure
def create_resume_structure(nodes, local_root_to_relevant_list_map, children):
    
    #things to still implement: new resume structure

    #each local root tracks it's possible resume locations. unchanged from previous versions
    #if anywhere upstream returns success/failure, indicate no resume
    #if local root returns failure, indicate no resume
    #if local root returns success, indicate SKIP or NO RESUME, depending on if parent it parallel_synch
    #if local root returns running, track running based on macros from children.

    #note here that we might need two propagations
    #propagation 1 -> resume_child_ID is what we currently have built
    #propagation 2 -> running_child_ID......wait what do we use this for? oh right. cuz we don't have active node? no.....we can just list through all the options? well. propagation might be cleaner?

    #well, we're gonna try it

    #so, resume_from_node_LOCAL_ROOT tracks the actual value that we need to resume from.

    var_resume_from_node_string = "" #this is a variable that actually stores what running state we're in
    init_resume_from_node_string = ""
    next_resume_from_node_string = ""
    var_define_status_string = "" #this is for storing the define versions that are constants.
    define_trace_running_source = "" #this is storing for the propagation mechanism. rename everything later lmao.
    for local_root in local_root_to_relevant_list_map:
        relevant_list = local_root_to_relevant_list_map[local_root]
        if len(relevant_list) == 0:
            #there's nothing to resume from. if we have a sequence node, then it apparently only had 0 or 1 children, and we don't need any special resume for it.
            var_define_status_string += "\t\tresume_from_node_" + str(local_root) + " := -3;" + os.linesep
            continue
        var_resume_from_node_string += "\t\tresume_from_node_" + str(local_root) + " : {" + str(local_root) + ", " + str(relevant_list)[1:-1] + "};" + os.linesep
        init_resume_from_node_string += "\t\tinit(resume_from_node_" + str(local_root) + ") := " + str(local_root) + ";" + os.linesep
        if -2 in relevant_list:
            inject_string = ("\t\t\t\t(statuses[" + str(local_root) + "] = success) : -2;" + os.linesep#if the local root returns success, this is skippable. note that this is checked after the reset condition, so we don't over-write the reset.
                             + "\t\t\t\t(statuses[" + str(local_root) + "] = failure) : " + str(local_root) + ";" + os.linesep#failure is still a reset though
            )
            relevant_list.remove(-2)#don't actually want it in the relevant set going forward
        else:
            inject_string = "\t\t\t\t(statuses[" + str(local_root) + "] in {success, failure}) : " + str(local_root) + ";" + os.linesep#reset since this isn't skippable.
        cur_node = nodes[local_root][1]#we've manually handled the root case using inject_string
        ancestor_string = ""
        while not cur_node == -1:
            ancestor_string += "\t\t\t\t(statuses[" + str(cur_node) + "] in {success, failure}) : " + str(local_root) + ";" + os.linesep
            cur_node=nodes[cur_node][1]
        #go through and add all the ancestors of the local root to a set for the purpose of resetting.
        next_resume_from_node_string += ("\t\tnext(resume_from_node_" + str(local_root) + ") := " + os.linesep
                                      + "\t\t\tcase" + os.linesep
                                      + ancestor_string #highest priority is reset
                                      + inject_string #parallel_synch nodes have a special condition
        )
        if len(relevant_list) == 0:
            #this was solely for the purpose of skipping success nodes with parallel_synch nodes
            #since ancestor and inject_string already happened, we'll just exit with a default case
            next_resume_from_node_string += ("\t\t\t\tTRUE : " + str(local_root) + ";" + os.linesep
                                             + "\t\t\tesac;" + os.linesep
                                             )
            continue
        
        def trace_running_source(node_id):
            nonlocal define_trace_running_source
            cases = ""
            if node_id not in children or len(children[node_id]) == 0:
                pass
            else:
                for child in children[node_id]:
                    if trace_running_source(child):
                        cases += "\t\t\t\t!(trace_running_source_" + str(child) + " = -2) : trace_running_source_" + str(child) + ";" + os.linesep
            if cases == "":
                if node_id in relevant_list:
                    define_trace_running_source += "\t\ttrace_running_source_" + str(node_id) + " := (statuses[" + str(node_id) + "] = running) ? " + str(node_id) + " : -2;" + os.linesep
                    return True
                return False
            if node_id in relevant_list:
                cases += "\t\t\t\t(statuses[" + str(node_id) + "] = running) : " + str(node_id) + ";" + os.linesep
            define_trace_running_source += ("\t\ttrace_running_source_" + str(node_id) + " := " + os.linesep
                                        + "\t\t\tcase" + os.linesep
                                        + cases
                                        + "\t\t\t\tTRUE : -2;" + os.linesep
                                        + "\t\t\tesac;" + os.linesep
            )
            return True
        trace_running_source(local_root)
        next_resume_from_node_string += ("\t\t\t\tTRUE : max(trace_running_source_"  + str(local_root) + ", " + str(local_root) + ");" + os.linesep
                               #we didn't encounter any reset triggers, so we use trace_running_source
                               #note that if trace_running_source = -2, then we're just setting to local_root.
                               #if something returned running, the value will be >= local_root, so we'll point to that
                               #note that since we are always executing the entire tree, if we returned running last time we will definitely resume this time.
                               + "\t\t\tesac;" + os.linesep
        )
        #below is the old version
        '''
        for resume_point in reversed(relevant_list):
            #this list is ordered so that selectors will not override their children returning running.
            next_resume_from_node_string += "\t\t\t\t(statuses[" + str(resume_point) + "] = running) : " + str(resume_point) + ";" + os.linesep#if running, set to that location
        for resume_point in relevant_list:
            next_resume_from_node_string += "\t\t\t\t(resume_from_node_" + str(local_root) + " = " + str(resume_point) + ") & !(next(relevant_child_" + str(resume_point) + ") = -2) : " + str(local_root) + ";" + os.linesep #reset if we
        next_resume_from_node_string += "\t\t\t\t(statuses[resume_from_node_" + str(local_root) + "] in {success, failure}) : " + str(local_root) + ";" + os.linesep#if the node we were planning to resume from has returned success or failure, then reset
        #next_resume_from_node_string += "\t\t\t\t(next(active_node)" + os.linesep
        next_resume_from_node_string += ("\t\t\t\tTRUE : resume_from_node_" + str(local_root) + ";" + os.linesep#otherwise, hold
                                      + "\t\t\tesac;" + os.linesep
        )
        '''
        
        
        
    define_string = var_define_status_string + define_trace_running_source
    var_string = var_resume_from_node_string
    init_string = init_resume_from_node_string
    next_string =  next_resume_from_node_string
    return (define_string, var_string, init_string, next_string)

#create the resume_point variable that tells sequence nodes which child to start at
def create_resume_point(sequence_set, node_to_local_root_map, local_root_to_relevant_list_map, node_to_descendants_map, children):
    resume_point_string = ""
    for sequence in sequence_set:
        #print('new sequence:')
        #print(sequence)
        if sequence not in children or len(children[sequence]) < 2:
            #print('few children. skipping')
            #we have 0 or 1 children
            #if there are no children, then resume_point really doesn't matter, but we need to pass a value
            #if there is 1 child, then we never skip it, so resume_point really doesn't matter, but we need to pass a value
            #hard code -2 into the sequence in this case
            pass
        else:
            #print('multiple children')
            #have an actual quantity of children
            local_root = node_to_local_root_map[sequence]
            relevant_list = local_root_to_relevant_list_map[local_root]
            if len(relevant_list) == 0:
                #print('no real resume children. hard coding -2')
                resume_point_string += "\t\tresume_point_" + str(sequence) + " := -2;" + os.linesep
            else:
                #print('real resume target present. initiating')
                resume_point_string += ("\t\tresume_point_" + str(sequence) + " := " + os.linesep
                                        + "\t\t\tcase" + os.linesep
                )
                descendants = node_to_descendants_map[sequence]
                child_index_to_relevant_descendants_map = {} 
                #print(descendants)
                for relevant_node in relevant_list:
                    #print(relevant_node)
                    if relevant_node in descendants:
                        for child_index in range(len(children[sequence])):
                            child = children[sequence][child_index]
                            if relevant_node in node_to_descendants_map[child]:
                                if child in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(relevant_node)
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {relevant_node}
                            elif child == relevant_node:
                                if child in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(relevant_node)
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {relevant_node}
                for child_index in child_index_to_relevant_descendants_map:
                    resume_point_string += "\t\t\t\t(resume_from_node_" + str(local_root) + " in " + str(child_index_to_relevant_descendants_map[child_index]) + ") : " + str(child_index) + ";" + os.linesep
                resume_point_string += ("\t\t\t\tTRUE : -2;" + os.linesep
                                        #we have nothing to resume from
                                        + "\t\t\tesac;" + os.linesep
                )

    define_string = resume_point_string
    var_string = ""
    init_string = ""
    next_string = ""

    return (define_string, var_string, init_string, next_string)
##############################################################################
# Main
##############################################################################

def main():
    global blackboard_needed

    arg_parser=argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('root_file')
    arg_parser.add_argument('root_method')
    arg_parser.add_argument('--root_args', default='', nargs='*')
    arg_parser.add_argument('--string_args', default='', nargs='*')
    arg_parser.add_argument('--min_val', default=0, type=int)
    arg_parser.add_argument('--max_val', default=1, type=int)
    arg_parser.add_argument('--force_parallel_unsynch', action='store_true')
    arg_parser.add_argument('--no_seperate_variable_modules', action='store_true')
    arg_parser.add_argument('--blackboard_input_file')
    arg_parser.add_argument('--module_input_file')
    arg_parser.add_argument('--specs_input_file')
    arg_parser.add_argument('--gen_modules', default=0, type=int)#0 means no generation, 1 means seperate var, 2 means seperate constant
    arg_parser.add_argument('--output_file', default=None)
    arg_parser.add_argument('--module_output_file', default=None)
    arg_parser.add_argument('--blackboard_output_file', default=None)
    arg_parser.add_argument('--overwrite', action='store_true')
    args=arg_parser.parse_args()

    module = __import__(args.root_file.replace('.py', ''))

    root_string = 'module.' + args.root_method + '('
    first = True
    for root_arg in args.root_args:
        if first:
            root_string += root_arg
            first=False
        else:
            root_string += ', ' + root_arg
    for string_arg in args.string_args:
        if first:
            root_string += '\'' + string_arg + '\''
            first=False
        else:
            root_string += ', ' + '\'' + string_arg + '\''
    root_string += ')'
    root = eval(root_string)

    #tracking variables
    children={-1:[]}#stores a list of children ID. is indexed via node id
    nodes={}#stores a tuple, (type, parent_id, node_name), where type informs us of the node type, and parent of the parent id, and node_name. it's indexed via node id
    node_names={}#a list of node names. each name is also associated with an integer that indicates how many times it has been seen, allowing us to automatically create a new name.
    variable_name_to_int={}#a mapping of variable names to their integer locations
    #max_children = 0#tracks the maximum number of children possible.
    parallel_policies = {} #a map from parallel nodes to True, False
    #-------------------------------------------------------------------------------
    #blackboard information
    variable_access={}#for each variable, a list of nodes with access to that variable.
    variable_check={}#for each variable, a list of nodes that check that variable. indexed by variable name
    #-------------------------------------------------------------------------------
    #sets
    parallel_synch_set = set()
    parallel_unsynch_set = set()
    sequence_set = set()
    selector_set = set()
    decorator_set = set()
    leaf_set = set()
    #-------------------------------------------------------------------------------
    #variables that we need to properly construct stuff later
    additional_arguments={}#stores additional arguments. it's index via node id
    external_status_req = []#list of nodes that require external status. each entry is the node name.
    needed_nodes=set()#the set of node types needed
    
    next_available_id = walk_tree(root, -1, 0, children, nodes, additional_arguments, needed_nodes, node_names, variable_access, variable_check, variable_name_to_int, external_status_req, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, parallel_policies, args.force_parallel_unsynch)
    #print(nodes)
    #for parent in children:
    #    max_children = max(max_children, len(children[parent]) - 1)
    
    node_to_local_root_map = create_node_to_local_root_map(nodes, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
    (local_root_to_relevant_list_map, sequence_to_relevant_descendants_map) = create_local_root_to_relevant_list_map(nodes, children, node_to_local_root_map, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
    variable_name_cleanup(variable_name_to_int, variable_access)
    node_to_descendants_map = create_node_to_descendants_map(nodes, children, leaf_set)

    
    int_to_variable = {}
    for variable in variable_name_to_int:
        int_to_variable[variable_name_to_int[variable]] = variable

    #------------------------------------------------------------------------------------------------------------------------
    #done with variable decleration, moving into string building.

        
    define_string = ("MODULE main" + os.linesep
                     + "\tCONSTANTS" + os.linesep
                     + "\t\tsuccess, failure, running, invalid;" + os.linesep
                     + "\tDEFINE" + os.linesep
                     + "\t\tstatuses := ["
    )
    for node_id in range(len(nodes)):
        if node_id==0:
            define_string += nodes[node_id][2] + ".status"
        else:
            define_string += ", " + nodes[node_id][2] + ".status"
    define_string += "];" + os.linesep

    #------------------------------------------------------------------------------------------------------------------------
    var_string = (""
                  + "\tVAR" + os.linesep
                  #+ "\t\tfake_node : fake_node();" + os.linesep
    )       
    if variable_name_to_int:
        var_string += "\t\tvariable_names : define_variables;" + os.linesep
    var_string += "\t\tnode_names : define_nodes;" + os.linesep
    if blackboard_needed:
        var_string += "\t\tblackboard : blackboard_module(node_names, variable_names, statuses);" + os.linesep
    #------------------------------------------------------------------------------------------------------------------------
    init_string = ("\tASSIGN" + os.linesep
    )
    next_string = ""
    #------------------------------------------------------------------------------------------------------------------------
    
    (new_define, new_var, new_init, new_next) = create_resume_structure(nodes, local_root_to_relevant_list_map, children)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    
    (new_define, new_var, new_init, new_next) = create_resume_point(sequence_set, node_to_local_root_map, local_root_to_relevant_list_map, node_to_descendants_map, children)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_nodes(nodes, children, additional_arguments, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, parallel_policies)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_additional_arguments(nodes, additional_arguments)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    nuxmv_string = define_string + var_string + init_string + next_string
    #------------------------------------------------------------------------------------------------------------------------
    if args.specs_input_file:
        nuxmv_string += open(args.specs_input_file).read() + os.linesep + os.linesep

    # nuxmv_string += ("MODULE fake_node()" + os.linesep
    #                  + "\tCONSTANTS" + os.linesep
    #                  + "\t\tsuccess, failure, running, invalid;" + os.linesep
    #                  + "\tDEFINE" + os.linesep
    #                  + "\t\tstatus := invalid;" + os.linesep
    # )
    for needed in needed_nodes:
        nuxmv_string = nuxmv_string +  eval('node_creator.create_'+needed+'()')
    seen_children = set()
    for selector in selector_set:
        if len(children[selector]) in seen_children:
            pass
        else:
            seen_children.add(len(children[selector]))
            nuxmv_string += node_creator.create_node_selector(len(children[selector]))
    seen_children = set()
    for sequence in sequence_set:
        if len(children[sequence]) in seen_children:
            pass
        else:
            seen_children.add(len(children[sequence]))
            nuxmv_string += node_creator.create_node_sequence(len(children[sequence]))
    seen_children_all = set()
    seen_children_one = set()
    for parallel in (parallel_synch_set.union(parallel_unsynch_set)):
        if parallel_policies[parallel]:
            if len(children[parallel]) in seen_children_all:
                pass
            else:
                seen_children_all.add(len(children[parallel]))
                nuxmv_string += node_creator.create_node_parallel(len(children[parallel]), True)
        else:
            if len(children[parallel]) in seen_children_one:
                pass
            else:
                seen_children_one.add(len(children[parallel]))
                nuxmv_string += node_creator.create_node_parallel(len(children[parallel]), False)
            
    
    

    nuxmv_string = nuxmv_string + node_creator.create_names_module(variable_name_to_int, nodes)


    #print a blackboard variable chart
    for variable in variable_name_to_int:
        nuxmv_string += ('--' + variable + ' : ' + str(variable_name_to_int[variable]) + os.linesep)
        if variable_name_to_int[variable] in variable_access:
            for access_node in variable_access[variable_name_to_int[variable]]:
                nuxmv_string += ('----' + nodes[access_node][2] + os.linesep)

    
    module_string = ''
    if args.blackboard_input_file:
        nuxmv_string = nuxmv_string + open(args.blackboard_input_file).read()
    else:
        blackboard_string = ''
        if blackboard_needed:
            blackboard_string = blackboard_string + node_creator.create_blackboard(int_to_variable, variable_name_to_int, variable_access, nodes, args.no_seperate_variable_modules, args.min_val, args.max_val)
        if args.blackboard_output_file is None:
            nuxmv_string = nuxmv_string + blackboard_string
        else:
            if args.overwrite:
                with open(args.blackboard_output_file, 'w') as f:
                    f.write(blackboard_string)
            else:
                try:
                    with open(args.blackboard_output_file, 'x') as f:
                        f.write(blackboard_string)
                except FileExistsError:
                    print('The specified blackboard file already exists. To overwrite the file, rerun the command with --overwrite True')
    
    if args.module_input_file:
        #print(open(modules).read())
        nuxmv_string = nuxmv_string + open(args.module_input_file).read()
    else:
        if args.gen_modules == 1:
            set_string = "{"
            first = True;
            for i in range(args.min_val, args.max_val + 1):
                if first:
                    first = False;
                    set_string += str(i)
                else:
                    set_string += ", " + str(i)
                    set_string += "}"
            if not args.no_seperate_variable_modules:
                for variable in variable_name_to_int:
                    module_string += ("MODULE " + variable + "_SET_module(variables, variable_exists, node_names, variable_names, statuses)" + os.linesep
                                      + "\tVAR" + os.linesep
                                      + "\t\t" + variable + " : " + str(args.min_val) + ".." + str(args.max_val) + ";" + os.linesep
                                      + "\t\t" + variable + "_exists" + " : boolean;" + os.linesep
                                      + "\tASSIGN" + os.linesep
                                      + "\t\tinit(" + variable + ") := " + str(args.min_val) + ";" + os.linesep
                                      + "\t\tinit(" + variable + "_exists) := FALSE;" + os.linesep
                                      + "\t\tnext(" + variable + ") := " + os.linesep
                                      + "\t\t\tcase" + os.linesep
                    )
                    for node in variable_access[variable]:
                        module_string += "\t\t\t\t(statuses[" + str(node) + "] = success) : " + set_string + ";" + os.linesep
                    module_string += ("\t\t\t\tTRUE : " + variable + ";" + os.linesep
                                      + "\t\t\tesac;" + os.linesep
                                      + "\t\tnext(" + variable + "_exists) := " + os.linesep
                                      + "\t\t\tcase" + os.linesep
                    )
                    for node in variable_access[variable]:
                        module_string += "\t\t\t\t(statuses[" + str(node) + "] = success) : TRUE;" + os.linesep
                    module_string += ("\t\t\t\tTRUE : " + variable + "_exists;" + os.linesep
                                      + "\t\t\tesac;" + os.linesep
                    )
            for node in external_status_req:
                module_string += ("MODULE " + node + "_SET_status_module(variables, variable_exists, node_names, variable_names)" + os.linesep
                                  + "\tCONSTANTS" + os.linesep
                                  + "\t\tsuccess, failure, running, invalid;" + os.linesep
                                  + "\tIVAR" + os.linesep
                                  + "\t\tinput_status : {success, failure, running};" + os.linesep
                                  + "\tDEFINE" + os.linesep
                                  + "\t\tstatus := input_status;" + os.linesep
                )
            for variable in variable_check:
                for node_id in variable_check[variable]:
                    module_string += ("MODULE " + nodes[node_id][2] + "_CHECK_" + variable + "_module(variables, variable_exists, node_names, variable_names)" + os.linesep
                                      + "\tDEFINE" + os.linesep
                                      + "\t\tresult := ((variable_exists[variable_names." + variable + "]) & (variables[variable_names." + variable + "] = " + str(args.max_val) + "));" + os.linesep
                    )
        elif args.gen_modules == 2:
            set_string = "{"
            first = True;
            for i in range(args.min_val, args.max_val + 1):
                if first:
                    first = False;
                    set_string += str(i)
                else:
                    set_string += ", " + str(i)
                    set_string += "}"

            if not args.no_seperate_variable_modules:
                for variable in variable_name_to_int:
                    module_string += ("MODULE " + variable + "_SET_module(variables, variable_exists, node_names, variable_names, statuses)" + os.linesep
                                      + "\tDEFINE" + os.linesep
                                      + "\t\t" + variable + " := " + str(args.min_val) + ";" + os.linesep
                                      + "\t\t" + variable + "_exists" + " := TRUE;" + os.linesep
                    )
            for node in external_status_req:
                module_string += ("MODULE " + node + "_SET_status_module(variables, variable_exists, node_names, variable_names)" + os.linesep
                                  + "\tCONSTANTS" + os.linesep
                                  + "\t\tsuccess, failure, running, invalid;" + os.linesep
                                  + "\tIVAR" + os.linesep
                                  + "\t\tinput_status : {success, failure, running};" + os.linesep
                                  + "\tDEFINE" + os.linesep
                                  + "\t\tstatus := input_status;" + os.linesep
                )
            for variable in variable_check:
                for node_id in variable_check[variable]:
                    module_string += ("MODULE " + nodes[node_id][2] + "_CHECK_" + variable + "_module(variables, variable_exists, node_names, variable_names)" + os.linesep
                                      + "\tDEFINE" + os.linesep
                                      + "\t\tresult := (variables[variable_names." + variable + "] = " + str(args.max_val) + ");" + os.linesep
                    )

        if args.module_output_file is None:
            nuxmv_string = nuxmv_string + module_string
        else:
            if args.overwrite:
                with open(args.module_output_file, 'w') as f:
                    f.write(module_string)
            else:
                try:
                    with open(args.module_output_file, 'x') as f:
                        f.write(module_string)
                except FileExistsError:
                    print('The specified module file already exists. To overwrite the file, rerun the command with --overwrite True')
    if args.output_file is None:
        print(nuxmv_string)
    else:
        if args.overwrite:
            with open(args.output_file, 'w') as f:
                f.write(nuxmv_string)
        else:
            try:
                with open(args.output_file, 'x') as f:
                    f.write(nuxmv_string)
            except FileExistsError:
                print('The specified output file already exists. To overwrite the file, rerun the command with --overwrite True')
        
    
    
    return
    

main()
