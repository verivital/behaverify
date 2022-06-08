#python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 


#whichever moron designed emacs to delete #FILE# when you delete FILE is an idiot

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


import argparse
import py_trees
import sys
import time
import os
import re
import inspect

import py_trees.console as console

import node_creator_total as node_creator

blackboard_needed = False
#----------------------------------------------------------------------------------------------------------------
#regex stuff
blackboard_name_pattern = re.compile(r"#*(?P<blackboard_name>[^\s=]+)\s*=\s*py_trees\.blackboard\.Blackboard\(\s*\)")
#----------------------------------------------------------------------------------------------------------------
        
#-----------------------------------------------------------------------------------------------------------------------
def walk_tree(t, parent_id, next_available_id, children, nodes, additional_arguments, needed_nodes, node_names, variable_access, variable_check, variable_name_to_int, external_status_req, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, parallel_unsynch = False):
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
            decl_string = ("\t\t" + node_name + "_SET_status : " + node_name + "_SET_status_module(active_node, " + str(this_id) + ", random_status, blackboard.variables, blackboard.variable_exists, node_names, variable_names);" + os.linesep)
            additional_arguments[this_id]=[{'arg': node_name + "_SET_status", 'decl' : decl_string},]
            #leaf_node_exit(this_id)
            return next_available_id
        elif t.serene_info_variable == "BlueROV_Task_Node":
            #currently this is beign used in the same way as the one above.
            pass
    except AttributeError as e:
        #print(e)
        #print(node_name+ " ERROR?")
        pass

    is_decorator = True
    if isinstance(t, py_trees.composites.Sequence):
        #children[this_id]=[]
        nodes[this_id]=('node_sequence', parent_id, node_name)
        needed_nodes.add('node_sequence')
        sequence_set.add(this_id)
        is_decorator = False
    elif isinstance(t, py_trees.composites.Selector):
        #resume_node=this_id
        #children[this_id]=[]
        nodes[this_id]=('node_selector', parent_id, node_name)
        needed_nodes.add('node_selector')
        selector_set.add(this_id)
        is_decorator = False
    elif isinstance(t, py_trees.composites.Parallel):
        is_decorator = False
        #resume_node=this_id
        #children[this_id]=[]
        if t.policy.synchronise and (not parallel_unsynch):
            parallel_synch_set.add(this_id)
            #nodes[this_id]=('node_parallel_synchronised', parent_id, node_name)
            nodes[this_id]=('node_parallel', parent_id, node_name)
            #needed_nodes.add('node_parallel_synchronised')
            needed_nodes.add('node_parallel')
            if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                additional_arguments[this_id]=[{'arg' : "TRUE, TRUE"}]
            elif isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                additional_arguments[this_id]=[{'arg' : "TRUE, FALSE"}]
            else:
                print('ERROR: the following parallel policy is not supported: ' + str(t.policy))
                sys.exit('Unsupported Parallel Policy')
        else:
            parallel_unsynch_set.add(this_id)
            #nodes[this_id]=('node_parallel_unsynchronised', parent_id, node_name)
            nodes[this_id]=('node_parallel', parent_id, node_name)
            #needed_nodes.add('node_parallel_unsynchronised')
            needed_nodes.add('node_parallel')
            if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                additional_arguments[this_id]=[{'arg' : "FALSE, TRUE"}]
            elif isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                additional_arguments[this_id]=[{'arg' : "FALSE, FALSE"}]
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
                                                     + ' : '+ node_name + '_CHECK_' + variable_name + '_module(active_node, ' + str(this_id) + ', blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep)
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
        decl_string = ("\t\t" + node_name + "_SET_status : " + node_name + "_SET_status_module(active_node, " + str(this_id) + ", random_status, blackboard.variables, blackboard.variable_exists, node_names, variable_names);" + os.linesep)
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
                                                     + ' : '+ node_name + '_CHECK_' + variable_name + '_module(active_node, ' + str(this_id) + ', blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep)
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
        additional_arguments[this_id] = [{'arg' : 'random_status'}]
        #leaf_node_exit(this_id)
        return next_available_id
    else:#currently defaulting to default. will rework this later probably
        nodes[this_id]=('node_default', parent_id, node_name)
        needed_nodes.add('node_default')
        additional_arguments[this_id] = [{'arg' : 'random_status'}]
        #leaf_node_exit(this_id)
        return next_available_id

    leaf_set.remove(this_id)
    if is_decorator:
        decorator_set.add(this_id)
    children[this_id] = []#if we've reached this point, then this node has children, and we are going to set up an empty list for it.
    for child in t.children:
        next_available_id = walk_tree(child, this_id, next_available_id, children, nodes, additional_arguments, needed_nodes, node_names, variable_access, variable_check, variable_name_to_int, external_status_req, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, parallel_unsynch)
    return next_available_id

