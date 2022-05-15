#python3 btree_serene.py create_root_FILE create_root_METHOD --root_args create_root_ARGS  --min_val min_val_INT --max_val max_val_INT --parallel_unsynch --modules additional_modules_FILE --specs specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --gen_module_file gen_module_file_FILE --overwrite

#TODO: neither parallel works correctly right now. implement both. DONE.

#resume from top most parallel node.

#if node is synch
#for each child, if variable indicates "finished", skip child. otherwise, run child.
#but! how does that child run!
#it cannot use normal logic. it must also use the 'finished' check. that....or i implement a recursive subtree subsytem where it 'resumes' using the same method as the overall tree. that, however, seems very expensive in terms of state space and other things.
#actually, let us consider this sub-tree proposal. instead of storing a boolean for each child, we store an integer for each sub-tree, with the parallel node acting as -1, and the child acting as the root 0.
#if the child has no children, this is equivalent to storing a boolean.
#if the child has children, each child increases the size of the integer by 1, rather than adding a full new boolean. this is, without a doubt, more space efficient.

#ok. so now....how do i implement this.

#for each parallel node p, i need to store n_p integers where n_p = num_children(p), and each integer can be as large as

#ugh. this works better for unsyched than synched.


#for synched -> can i find the first non-negative entry of an array using a define statement in nuxmv? if so, we're golden.


#nope.


#ok new plan. it's ugly, but w.e. for each parallel node store an array such that, for each child, store a value that tracks that subtree (treating parallel nodes as leaf nodes) and tells the parallel node where to start for that child.

#in the MAIN module, we will change active_node based on something like this
# (active_node in parallel) : parallel_shenanigan[active_node];

#where parallel_shenanigan is defined as [-2, -2, ...x,,,], where each x is a parallel nodes value, and -2 is everything else.

#the x is determined by a define statement that parses the array of it's parallel node. something like

#DEFINE
#\tx :=
#\t\tcase
#\t\t\t(array[min(num_children-1, 1)] >= 0) : array[min(num_children-1, 1);
#\t\t\t(array[min(num_children-1, 2)] >= 0) : array[min(num_children-1, 2);
#\t\t\t(array[min(num_children-1, 3)] >= 0) : array[min(num_children-1, 3);
#...

#\t\t\t(array[min(num_children-1, biggest_number_of_children)] >= 0) : array[min(num_children-1, biggest_number_of_children);
#TRUE : parent;
#esac;

#and then we literally just use this, and ditch any other attempts at actually having a transition for parallel nodes. this is so disgusting, but w.e
#it should work.

#oh yeah. we track the value for each child using something like this

#MODULE parallel_child_tracker(previous_node, previous_status set_of_descendants)
#\tVAR
#\t\t x : set_of_descendants U self U -1;
#\tASSIGN
#\t\tinit(x) := self;
#\t\tnext(x) :=
#\t\t\tcase
#\t\t\t\t(x = self) & (previous_node in set_of_descendants) & (previous_status = running) : previous_node;
#\t\t\t\t(previous_node = self) & (previous_status = success | previous_status = failure) : -1;#change from -1 to self if unsych
#\t\t\t\t(previous_node = 0) & (previous_status = success | previous_status = failure) : self;#reset if we didn't end up on running
#\t\t\t\tTRUE : x;
#\t\t\tesac;


import argparse
import py_trees
import sys
import time
import os
import re
import inspect

import py_trees.console as console

import node_creator

#tracking variables
node_count=0#the value represents the next ID to be assigned.
children={-1:[]}#stores a list of children ID. is indexed via node id
nodes={}#stores a pair, (type, parent_id, node_name), where type informs us of the node type, and parent of the parent id, and node_name. it's indexed via node id
additional_arguments={}#stores additional arguments. it's index via node id
needed_nodes={}#a 'list' of nodes needed
variable_to_int={}#a mapping of variable names to their integer locations
variable_access={}#for each variable, a list of nodes with access to that variable.
variable_check={}#for each variable, a list of nodes that check that variable. indexed by variable name
blackboard_needed=False#stores if we need the blackboard
node_names={}#a list of node names. each name is also associated with an integer that indicates how many times it has been seen, allowing us to automatically create a new name.
last_child={}#a list of the last child index for each node
parallel_resume={}#each parallel node_id indexes to a dict. this dict is indexed by the direct children of the parallel node, and stores a list of all their descendents (though when it reaches a new parallel node that counts as a leaf)
parallel_synch_list = {}#list of parallel_synch
parallel_unsynch_list = {}
external_status_req = []#list of nodes that require external status. each entry is the node name.
#----------------------------------------------------------------------------------------------------------------
#regex stuff
blackboard_name_pattern = re.compile(r"#*(?P<blackboard_name>[^\s=]+)\s*=\s*py_trees\.blackboard\.Blackboard\(\)")
#----------------------------------------------------------------------------------------------------------------

