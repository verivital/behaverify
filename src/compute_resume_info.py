
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
        is a parallel node and there is no P between N and M
        such that P's parent is a parallel node.
    --
    effects and method
    begin by marking the root as the local root of the root.
    for each other node N, check if N's parent is a parallel node
    if it is, N is a local root, and N's local root is N
    otherwise, N's local root is N's parent's local root.
    """
    node_to_local_root_map = {0 : 0}
    # a map from node_id to the local root for that node_id
    for node_id in range(1, len(nodes)):
        # start at 1 to avoid the root, which was covered above.
        if 'parallel' in nodes[nodes[node_id]['parent_id']]['type']:
            # if the parent is a parallel node, then this it the local root
            node_to_local_root_map[node_id] = node_id
        else:
            # otherwise, the local root is w/e my parent's local root is
            node_to_local_root_map[node_id] = node_to_local_root_map[nodes[node_id]['parent_id']]
    return node_to_local_root_map


def can_create_running(node):
    """
    used to determine if a given node can 'create' a running result.
    Note that this is not the same as RETURNING running. For instance,
    a decorator might return running solely because it's child returned running.
    The child created running in this case, not the decorator
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    --
    return
    @ Boolean. True indicates the node in question can create running.
      False indicates it cannot.
    --
    effects and method
    the node type is checked. based on the node type, we return a value.
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
        return node['return_arguments']['running']
    else:
        # without memory and parallel can, everything else covered above
        return True


def map_can_return_running(nodes, node_id):
    """
    used to create a map from node id to booleans,
    indicating if a node can return running.
    Process is done recursively from whichever node is passed.
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    @ node_id -> the id of the node we are currently considering
    --
    return
    @ running_map -> a map (dictionary) from node union descendents
      to booleans. nodes and descendents are represented via node_id
      each node id maps to True if the node can return running
      and False otherwise
    --
    effects and methods
    the node category and type are considered. each child is ran.
    note that in some cases advanced techniques are considered.
    for instance, a selector can only return running if one of it's children
    can return running.
    """
    node = nodes[node_id]
    if node['category'] == 'leaf':
        return {node_id : node['return_arguments']['running']}
    elif node['category'] == 'decorator':
        running_map = map_can_return_running(nodes, node['children'][0])
        if node['type'] == 'X_is_Y':
            if node['additional_arguments'][0] == 'running':
                running_map[node_id] = False
            elif node['additional_arguments'][1] == 'running':
                running_map[node_id] = True
            else:
                running_map[node_id] = running_map[node['children'][0]]
        else:
            running_map[node_id] = running_map[node['children'][0]]
        return running_map
    else:
        # it's a parallel, selector, or sequence node
        running = False
        running_map = {}
        for child in node['children']:
            running_map.update(map_can_return_running(nodes, child))
            running = running or running_map[child]
        if len(node['children']) == 0:
            # this is an edge case check.
            if 'parallel' in node['type']:
                running_map[node_id] = True
                return True
            else:
                running_map[node_id] = False
                return False
        running_map[node_id] = running
        return running_map


