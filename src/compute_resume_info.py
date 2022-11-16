
# arg_parser.add_argument('input_file')
# arg_parser.add_argument('--blackboard_input_file', default = None)
# arg_parser.add_argument('--module_input_file', default = None)
# arg_parser.add_argument('--specs_input_file', default = None)
# arg_parser.add_argument('--output_file', default = None)
# arg_parser.add_argument('--blackboard_output_file', default = None)
# arg_parser.add_argument('--module_output_file', default = None)
# arg_parser.add_argument('--overwrite', action = 'store_true')

# -----------------------------------------------------------------------------------------------------------------------

def create_node_to_local_root_map(nodes):
    """
    used to create a map from nodes to local root
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    --
    return
    @ node_to_local_root_map -> a map (dictionary) from node id to the
      node id of the local root.
      @ local_root -> the local root of a node N is a node M such that
        M is an ancestor of N and M is the root node or M's parent
        is a parallel synchronised node and there is no P between N and M
        such that P's parent is a parallel synchronised node.
    --
    effects
    goes through all the nodes in
    """
    node_to_local_root_map = {0: 0}
    # a map from node_id to the local root for that node_id
    for node_id in range(1, len(nodes)):
        if 'parallel' in nodes[nodes[node_id]['parent_id']]['type']:
            node_to_local_root_map[node_id] = node_id
        else:
            node_to_local_root_map[node_id] = node_to_local_root_map[nodes[node_id]['parent_id']]
    return node_to_local_root_map


def can_create_running(node):
    """
    used to determine if a given node can 'create' a running result.
    Note that this is not the same as RETURNING running. For instance,
    a decorator might return running solely because it's child returned running.
    The child created running in this case, not the decorator
    --
    return
    A boolean. True indicates the node in question can create running.
    False indicates it cannot.
    """
    if node['category'] == 'composite' and 'with_memory' in node['type']:
        # nodes with memory do not create running;
        # they pass on a running that their children create.
        return False  # even if it has no children, it will not create running
    elif node['category'] == 'decorator':
        # this needs to encompass all cases
        # where a decorator can create Running
        if node['type'] == 'X_is_Y':
            if node['additional_arguments'][1] == 'running':
                # Y is running, so this is a decorator that
                # turns something that is not running into running
                return True
        return False
    elif node['type'] == 'leaf':
        # TODO: modify this so that it's more accurate.
        return node['return_arguments']['running']
    else:
        # without memory and parallel can, everything else covered above
        return True


def map_can_return_running(nodes, node_id, running_map):
    """
    used to create a map from node id to booleans,
    indicating if a node can return running.
    Process is done recursively from whichever node is passed.
    the true 'result' will be contained in running_map
    --
    returns
    a boolean indicating if the given node can return running
    """
    node = nodes[node_id]
    if node['category'] == 'leaf':
        running_map[node_id] = node['return_arguments']['running']
        return node['return_arguments']['running']
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
        running_map[node_id] = map_can_return_running(nodes,
                                                      node['children'][0],
                                                      running_map)
        return running_map[node_id]
    else:
        # it's a parallel, selector, or sequence node
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