def walk_tree(t, parent_id, assigned_id, sub_parallel = -1, sub_child = -1, parallel_unsynch = False):
    global node_count, children, nodes, additional_arguments, needed_nodes, variable_to_int, variable_access, blackboard_needed, last_child, parallel_resume, parallel_synch_list, parallel_unsych_list, variable_check, external_status_req;
    this_id=assigned_id
    #print(parallel_unsynch)
    try:
        children[parent_id].append(assigned_id)#if this fails, it means the parent is a decorator, which means there is only one child and no reason to track multiple
        #actually, this should never fail at this point.
    except KeyError:
        pass

    node_name=t.name
    if node_name in node_names:
        node_names[node_name]=node_names[node_name]+1
        node_name=node_name+str(node_names[node_name])
    else:
        node_names[node_name]=0

    last_child[this_id]=-1

    if sub_parallel >= 0:
        if sub_parallel in parallel_resume:
            if sub_child in parallel_resume[sub_parallel]:
                parallel_resume[sub_parallel][sub_child].append(this_id)
            else:
                parallel_resume[sub_parallel][sub_child] = [this_id]
        else:
            parallel_resume[sub_parallel]={ sub_child : [this_id] }


    try:
        #this is to overwrite the later checks in order to directly create a specific type of node.
        if t.serene_info_variable == "BlueROV_Blackboard_Node" or t.serene_info_variable == "BlueROV_Task_Node":
            external_status_req.append(node_name)
            nodes[this_id]=('node_set_blackboard_variables', parent_id, node_name)
            needed_nodes['node_set_blackboard_variables']=True
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
                variable_name_pattern=re.compile(r"#*\s*" + blackboard_name + "\.(?P<variable_name>[^\s=]+)\s*([+\-*/%&|^]?=|//=|\*\*=|>>=|<<=)\s*")
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
                        if variable_name in variable_to_int:
                            var_num=variable_to_int[variable_name]
                        else:
                            var_num=len(variable_to_int)
                            variable_to_int[variable_name]=var_num
                        if var_num in variable_access:
                            variable_access[var_num].append(this_id)
                        else:
                            variable_access[var_num]=[this_id]
                    else:
                        done=True
            else:
                variable_name=t.variable_name
                variable_name=variable_name.replace('.', '_dot_')
                if variable_name in variable_to_int:
                    var_num=variable_to_int[variable_name]
                else:
                    var_num=len(variable_to_int)
                    variable_to_int[variable_name]=var_num
                if var_num in variable_access:
                    variable_access[var_num].append(this_id)
                else:
                    variable_access[var_num]=[this_id]
            decl_string = ("\t\t" + node_name + "_SET_status : " + node_name + "_SET_status_module(active_node, " + str(this_id) + ", blackboard.variables, blackboard.variable_exists, node_names, variable_names);" + os.linesep)
            additional_arguments[this_id]=[{'arg': node_name + "_SET_status", 'decl' : decl_string},]
            return
        elif t.serene_info_variable == "BlueROV_Task_Node":
            #currently this is beign used in the same way as the one above.
            pass
    except AttributeError as e:
        #print(e)
        #print(node_name+ " ERROR?")
        pass
        
    if isinstance(t, py_trees.composites.Sequence):
        #children[this_id]=[]
        nodes[this_id]=('node_sequence', parent_id, node_name)
        needed_nodes['node_sequence']=True
    elif isinstance(t, py_trees.composites.Selector):
        #children[this_id]=[]
        nodes[this_id]=('node_selector', parent_id, node_name)
        needed_nodes['node_selector']=True
    elif isinstance(t, py_trees.composites.Parallel):
        sub_parallel=this_id
        #children[this_id]=[]
        if t.policy.synchronise and (not parallel_unsynch):
            parallel_synch_list[this_id]=True
            #nodes[this_id]=('node_parallel_synchronised', parent_id, node_name)
            nodes[this_id]=('node_parallel', parent_id, node_name)
            #needed_nodes['node_parallel_synchronised']=True
            needed_nodes['node_parallel']=True
            if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                additional_arguments[this_id]=[{'arg' : "TRUE, TRUE, parallel_resume_" + str(this_id)}, ]
            elif isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                additional_arguments[this_id]=[{'arg' : "TRUE, FALSE, parallel_resume_" + str(this_id)}, ]
            else:
                print('ERROR: the following parallel policy is not supported: ' + str(t.policy))
                sys.exit('Unsupported Parallel Policy')
        else:
            parallel_unsynch_list[this_id]=True
            #nodes[this_id]=('node_parallel_unsynchronised', parent_id, node_name)
            nodes[this_id]=('node_parallel', parent_id, node_name)
            #needed_nodes['node_parallel_unsynchronised']=True
            needed_nodes['node_parallel']=True
            if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                additional_arguments[this_id]=[{'arg' : "FALSE, TRUE, parallel_resume_" + str(this_id)}, ]
            elif isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                additional_arguments[this_id]=[{'arg' : "FALSE, FALSE, parallel_resume_" + str(this_id)}, ]
            else:
                print('ERROR: the following parallel policy is not supported: ' + str(t.policy))
                sys.exit('Unsupported Parallel Policy')
    
            
    elif isinstance(t, py_trees.decorators.Condition):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_condition', parent_id, node_name)
        needed_nodes['decorator_condition']=True
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}, {'arg' : t.succeed_status.name.lower()}]
    elif isinstance(t, py_trees.decorators.Inverter):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_inverter', parent_id, node_name)
        needed_nodes['decorator_inverter']=True
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}]
    elif isinstance(t, py_trees.decorators.OneShot):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_one_shot', parent_id, node_name)
        needed_nodes['decorator_one_shot']=True
        if t.policy.name == "ON_SUCCESSFUL_COMPLETION":
            policy='TRUE'
        else:
            policy='FALSE'
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}, {'arg' : policy}]
    #there's a solid argument for combining all the X is Y types into one module, and just having 2 additional arguments for that module.
    elif isinstance(t, py_trees.decorators.FailureIsRunning):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_failure_is_running', parent_id, node_name)
        needed_nodes['decorator_failure_is_running']=True
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}]
    elif isinstance(t, py_trees.decorators.FailureIsSuccess):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_failure_is_success', parent_id, node_name)
        needed_nodes['decorator_failure_is_success']=True
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}]
    elif isinstance(t, py_trees.decorators.RunningIsFailure):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_running_is_failure', parent_id, node_name)
        needed_nodes['decorator_running_is_failure']=True
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}]
    elif isinstance(t, py_trees.decorators.RunningIsSuccess):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_running_is_success', parent_id, node_name)
        needed_nodes['decorator_running_is_success']=True
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}]
    elif isinstance(t, py_trees.decorators.SuccessIsFailure):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_success_is_failure', parent_id, node_name)
        needed_nodes['decorator_success_is_failure']=True
        #additional_arguments[this_id]=[{'arg' : str(node_count+1)}]
    elif isinstance(t, py_trees.decorators.SuccessIsRunning):
        #does have a child, but only 1, and we know that it's this_id+1, so we'll just use that as a constant.
        nodes[this_id]=('decorator_success_is_running', parent_id, node_name)
        needed_nodes['decorator_success_is_running']=True
        additional_arguments[this_id]=[{'arg' : str(node_count+1)}]
    elif isinstance(t, py_trees.behaviours.CheckBlackboardVariableExists):
        nodes[this_id]=('node_check_blackboard_variable_exists', parent_id, node_name)
        needed_nodes['node_check_blackboard_variable_exists']=True
        blackboard_needed=True
        variable_name=t.variable_name
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_to_int:
            var_num=variable_to_int[variable_name]
        else:
            var_num=len(variable_to_int)
            variable_to_int[variable_name]=var_num
        additional_arguments[this_id]=[{'arg' : 'blackboard'}, {'arg' : str(var_num)}]
        return
    elif isinstance(t, py_trees.behaviours.CheckBlackboardVariableValue):
        #(statuses, active_node, id, parent, blackboard, variable, check)" + os.linesep
        nodes[this_id]=('node_check_blackboard_variable_value', parent_id, node_name)
        needed_nodes['node_check_blackboard_variable_value']=True
        blackboard_needed=True
        variable_name=t.check.variable
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_to_int:
            var_num=variable_to_int[variable_name]
        else:
            var_num=len(variable_to_int)
            variable_to_int[variable_name]=var_num
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
        return
    elif isinstance(t, py_trees.behaviours.CheckBlackboardVariableValues):
        return #not doing the below right now. it's way too much of a pain. don't know how to deal with operator
    elif isinstance(t, py_trees.behaviours.SetBlackboardVariable):
        external_status_req.append(node_name)
        nodes[this_id]=('node_set_blackboard_variables', parent_id, node_name)
        needed_nodes['node_set_blackboard_variables']=True
        blackboard_needed=True
        variable_name=t.variable_name
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_to_int:
            var_num=variable_to_int[variable_name]
        else:
            var_num=len(variable_to_int)
            variable_to_int[variable_name]=var_num
        if var_num in variable_access:
            variable_access[var_num].append(this_id)
        else:
            variable_access[var_num]=[this_id]
        decl_string = ("\t\t" + node_name + "_SET_status : " + node_name + "_SET_status_module(active_node, " + str(this_id) + ", blackboard.variables, blackboard.variable_exists, node_names, variable_names);" + os.linesep)
        additional_arguments[this_id]=[{'arg': node_name + "_SET_status", 'decl' : decl_string},]
        return
    
    elif isinstance(t, py_trees.behaviours.UnsetBlackboardVariable):
        #statuses, id, parent, variable, nodes_with_access)" + os.linesep
        nodes[this_id]=('node_unset_blackboard_variable', parent_id, node_name)
        needed_nodes['node_unset_blackboard_variable']=True
        blackboard_needed=True
        variable_name=t.key
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_to_int:
            var_num=variable_to_int[variable_name]
        else:
            var_num=len(variable_to_int)
            variable_to_int[variable_name]=var_num
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
        return
    elif isinstance(t, py_trees.behaviours.WaitForBlackboardVariable):
        nodes[this_id]=('node_wait_for_blackboard_variable', parent_id, node_name)
        needed_nodes['node_wait_for_blackboard_variable_exists']=True
        blackboard_needed=True
        variable_name=t.variable_name
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_to_int:
            var_num=variable_to_int[variable_name]
        else:
            var_num=len(variable_to_int)
            variable_to_int[variable_name]=var_num
        additional_arguments[this_id]=[{'arg' : 'blackboard'}, {'arg' : str(var_num)}]
        return
    elif isinstance(t, py_trees.behaviours.WaitForBlackboardVariableValue):
        nodes[this_id]=('node_wait_for_blackboard_variable_value', parent_id, node_name)
        needed_nodes['node_wait_for_blackboard_variable_value']=True
        blackboard_needed=True
        variable_name=t.check.variable
        variable_name=variable_name.replace('.', '_dot_')
        if variable_name in variable_to_int:
            var_num=variable_to_int[variable_name]
        else:
            var_num=len(variable_to_int)
            variable_to_int[variable_name]=var_num
            
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
        return
    elif isinstance(t, py_trees.behaviours.Count):
        nodes[this_id]=('node_count', parent_id, node_name)
        needed_nodes['node_count']=True
        additional_arguments[this_id]=[{'arg' : str(t.fail_until)}, {'arg' : str(t.running_until)}, {'arg' : str(t.success_until)}, {'arg' : str(t.reset).upper()}]
        return
    elif isinstance(t, py_trees.behaviours.Failure):
        nodes[this_id]=('node_failure', parent_id, node_name)
        needed_nodes['node_failure']=True
        return
    elif isinstance(t, py_trees.behaviours.Periodic):
        nodes[this_id]=('node_periodic', parent_id, node_name)
        needed_nodes['node_periodic']=True
        additional_arguments[this_id]=({'arg':str(t.period)}, )
        return
    elif isinstance(t, py_trees.behaviours.Running):
        nodes[this_id]=('node_running', parent_id, node_name)
        needed_nodes['node_running']=True
        return
    elif isinstance(t, py_trees.behaviours.StatusSequence):
        nodes[this_id]=('node_status_sequence', parent_id, node_name)
        needed_nodes['node_status_sequence']=True
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
        return
    elif isinstance(t, py_trees.behaviours.Success):
        nodes[this_id]=('node_success', parent_id, node_name)
        needed_nodes['node_success']=True
        return
    elif isinstance(t, py_trees.behaviours.SuccessEveryN):
        nodes[this_id]=('node_success_every_n', parent_id, node_name)
        needed_nodes['node_success_every_n']=True
        additional_arguments[this_id]=[{'arg' : str(t.every_n)}, ]
        return
    elif isinstance(t, py_trees.behaviours.TickCounter):
        nodes[this_id]=('node_tick_counter', parent_id, node_name)
        needed_nodes['node_tick_counter']=True
        additional_arguments[this_id]=[{'arg' : str(t.duration)}, {'arg' : t.completion_status.name.lower()}]
        return
    elif isinstance(t, py_trees.timers.Timer):
        nodes[this_id]=('node_timer', parent_id, node_name)
        needed_nodes['node_timer']=True
        return
    else:#currently defaulting to default. will rework this later probably
        nodes[this_id]=('node_default', parent_id, node_name)
        needed_nodes['node_default']=True
        return


    children[assigned_id] = []#if we've reached this point, then this node has children, and we are going to set up an empty list for it.
    node_count_now=node_count
    node_count=node_count+len(t.children)
    #----------------------------------------------------------------------------------------------------------------------
    for child in t.children:
        node_count_now = node_count_now + 1
        if this_id == sub_parallel:#this means we are currently in a parallel node, which means we need to go through each child and create a resume tree
            walk_tree(child, this_id, node_count_now, sub_parallel, node_count_now, parallel_unsynch)#which is why we're setting sub_child to be node_count_now
        elif nodes[this_id] == 'node_selector':
            walk_tree(child, this_id, node_count_now, -1, -1, parallel_unsynch)#can't resume from within a selector node. always resume from the selector node itself.
        else:
            walk_tree(child, this_id, node_count_now, sub_parallel, sub_child, parallel_unsynch)
    last_child[this_id]=node_count_now

    #-----------------------------------------------------------------------------------------------------------------------



