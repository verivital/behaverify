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
def create_node_to_local_root_map(nodes):
    node_to_local_root_map = {0: 0}# a map from node_id to the local root for that node_id
    for node_id in range(1, len(nodes)):
        if 'parallel' in nodes[nodes[node_id]['parent_id']]['type']:
            node_to_local_root_map[node_id] = node_id
        else:
            node_to_local_root_map[node_id] = node_to_local_root_map[nodes[node_id][1]]
    return node_to_local_root_map

#returns Bool
"""
used to determine if a given node can 'create' a running result. Note that this is not the same as RETURNING running. For instance, a decorator might return running solely because it's child returned running. The child created running in this case, not the decorator
--
return
A boolean. True indicates the node in question can create running. False indicates it cannot.
"""
def can_create_running(node):
    if node['category'] == 'composite' and 'with_memory' in node['type']:
        #nodes with memory do not create running, they pass on a running that their children create.
        return False#even if it has no children, it will not create running
    elif node['category'] == 'decorator':
        #this needs to encompass all cases where a decorator can return Running
        if node['type'] == 'X_is_Y':
            if node['additional_arguments'][1] == 'running':
                #Y is running, so this is a decorator that turns something that is not running into running
                return True
        return False
    elif node['type'] == 'leaf':
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
def map_can_return_running(nodes, node_id, running_map):
    #print(running_map)
    node = nodes[node_id]
    if node['category'] == 'leaf':
        #this needs to encompass all cases where a leaf node can return Running
        if node['type'] == "success":
            running_map[node_id] = False
            return False
        elif node['type'] == "failure":
            running_map[node_id] = False
            return False
        elif node['type'] == "non_blocking":
            running_map[node_id] = False
            return False
        elif node['type'] == "check_blackboard_variable_exists":
            running_map[node_id] = False
            return False
        elif node['type'] == "check_blackboard_variable_value":
            running_map[node_id] = False
            return False
        else:
            running_map[node_id] = True
            return True#currently being lazy, and just going to assume they can all return Running, even though this is not the case
    elif node['category'] == 'decorator':
        if node['type'] == 'X_is_Y':
            if node['additional_arguments'][0] == 'running':
                map_can_return_running(nodes, node['children'][0], running_map)
                running_map[node_id] = False
                return False
            elif node['additional_arguments'][1] == 'running':
                map_can_return_running(nodes, node['children'][0], running_map)
                running_map[node_id] = True
                return True
        running_map[node_id] = map_can_return_running(nodes, node['children'][0], running_map)
        return running_map[node_id]
    else:
        #it's a parallel, selector, or sequence node
        running = False
        for child in node['children']:
            running = map_can_return_running(nodes, child, running_map) or running
        if len(node['children']) == 0:
            if 'parallel' in node['type']:
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
def create_local_root_to_relevant_list_map(nodes, node_to_local_root_map):
    running_map = {}
    map_can_return_running(nodes, 0, running_map)
    #print(running_map)
    local_root_to_relevant_list_map = {} # a map from local_root to the list of relevant things to track in terms of running
    nodes_with_memory_to_relevant_descendants_map = {} # a map from each node_with_memory to the set of relevant descendants
    for node_id in range(len(nodes)):
        if node_id == node_to_local_root_map[node_id]:
            #this is a local_root
            if 'parallel_synchronized' in nodes[nodes[node_id]['parent_id']]['type']:
                #the local root's parent is a parallel_synch node, so we have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = [-2]
            else:
                #the local root's parent is not a parallel_synch node, so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = []
        elif running_map[node_id] and can_create_running(nodes[node_id]):
            cur_id = node_id
            first_child = True
            done = False
            true_done = False
            end_target = nodes[node_to_local_root_map[node_id]]['parent_id']#we end at the parent of the local root.
            nodes_with_memory_found = []
            to_add = False
            while not done:
                previous_id = cur_id
                cur_id = nodes[cur_id]['parent_id']#get the parent
                if cur_id == end_target:
                    done = True
                    true_done = True
                elif nodes[cur_id]['category'] == 'decorator':
                    if nodes[cur_id]['type'] == "X_is_Y" and nodes['type']['additional_arguments'][0] == 'running':#if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
                        done = True
                        true_done = True
                        to_add = False
                        for node_with_memory in nodes_with_memory_found:#this node_with_memory cannot resume. indicate as such.
                            nodes_with_memory_to_relevant_descendants_map[node_with_memory] = set()
                elif nodes[cur_id]['category'] == 'composite':
                    if ('without_memory' in nodes[cur_id]['type'] or 'parallel' in nodes[cur_id]['type']):
                        done = True#nothing above us will care. without memory collapses everything. either this location will be tracked, or nothing will be tracked.
                    elif 'with_memory' in nodes[cur_id]['type']:
                        nodes_with_memory_found.append(cur_id)
                        if cur_id not in nodes_with_memory_to_relevant_descendants_map:
                            nodes_with_memory_to_relevant_descendants_map[cur_id] = set()
                        if nodes[cur_id]['children'][0] == previous_id:
                            #this is the first child. change nothing
                            pass
                        else:
                            #this was not the first child. mark this down
                            first_child = False
                            to_add = True
                        if not first_child:#if at some point we encountered a not first child, then this node is relevant.
                            nodes_with_memory_to_relevant_descendants_map[cur_id].add(node_id)
                    else:
                        print(nodes[node_id]['type'])
                        print('the above node is a composite node of unknown type. it is not parallel, nor does it indicate memory or lack of memory.')
            #make sure there's not a decorator above the end point that invalidates our need to track running.
            while not true_done:
                previous_id = cur_id
                cur_id = nodes[cur_id]['parent_id']
                if cur_id == end_target:
                    true_done = True
                elif nodes[cur_id]['category'] == 'decorator':
                    if nodes[cur_id]['type'] == "X_is_Y" and nodes['type']['additional_arguments'][0] == 'running':#if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
                        true_done = True
                        to_add = False
                        for node_with_memory in nodes_with_memory_found:#this node_with_memory cannot resume. indicate as such.
                            nodes_with_memory_to_relevant_descendants_map[node_with_memory] = set()
            if to_add:
                local_root_to_relevant_list_map[node_to_local_root_map[node_id]].append(node_id)#this is a valid resume point. tell the local root about it. 

    return (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map)

