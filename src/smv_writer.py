#-----------------------------------------------------------------------------------------------------------------------
import argparse
import py_trees
import sys
import time
import os
import re
import inspect
import json
#----------------------------------------------------------------------------------------------------------------
import py_trees.console as console


#return node_to_local_root_map
"""
used to create a map from nodes to local root
--
return
node_to_local_root_map : a map (dictionary) from node id to the node id of the local root.
	-> the local root is defined as the most recent ancestor s.t. EXPLAIN DETAILS HERE.
"""
def create_node_to_local_root_map(nodes, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set):
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
"""
used to determine if a given node can 'create' a running result. Note that this is not the same as RETURNING running. For instance, a decorator might return running solely because it's child returned running. The child created running in this case, not the decorator
--
return
A boolean. True indicates the node in question can create running. False indicates it cannot.
"""
def can_create_running(nodes, node_id, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, selector_with_memory_set, decorator_set, leaf_set):
    if node_id in sequence_with_memory_set or node_id in selector_with_memory_set:
        #nodes with memory do not create running, they pass on a running that their children create.
        return False#even if it has no children, it will not create running
    elif node_id in decorator_set:
        #this needs to encompass all cases where a decorator can return Running
        #TODO: modify this to deal with the new X_is_Y layout used for all of these. shouldn't be hard.
        if 'is_running' in nodes[node_id][0]:
            return True
        else:
            return False
    elif node_id in leaf_set:
        #temporarily assuming all leafs can return running. this is not accurate, and will be changed
        #TODO: modify this so that it's more accurate.
        return True
    else:
        return True#without memory and parallel can, everything else covered above
"""
used to create a map from node id to booleans, indicating if a node can return running. Process is done recursively from whichever node is passed.
the true 'result' will be contained in running_map
--
returns
a boolean indicating if the given node can return running
"""
def map_can_return_running(nodes, node_id, running_map, children, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set):
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
            map_can_return_running(nodes, children[node_id][0], running_map, children, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set)
            running_map[node_id] = False
            return False
        elif 'is_running' in nodes[node_id][0]:
            map_can_return_running(nodes, children[node_id][0], running_map, children, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set)
            running_map[node_id] = True
            return True
        else:
            running_map[node_id] = map_can_return_running(nodes, children[node_id][0], running_map, children, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set)
            return running_map[node_id]
    else:
        #it's a parallel, selector, or sequence node
        running = False
        for child in children[node_id]:
            running = map_can_return_running(nodes, child, running_map, children, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set) or running
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
#TODO. consider replacing relevant_list with relevant_map, though i think it might have been done this way for efficiencyh reasons, because lists are better with "for each" operations.
"""
creates a map from a local root to a lit of relevant nodes
--
returns (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map)

local_root_to_relevant_list_map -> a map (dictionary) that maps the local root's node id to a list of node ids. Each node id in the list is a 'relevant' node to that local root, meaning it must track it as a possible location to resume from
nodes_with_memory_to_relevant_descendants_map -> a map (dictionary) that maps a node with memory to a set of relevant descendants.
"""
def create_local_root_to_relevant_list_map(nodes, children, node_to_local_root_map, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, decorator_set, leaf_set):
    running_map = {}
    map_can_return_running(nodes, 0, running_map, children, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set)
    #print(running_map)
    local_root_to_relevant_list_map = {} # a map from local_root to the list of relevant things to track in terms of running
    nodes_with_memory_to_relevant_descendants_map = {} # a map from each node_with_memory to the set of relevant descendants
    for node_id in range(len(nodes)):
        if node_id == node_to_local_root_map[node_id]:
            #this is a local_root
            if nodes[node_id][1] in parallel_synch_set:
                #the local root's parent is a parallel_synch node, so we have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = [-2]
            else:
                #the local root's parent is not a parallel_synch node, so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = []
        elif running_map[node_id] and can_create_running(nodes, node_id, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, selector_with_memory_set, decorator_set, leaf_set):
            cur_id = node_id
            first_child = True
            done = False
            true_done = False
            end_target = nodes[node_to_local_root_map[node_id]][1]#we end at the parent of the local root.
            nodes_with_memory_found = []
            to_add = False
            while not done:
                previous_id = cur_id
                cur_id = nodes[cur_id][1]#get the parent
                if cur_id == end_target:
                    done = True
                    true_done = True
                elif cur_id in decorator_set:
                    if "running_is" in nodes[cur_id][0]:#if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
                        done = True
                        true_done = True
                        to_add = False
                        #if node_id in local_root_to_relevant_list_map[node_to_local_root_map[node_id]]:#check if we added it in
                            #local_root_to_relevant_list_map[node_to_local_root_map[node_id]].pop()#if we added it in, it must be at the end.
                        for node_with_memory in nodes_with_memory_found:#this node_with_memory cannot resume. indicate as such.
                            nodes_with_memory_to_relevant_descendants_map[node_with_memory] = set()
                elif cur_id in selector_without_memory_set or cur_id in sequence_without_memory_set or cur_id in parallel_synch_set or cur_id in parallel_unsynch_set:
                    done = True#nothing above us will care. without memory collapses everything. either this location will be tracked, or nothing will be tracked.
                elif cur_id in sequence_with_memory_set or cur_id in selector_with_memory_set:
                    nodes_with_memory_found.append(cur_id)
                    if cur_id not in nodes_with_memory_to_relevant_descendants_map:
                       nodes_with_memory_to_relevant_descendants_map[cur_id] = set()
                    if children[cur_id][0] == previous_id:
                        #this is the first child. change nothing
                        pass
                    else:
                        #this was not the first child. mark this down
                        first_child = False
                        to_add = True
                    if not first_child:#if at some point we encountered a not first child, then this node is relevant.
                        nodes_with_memory_to_relevant_descendants_map[cur_id].add(node_id)
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
                        for node_with_memory in nodes_with_memory_found:#this node_with_memory cannot resume. indicate as such.
                            nodes_with_memory_to_relevant_descendants_map[node_with_memory] = set()
            if to_add:
                local_root_to_relevant_list_map[node_to_local_root_map[node_id]].append(node_id)#this is a valid resume point. tell the local root about it. 

    return (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map)