##############################################################################
# Main
##############################################################################

def main():
    """
    Entry point for the demo script.
    """
    global node_count, children, nodes, additional_arguments, needed_nodes, variable_to_int, variable_access, blackboard_needed, last_child, parallel_resume, parallel_synch_list, parallel_unsych_list, variable_check, external_status_req;

    arg_parser=argparse.ArgumentParser()
    #python3 btree_serene.py create_root_FILE create_root_METHOD --root_args create_root_ARGS  --min_val min_val_INT --max_val max_val_INT --parallel_unsynch --modules additional_modules_FILE --specs specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --gen_module_file gen_module_file_FILE --overwrite
    arg_parser.add_argument('root_file')
    arg_parser.add_argument('root_method')
    arg_parser.add_argument('--root_args', default='', nargs='*')
    arg_parser.add_argument('--string_args', default='', nargs='*')
    arg_parser.add_argument('--min_val', default=0, type=int)
    arg_parser.add_argument('--max_val', default=1, type=int)
    arg_parser.add_argument('--parallel_unsynch', action='store_true')
    arg_parser.add_argument('--modules')
    arg_parser.add_argument('--specs')
    arg_parser.add_argument('--gen_modules', default=0, type=int)
    arg_parser.add_argument('--output_file', default=None)
    arg_parser.add_argument('--gen_module_file', default=None)
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

    #print(parallel_unsynch)
    walk_tree(root, -1, 0, -1, -1, args.parallel_unsynch)
    node_count=node_count+1#this is included because it used to happen as part of walk_tree, and there's a lot of logic to update if this value is different now.
    
    
    #this segment is to detect and create sub-variables
    #i.e., if a variable in the original was just "meh = Object"
    #but other places use meh.val1, meh.val2, etc, then the original "meh" needs to handle those.
    #note: currently not handling recursive things, like meh.val1.val3
    #should maybe look into this a bit more. 
    for variable in variable_to_int:
        blackboard_name_pattern = re.compile(r"#(?P<blackboard_name>[^\s=]+)\s*=\s*py_trees\.blackboard\.Blackboard\(\)")
        variable_regex=re.compile(r""+variable+"_dot_")
        for child_variable in variable_to_int:
            if variable_regex.match(child_variable):
                for access_node in variable_access[variable_to_int[variable]]:
                    if variable_to_int[child_variable] in variable_access:
                        pass
                    else:
                        variable_access[variable_to_int[child_variable]]=[]
                    if access_node in variable_access[variable_to_int[child_variable]]:
                        pass
                    else:
                        variable_access[variable_to_int[child_variable]].append(access_node)
                        

    int_to_variable = {}
    for variable in variable_to_int:
        int_to_variable[variable_to_int[variable]] = variable
    #print(node_count)
    #print(children)
    #print(nodes)
    #print(needed_nodes)
    pre_nuxmv_string = ("MODULE main" + os.linesep
                        + "\tDEFINE" + os.linesep
                        #+ "\t\tactive_node := next(previous_node);" + os.linesep
                        + "\t\tmax_active_node := " + str(node_count-1) + ";" + os.linesep
                        + "\t\tstatuses := [")
    for node_id in range(0, node_count):
        if node_id==0:
            pre_nuxmv_string += nodes[node_id][2] + ".status"
        else:
            pre_nuxmv_string += ", " + nodes[node_id][2] + ".status"
    pre_nuxmv_string += ("];" + os.linesep
                         + "\t\tparents := [")
    for node_id in range(0, node_count):
        if node_id==0:
            pre_nuxmv_string += str(nodes[node_id][1])
        else:
            pre_nuxmv_string += ", " + str(nodes[node_id][1])
    pre_nuxmv_string += ("];" + os.linesep)
                

    
    leafs = ("\t\tleafs := {-3")
    selectors = ("\t\tselectors := {-3")
    sequences = ("\t\tsequences := {-3")
    parallels_synchronised_all = ("\t\tparallels_synchronised_all := {-3")
    parallels_unsynchronised_all = ("\t\tparallels_unsynchronised_all := {-3")
    parallels_synchronised_one = ("\t\tparallels_synchronised_one := {-3")
    parallels_unsynchronised_one = ("\t\tparallels_unsynchronised_one := {-3")
    parallels = ("\t\tparallels := {-3")
    decorators = ("\t\tdecorators := {-3")
    first_child_str = ("\t\tfirst_child := [")
    last_child_str = ("\t\tlast_child := [")
    parallel_synch_exists = False
    for node_id in range(0, node_count):
        last_child_str += str(last_child[node_id]) + ', ' 
        if 'sequence' in nodes[node_id][0]:
            sequences += ", " + str(node_id)
        elif 'selector' in nodes[node_id][0]:
            selectors += ", " + str(node_id)
        elif 'parallel' in nodes[node_id][0]:
            parallels += ", " + str(node_id)
            if node_id in parallel_unsynch_list:
                if 'one' in nodes[node_id][0]:
                    parallels_unsynchronised_one += ", " + str(node_id)
                else:
                    parallels_unsynchronised_all += ", " + str(node_id)
            else:
                parallel_synch_exists = True
                if 'one' in nodes[node_id][0]:
                    parallels_synchronised_one += ", " + str(node_id)
                else:
                    parallels_synchronised_all += ", " + str(node_id)
        elif 'decorator' in nodes[node_id][0]:
            decorators += ", " + str(node_id)
        else:
            leafs += ", " + str(node_id)
            first_child_str += "-2, "
            continue
        first_child_str += str(children[node_id][0]) + ", "
    pre_nuxmv_string += (leafs + "};" + os.linesep
                         + selectors + "};" + os.linesep
                         + sequences + "};" + os.linesep
                         + parallels_synchronised_all + "};" + os.linesep
                         + parallels_unsynchronised_all + "};" + os.linesep
                         + parallels_synchronised_one + "};" + os.linesep
                         + parallels_unsynchronised_one + "};" + os.linesep
                         + parallels + "};" + os.linesep
                         + decorators + "};" + os.linesep
                         + first_child_str[0:-2] + "];" + os.linesep
                         + last_child_str[0:-2] + "];" + os.linesep)

    #------------------------------------------------------------------------------------------------------------------------
    nuxmv_string = (""
                    + "\tVAR" + os.linesep 
                    + "\t\tactive_node : -2..max_active_node;" + os.linesep
                    + "\t\tprevious_node : -1..max_active_node;" + os.linesep
                    + "\t\tresume_node : -1..max_active_node;" + os.linesep
                    + "\t\tprevious_status : {running, success, failure, invalid};" + os.linesep)

    #------------------------------------------------------------------------------------------------------------------------
    if len(parallel_resume) > 0:
        pre_nuxmv_string += ("\t\tparallel_resume := [")
        first = True
        for node_id in range(0, node_count):
            if first:
                first = False
            else:
                pre_nuxmv_string += ", "
            if node_id in parallel_resume: #this means it's a parallel_node
                pre_nuxmv_string += ("parallel_resume_" + str(node_id))
            else:
                pre_nuxmv_string += "-2"
        pre_nuxmv_string += "];" + os.linesep
        parallel_init = ""
        parallel_next = ""
        pre_post_nuxmv_string = ""
        for parallel_node in parallel_resume:
            pre_nuxmv_string += ("\t\tparallel_resume_" + str(parallel_node) + " := " + os.linesep
                                      + "\t\t\tcase" + os.linesep)
            #for direct_child in parallel_resume[parallel_node]:#order guaranteed in python3.7, but just in case swapping to the list set of children, which is guaranteed to iterate correctly
            for direct_child in children[parallel_node]:
                if parallel_node in parallel_unsynch_list:
                    valid_set = "{"#don't need an extra state if unsynched. every descendant of an unsyched is always used for resume
                else:
                    valid_set = "{-2, "#need the extra state if synched. marks a skippable node
                valid_set += str(parallel_resume[parallel_node][direct_child])[1 : -1] + "}"
                if ',' in valid_set:
                    nuxmv_string += ("\t\tparallel_resume_" + str(parallel_node) + "_" + str(direct_child) + " : " + valid_set + ";" + os.linesep)
                    parallel_init += ("\t\tinit(parallel_resume_" + str(parallel_node) + "_" + str(direct_child) + ") := " + str(direct_child) + ";" + os.linesep)
                    parallel_next += ("\t\tnext(parallel_resume_" + str(parallel_node) + "_" + str(direct_child) + ") :=" + os.linesep
                                      + "\t\t\tcase" + os.linesep
                                      + "\t\t\t\t(parallel_resume_" + str(parallel_node) + "_" + str(direct_child) + " = " + str(direct_child) + ") & (previous_node in " + valid_set + ") & (previous_status = running) : previous_node;" + os.linesep #if we are currently pointing to the direct descendant and we encounter something that returned running, point to that instead.
                                      + "\t\t\t\t(previous_node = " + str(direct_child) + ") & (previous_status = success | previous_status = failure) : ")
                    if parallel_node in parallel_unsynch_list:
                        parallel_next += (str(direct_child) + ";" + os.linesep) #if it's unsynched, success means we point at direct descendant
                    else:
                        parallel_next += "-2;" + os.linesep #if it's synched, success means we mark it as finished
                    parallel_next += ("\t\t\t\t(previous_node = 0) & (previous_status = success | previous_status = failure) : " + str(direct_child) + ";" + os.linesep#reset if we didn't end up on running
                                      + "\t\t\t\tTRUE : parallel_resume_" + str(parallel_node) + "_" + str(direct_child) + ";" + os.linesep
                                      + "\t\t\tesac;" + os.linesep + os.linesep)
                else:#we're storing it as a constant
                    pre_post_nuxmv_string += ("\t\tparallel_resume_" + str(parallel_node) + "_" + str(direct_child) + " := " + valid_set[ 1 : -1] + ";" + os.linesep)
                pre_nuxmv_string += "\t\t\t\t(previous_node < " + str(direct_child) + ") & !(parallel_resume_" + str(parallel_node) + "_" + str(direct_child) + " = -2) : parallel_resume_" + str(parallel_node) + "_" + str(direct_child) + ";" + os.linesep #if the previous_node is less than this direct child, check if we're supposed to use it for a resume.
            pre_nuxmv_string += ("\t\t\t\tTRUE : parents[" + str(parallel_node) + "];" + os.linesep
                                 + "\t\t\tesac;" + os.linesep)
        pre_nuxmv_string += pre_post_nuxmv_string
                
    
    for node_id in range(0, node_count):
        #print(node_id)
        nuxmv_string = (nuxmv_string
                        + "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + "(active_node, " + str(node_id))
                        #              node_name         :     node_type        active_node,      node_number
        if node_id in children : #has children in module argument
            if "decorator" not in nodes[node_id][0]:#ensure it's not a decorator
                nuxmv_string = (nuxmv_string + ", previous_status, " + str(last_child[node_id]) + ", previous_node")
            else:
                nuxmv_string = (nuxmv_string + ", previous_status")
                
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'arg' in additional_arguments[node_id][i]:
                    nuxmv_string = (nuxmv_string + ", " + additional_arguments[node_id][i]['arg'])
                if 'nodes_with_access_to' in additional_arguments[node_id][i]:
                    set_string='{'
                    for node_with_access in variable_access[additional_arguments[node_id][i]['nodes_with_access_to']]:
                        set_string = set_string + str(node_with_access) + ', '
                    set_string=set_string[0:-2]+'}'#replace the last comma with a }
                    nuxmv_string = (nuxmv_string + ", " + set_string)
                if 'range_placeholder' in additional_arguments[node_id][i]:
                    nuxmv_string = (nuxmv_string + ", " + str(len(children[node_id])-1))
                    
            nuxmv_string = nuxmv_string + ");" + os.linesep
            for i in range(0, len(additional_arguments[node_id])):
                if 'decl' in additional_arguments[node_id][i]:
                    nuxmv_string = nuxmv_string + additional_arguments[node_id][i]['decl']       
        else:#does not have  additional arguments
            nuxmv_string = (nuxmv_string + ");" + os.linesep)
        #nuxmv_string = nuxmv_string + children_string

    nuxmv_string = pre_nuxmv_string + nuxmv_string
    if variable_to_int:
        nuxmv_string = (nuxmv_string
                        + "\t\tvariable_names : define_variables;" + os.linesep)
    
    nuxmv_string = (nuxmv_string
                    + "\t\tnode_names : define_nodes;" + os.linesep)
    if blackboard_needed:
        nuxmv_string = (nuxmv_string
                        + "\t\tblackboard : blackboard_module(active_node, node_names, variable_names, previous_status);" + os.linesep)

    for node_id in range(0, node_count):
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'invar' in additional_arguments[node_id][i]:
                    nuxmv_string = (nuxmv_string + additional_arguments[node_id][i]['invar'])

    #------------------------------------------------------------------------------------------------------------------------
    nuxmv_string = (nuxmv_string
                    + "\tASSIGN" + os.linesep
                    + "\t\tinit(active_node) := -1;" + os.linesep
                    + "\t\tinit(previous_node) := -1;" + os.linesep
                    + "\t\tinit(resume_node) := -1;" + os.linesep
                    + "\t\tinit(previous_status) := invalid;" + os.linesep)
    if len(parallel_resume) > 0:
        nuxmv_string += parallel_init
    for node_id in range(0, node_count):
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'init' in additional_arguments[node_id][i]:
                    nuxmv_string = nuxmv_string + additional_arguments[node_id][i]['init']
    for node_id in range(0, node_count):
        if node_id in additional_arguments:
            for i in range(0, len(additional_arguments[node_id])):
                if 'next' in additional_arguments[node_id][i]:
                    nuxmv_string = nuxmv_string + additional_arguments[node_id][i]['next']

    nuxmv_string = (nuxmv_string
                    + "\t\tnext(previous_node) :=" + os.linesep
                    + "\t\t\tcase" + os.linesep
                    + "\t\t\t\t(active_node < 0) : -1;" + os.linesep
                    + "\t\t\t\tTRUE : active_node;" + os.linesep
                    + "\t\t\tesac;" + os.linesep)

    nuxmv_string = (nuxmv_string
                    + "\t\tnext(resume_node) :=" + os.linesep
                    + "\t\t\tcase" + os.linesep
                    + "\t\t\t\t(previous_node < 0) : resume_node;" + os.linesep #don't change if the previous node wasn't a real place
                    #at this point, previous_node >= 0
                    + "\t\t\t\t!(previous_status = running) : -1;" + os.linesep #if we encounter a node that isn't running, then we clearly don't need to resume.
                    #at this point, previous_node >= 0, and previous_status = running
                    + "\t\t\t\t(resume_node = -1) : previous_node;" + os.linesep#we encountered running, and weren't planning on resuming. plan to resume from running
                    #at this point, previous_node >= 0, previous_status = running, and we were planning on resuming
                    + "\t\t\t\t(previous_node in parallels) | (previous_node in selectors) : previous_node;" + os.linesep #we were planning on resuming, but we should resume from here instead.
                    + "\t\t\t\tTRUE : resume_node;" + os.linesep #we encountered nodes that were running, but none of them were parallel, so we don't change our plan.
                    + "\t\t\tesac;" + os.linesep)

    nuxmv_string = (nuxmv_string
                    + "\t\tnext(previous_status) :=" + os.linesep
                    + "\t\t\tcase" + os.linesep
                    + "\t\t\t\t(active_node < 0) : invalid;" + os.linesep
                    + "\t\t\t\tTRUE : statuses[active_node];" + os.linesep
                    + "\t\t\tesac;" + os.linesep)

    nuxmv_string = (nuxmv_string
                    + "\t\tnext(active_node) :=" + os.linesep
                    + "\t\t\tcase" + os.linesep
                    + "\t\t\t\t(active_node = -2) : -2;" + os.linesep#stay in error state
                    + "\t\t\t\t(active_node = -1) & (resume_node = -1) : 0;" + os.linesep#go to root
                    + "\t\t\t\t(active_node = -1) & !(resume_node = -1) : resume_node;" + os.linesep #resume, because apparently we need to resume. 
                    #ok, we've handled the edge cases
                    + "\t\t\t\t(active_node in leafs) : parents[active_node];" + os.linesep#leaf always goes back to parent
                    #we are now in the case of a node with children
                    + "\t\t\t\t(previous_status = invalid) : first_child[active_node];" + os.linesep#previous node was invalid, means we entered from a parent, not a child. start at first child
                    #we are now in the case of a node with children, and have returned from a child
                    + "\t\t\t\t(previous_node = last_child[active_node]) : parents[active_node];" + os.linesep)#that was the last child, we're done.
                    #we are now in the case of a node with children, have returned from a child, and have more children
    if len(parallel_resume) > 0:
        nuxmv_string = (nuxmv_string
                        + "\t\t\t\t(active_node in parallels) : parallel_resume[active_node];" + os.linesep)
    nuxmv_string = (nuxmv_string
                    + "\t\t\t\t(active_node in sequences) & (previous_status = success) : min(max_active_node, previous_node + 1);" + os.linesep #if this is a sequence node and we succeeded, just go to the next child
                    + "\t\t\t\t(active_node in selectors) & (previous_status = failure) : min(max_active_node, previous_node + 1);" + os.linesep #if this is a selector node and we failed, just go to the next child
                    #we have handled all cases where we go to the next child
                    #parallel_unsyhc->have another child
                    #parallel_sych ->uh...see custom code above in the if statement.
                    #sequence->succeeded previous child
                    #selector->failed previous child
                    #so at this point, we must go to parent
                    + "\t\t\t\tTRUE : parents[active_node];" + os.linesep
                    + "\t\t\tesac;" + os.linesep)
    
    if len(parallel_resume) > 0:
        nuxmv_string += parallel_next

                    
    if args.specs:
        nuxmv_string += open(args.specs).read() + os.linesep + os.linesep

    for needed in needed_nodes:
        nuxmv_string = nuxmv_string +  eval('node_creator.create_'+needed+'(node_count-1)')

    nuxmv_string = nuxmv_string + node_creator.create_names_module(variable_to_int, nodes)


    #print a blackboard variable chart
    for variable in variable_to_int:
        nuxmv_string += ('--' + variable + ' : ' + str(variable_to_int[variable]) + os.linesep)
        if variable_to_int[variable] in variable_access:
            for access_node in variable_access[variable_to_int[variable]]:
                nuxmv_string += ('----' + nodes[access_node][2] + os.linesep)
    
    if blackboard_needed:
        nuxmv_string = nuxmv_string + node_creator.create_blackboard(int_to_variable, variable_to_int, variable_access, nodes)

    module_string = ''

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
        for variable in variable_to_int:
            module_string += ("MODULE " + variable + "_SET_module(active_node, nodes_with_access, variables, variable_exists, node_names, variable_names, previous_status)" + os.linesep
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
            module_string += ("MODULE " + node + "_SET_status_module(active_node, id, variables, variable_exists, node_names, variable_names)" + os.linesep
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
        for variable in variable_to_int:
            module_string += ("MODULE " + variable + "_SET_module(active_node, nodes_with_access, variables, variable_exists, node_names, variable_names, previous_status)" + os.linesep
                             + "\tDEFINE" + os.linesep
                             + "\t\t" + variable + " := " + str(args.min_val) + ";" + os.linesep
                             + "\t\t" + variable + "_exists" + " := TRUE;" + os.linesep
            )
        for node in external_status_req:
            module_string += ("MODULE " + node + "_SET_status_module(active_node, id, variables, variable_exists, node_names, variable_names)" + os.linesep
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
                                 + "\t\tresult := (variables[variable_names." + variable + "] = " + str(max_val) + ");" + os.linesep
                )

    if args.gen_module_file is None:
        nuxmv_string = nuxmv_string + module_string
    else:
        if args.overwrite:
            with open(args.gen_module_file, 'w') as f:
                f.write(module_string)
        else:
            try:
                with open(args.gen_module_file, 'x') as f:
                    f.write(module_string)
            except FileExistsError:
                print('The specified module file already exists. To overwrite the file, rerun the command with --overwrite True')
    if args.modules:
        #print(open(modules).read())
        nuxmv_string = nuxmv_string + open(modules.read())
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
