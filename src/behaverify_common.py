
# arg_parser.add_argument('input_file')
# arg_parser.add_argument('--blackboard_input_file', default = None)
# arg_parser.add_argument('--module_input_file', default = None)
# arg_parser.add_argument('--specs_input_file', default = None)
# arg_parser.add_argument('--output_file', default = None)
# arg_parser.add_argument('--blackboard_output_file', default = None)
# arg_parser.add_argument('--module_output_file', default = None)
# arg_parser.add_argument('--overwrite', action = 'store_true')

# -----------------------------------------------------------------------------------------------------------------------

# def create_variable_template(name, mode, custom_value_range, min_value, max_value, initial_value, next_value, prefix = ''):
#     return {
#         'prefix' : prefix,
#         'name' : name,
#         'mode' : mode,
#         'custom_value_range' : custom_value_range,
#         'min_value' : min_value,
#         'max_value' : max_value,
#         'initial_value' : initial_value,
#         'next_value' : next_value
#     }


def create_variable_template(name, mode, custom_value_range, min_value, max_value, initial_value, next_value, prefix = '', keep_stage_0 = True):
    return {
        'prefix' : prefix,
        'name' : name,
        'mode' : mode,
        'custom_value_range' : custom_value_range,
        'min_value' : min_value,
        'max_value' : max_value,
        'initial_value' : initial_value,
        'next_value' : next_value,
        'keep_stage_0' : keep_stage_0
    }


def create_node_template(node_name, parent_name, category, node_type,
                         success, running, failure,
                         additional_arguments = None,
                         internal_status_module_name = None,
                         internal_status_module_code = None):
    return {
            'name' : node_name,
            'parent' : parent_name,
            'children' : [],
            'category' : category,
            'type' : node_type,
            'return_possibilities' : {
                'success' : success,
                'running' : running,
                'failure' : failure
            },
            'additional_arguments' : additional_arguments,
            'internal_status_module_name' : internal_status_module_name,
            'internal_status_module_code' : internal_status_module_code
        }


def create_node_name(base_name, node_names, modifier = 0):
    formatted_name = base_name + (('_' + str(modifier)) if modifier > 0 else '')
    return (create_node_name(base_name, node_names, modifier + 1)
            if formatted_name in node_names else (
                    formatted_name
                    )
            )


def get_root_node(nodes):
    return next(filter((lambda x : nodes[x]['parent'] is None), nodes))


def order_nodes(node_name, nodes):
    return ([node_name]
            + [node_name_ for list_of_names in
               [order_nodes(descendant_name, nodes)
                for descendant_name in nodes[node_name]['children']
                ]
               for node_name_ in list_of_names
               ]
            )


def map_node_name_to_number(nodes, nodes_in_order):
    return {nodes_in_order[i] : i for i in range(len(nodes_in_order))}