def refine_return_types(nodes, node_id):
    node = nodes[node_id]
    if node['category'] == 'leaf':
        return
    elif node['category'] == 'composite':
        if 'selector' in node['type']:
            can_return_success = False
            can_return_failure = True
            can_return_running = False
            for child_id in node['children']:
                refine_return_types(nodes, child_id)
                can_return_success = can_return_success or nodes[child_id]['return_arguments']['success']
                can_return_running = can_return_running or nodes[child_id]['return_arguments']['running']
                can_return_failure = can_return_failure and nodes[child_id]['return_arguments']['failure']
            node['return_arguments'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        elif 'sequence' in node['type']:
            can_return_success = True
            can_return_failure = False
            can_return_running = False
            for child_id in node['children']:
                refine_return_types(nodes, child_id)
                can_return_success = can_return_success and nodes[child_id]['return_arguments']['success']
                can_return_running = can_return_running or nodes[child_id]['return_arguments']['running']
                can_return_failure = can_return_failure or nodes[child_id]['return_arguments']['failure']
            node['return_arguments'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        elif 'success_on_all' in node['type']:
            can_return_success = True
            can_return_failure = False
            can_return_running = False
            for child_id in node['children']:
                refine_return_types(nodes, child_id)
                can_return_success = can_return_success and nodes[child_id]['return_arguments']['success']
                can_return_running = can_return_running or nodes[child_id]['return_arguments']['running']
                can_return_failure = can_return_failure or nodes[child_id]['return_arguments']['failure']
            node['return_arguments'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        elif 'success_on_one' in node['type']:
            can_return_success = False
            can_return_failure = False
            can_return_running = True
            for child_id in node['children']:
                refine_return_types(nodes, child_id)
                can_return_success = can_return_success or nodes[child_id]['return_arguments']['success']
                can_return_running = can_return_running and nodes[child_id]['return_arguments']['running']
                can_return_failure = can_return_failure or nodes[child_id]['return_arguments']['failure']
            node['return_arguments'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        else:
            print('unknown composite type!!! ', node['type'])
            return
    elif node['category'] == 'decorator':
        child_id = node['children'][0]
        child = nodes[child_id]
        refine_return_types(nodes, child_id)
        if node['type'] == 'X_is_Y':
            node['return_arguments'][node['additional_arguments'][1]] = False
            for return_val in ('success', 'failure', 'running'):
                if return_val in node['additional_arguments']:
                    node['return_arguments'][node['additional_arguments'][1]] = node['return_arguments'][node['additional_arguments'][1]] or child['return_arguments'][return_val]
                else:
                    node['return_arguments'][return_val] = child['return_arguments'][return_val]
        elif node['type'] == 'inverter':
            node['return_arguments'] = {
                'success' : child['return_arguments']['failure'],
                'failure' : child['return_arguments']['success'],
                'running' : child['return_arguments']['running']}
        return
    else:
        print('unknown node category!!!', node['category'])
        return


def refine_invalid(nodes, node_id = 0, is_root = True):
    node = nodes[node_id]
    if is_root:
        node['can_be_invalid'] = False
        for child_id in node['children']:
            refine_invalid(nodes, child_id, False)
        return
    parent = nodes[node['parent_id']]
    if parent['can_be_invalid']:
        node['can_be_invalid'] = True
    elif 'unsynchronized' in parent['type']:
        node['can_be_invalid'] = False
    elif 'synchronized' in parent['type']:
        if node['return_arguments']['success'] is False:
            node['can_be_invalid'] = False
        else:
            node['can_be_invalid'] = True
    elif parent['type'] == 'selector_without_memory':
        pass


def create_local_root_to_relevant_list_map(nodes, node_to_local_root_map):
    """
    creates a map from a local root to a lit of relevant nodes
    --
    returns
    local_root_to_relevant_list_map,
    nodes_with_memory_to_relevant_descendants_map
    --
    local_root_to_relevant_list_map ->
     a map (dictionary) that maps the
     local root's node id to a list of node ids. Each node id in
     the list is a 'relevant' node to that local root,
     meaning it must track it as a possible location to resume from
    nodes_with_memory_to_relevant_descendants_map ->
     a map (dictionary) that maps a node with memory
     to a set of relevant descendants.
    """

    running_map = {}
    map_can_return_running(nodes, 0, running_map)

    local_root_to_relevant_list_map = {}
    # a map from local_root to the list of relevant things
    # to track in terms of running
    nodes_with_memory_to_relevant_descendants_map = {}
    # a map from each node_with_memory to the set of relevant descendants
    for node_id in range(len(nodes)):
        if node_id == node_to_local_root_map[node_id]:
            # this is a local_root
            if node_id == 0:
                # the local root's parent is not a parallel_synch node
                # so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = []
            elif 'parallel_synchronized' in nodes[nodes[node_id]['parent_id']]['type']:
                # the local root's parent is a parallel_synch node
                # so we have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = [-2]
            else:
                # the local root's parent is not a parallel_synch node
                # so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_id] = []
        elif running_map[node_id] and can_create_running(nodes[node_id]):
            cur_id = node_id
            first_child = True
            done = False
            true_done = False
            end_target = nodes[node_to_local_root_map[node_id]]['parent_id']
            # we end at the parent of the local root.
            nodes_with_memory_found = []
            to_add = False
            while not done:
                previous_id = cur_id
                cur_id = nodes[cur_id]['parent_id']  # get the parent
                if cur_id == end_target:
                    done = True
                    true_done = True
                elif nodes[cur_id]['category'] == 'decorator':
                    if nodes[cur_id]['type'] == "X_is_Y" and nodes[cur_id]['additional_arguments'][0] == 'running':
                        # if we encounter a decorator that undoes running,
                        # we no longer care.
                        # TODO: update so it hits
                        # all decorators that can do this.
                        done = True
                        true_done = True
                        to_add = False
                        for node_with_memory in nodes_with_memory_found:
                            # this node_with_memory cannot resume. indicate as such.
                            nodes_with_memory_to_relevant_descendants_map[node_with_memory] = set()
                elif nodes[cur_id]['category'] == 'composite':
                    if ('without_memory' in nodes[cur_id]['type'] or 'parallel' in nodes[cur_id]['type']):
                        done = True
                        # nothing above us will care.
                        # without memory collapses everything.
                        # either this location will be tracked, or nothing will be tracked.
                    elif 'with_memory' in nodes[cur_id]['type']:
                        nodes_with_memory_found.append(cur_id)
                        if cur_id not in nodes_with_memory_to_relevant_descendants_map:
                            nodes_with_memory_to_relevant_descendants_map[cur_id] = set()
                        if nodes[cur_id]['children'][0] == previous_id:
                            # this is the first child. change nothing
                            pass
                        else:
                            # this was not the first child. mark this down
                            first_child = False
                            to_add = True
                        if not first_child:
                            # if at some point we encountered a not first child,
                            # then this node is relevant.
                            nodes_with_memory_to_relevant_descendants_map[cur_id].add(node_id)
                    else:
                        print(nodes[node_id]['type'])
                        print('the above node',
                              'is a composite node of unknown type',
                              'It is not parallel,',
                              'nor does it indicate memory or lack of memory.')
            # make sure there's not a decorator above the end point
            # that invalidates our need to track running.
            while not true_done:
                previous_id = cur_id
                cur_id = nodes[cur_id]['parent_id']
                if cur_id == end_target:
                    true_done = True
                elif nodes[cur_id]['category'] == 'decorator':
                    if nodes[cur_id]['type'] == "X_is_Y" and nodes[cur_id]['additional_arguments'][0] == 'running':  # if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
                        true_done = True
                        to_add = False
                        for node_with_memory in nodes_with_memory_found:
                            # this node_with_memory cannot resume.
                            # indicate as such.
                            nodes_with_memory_to_relevant_descendants_map[node_with_memory] = set()
            if to_add:
                # this is a valid resume point. tell the local root about it.
                local_root_to_relevant_list_map[node_to_local_root_map[node_id]].append(node_id)

    return (local_root_to_relevant_list_map,
            nodes_with_memory_to_relevant_descendants_map)


def create_node_to_descendants_map(nodes):
    '''
    return
    node_to_descendants_map.
    ---
    node_to_descendants_map ->
    this maps each node to the set of all of it's descendants.
    leaf nodes map to an empty set. a node is not it's own descendant
    ---
    method explanation
    go through all the nodes in order
    add a set() for each node
    go back up until we reach -1.
    for each stop along the way, add the current node
    '''
    node_to_descendants_map = {}
    for node_id in range(len(nodes)):
        node_to_descendants_map[node_id] = set()
        cur_id = nodes[node_id]['parent_id']
        while not cur_id == -1:
            node_to_descendants_map[cur_id].add(node_id)
            cur_id = nodes[cur_id]['parent_id']
    return node_to_descendants_map

# -----------------------------------------------------------------------------------------------------------------------