#return node_to_descendants_map. this maps each node to the set of all of it's descendants. leaf nodes map to an empty set. a node is not it's own descendant
def create_node_to_descendants_map(nodes):
    #method explanation
    #go through all the nodes in order
    #add a set() for each node
    #go back up until we reach -1. for each stop along the way, add the current node

    node_to_descendants_map = {}
    for node_id in range(len(nodes)):
        node_to_descendants_map[node_id] = set()
        cur_id = nodes[node_id]['parent_id']
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
def create_nodes(nodes):
    define_string = ""
    init_string = ""
    next_string = ""
    var_string = ""
    for node_id in range(0, len(nodes)):
        node = nodes[node_id]
        #print(node_id)
        if node_id == 0:
            define_string += "\t\t" + node['name'] + ".active := TRUE;" + os.linesep
        children_string = ''
        #if node_id in selector_without_memory_set or node_id in sequence_without_memory_set or node_id in selector_with_memory_set or node_id in sequence_with_memory_set or node_id in parallel_synch_set or node_id in parallel_unsynch_set:
        if len(node['children']) == 0:
            #this node has no children
            children_string = ''
        else:
            children_string = ''
            for child in node['children']:
                children_string += ", " + nodes[child]['name']
            children_string = children_string[2:]
        #---------------------------------
        if node['category'] == 'leaf':
            var_string += "\t\t" + node['name'] + " : " + node['category'] + '_' + node['type'] + "("
        elif node['category'] == 'decorator':
            var_string += "\t\t" + node['name'] + " : " + node['category'] + '_' + node['type'] + "(" + children_string
        elif node['category'] == 'composite':
            if 'without_memory' in node['type']:
                var_string += "\t\t" + node['name'] + " : " + node['category'] + '_' + node['type'] + str(len(children[node_id])) + "(" + children_string
            elif 'with_memory' in node['type']:
                if len(node['children']) < 2:
                    resume_point = "-2"
                else:
                    resume_point = "resume_point_" + str(node_id)
                if children_string == '':
                    pass
                else:
                    children_string = children_string + ', '
                var_string += "\t\t" + node['name'] + " : " + node['category'] + '_' + node['type'] + str(len(children[node_id])) + "(" + children_string + resume_point
            elif 'parallel' in node['type']:
                if len(node['children']) < 2:
                    skip_string = "[-2]"
                else:
                    skip_string = "["
                    for child in node['children']:
                        skip_string += "resume_from_node_" + str(child) + ", "
                    skip_string = skip_string[0:-2] + "]"
                define_string += "\t\tparallel_skip_" + str(node_id) + " := " + skip_string + ";" + os.linesep

                if children_string == "":
                    pass
                else:
                    children_string = children_string + ', '
                var_string += "\t\t" + node['name'] + " : " + node['category'] + '_' + node['type'] + str(len(children[node_id])) + "(" + children_string + " parallel_skip_" + str(node_id)
            else:
                print('composite node of unknown type. is not parallel. is not with_memory. is not without_memory. Node infromation follows')
                print(node)
        else:
            print('ERROR: node is not leaf, decorator, or composite. This should not be possible. Node information follows')
            print(node)
            var_string += "0"
        #---------------------------------
        if node['type'] == 'leaf':
            first = True
        else:
            first = False
        for arg in node['additional_arguments']:
            if first:
                first = False
                var_string += arg
            else:
                var_string += ', ' + arg
        var_string = var_string + ");" + os.linesep
    return (define_string, var_string, init_string, next_string)