#return node_to_descendants_map. this maps each node to the set of all of it's descendants. leaf nodes map to an empty set. a node is not it's own descendant
def create_node_to_descendants_map(nodes, children, leaf_set):
    #method explanation
    #go through all the nodes in order
    #add a set() for each node
    #if we find a node without children, go back up until we reach -1. for each stop along the way, add the node without children.

    #so this method only adds leaf nodes????
    node_to_descendants_map = {}
    for node_id in range(len(nodes)):
        node_to_descendants_map[node_id] = set()
        # if node_id in leaf_set or node_id not in children or len(children[node_id]) == 0:
        #     #this is a terminus point
        #     cur_id = nodes[node_id][1]
        #     while not cur_id == -1:
        #         node_to_descendants_map[cur_id].add(node_id)
        #         cur_id = nodes[cur_id][1]
        cur_id = nodes[node_id][1]
        while not cur_id == -1:
            node_to_descendants_map[cur_id].add(node_id)
            cur_id = nodes[cur_id][1]
    return node_to_descendants_map



#-----------------------------------------------------------------------------------------------------------------------

def create_leaf_to_status(nodes, children, node_to_local_root_map, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, decorator_set, leaf_set):
    #plan. create an ordered set of leafs, then cascade them through.
    #probably just go through the nodes in order, which will cause us to hit the leaf nodes in order.
    
    pass

#-----------------------------------------------------------------------------------------------------------------------