def create_node_to_local_root_map(nodes, root_node_name):
    """
    used to create a map from nodes to local root
    --
    arguments
    @ nodes -> a map (dictionary) from node_id to node information
    --
    return
    @ node_to_local_root_map -> a map (dictionary) from node id to the
      node id of the local root.
      @ local_root -> the local root of a node N
        is N if N is the root node or N's parent is parallel
        else
        a node M such that
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
    def local_root_map(nodes, node_name, local_root):
        # print(node_name + ' -> ' + local_root)
        return {node_name : (node_name
                            if (
                                    nodes[node_name]['parent'] is None
                                    or 'parallel' in nodes[nodes[node_name]['parent']]['type']
                            )
                            else local_root),
                **{desecendent_name : desecendent_value
                   for child_name in nodes[node_name]['children']
                   for desecendent_name, desecendent_value in local_root_map(nodes,
                                                                            child_name,
                                                                            (
                                                                                node_name
                                                                                if (
                                                                                        nodes[node_name]['parent'] is None
                                                                                        or 'parallel' in nodes[nodes[node_name]['parent']]['type']
                                                                                )
                                                                                else local_root
                                                                            )
                                                                            ).items()
                   }
                }
    return local_root_map(nodes, root_node_name, root_node_name)


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
    return (
        False if (node['category'] == 'composite' and 'with_memory' in node['type']) else (
            (node['additional_arguments'][1] == 'running') if node['type'] == 'X_is_Y' else (
                False if node['category'] == 'decorator' else (
                    node['return_possibilities']['running'] if node['category'] == 'leaf' else (
                        True
                    )
                )
            )
        )
    )


def create_node_to_descendants_map(nodes, node_name):
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
    # print(nodes[node_name]['children'])
    children_results = [create_node_to_descendants_map(nodes, child_name)
                        for child_name in nodes[node_name]['children']
                        ]
    return {node_name : {descendant_name
                        for child_result in children_results
                        for descendant_name in child_result
                        },
            **{descendant_name : descendant_value
               for child_result in children_results
               for descendant_name,  descendant_value in child_result.items()
               }
            }


def prune_nodes(nodes):
    '''
    used to remove unncessary nodes (composite nodes with one or less children, and nodes that cannot run)
    --
    arguments
    @ nodes := dictionary, s -> n
      s := name of a node, string
      n := dictionary containing node informaion, dictionary
    --
    return
    @ nodes := dictionary, s -> n
      s := name of a node, string
      n := dictionary containing node informaion, dictionary
    --
    effects
    none. purely functional.
    '''
    nodes = {node_name : {field :
                          ((list(filter(
                              (lambda x : (nodes[x]['return_possibilities']['success']
                                           or nodes[x]['return_possibilities']['failure']
                                           or nodes[x]['return_possibilities']['running'])),
                              nodes[node_name]['children'])))
                           if field == 'children' else (nodes[node_name][field]))
                          for field in nodes[node_name]}
             for node_name in filter((lambda x : (nodes[x]['return_possibilities']['success']
                                                  or nodes[x]['return_possibilities']['failure']
                                                  or nodes[x]['return_possibilities']['running'])),
                                     nodes)}
    # we've now removed all dead nodes.

    nodes = {node_name :
             (
                 nodes[node_name] if (nodes[node_name]['category'] != 'composite' or len(nodes[node_name]['children']) != 0) else (
                     {field :
                      (
                          'action' if field == 'type' else (
                              'leaf' if field == 'category' else (
                                  nodes[node_name][field]
                              )
                          )
                      )
                      for field in nodes[node_name]}
                 )
             )
             for node_name in nodes}

    # ok, now we've replaced all composite nodes with no children with the appropriate constants.

    def find_new_parent(nodes, node_name):
        return (None if nodes[node_name]['parent'] is None else (
            (find_new_parent(nodes, nodes[node_name]['parent'])) if (nodes[nodes[node_name]['parent']]['category'] == 'composite' and len(nodes[nodes[node_name]['parent']]['children']) < 2) else (
                nodes[node_name]['parent'])))

    def find_new_child(nodes, node_name):
        return (node_name if (nodes[node_name]['category'] != 'composite' or len(nodes[node_name]['children']) > 1) else (find_new_child(nodes, nodes[node_name]['children'][0])))

    nodes = {node_name : {field :
                          (
                              (
                                  [
                                      (child_name if (nodes[child_name]['category'] != 'composite' or len(nodes[child_name]['children']) > 1) else (
                                          find_new_child(nodes, child_name)
                                          )
                                       )
                                      for child_name in nodes[node_name]['children']
                                  ]
                              )
                              if field == 'children' else (
                                      (find_new_parent(nodes, node_name)) if field == 'parent' else (
                                          nodes[node_name][field]
                                      )
                              )
                          )
                          for field in nodes[node_name]}
             for node_name in filter((lambda x : (nodes[x]['category'] != 'composite' or len(nodes[x]['children']) > 1)),
                                     nodes)}
    # we've now removed all composite nodes that had less than 2 children.
    return nodes


def indent(indent_level):
    return (' '*(4*indent_level))


def refine_return_types(nodes, node_name):
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
    node = nodes[node_name]

    cannot_run = False

    # first we are going to check if the node cannot run.
    # the node cannot run if it's parent is a selector/sequence
    # and it's left sibling cannot return the relevant type
    if node['parent'] in nodes:
        # not the root
        parent = nodes[node['parent']]
        if (not parent['return_possibilities']['success'] and not parent['return_possibilities']['running'] and not parent['return_possibilities']['failure']):
            node['return_possibilities'] = {
                'success' : False,
                'running' : False,
                'failure' : False
            }
            cannot_run = True
            print(node['name'] + ' : my parents failed me')
        elif parent['category'] == 'composite':
            # we don't care about decorators
            left_sibling_index = parent['children'].index(node_name) - 1
            if left_sibling_index >= 0:
                # if sibling_index is >= 0, then we have a left sibling
                # that left sibling might prevent us from running.
                left_sibling_name = parent['children'][left_sibling_index]
                left_sibling = nodes[left_sibling_name]
                if 'selector' in parent['type']:
                    if not left_sibling['return_possibilities']['failure']:
                        node['return_possibilities'] = {
                            'success' : False,
                            'running' : False,
                            'failure' : False}
                        cannot_run = True
                        print(node['name'] + ' : SIBLING = ' + left_sibling_name)
                        # print(left_sibling)
                elif 'sequence' in parent['type']:
                    if not left_sibling['return_possibilities']['success']:
                        node['return_possibilities'] = {
                            'success' : False,
                            'running' : False,
                            'failure' : False}
                        cannot_run = True
                        print(node['name'] + ' : SIBLING = ' + left_sibling_name)

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
            for child_name in node['children']:
                refine_return_types(nodes, child_name)
                can_return_success = can_return_success or nodes[child_name]['return_possibilities']['success']
                can_return_running = can_return_running or nodes[child_name]['return_possibilities']['running']
                can_return_failure = can_return_failure and nodes[child_name]['return_possibilities']['failure']
            node['return_possibilities'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        elif 'sequence' in node['type']:
            can_return_success = True
            can_return_failure = False
            can_return_running = False
            for child_name in node['children']:
                refine_return_types(nodes, child_name)
                can_return_success = can_return_success and nodes[child_name]['return_possibilities']['success']
                can_return_running = can_return_running or nodes[child_name]['return_possibilities']['running']
                can_return_failure = can_return_failure or nodes[child_name]['return_possibilities']['failure']
            node['return_possibilities'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        elif 'success_on_all' in node['type']:
            can_return_success = True
            can_return_failure = False
            can_return_running = False
            for child_name in node['children']:
                refine_return_types(nodes, child_name)
                can_return_success = can_return_success and nodes[child_name]['return_possibilities']['success']
                can_return_running = can_return_running or nodes[child_name]['return_possibilities']['running']
                can_return_failure = can_return_failure or nodes[child_name]['return_possibilities']['failure']
            node['return_possibilities'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        elif 'success_on_one' in node['type']:
            can_return_success = False
            can_return_failure = False
            can_return_running = True
            for child_name in node['children']:
                refine_return_types(nodes, child_name)
                can_return_success = can_return_success or nodes[child_name]['return_possibilities']['success']
                can_return_running = can_return_running and nodes[child_name]['return_possibilities']['running']
                can_return_failure = can_return_failure or nodes[child_name]['return_possibilities']['failure']
            node['return_possibilities'] = {
                'success' : can_return_success,
                'running' : can_return_running,
                'failure' : can_return_failure}
            return
        else:
            print('unknown composite type!!! ', node['type'])
            return
    elif node['category'] == 'decorator':
        child_name = node['children'][0]
        child = nodes[child_name]
        refine_return_types(nodes, child_name)
        if node['type'] == 'X_is_Y':
            node['return_possibilities'][node['additional_arguments'][1]] = (child['return_possibilities'][node['additional_arguments'][0]]
                                                                             or child['return_possibilities'][node['additional_arguments'][1]])
            for return_val in ('success', 'failure', 'running'):
                if return_val not in node['additional_arguments']:
                    node['return_possibilities'][return_val] = child['return_possibilities'][return_val]
        elif node['type'] == 'inverter':
            node['return_possibilities'] = {
                'success' : child['return_possibilities']['failure'],
                'failure' : child['return_possibilities']['success'],
                'running' : child['return_possibilities']['running']}
        return
    else:
        print('unknown node category!!!', node['category'])
    return


def refine_invalid(nodes, node_name):
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
    node = nodes[node_name]
    if node['parent'] is None:
        # root is never invalid.
        node['can_be_invalid'] = False
        node['always_invalid'] = False
        for child_name in node['children']:
            refine_invalid(nodes, child_name)
        return
    parent = nodes[node['parent']]
    if parent['always_invalid']:
        node['can_be_invalid'] = True
        node['always_invalid'] = True
    # at this point, parent is sometimes valid
    elif parent['category'] == 'composite' and 'unsynchronized' in parent['type']:
        node['can_be_invalid'] = parent['can_be_invalid']
        node['always_invalid'] = False
        # parallel unsynchronized always runs all children
    elif parent['category'] == 'composite' and 'synchronized' in parent['type']:
        if node['return_possibilities']['success'] is False:
            # this node cannot return success.
            # it will never be skipped.
            # therefore, it can never be invalid (unless the parent is invalid).
            node['can_be_invalid'] = parent['can_be_invalid']
        else:
            # this node can return success, so it can be
            # skipped
            node['can_be_invalid'] = True
        node['always_invalid'] = False
    elif parent['category'] == 'composite' and 'selector' in parent['type']:
        done = False
        done_always = False
        for sibling_index in range(0, parent['children'].index(node_name)):
            sibling_id = parent['children'][sibling_index]
            if nodes[sibling_id]['return_possibilities']['success'] \
               or nodes[sibling_id]['return_possibilities']['running']:
                # if a left neighbor can cause the parent to return, then this
                # node can be invalid
                done = True
                node['can_be_invalid'] = True
                if not nodes[sibling_id]['return_possibilities']['failure']:
                    # a node to the left of this always returns running or success.
                    # we cannot possibly reach this node.
                    done_always = True
                    # print('the source???? ' + node_name + ' : ' + str(sibling_id))
                    break
        node['always_invalid'] = done_always
        if not done:
            # we weren't done.
            if 'with_memory' in parent['type']:
                # check if a right neighbor can cause us to be skipped.
                for sibling_index in range(parent['children'].index(node_name) + 1,
                                           len(parent['children'])):
                    sibling_id = parent['children'][sibling_index]
                    if nodes[sibling_id]['return_possibilities']['running']:
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
        for sibling_index in range(0, parent['children'].index(node_name)):
            sibling_id = parent['children'][sibling_index]
            if nodes[sibling_id]['return_possibilities']['failure'] \
               or nodes[sibling_id]['return_possibilities']['running']:
                # if a left neighbor can cause the parent to return, then this
                # node can be invalid
                done = True
                node['can_be_invalid'] = True
                if not nodes[sibling_id]['return_possibilities']['success']:
                    # a node to the left of this always returns running or failure.
                    # we cannot possibly reach this node.
                    done_always = True
                    # print('the source2????')
                    break
        node['always_invalid'] = done_always
        if not done:
            # we weren't done.
            if 'with_memory' in parent['type']:
                # check if a right neighbor can cause us to be skipped.
                for sibling_index in range(parent['children'].index(node_name) + 1,
                                           len(parent['children'])):
                    sibling_id = parent['children'][sibling_index]
                    if nodes[sibling_id]['return_possibilities']['running']:
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
    for child_name in node['children']:
        refine_invalid(nodes, child_name)
    return


def create_local_root_to_relevant_list_map(nodes, node_to_local_root_map, nodes_in_order):
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

    # running_map = map_can_return_running(nodes, nodes_in_order[0])

    local_root_to_relevant_list_map = {}
    # a map from local_root to the list of relevant things
    # to track in terms of running
    nodes_with_memory_to_relevant_descendants_map = {}
    # a map from each node_with_memory to the set of relevant descendants
    # print(node_to_local_root_map)
    for node_name in nodes_in_order:
        # print('------------------------------------------')
        # print(node_name)
        if node_name == node_to_local_root_map[node_name]:
            # this is a local_root
            if nodes[node_name]['parent'] is None:
                # this local root is THE root, and therefore it can't be skipped
                # so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_name] = []
            elif ('parallel' in nodes[nodes[node_name]['parent']]['type']
                  and '_synchronized' in nodes[nodes[node_name]['parent']]['type']):
                # the local root's parent is a parallel_synch node
                # so we have to track if it's skippable
                local_root_to_relevant_list_map[node_name] = [-2]
            else:
                # the local root's parent is not a parallel_synch node
                # so we don't have to track if it's skippable
                local_root_to_relevant_list_map[node_name] = []
        elif nodes[node_name]['return_possibilities']['running'] and can_create_running(nodes[node_name]):
            cur_name = node_name
            first_child = True
            done = False
            true_done = False
            end_target = nodes[node_to_local_root_map[node_name]]['parent']
            # we end at the parent of the local root.
            nodes_with_memory_found = []
            to_add = False
            while not done:
                previous_name = cur_name
                cur_name = nodes[cur_name]['parent']  # get the parent
                if cur_name == end_target:
                    done = True
                    true_done = True
                elif nodes[cur_name]['category'] == 'decorator':
                    if nodes[cur_name]['type'] == "X_is_Y" and nodes[cur_name]['additional_arguments'][0] == 'running':
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
                elif nodes[cur_name]['category'] == 'composite':
                    if ('without_memory' in nodes[cur_name]['type'] or 'parallel' in nodes[cur_name]['type']):
                        done = True
                        # nothing above us will care.
                        # without memory collapses everything.
                        # either this location will be tracked, or nothing will be tracked.
                    elif 'with_memory' in nodes[cur_name]['type']:
                        nodes_with_memory_found.append(cur_name)
                        if cur_name not in nodes_with_memory_to_relevant_descendants_map:
                            nodes_with_memory_to_relevant_descendants_map[cur_name] = set()
                        if nodes[cur_name]['children'][0] == previous_name:
                            # this is the first child. change nothing
                            pass
                        else:
                            # this was not the first child. mark this down
                            first_child = False
                            to_add = True
                        if not first_child:
                            # if at some point we encountered a not first child,
                            # then this node is relevant.
                            nodes_with_memory_to_relevant_descendants_map[cur_name].add(node_name)
                    else:
                        print(nodes[node_name]['type'])
                        print('the above node',
                              'is a composite node of unknown type',
                              'It is not parallel,',
                              'nor does it indicate memory or lack of memory.')
            # make sure there's not a decorator above the end point
            # that invalidates our need to track running.
            while not true_done:
                previous_name = cur_name
                cur_name = nodes[cur_name]['parent']
                if cur_name == end_target:
                    true_done = True
                elif nodes[cur_name]['category'] == 'decorator':
                    if nodes[cur_name]['type'] == "X_is_Y" and nodes[cur_name]['additional_arguments'][0] == 'running':  # if we encounter a decorator that undoes running, we no longer care. TODO: update so it hits all decorators that can do this.
                        true_done = True
                        to_add = False
                        for node_with_memory in nodes_with_memory_found:
                            # this node_with_memory cannot resume.
                            # indicate as such.
                            nodes_with_memory_to_relevant_descendants_map[node_with_memory] = set()
            if to_add:
                # this is a valid resume point. tell the local root about it.
                local_root_to_relevant_list_map[node_to_local_root_map[node_name]].append(node_name)

    return (local_root_to_relevant_list_map,
            nodes_with_memory_to_relevant_descendants_map)

# -----------------------------------------------------------------------------------------------------------------------
# depricated! DO NOT USE.


# def map_can_return_running(nodes, node_name):
#     """
#     used to create a map from node id to booleans,
#     indicating if a node can return running.
#     Process is done recursively from whichever node is passed.
#     --
#     arguments
#     @ nodes -> a map (dictionary) from node_id to node information
#     @ node_id -> the id of the node we are currently considering
#     --
#     return
#     @ running_map -> a map (dictionary) from node union descendents
#       to booleans. nodes and descendents are represented via node_id
#       each node id maps to True if the node can return running
#       and False otherwise
#     --
#     effects and methods
#     the node category and type are considered. each child is ran.
#     note that in some cases advanced techniques are considered.
#     for instance, a selector can only return running if one of it's children
#     can return running.
#     """
#     # node = nodes[node_name]
#     # return (
#     #     {node_name : node['return_possibilities']['running']} if node['category'] == 'leaf' else (
#     #         {node_name : node['
#     node = nodes[node_name]
#     if node['category'] == 'leaf':
#         return {node_name : node['return_possibilities']['running']}
#     elif node['category'] == 'decorator':
#         running_map = map_can_return_running(nodes, node['children'][0])
#         if node['type'] == 'X_is_Y':
#             if node['additional_arguments'][0] == 'running':
#                 running_map[node_name] = False
#             elif node['additional_arguments'][1] == 'running':
#                 running_map[node_name] = (nodes[node['children'][0]]['return_possibilities']['running']
#                                           or nodes[node['children'][0]]['return_possibilities'][node['additional_arguments'][0]])
#             else:
#                 running_map[node_name] = running_map[node['children'][0]]
#         else:
#             running_map[node_name] = running_map[node['children'][0]]
#         return running_map
#     else:
#         # it's a parallel, selector, or sequence node
#         running = False
#         running_map = {}
#         for child_name in node['children']:
#             running_map.update(map_can_return_running(nodes, child_name))
#             running = running or running_map[child_name]
#         if len(node['children']) == 0:
#             # this is an edge case check.
#             if 'parallel' in node['type']:
#                 running_map[node_name] = True
#                 return True
#             else:
#                 running_map[node_name] = False
#                 return False
#         running_map[node_name] = running
#         return running_map