#-----------------------------------------------------------------------------------------------------------------------
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
        #this needs to encompass all cases where a leaf node can return Running
        return True#currently being lazy, and just going to assume they can all return Running, even though this is not the case
    else:
        return True#selector and parallel can, everything else covered above
        
#return (local_root_to_relevant_list_map, sequence_to_relevant_descendants_map)
def create_local_root_to_relevant_list_map(nodes, children, node_to_local_root_map, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
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
        elif can_create_running(nodes, node_id, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
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
def create_nodes(nodes, children, additional_arguments, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
    define_string = ""
    init_string = ""
    next_string =  ""
    var_string = ""
    for parallel_node in parallel_synch_set:
        cur_node = parallel_node
        ancestor_string = ("\t\tparallel_reset_" + str(parallel_node) + " := " + os.linesep
                           + "\t\t\tcase" + os.linesep)
        
        while not cur_node == -1:
            ancestor_string += ("\t\t\t\t(statuses[" + str(cur_node) + "] in {success, failure}) : TRUE;" + os.linesep#reset on success, failure
            )
            cur_node=nodes[cur_node][1]
        define_string += (ancestor_string
                          + "\t\t\t\tTRUE : FALSE;" + os.linesep
                          + "\t\t\tesac;" + os.linesep
        )
        if parallel_node in children and len(children[parallel_node]) >= 0:
            define_string += "\t\tlast_child_" + str(parallel_node) + " := " + str(children[-1]) + ";" + os.linesep
            define_string += ("\t\tlast_child_" + str(parallel_node) + " := ;" + os.linesep
                              + "\t\t\tcase" + os.linesep
            )
            for child_index in range(len(children[parallel_node])-1, -1, -1):
                define_string += "\t\t\t\t(resume_from_node_" + str(children[parallel_node][child_index]) + ") : " + children[parallel_node][child_index] + ";" + os.linesep
                
            define_string += ("\t\t\t\tTRUE: -2;" + os.linesep
                              + "\t\t\tesac;" + os.linesep
            )
        else:
            define_string += "\t\tlast_child_" + str(parallel_node) + " := -2;" + os.linesep
    for parallel_node in parallel_unsynch_set:
        cur_node = parallel_node
        ancestor_string = ("\t\tparallel_reset_" + str(parallel_node) + " := " + os.linesep
                           + "\t\t\tcase" + os.linesep)
        
        while not cur_node == -1:
            ancestor_string += ("\t\t\t\t(statuses[" + str(cur_node) + "] in {success, failure, running}) : TRUE;" + os.linesep#reset always.
            )
            cur_node=nodes[cur_node][1]
        define_string += (ancestor_string
                          + "\t\t\t\tTRUE : FALSE;" + os.linesep
                          + "\t\t\tesac;" + os.linesep
        )
        if parallel_node in children and len(children[parallel_node]) >= 0:
            define_string += "\t\tlast_child_" + str(parallel_node) + " := " + str(children[parallel_node][-1]) + ";" + os.linesep
        else:
            define_string += "\t\tlast_child_" + str(parallel_node) + " := -2;" + os.linesep
    for selector_node in selector_set:
        if selector_node in children and len(children[selector_node]) >= 0:
            define_string += "\t\tlast_child_" + str(selector_node) + " := " + str(children[selector_node][-1]) + ";" + os.linesep
        else:
            define_string += "\t\tlast_child_" + str(selector_node) + " := -2;" + os.linesep
    for sequence_node in sequence_set:
        if sequence_node in children and len(children[sequence_node]) >= 0:
            define_string += "\t\tlast_child_" + str(sequence_node) + " := " + str(children[sequence_node][-1]) + ";" + os.linesep
        else:
            define_string += "\t\tlast_child_" + str(sequence_node) + " := -2;" + os.linesep
        
    for node_id in range(0, len(nodes)):
        #print(node_id)
        var_string = (var_string
                        + "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + "("
        )
        if node_id not in children or len(children[node_id]) == 0:
            #this node has no children
            relevant_status = "invalid"
        else:
            relevant_status = "relevant_status_" + str(node_id)
        if node_id in leaf_set:
            var_string += "active_node, " + str(node_id)
        elif node_id in selector_set:
            var_string += "relevant_child_" + str(node_id) + ", " + relevant_status + ", last_child_" + str(node_id)
        elif node_id in sequence_set:
            var_string += "relevant_child_" + str(node_id) + ", " + relevant_status + ", last_child_" + str(node_id)
        elif node_id in decorator_set:
            var_string += "relevant_child_" + str(node_id) + ", " + relevant_status + ""
        elif node_id in parallel_synch_set or node_id in parallel_unsynch_set:
            var_string += "relevant_child_" + str(node_id) + ", " + relevant_status + ", last_child_" + str(node_id) + ", parallel_reset_" + str(node_id)

        else:
            print('ERROR: node is not leaf, selector, sequence, decorator, or parallel. This should not be possible. Node information follows')
            print(nodes[node_id])
            var_string += "0"
        
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'arg' in additional_arguments[node_id][i]:
                    var_string = (var_string + ", " + additional_arguments[node_id][i]['arg'])
                if 'nodes_with_access_to' in additional_arguments[node_id][i]:
                    set_string='{'
                    for node_with_access in variable_access[additional_arguments[node_id][i]['nodes_with_access_to']]:
                        set_string = set_string + str(node_with_access) + ', '
                    set_string=set_string[0:-2]+'}'#replace the last comma with a }
                    var_string = (var_string + ", " + set_string)
                if 'range_placeholder' in additional_arguments[node_id][i]:
                    var_string = (var_string + ", " + str(len(children[node_id])-1))
                    
            var_string = var_string + ");" + os.linesep
            for i in range(0, len(additional_arguments[node_id])):
                if 'decl' in additional_arguments[node_id][i]:
                    var_string = var_string + additional_arguments[node_id][i]['decl']       
        else:#does not have  additional arguments
            var_string = (var_string + ");" + os.linesep)

    return (define_string, var_string, init_string, next_string)

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


def create_resume_structure(nodes, local_root_to_relevant_list_map):
    var_resume_from_node_string = "" #this is a variable that actually stores what running state we're in
    init_resume_from_node_string = ""
    next_resume_from_node_string = ""
    var_define_status_string = "" #this is for storing the define versions that are constants.
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
        
        
        
    define_string = var_define_status_string
    var_string = var_resume_from_node_string
    init_string = init_resume_from_node_string
    next_string =  next_resume_from_node_string
    return (define_string, var_string, init_string, next_string)

def create_next_node_structure(nodes, children, node_to_local_root_map, sequence_to_relevant_descendants_map, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set):
    next_node_string = ("\t\tnext_node := [")
    descent_string = ""
    ascent_string = ""
    for node_id in range(0, len(nodes)):
        next_node_string += "ascent_from_" + str(node_id) + ", "

        if node_id not in children or len(children[node_id]) == 0:
            #if there are no childredn, descent always points to self. ascent always points to parent.
            descent_string += ("\t\tdescent_from_" + str(node_id) + " := " + str(node_id) + ";" + os.linesep)
            ascent_string += ("\t\tascent_from_" + str(node_id) + " := ascent_from_" + str(nodes[node_id][1]) + ";" + os.linesep)
            continue
        if node_id == 0:
            #special case for root, because it would be annoying to find a way to make ascent_from_-1 to actually work
            ascent_string += ("\t\tascent_from_" + str(node_id) + " := " + os.linesep
                              + "\t\t\tcase" + os.linesep
                              + "\t\t\t\t(statuses[" + str(node_id) +"] = invalid) : descent_from_" + str(node_id) + ";" + os.linesep
                              + "\t\t\t\tTRUE : -1;" + os.linesep
                              + "\t\t\tesac;" + os.linesep
            )
        else:
            ascent_string += ("\t\tascent_from_" + str(node_id) + " := " + os.linesep
                              + "\t\t\tcase" + os.linesep
                              + "\t\t\t\t(statuses[" + str(node_id) +"] = invalid) : descent_from_" + str(node_id) + ";" + os.linesep
                              # if the status is not determined, then descend.
                              + "\t\t\t\tTRUE : ascent_from_" + str(nodes[node_id][1]) + ";" + os.linesep
                              # if the status is determined, then ascend.
                              + "\t\t\tesac;" + os.linesep
            )
        if len(children[node_id]) == 1:
            #if there is only one child, then we always descend to the same place
            #NOTE: something like decorator would need a condition here to terminate
            descent_string += ("\t\tdescent_from_" + str(node_id) + " := descent_from_" + str(children[node_id][0]) + ";" + os.linesep)
            continue
            #descent_string += ("\t\t\t\t(active_node < " + str(node_id) + ") : next_node_" + str(children[node_id][0]) + ";" + os.linesep)#point to where the direct child is pointing
            #otherwise point to parent
        descent_string += ("\t\tdescent_from_" + str(node_id) + " := " + os.linesep
                          + "\t\t\tcase" + os.linesep
        )
        if node_id in parallel_synch_set:
            for child in children[node_id]:
                descent_string += ("\t\t\t\t(active_node <" + str(child) + ") & !(resume_from_node_" + str(child) + " = -2) : descent_from_" + str(child) + ";" + os.linesep)#if resume_from_node_ = -2, then we were instructed to skip this child. otherwise, if we're infront of it, point to w/e the child is pointing.
        elif node_id in parallel_unsynch_set:
            for child in children[node_id]:
                descent_string += ("\t\t\t\t(active_node <" + str(child) + ") : descent_from_" + str(child) + ";" + os.linesep)
        elif node_id in selector_set:
            #no need for early termination. it's handled by ascent
            for child in children[node_id]:
                descent_string += ("\t\t\t\t(active_node <" + str(child) + ") : descent_from_" + str(child) + ";" + os.linesep)#otherwise, go through each child in order
        elif node_id in sequence_set:
            #no need for early termination. it's handled by ascent
            #the previous version of this causes recursion errors. instead, do this
            #for descendant in sequence_to_relevant_descendants_map[node_id]:
                #descent_string +=("\t\t\t\t(resume_from_node_" + str(node_to_local_root_map[node_id]) + " = " + str(descendant) + ") : descent_from_" + str(descendant) + ";" + os.linesep)#if the relevant resume status is indicating a node that is our descendent, then jump to wherever it points to
            for child in children[node_id]:
                descent_string += "\t\t\t\t(active_node <" + str(child) + ") & (resume_relevant_child_" + str(child) + ") : descent_from_" + str(child) + ";" + os.linesep
                #ok, so if the resume_relevant_child_X is true, then we need to resume from X, so point to it.
            for child in children[node_id]:
                descent_string += ("\t\t\t\t(active_node <" + str(child) + ") : descent_from_" + str(child) + ";" + os.linesep)#otherwise, go through each child in order
        descent_string += ("\t\t\t\tTRUE : -2;" + os.linesep#error state, because descent should never trigger this
                           + "\t\t\tesac;" + os.linesep
        )
    define_string = (next_node_string[0:-2] + "];" + os.linesep
                        + descent_string
                        + ascent_string
    )
    var_string = ""
    init_string = ""
    next_string = ""
    
    return (define_string, var_string, init_string, next_string)

def create_relevant_child_and_status(nodes, children, node_to_descendants_map, node_to_local_root_map):
    item_string = ""
    for node_id in range(len(node_to_descendants_map)):
        if node_id not in children or len(children[node_id]) == 0:
            #item_string += "\t\trelevant_child_" + str(node_id) + " := -1;" + os.linesep
            item_string += "\t\trelevant_child_" + str(node_id) + " := (active_node = " + str(node_id) + ") ? -1 : -2 ;" + os.linesep
            
        else:
            item_string += ("\t\trelevant_child_" + str(node_id) + " := " + os.linesep
                            + "\t\t\tcase" + os.linesep)
            for child in children[node_id]:
                item_string += "\t\t\t\t !(relevant_child_" + str(child) + " = -2) : " + str(child) + ";" + os.linesep
            item_string += ("\t\t\t\tTRUE : -2;" + os.linesep
                            + "\t\t\tesac;" + os.linesep
            )
        local_root = node_to_local_root_map[node_id]
        if node_id not in children or len(children[node_id]) == 0:
            item_string += "\t\tresume_relevant_child_" + str(node_id) + " := (resume_from_node_" + str(local_root) + " = " + str(node_id) + ") ? TRUE : FALSE ;" + os.linesep
        else:
            item_string += ("\t\tresume_relevant_child_" + str(node_id) + " := " + os.linesep
                            + "\t\t\tcase" + os.linesep
                            + "\t\t\t\t(resume_from_node_" + str(local_root) + " = " + str(node_id) + ") : TRUE ;" + os.linesep#if it's poiting directly to us, true regardless.
            )
            for child in children[node_id]:
                item_string += "\t\t\t\t(resume_relevant_child_" + str(child) + ") : TRUE;" + os.linesep#if it's pointing to a child of ours, TRUE
            item_string += ("\t\t\t\tTRUE : FALSE;" + os.linesep#wasn't. therefore, false
                            + "\t\t\tesac;" + os.linesep
            )
        #if node_id in leaf_set:
            #leaf nodes do not reference the statuses
            #pass
        if node_id not in children or len(children[node_id]) == 0:
            pass#pass version means one less constant, but have to track this in the arguments area then.
            #item_string += "\t\tstatus_" + str(node_id) + " := invalid;" + os.linesep
            #just default to invalid if it doesn't have children
        else:
            item_string += ("\t\trelevant_status_" + str(node_id) + " := " + os.linesep
                            + "\t\t\tcase" + os.linesep
            )
            for child in children[node_id]:
                item_string += "\t\t\t\t(relevant_child_" + str(node_id) + " = " + str(child) + ") : " + nodes[child][2] + ".status;" + os.linesep
            item_string += ("\t\t\t\tTRUE : invalid;" + os.linesep
                            + "\t\t\tesac;" + os.linesep
            )
    define_string = item_string
    var_string = ""
    init_string = ""
    next_string =  ""
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
    
    next_available_id = walk_tree(root, -1, 0, children, nodes, additional_arguments, needed_nodes, node_names, variable_access, variable_check, variable_name_to_int, external_status_req, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set, args.force_parallel_unsynch)
    #print(nodes)
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
    
    # for split_point in range(len(nodes)):
    #     define_string += "\t\tstatuses_" + str(split_point) + " := ["
    #     for invalid in range(split_point + 1):
    #         if invalid == 0:
    #             define_string += "invalid"
    #         else:
    #             define_string += ", invalid"
    #     for node_id in range(split_point + 1, len(nodes)):
    #         define_string += ", " + nodes[node_id][2] + ".status"
    #     define_string += "];" + os.linesep

    #------------------------------------------------------------------------------------------------------------------------
    var_string = (""
                    + "\tVAR" + os.linesep 
                    + "\t\tactive_node : {-2, -1," + str(leaf_set)[1:]  + ";" + os.linesep#NOTE: this needs to be expanded to include some decorators, like one shot.
                    + "\t\trandom_status : {running, success, failure};" + os.linesep
    )       
    if variable_name_to_int:
        var_string += "\t\tvariable_names : define_variables;" + os.linesep
    var_string += "\t\tnode_names : define_nodes;" + os.linesep
    if blackboard_needed:
        var_string += "\t\tblackboard : blackboard_module(active_node, node_names, variable_names, random_status, statuses);" + os.linesep
    #------------------------------------------------------------------------------------------------------------------------
    init_string = ("\tINVAR" + os.linesep
                   + "\t\tactive_node = -1 -> random_status = running;" + os.linesep
                   + "\tASSIGN" + os.linesep
                   + "\t\tinit(active_node) := -1;" + os.linesep
    )
    next_string = ("\t\tnext(active_node) :=" + os.linesep
                    + "\t\t\tcase" + os.linesep
                    + "\t\t\t\t(active_node = -2) : -2;" + os.linesep#stay in error state
                    + "\t\t\t\t(active_node = -1) : next_node[0];" + os.linesep#go to where the root points
                    + "\t\t\t\tTRUE : next_node[active_node];" + os.linesep
                    + "\t\t\tesac;" + os.linesep
    )
    #------------------------------------------------------------------------------------------------------------------------
    
    (new_define, new_var, new_init, new_next) = create_resume_structure(nodes, local_root_to_relevant_list_map)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next
    (new_define, new_var, new_init, new_next) = create_next_node_structure(nodes, children, node_to_local_root_map, sequence_to_relevant_descendants_map, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next
    (new_define, new_var, new_init, new_next) = create_relevant_child_and_status(nodes, children, node_to_descendants_map, node_to_local_root_map)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next
    (new_define, new_var, new_init, new_next) = create_nodes(nodes, children, additional_arguments, parallel_synch_set, parallel_unsynch_set, sequence_set, selector_set, decorator_set, leaf_set)
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

    for needed in needed_nodes:
        nuxmv_string = nuxmv_string +  eval('node_creator.create_'+needed+'(next_available_id-1)')

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
                    module_string += ("MODULE " + variable + "_SET_module(active_node, nodes_with_access, variables, variable_exists, node_names, variable_names, statuses)" + os.linesep
                                      + "\tVAR" + os.linesep
                                      + "\t\t" + variable + " : " + str(args.min_val) + ".." + str(args.max_val) + ";" + os.linesep
                                      + "\t\t" + variable + "_exists" + " : boolean;" + os.linesep
                                      + "\tASSIGN" + os.linesep
                                      + "\t\tinit(" + variable + ") := " + str(args.min_val) + ";" + os.linesep
                                      + "\t\tinit(" + variable + "_exists) := FALSE;" + os.linesep
                                      + "\t\tnext(" + variable + ") := " + os.linesep
                                      + "\t\t\tcase" + os.linesep
                                      + "\t\t\t\t(active_node in nodes_with_access) : " + set_string + ";" + os.linesep
                                      + "\t\t\t\tTRUE : " + variable + ";" + os.linesep
                                      + "\t\t\tesac;" + os.linesep
                                      + "\t\tnext(" + variable + "_exists) := " + os.linesep
                                      + "\t\t\tcase" + os.linesep
                                      + "\t\t\t\t(active_node in nodes_with_access) : TRUE;" + os.linesep
                                      + "\t\t\t\tTRUE : " + variable + "_exists;" + os.linesep
                                      + "\t\t\tesac;" + os.linesep
                    )
            for node in external_status_req:
                module_string += ("MODULE " + node + "_SET_status_module(active_node, id, random_status, variables, variable_exists, node_names, variable_names)" + os.linesep
                                  + "\tDEFINE" + os.linesep
                                  + "\t\tstatus := " + os.linesep
                                  + "\t\t\tcase" + os.linesep
                                  + "\t\t\t\t(active_node = id) : {success, failure, running};" + os.linesep
                                  + "\t\t\t\tTRUE : invalid;" + os.linesep
                                  + "\t\t\tesac;" + os.linesep
                )
            for variable in variable_check:
                for node_id in variable_check[variable]:
                    module_string += ("MODULE " + nodes[node_id][2] + "_CHECK_" + variable + "_module(active_node, id, variables, variable_exists, node_names, variable_names)" + os.linesep
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
                    module_string += ("MODULE " + variable + "_SET_module(active_node, nodes_with_access, variables, variable_exists, node_names, variable_names, statuses)" + os.linesep
                                      + "\tDEFINE" + os.linesep
                                      + "\t\t" + variable + " := " + str(args.min_val) + ";" + os.linesep
                                      + "\t\t" + variable + "_exists" + " := TRUE;" + os.linesep
                    )
            for node in external_status_req:
                module_string += ("MODULE " + node + "_SET_status_module(active_node, id, random_status, variables, variable_exists, node_names, variable_names)" + os.linesep
                                  + "\tDEFINE" + os.linesep
                                  + "\t\tstatus := " + os.linesep
                                  + "\t\t\tcase" + os.linesep
                                  + "\t\t\t\t(active_node = id) : {success, failure, running};" + os.linesep
                                  + "\t\t\t\tTRUE : invalid;" + os.linesep
                                  + "\t\t\tesac;" + os.linesep
                )
            for variable in variable_check:
                for node_id in variable_check[variable]:
                    module_string += ("MODULE " + nodes[node_id][2] + "_CHECK_" + variable + "_module(active_node, id, variables, variable_exists, node_names, variable_names)" + os.linesep
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