#runs through any additional arguments
def create_additional_arguments(nodes):
    var_string = ""
    define_string = ""
    init_string = ""
    next_string =  ""
    for node_id in nodes:
        node = nodes[node_id]
        for arg in node['additional_definitions']:
            define_string += arg
        for arg in node['additional_declarations']:
            var_string += arg
        for arg in node['additional_initialization']:
            init_string += arg
    return(var_string, define_string, init_string, next_string)

#responsible for creating the resume structure
def create_resume_structure(nodes, local_root_to_relevant_list_map):
    
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
        #we've manually handled the root case using inject_string
        cur_node = nodes[local_root]['parent_id']#start from the parent.
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
            if len(nodes[node_id]['children']) == 0:
                pass
            else:
                for child in nodes[node_id]['children']:
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
def create_resume_point(nodes, node_to_local_root_map, local_root_to_relevant_list_map, node_to_descendants_map):
    resume_point_string = ""
    for node_id in nodes:
        node = nodes[node_id]
        if not node['category'] == 'composite':
            continue
        if not 'with_memory' in node['type']:
            continue
        if len(node['children']) < 2:
            #print('few children. skipping')
            #we have 0 or 1 children
            #if there are no children, then resume_point really doesn't matter, but we need to pass a value
            #if there is 1 child, then we never skip it, so resume_point really doesn't matter, but we need to pass a value
            #hard code -2 into the node_with_memory in this case
            pass
        else:
            #print('multiple children')
            #have an actual quantity of children
            local_root = node_to_local_root_map[node_id]
            relevant_list = local_root_to_relevant_list_map[local_root]
            #print(relevant_list)
            if len(relevant_list) == 0:
                #print('no real resume children. hard coding -2')
                resume_point_string += "\t\tresume_point_" + str(node_id) + " := -2;" + os.linesep
            else:
                #print('real resume target present. initiating')
                resume_point_string += ("\t\tresume_point_" + str(node_id) + " := " + os.linesep
                                        + "\t\t\tcase" + os.linesep
                )
                descendants = node_to_descendants_map[node_id]
                child_index_to_relevant_descendants_map = {} #basically, we are going to use this to figure out where we need to point.
                #i.e., if resume_from_node is pointing to 400, which of our children, if any, needs to be resumed? this is what this map answers.
                #print(descendants)
                for relevant_node in relevant_list:
                    #print(relevant_node)
                    if relevant_node in descendants:
                        for child_index in range(len(node['children'])):
                            #so we're gonna map this based on relative children
                            #i.e, do i resume from my first child? second child?
                            #print('---------------------------')
                            #print(child_index)
                            #print(child_index_to_relevant_descendants_map)
                            child = node['children'][child_index]
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

##############################################################################
# Main
##############################################################################