def refine_return_types(nodes, node_id):
    """
    used to refine the possible return types of each node. This
    should be called BEFORE refine_invalid
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    @ node_id -> the id of the node we are currently considering
    --
    return
    NONE
    --
    effects and methods
    From the node indicated by node_id, we recursively consider
    all descendants. Based on what the children can return,
    the nodes have their return types updated.
    """
    # TODO: add a check to see if a node can even be run.
    node = nodes[node_id]

    cannot_run = False

    # first we are going to check if the node cannot run.
    # the node cannot run if it's parent is a selector/sequence
    # and it's left sibling cannot return the relevant type
    if node['parent_id'] in nodes:
        # not the root
        parent = nodes[node['parent_id']]
        if parent['category'] == 'composite':
            # we don't care about decorators
            left_sibling_index = parent['children'].index(node_id) - 1
            if left_sibling_index >= 0:
                # if sibling_index is >= 0, then we have a left sibling
                # that left sibling might prevent us from running.
                left_sibling_id = parent['children'][left_sibling_index]
                left_sibling = nodes[left_sibling_id]
                if 'selector' in parent['type']:
                    if not left_sibling['return_arguments']['failure']:
                        node['return_arguments'] = {
                            'success' : False,
                            'running' : False,
                            'failure' : False}
                        cannot_run = True
                elif 'sequence' in parent['type']:
                    if not left_sibling['return_arguments']['success']:
                        node['return_arguments'] = {
                            'success' : False,
                            'running' : False,
                            'failure' : False}
                        cannot_run = True

    if cannot_run:
        for child_id in node['children']:
            refine_return_types(nodes, child_id)
        return
    elif node['category'] == 'leaf':
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
                    node['return_arguments'][node['additional_arguments'][1]] = (
                        node['return_arguments'][node['additional_arguments'][1]]
                        or child['return_arguments'][return_val]
                    )
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
    """
    used to refine the possiblity of being invalid. This should be
    called AFTER refine_return_types
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    @ node_id -> the id of the node we are currently considering
    @ is_root -> true if node_id is the root,  False otherwise.
    --
    return
    NONE
    --
    effects and methods
    From the node indicated by node_id, we recursively consider
    all descendants. Based on what the children can return,
    the nodes have their invalidity updated
    """
    node = nodes[node_id]
    if is_root:
        # root is never invalid.
        node['can_be_invalid'] = False
        node['always_invalid'] = False
        for child_id in node['children']:
            refine_invalid(nodes, child_id, False)
        return
    parent = nodes[node['parent_id']]
    if parent['always_invalid']:
        node['can_be_invalid'] = True
        node['always_invalid'] = True
    # at this point, parent is sometimes valid
    elif parent['category'] == 'composite' and 'unsynchronized' in parent['type']:
        node['can_be_invalid'] = parent['can_be_invalid']
        node['always_invalid'] = False
        # parallel unsynchronized always runs all children
    elif parent['category'] == 'composite' and 'synchronized' in parent['type']:
        if node['return_arguments']['success'] is False:
            # this node cannot return success.
            # it will never be skipped.
            # therefore, it can never be invalid.
            node['can_be_invalid'] = parent['can_be_invalid']
        else:
            # this node can return success, so it can be
            # skipped
            node['can_be_invalid'] = True
        node['always_invalid'] = False
    elif parent['category'] == 'composite' and 'selector' in parent['type']:
        done = False
        done_always = False
        for sibling_index in range(0, parent['children'].index(node_id)):
            sibling_id = parent['children'][sibling_index]
            if nodes[sibling_id]['return_arguments']['success'] \
               or nodes[sibling_id]['return_arguments']['running']:
                # if a left neighbor can cause the parent to return, then this
                # node can be invalid
                done = True
                node['can_be_invalid'] = True
                if not nodes[sibling_id]['return_arguments']['failure']:
                    # a node to the left of this always returns running or success.
                    # we cannot possibly reach this node.
                    done_always = True
                    print('the source???? ' + str(node_id) + ' : ' + str(sibling_id))
                    break
        node['always_invalid'] = done_always
        if not done:
            # we weren't done.
            if 'with_memory' in parent['type']:
                # check if a right neighbor can cause us to be skipped.
                for sibling_index in range(parent['children'].index(node_id) + 1,
                                           len(parent['children'])):
                    sibling_id = parent['children'][sibling_index]
                    if nodes[sibling_id]['return_arguments']['running']:
                        # a sibling to the right can return running
                        # that means this can be invalid
                        done = True
                        node['can_be_invalid'] = True
                        break
            if not done:
                node['can_be_invalid'] = parent['can_be_invalid']
    elif parent['category'] == 'composite' and 'sequence' in parent['type']:
        done = False
        done_always = False
        for sibling_index in range(0, parent['children'].index(node_id)):
            sibling_id = parent['children'][sibling_index]
            if nodes[sibling_id]['return_arguments']['failure'] \
               or nodes[sibling_id]['return_arguments']['running']:
                # if a left neighbor can cause the parent to return, then this
                # node can be invalid
                done = True
                node['can_be_invalid'] = True
                if not nodes[sibling_id]['return_arguments']['success']:
                    # a node to the left of this always returns running or failure.
                    # we cannot possibly reach this node.
                    done_always = True
                    print('the source2????')
                    break
        node['always_invalid'] = done_always
        if not done:
            # we weren't done.
            if 'with_memory' in parent['type']:
                # check if a right neighbor can cause us to be skipped.
                for sibling_index in range(parent['children'].index(node_id) + 1,
                                           len(parent['children'])):
                    sibling_id = parent['children'][sibling_index]
                    if nodes[sibling_id]['return_arguments']['running']:
                        # a sibling to the right can return running
                        # that means this can be invalid
                        done = True
                        node['can_be_invalid'] = True
                        break
            if not done:
                node['can_be_invalid'] = parent['can_be_invalid']
    else:
        # assume decorator nodes always run their children.
        node['can_be_invalid'] = parent['can_be_invalid']
        node['always_invalid'] = False
    for child_id in node['children']:
        refine_invalid(nodes, child_id, False)
    return


def create_local_root_to_relevant_list_map(nodes, node_to_local_root_map):
    """
    creates a map from a local root to a lit of relevant nodes
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    @ node_to_local_root_map -> a map (dictionary) from node_id to the local root
      @ local_root -> the local root of a node N is a node M such that
        M is an ancestor of N and M is the root node or M's parent
        is a parallel node and there is no P between N and M
        such that P's parent is a parallel node.
    --
    returns
    @ local_root_to_relevant_list_map -> a map (dictionary) from
      local roots to a list of nodes that can be resumed from
    @ nodes_with_memory_to_relevant_descendants_map -> a map (dictionary)
      from node id of nodes with memory to nodes that can be resumed from
    --
    effects and methods
    for each node N, if it's a local root, do basically nothing.
    if it's NOT a local root, begin a track back up the tree.
    based on what we encounter, we can either discount the thing as being
    relevant, or we reach the local root. If we reach the local root,
    then we started from a relevant point.
    """

    running_map = map_can_return_running(nodes, 0)

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
    """
    used to create a map from nodes to their descendants
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    --
    return
    @ node_to_descendants_map -> a map (dictionary) from node_id to
      the descendents of the node (not just children). A node is NOT
      it's own descendant.
    --
    effects and methods
    For each node N, traverse the tree until we pass the root.
    For each visited node M, tell M that N is a descendant.
    """
    node_to_descendants_map = {}
    for node_id in range(len(nodes)):
        node_to_descendants_map[node_id] = set()
        cur_id = nodes[node_id]['parent_id']
        while not cur_id == -1:
            node_to_descendants_map[cur_id].add(node_id)
            cur_id = nodes[cur_id]['parent_id']
    return node_to_descendants_map

# -----------------------------------------------------------------------------------------------------------------------