#creates the strings necessary for initialization stuff
def create_nodes(nodes, children, additional_arguments, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, decorator_set, leaf_set, parallel_policies):
    define_string = ""
    init_string = ""
    next_string = ""
    var_string = ""
    for node_id in range(0, len(nodes)):
        #print(node_id)
        if node_id == 0:
            define_string += "\t\t" + nodes[node_id][2] + ".active := TRUE;" + os.linesep
        children_string = ""
        #if node_id in selector_without_memory_set or node_id in sequence_without_memory_set or node_id in selector_with_memory_set or node_id in sequence_with_memory_set or node_id in parallel_synch_set or node_id in parallel_unsynch_set:
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
        elif node_id in selector_without_memory_set or node_id in sequence_without_memory_set:
            var_string += "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0] + str(len(children[node_id])) + "(" + children_string
        elif node_id in selector_with_memory_set or node_id in sequence_with_memory_set:
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
                    set_string = '{'
                    for node_with_access in variable_access[additional_arguments[node_id][i]['nodes_with_access_to']]:
                        set_string = set_string + str(node_with_access) + ', '
                    set_string = set_string[0:-2]+'}'#replace the last comma with a }
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
            cur_node = nodes[cur_node][1]
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
                               #if something returned running, the value will be > = local_root, so we'll point to that
                               #note that since we are always executing the entire tree, if we returned running last time we will definitely resume this time.
                               + "\t\t\tesac;" + os.linesep
        )
    define_string = var_define_status_string + define_trace_running_source
    var_string = var_resume_from_node_string
    init_string = init_resume_from_node_string
    next_string =  next_resume_from_node_string
    return (define_string, var_string, init_string, next_string)

#create the resume_point variable that tells sequence nodes which child to start at
def create_resume_point(sequence_with_memory_set, selector_with_memory_set, node_to_local_root_map, local_root_to_relevant_list_map, node_to_descendants_map, children):
    resume_point_string = ""
    nodes_with_memory_set = sequence_with_memory_set.union(selector_with_memory_set)
    for node_with_memory in nodes_with_memory_set:
        #print('new node_with_memory:')
        #print(node_with_memory)
        if node_with_memory not in children or len(children[node_with_memory]) < 2:
            #print('few children. skipping')
            #we have 0 or 1 children
            #if there are no children, then resume_point really doesn't matter, but we need to pass a value
            #if there is 1 child, then we never skip it, so resume_point really doesn't matter, but we need to pass a value
            #hard code -2 into the node_with_memory in this case
            pass
        else:
            #print('multiple children')
            #have an actual quantity of children
            local_root = node_to_local_root_map[node_with_memory]
            relevant_list = local_root_to_relevant_list_map[local_root]
            #print(relevant_list)
            if len(relevant_list) == 0:
                #print('no real resume children. hard coding -2')
                resume_point_string += "\t\tresume_point_" + str(node_with_memory) + " := -2;" + os.linesep
            else:
                #print('real resume target present. initiating')
                resume_point_string += ("\t\tresume_point_" + str(node_with_memory) + " := " + os.linesep
                                        + "\t\t\tcase" + os.linesep
                )
                descendants = node_to_descendants_map[node_with_memory]
                child_index_to_relevant_descendants_map = {} #basically, we are going to use this to figure out where we need to point.
                #i.e., if resume_from_node is pointing to 400, which of our children, if any, needs to be resumed? this is what this map answers.
                #print(descendants)
                for relevant_node in relevant_list:
                    #print(relevant_node)
                    if relevant_node in descendants:
                        for child_index in range(len(children[node_with_memory])):
                            #so we're gonna map this based on relative children
                            #i.e, do i resume from my first child? second child?
                            #print('---------------------------')
                            #print(child_index)
                            #print(child_index_to_relevant_descendants_map)
                            child = children[node_with_memory][child_index]
                            #print(child)
                            if relevant_node in node_to_descendants_map[child]:#if the relevant node is a descendant of this child, then we need to mark that down. if it's not, continue
                                if child_index in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(relevant_node)
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {relevant_node}
                            elif child == relevant_node:#unless of course, the relevant node IS the child, then we also need to mark that down.
                                if child_index in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(relevant_node)
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {relevant_node}
                            
                            #print(child_index_to_relevant_descendants_map)
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

