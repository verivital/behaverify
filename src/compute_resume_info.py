
# arg_parser.add_argument('input_file')
# arg_parser.add_argument('--blackboard_input_file', default = None)
# arg_parser.add_argument('--module_input_file', default = None)
# arg_parser.add_argument('--specs_input_file', default = None)
# arg_parser.add_argument('--output_file', default = None)
# arg_parser.add_argument('--blackboard_output_file', default = None)
# arg_parser.add_argument('--module_output_file', default = None)
# arg_parser.add_argument('--overwrite', action = 'store_true')

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
import node_creator


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
            node_to_local_root_map[node_id] = node_to_local_root_map[nodes[node_id]['parent_id']]
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
            if node_id == 0:
                #the local root's parent is not a parallel_synch node, so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = []
            elif 'parallel_synchronized' in nodes[nodes[node_id]['parent_id']]['type']:
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
                    if nodes[cur_id]['type'] == "X_is_Y" and nodes[cur_id]['additional_arguments'][0] == 'running':#if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
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
                    if nodes[cur_id]['type'] == "X_is_Y" and nodes[cur_id]['additional_arguments'][0] == 'running':#if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
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
            cur_id = nodes[cur_id]['parent_id']
    return node_to_descendants_map



#-----------------------------------------------------------------------------------------------------------------------

def create_leaf_to_status(nodes, children, node_to_local_root_map, parallel_synch_set, parallel_unsynch_set, sequence_with_memory_set, sequence_without_memory_set, selector_with_memory_set, selector_without_memory_set, decorator_set, leaf_set):
    #plan. create an ordered set of leafs, then cascade them through.
    #probably just go through the nodes in order, which will cause us to hit the leaf nodes in order.
    
    pass

#-----------------------------------------------------------------------------------------------------------------------