def main():
    arg_parser = argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('input_file')
    arg_parser.add_argument('--blackboard_input_file', default = None)
    arg_parser.add_argument('--module_input_file', default = None)
    arg_parser.add_argument('--specs_input_file', default = None)
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--blackboard_output_file', default = None)
    arg_parser.add_argument('--module_output_file', default = None)
    arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()



    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']
    
    node_to_local_root_map = create_node_to_local_root_map(nodes)
    (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map) = create_local_root_to_relevant_list_map(nodes, node_to_local_root_map)
    node_to_descendants_map = create_node_to_descendants_map(nodes)

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
            define_string += nodes[node_id]['name'] + ".status"
        else:
            define_string += ", " + nodes[node_id]['name'] + ".status"
    define_string += "];" + os.linesep

    #------------------------------------------------------------------------------------------------------------------------
    var_string = (""
                  + "\tVAR" + os.linesep
    )       
    if variables:
        var_string += "\t\tvariable_names : define_variables;" + os.linesep
    var_string += "\t\tnode_names : define_nodes;" + os.linesep
    if variables:
        var_string += "\t\tblackboard : blackboard_module(node_names, variable_names, statuses);" + os.linesep
    #------------------------------------------------------------------------------------------------------------------------
    init_string = "\tASSIGN" + os.linesep
    next_string = ""
    #------------------------------------------------------------------------------------------------------------------------
    
    (new_define, new_var, new_init, new_next) = create_resume_structure(nodes, local_root_to_relevant_list_map)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    
    (new_define, new_var, new_init, new_next) = create_resume_point(nodes, node_to_local_root_map, local_root_to_relevant_list_map, node_to_descendants_map)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_nodes(nodes)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_additional_arguments(nodes)
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
                nuxmv_string += eval('node_creator.create_' + nodes[node]['category'] + '_' + nodes[node]['type'] + '()')
        elif nodes[node]['category'] == 'composite':
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
                    nuxmv_string += eval('node_creator.create_' + nodes[node]['category'] + '_' + call_type + '(' + str(len(nodes[node]['children'])) + ')')
            else:
                if not cur_type in created_types:
                    created_types.add(cur_type)
                    nuxmv_string += eval('node_creator.create_' + nodes[node]['category'] + '_' + nodes[node]['type'] + '(' + stwr(len(nodes[node]['children'])) + ')')
        else:
            print('unknown node category')
            print(nodes[node])
    
    

    nuxmv_string += node_creator.create_names_module(variables, nodes)


    #print a blackboard variable chart
    for variable in variables:
        nuxmv_string += ('--' + variable + ' : ' + str(variables[variable]['variable_id']) + os.linesep)
        for access_node in variables[variable]['access']:
            nuxmv_string += ('----' + nodes[access_node]['name'] + os.linesep)

    
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
        for node_id in nodes:
            for module in nodes[node_id]['additional_modules']:
                if module['type'] == 'status':
                    if len(module['possible_values']) == 1:
                        pass
                    else:
                        if len(module['possible_values']) == 0:
                            print('no possible values for module, defaulting to all values acceptable')
                            print(nodes[node_id])
                        module_string += ("MODULE" + module['name'] + '(' + str(module['args'][1:-1]) + ')' + os.linesep
                                          + "\tCONSTANTS" + os.linesep
                                          + "\t\tsuccess, failure, running;" + os.linesep
                                          + "\tVAR" + os.linesep
                                          + "\t\tstatus : {" + str(module['possible_values'][1:-1]) +"};" + os.linesep
                                          )
                        assigned = False
                        if not module['initial_value'] is None:
                            assigned = True
                            semicolon = ';'
                            if module['initial_value'].rstrip()[-1] == ';':
                                semicolon = ''
                            module_string += ("\tASSIGN" + os.linesep
                                              + "\t\tinit(status) := " + module['initial_value'] + semicolon + os.linesep
                                              )
                        if not module['next_value'] is None:
                            if assigned:
                                module_string += "\tASSIGN" + os.linesep
                                
                            semicolon = ';'
                            if module['next_value'].rstrip()[-1] == ';':
                                semicolon = ''
                            module_string += "\t\t(status) := " + module['next_value'] + semicolon + os.linesep
                                              
                        
                elif module['type'] == 'check':
                    module_string += ("MODULE" + module['name'] + '(' + str(module['args'][1:-1]) + ')' + os.linesep
                                      + "\tDEFINE" + os.linesep
                                      + "\t\t result := variable_exists[variable_names." + module['variable_name'] + "] & (" + module['left_hand_side'] + module['operator'] + module['right_hand_side'] + ");" + os.linesep
                                      )
                else:
                    module_string += module['custom_module']
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