def reconstruct(nodes):
        #tracking variables
    
    children = {-1:[]}#stores a list of children ID. is indexed via node id
    variable_name_to_int = {}#a mapping of variable names to their integer locations
    variable_int_to_name = {}


    
    #-------------------------------------------------------------------------------
    #blackboard information
    
    variable_access = {}#for each variable, a list of nodes with access to that variable. indexed by variable_name
    variable_check = {}#for each variable, a list of nodes that check that variable. indexed by variable name
    #-------------------------------------------------------------------------------
    #sets
    parallel_synch_set = set()
    parallel_unsynch_set = set()
    sequence_with_memory_set = set()
    sequence_without_memory_set = set()
    selector_with_memory_set = set()
    selector_without_memory_set = set()
    decorator_set = set()
    leaf_set = set()
    parallel_policies = {}
    #^this whole sectgion just being loaded from nodes
    #-------------------------------------------------------------------------------
    #variables that we need to properly construct stuff later

    #still deciding if i want to use this stuff or change it.
    additional_arguments = {}#stores additional arguments. it's index via node id
    external_status_req = []#list of nodes that require external status. each entry is the node name.

    for node_id in nodes:
        children[node_id] = nodes[node_id]['children']
        if nodes[node_id]['type'] == 'check_blackboard_variable_value' or nodes[node_id]['type'] == 'wait_for_blackboard_variable_value':
            for (variable_number, variable_name) in nodes[node_id]['variables']:
                if variable_name in variable_check:
                    variable_check[variable_name].append(node_id)
                else:
                    variable_check[variable_name] = [node_id]
                variable_name_to_int[variable_name] = variable_number
                variable_int_to_name[variable_number] = variable_name
                
        else:
            for (variable_number, variable_name) in nodes[node_id]['variables']:
                if variable_name in variable_access:
                    variable_access[variable_name].append(node_id)
                else:
                    variable_access[variable_name] = [node_id]
                variable_name_to_int[variable_name] = variable_number
                variable_int_to_name[variable_number] = variable_name
        if nodes[node_id]['category'] == 'leaf':
            leaf_set.add(node_id)
        elif nodes[node_id]['category'] == 'decorator':
            decorator_set.add(node_id)
        else:
            if nodes[node_id]['type'] == 'selector_with_memory':
                selector_with_memory_set.add(node_id)
            elif nodes[node_id]['type'] == 'selector_without_memory':
                selector_without_memory_set.add(node_id)
            elif nodes[node_id]['type'] == 'sequence_with_memory':
                sequence_with_memory_set.add(node_id)
            elif nodes[node_id]['type'] == 'sequence_without_memory':
                sequence_without_memory_set.add(node_id)
            else:
                if "unsynchronized" in nodes[node_id]['type']:
                    parallel_unsynch_set.add(node_id)
                else:
                    parallel_synch_set.add(node_id)
                if "success_on_all" in nodes[node_id]['type']:
                    parallel_policies[node_id] = True
                else:
                    parallel_policies[node_id] = False
        
        additional_arguments[node_id] = nodes[node_id]['additional_arguments']
        external_status_req.append(nodes[node_id]['name'])
                
    
    return (children, variable_name_to_int, variable_int_to_name, variable_access, variable_check, leaf_set, decorator_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, parallel_synch_set, parallel_unsynch_set, parallel_policies, external_status_req, additional_arguments)
##############################################################################
# Main
##############################################################################

def main():
    global blackboard_needed

    arg_parser = argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('json_file')
    arg_parser.add_argument('--blackboard_input_file', default = None)
    arg_parser.add_argument('--module_input_file', default = None)
    arg_parser.add_argument('--specs_input_file', default = None)
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--blackboard_output_file', default = None)
    arg_parser.add_argument('--module_output_file', default = None)
    arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()

    module = __import__(args.root_file.replace('.py', ''))

    root_string = 'module.' + args.root_method + '('
    first = True
    for root_arg in args.root_args:
        if first:
            root_string += root_arg
            first = False
        else:
            root_string += ', ' + root_arg
    for string_arg in args.string_args:
        if first:
            root_string += '\'' + string_arg + '\''
            first = False
        else:
            root_string += ', ' + '\'' + string_arg + '\''
    root_string += ')'
    root = eval(root_string)




    temp = json.load(args.json_file)#this should just be a json call
    nodes = temp[nodes]
    variables = temp[variables]

    #reconstruct useful information

    (children, variable_name_to_int, variable_int_to_name, variable_access, variable_check, leaf_set, decorator_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, parallel_synch_set, parallel_unsynch_set, parallel_policies) = reconstruct(nodes)
    
    node_to_local_root_map = create_node_to_local_root_map(nodes, parallel_synch_set, parallel_unsynch_set, decorator_set, leaf_set)

    (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map) = create_local_root_to_relevant_list_map(nodes, children, node_to_local_root_map, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, decorator_set, leaf_set)
    
    variable_name_cleanup(variable_name_to_int, variable_access)

    node_to_descendants_map = create_node_to_descendants_map(nodes, children, leaf_set)

    #this is handled earlier.
    #int_to_variable = {}
    #for variable in variable_name_to_int:
        #int_to_variable[variable_name_to_int[variable]] = variable

    #------------------------------------------------------------------------------------------------------------------------
    #done with variable decleration, moving into string building.

        
    define_string = ("MODULE main" + os.linesep
                     + "\tCONSTANTS" + os.linesep
                     + "\t\tsuccess, failure, running, invalid;" + os.linesep
                     + "\tDEFINE" + os.linesep
                     + "\t\tstatuses := ["
    )
    for node_id in range(len(nodes)):
        if node_id == 0:
            define_string += nodes[node_id][2] + ".status"
        else:
            define_string += ", " + nodes[node_id][2] + ".status"
    define_string += "];" + os.linesep

    #------------------------------------------------------------------------------------------------------------------------
    var_string = (""
                  + "\tVAR" + os.linesep
    )       
    if variable_name_to_int:
        var_string += "\t\tvariable_names : define_variables;" + os.linesep
    var_string += "\t\tnode_names : define_nodes;" + os.linesep
    if variable_name_to_int:
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

    
    (new_define, new_var, new_init, new_next) = create_resume_point(sequence_with_memory_set, selector_with_memory_set, node_to_local_root_map, local_root_to_relevant_list_map, node_to_descendants_map, children)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_nodes(nodes, children, additional_arguments, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, decorator_set, leaf_set, parallel_policies)
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


    created_types = set()
    for node in nodes:
        if nodes[node]['category'] == 'leaf' or nodes[node]['category'] == 'decorator':
            if not nodes[node]['type'] in created_types:
                created_types.add(nodes[node]['type'])
                nuxmv_string += eval('node_creator.create_' + nodes[node]['type'] + '()')
        else:
            cur_type = nodes[node]['type'] + "_" + str(len(nodes[node]['children'])) 
            if 'parallel' in cur_type:
                if 'unsynchronized' in cur_type:
                    alt_type = cur_type.replace('_unsynchronized', '_synchronized')
                    call_type = nodes[node]['type'].replace('_unsynchronized', '')
                else:
                    alt_type = cur_type.replace('_synchronized', '_unsynchronized')
                    call_type = nodes[node]['type'].replace('_synchronized', '')
                if cur_type in created_types or alt_type in created_types:
                    created_types.add(cur_type)
                    nuxmv_string += eval('node_creator.create_' + call_type + '(' + str(len(nodes[node]['children'])) + ')')
            else:
                if not cur_type in created_types:
                    created_types.add(cur_type)
                    nuxmv_string += eval('node_creator.create_' + nodes[node]['type'] + '(' + stwr(len(nodes[node]['children'])) + ')')
    
    

    nuxmv_string += node_creator.create_names_module(variable_name_to_int, nodes)


    #print a blackboard variable chart
    for variable in variable_name_to_int:
        nuxmv_string += ('--' + variable + ' : ' + str(variable_name_to_int[variable]) + os.linesep)
        if variable in variable_access:
            for access_node in variable_access[variable]:
                nuxmv_string += ('----' + nodes[access_node][2] + os.linesep)

    
    if args.blackboard_input_file:
        nuxmv_string += open(args.blackboard_input_file).read()
    else:
        blackboard_string = ''
        if variable_name_to_int:
            blackboard_string += node_creator.create_blackboard(int_to_variable, variable_name_to_int, variable_access, nodes, args.min_val, args.max_val)
        nuxmv_string += blackboard_string
        if args.blackboard_output_file is None:
            pass
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
    module_string = ''
    if args.module_input_file:
        #print(open(modules).read())
        nuxmv_string = nuxmv_string + open(args.module_input_file).read()
    else:
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
        nuxmv_string += module_string
        if args.module_output_file is None:
            pass
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
