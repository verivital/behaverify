
# arg_parser.add_argument('input_file')
# arg_parser.add_argument('--blackboard_input_file', default = None)
# arg_parser.add_argument('--module_input_file', default = None)
# arg_parser.add_argument('--specs_input_file', default = None)
# arg_parser.add_argument('--output_file', default = None)
# arg_parser.add_argument('--blackboard_output_file', default = None)
# arg_parser.add_argument('--module_output_file', default = None)
# arg_parser.add_argument('--overwrite', action = 'store_true')

# -----------------------------------------------------------------------------------------------------------------------
import argparse
import os
import re
# ----------------------------------------------------------------------------------------------------------------
# serene custom imports
import node_creator
from behaverify_common import (tab_indent,
                               get_root_node,
                               refine_return_types,
                               refine_invalid,
                               prune_nodes, order_nodes,
                               map_node_name_to_number,
                               create_node_to_local_root_map,
                               create_local_root_to_relevant_list_map,
                               create_node_to_descendants_map,
                               format_node_type)
# -----------------------------------------------------------------------------------------------------------------------

LOCAL_ROOT_TREE_STRING = 'resume_from_here_in_subtree__'
CHILD_TRACK_STRING = 'child_index_to_resume_from__'
# PARALLEL_SKIP_STRING = 'parallel_skip__'
NEXT_CHILD_STRING = 'next_child__'
STATUS_STRING = 'status__'
RUNNING_TRACE_STRING = 'trace_running_source__'
PARALLEL_STATUS_STRING = 'parallel_status_depth__'

STATUS_FUNCTIONS = {
    'composite_parallel_success_on_all_without_memory' : node_creator.create_composite_parallel_success_on_all_without_memory,
    'composite_parallel_success_on_all_with_memory' : node_creator.create_composite_parallel_success_on_all_with_memory,
    'composite_parallel_success_on_one_without_memory' : node_creator.create_composite_parallel_success_on_one_without_memory,
    'composite_parallel_success_on_one_with_memory' : node_creator.create_composite_parallel_success_on_one_with_memory,
    'composite_selector_with_memory' : node_creator.create_composite_selector_with_memory,
    'composite_selector_without_memory' : node_creator.create_composite_selector_without_memory,
    'composite_sequence_with_memory' : node_creator.create_composite_sequence_with_memory,
    'composite_sequence_without_memory' : node_creator.create_composite_sequence_without_memory,
    'decorator_X_is_Y' : node_creator.create_decorator_X_is_Y,
    'decorator_inverter' : node_creator.create_decorator_inverter
}


def create_previous_status():
    define_string = ''
    var_string = (tab_indent(2) + 'previous_status : {success, running, failure, invalid};' + os.linesep)
    init_string = tab_indent(2) + 'init(previous_status) := invalid;' + os.linesep
    next_string = (tab_indent(2) + 'next(previous_status) := current_status;' + os.linesep)
    return (define_string, var_string, init_string, next_string)


def create_current_status(nodes):
    def current_status_node(node):
        return (
            node_creator.create_leaf(node)
            if node['category'] == 'leaf'
            else STATUS_FUNCTIONS[format_node_type(node, False)](node)
        )
    define_string = ''
    var_string = (tab_indent(2) + 'current_status : {success, running, failure, invalid};' + os.linesep)
    init_string = ''
    next_string = (tab_indent(2) + 'current_status :=' + os.linesep
                   + tab_indent(3) + 'case' + os.linesep
                   + ''.join(map(current_status_node, nodes.values()))
                   + tab_indent(4) + 'TRUE : invalid;' + os.linesep
                   + tab_indent(3) + 'esac;' + os.linesep
                   )
    return (define_string, var_string, init_string, next_string)


def create_previous_node(nodes):
    define_string = ''
    var_string = tab_indent(2) + 'previous_node : -1..' + str(len(nodes)) + ';' + os.linesep
    init_string = tab_indent(2) + 'init(previous_node) := -1;' + os.linesep
    next_string = (tab_indent(2) + 'next(previous_node) := active_node;' + os.linesep)
    return (define_string, var_string, init_string, next_string)


def create_active_node(nodes, root_node_name, tick_condition):
    define_string = ''
    var_string = tab_indent(2) + 'active_node : -1..' + str(len(nodes)) + ';' + os.linesep
    init_string = tab_indent(2) + 'init(active_node) := -1;' + os.linesep
    next_string = (
        tab_indent(2) + 'next(active_node) :=' + os.linesep
        + tab_indent(3) + 'case' + os.linesep
        + tab_indent(4) + 'active_node = -1 & ' + tick_condition + ' : node_names.' + root_node_name + ';' + os.linesep
        + tab_indent(4) + 'active_node = -1 & !(' + tick_condition + ') : -1;' + os.linesep
        + ''.join(
            [
                (
                    tab_indent(4) + '(active_node = node_names.' + node['name'] + ') & (current_status != invalid) : ' + ('-1' if node['parent'] is None else ('node_names.' + node['parent'])) + ';' + os.linesep
                    + ((tab_indent(4) + '(active_node = node_names.' + node['name'] + ') & (current_status = invalid) : ' + NEXT_CHILD_STRING + node['name'] + ';' + os.linesep) if node['category'] != 'leaf' else '')
                )
                for node in nodes.values()
            ]
        )
        + tab_indent(4) + 'TRUE : active_node;' + os.linesep
        + tab_indent(3) + 'esac;' + os.linesep
    )
    return (define_string, var_string, init_string, next_string)


def has_memory(node):
    return (
        False if node['category'] != 'composite' else (
            False if 'without_memory' in node['type'] else (
                False if 'success_on_one' in node['type'] else (
                    True
                )
            )
        )
    )


def create_next_child(nodes):
    define_string = (
        ''.join(
            [
                (
                    tab_indent(2) + NEXT_CHILD_STRING + node['name'] + ' := ' + os.linesep
                    + tab_indent(3) + 'case' + os.linesep
                    + ''.join(
                        [
                            (
                                tab_indent(4) + '(previous_node < node_names.' + node['children'][child_index] + ')'
                                + (
                                    '' if not has_memory(node) else (
                                        ('& !(' + LOCAL_ROOT_TREE_STRING + node['children'][child_index] + ' = -2)') if 'parallel' in node['type'] else (
                                            ('& (' + CHILD_TRACK_STRING + node['name'] + ' <= ' + str(child_index) + ')')
                                        )
                                    )
                                )
                                + ' : node_names.' + node['children'][child_index] + ';' + os.linesep
                            )
                            for child_index in range(len(node['children']))
                        ]
                    )
                    + tab_indent(4) + 'TRUE : -1;' + os.linesep
                    + tab_indent(3) + 'esac;' + os.linesep
                ) if len(node['children']) >= 2 else (
                    (tab_indent(2) + NEXT_CHILD_STRING + node['name']
                     + ' := node_names.' + node['children'][0] + ';' + os.linesep)
                    if len(node['children']) == 1 else (
                            (tab_indent(2) + NEXT_CHILD_STRING + node['name']
                             + ' := ' + ('-1' if node['parent'] is None else ('node_names.' + node['parent'])) + ';' + os.linesep)
                    )
                )
                for node in nodes.values() if node['category'] != 'leaf'
            ]
        )
    )
    var_string = ''
    init_string = ''
    next_string = ''
    return (define_string, var_string, init_string, next_string)


def calculate_parallel_depth(nodes, node):
    return (
        0 if node['parent'] is None else (
            (calculate_parallel_depth(nodes, nodes[node['parent']]) + 1) if 'parallel' in nodes[node['parent']]['type'] else (
                calculate_parallel_depth(nodes, nodes[node['parent']])
            )
        )
    )


def create_parallel_depth_map(nodes):
    return {node['name'] : calculate_parallel_depth(nodes, node) for node in nodes.values() if 'parallel' in node['type']}


def create_inverse_depth_map(depth_map):
    return {depth : [parallel for parallel in depth_map if depth_map[parallel] == depth] for depth in depth_map.values()}


def add_depth(nodes, depth_map):
    for node_name in nodes:
        if 'parallel' in nodes[node_name]['type']:
            nodes[node_name]['depth'] = depth_map[node_name]


def create_parallel_status(nodes, depth_map, inverse_map):
    define_string = ''
    depth_list = list(set(depth_map.values()))
    var_string = ''.join(
        [
            (tab_indent(2) + PARALLEL_STATUS_STRING + str(depth) + ' : {success, running, failure};' + os.linesep)
            for depth in depth_list
        ]
    )
    init_string = ''.join(
        [
            (tab_indent(2) + 'init(' + PARALLEL_STATUS_STRING + str(depth) + ') := failure;' + os.linesep)
            for depth in depth_list
        ]
    )
    next_string = ''.join(
        [
            (tab_indent(2) + 'next(' + PARALLEL_STATUS_STRING + str(depth) + ') := ' + os.linesep
             + tab_indent(3) + 'case' + os.linesep
             + tab_indent(4) + 'next(active_node) = -1 : failure;' + os.linesep
             + ''.join(
                 [
                     (
                         (
                             (tab_indent(4) + '(next(active_node) = node_names.' + node_name + ') & (current_status = invalid) : success;' + os.linesep)
                             if 'success_on_all' in nodes[node_name]['type'] else
                             (tab_indent(4) + '(next(active_node) = node_names.' + node_name + ') & (current_status = invalid) : running;' + os.linesep))
                         + tab_indent(4) + '(next(active_node) = node_names.' + node_name + ') & (current_status = failure) : failure;' + os.linesep
                         + (
                             (tab_indent(4) + '(next(active_node) = node_names.' + node_name + ') & (current_status = running) : running;' + os.linesep)
                             if 'success_on_all' in nodes[node_name]['type'] else
                             (tab_indent(4) + '(next(active_node) = node_names.' + node_name + ') & (current_status = success) : success;' + os.linesep))
                     )
                     for node_name in inverse_map[depth]
                 ]
             )
             + tab_indent(4) + 'TRUE : ' + PARALLEL_STATUS_STRING + str(depth) + ';' + os.linesep
             + tab_indent(3) + 'esac;' + os.linesep
             )
            for depth in inverse_map
        ]
    )
    return (define_string, var_string, init_string, next_string)


def create_resume_structure(nodes, local_root_to_relevant_list_map, node_name_to_number):
    '''
    responsible for creating the resume structure
    --
    arguments
    @ nodes := dictionary, s -> n
      s := name of a node, string
      n := dictionary containing node informaion, dictionary
    @ local_root_to_relevant_list_map := dictionary, s -> l
      s := name of a local root, string
        local root := a node n such that n is the root or the parent of n is parallel
      l := nodes which can be resumed from, list
    --
    return
    @ define_string := a string with defintions
    @ init_string := a string with initializations
    @ next_string := a string with next conditions
    @ var_string := a string with variable declarations
    --
    effects
    purely functional from a black box perspective
    '''
    # things to still implement: new resume structure

    # each local root tracks it's possible resume locations. unchanged from previous versions
    # if anywhere upstream returns success/failure, indicate no resume
    # if local root returns failure, indicate no resume
    # if local root returns success, indicate SKIP or NO RESUME, depending on if parent it parallel_synch
    # if local root returns running, track running based on macros from children.

    # note here that we might need two propagations
    # propagation 1 -> resume_child_ID is what we currently have built
    # propagation 2 -> running_child_ID......wait what do we use this for? oh right. cuz we don't have active node? no.....we can just list through all the options? well. propagation might be cleaner?

    # well, we're gonna try it

    # so, resume_from_node_LOCAL_ROOT tracks the actual value that we need to resume from.

    var_resume_from_node_string = ''  # this is a variable that actually stores what running state we're in
    init_resume_from_node_string = ''
    next_resume_from_node_string = ''
    var_define_status_string = ''  # this is for storing the define versions that are constants.
    # define_trace_running_source = ''  # this is storing for the propagation mechanism. rename everything later lmao.

    for local_root_name in local_root_to_relevant_list_map:
        local_root_id_str = str(node_name_to_number[local_root_name])
        relevant_list = local_root_to_relevant_list_map[local_root_name]
        if len(relevant_list) == 0:
            # there's nothing to resume from. if we have a sequence node, then it apparently only had 0 or 1 children, and we don't need any special resume for it.
            var_define_status_string += tab_indent(2) + LOCAL_ROOT_TREE_STRING + local_root_name + ' := -3;' + os.linesep
            continue
        # var_resume_from_node_string += '\t\t' + LOCAL_ROOT_TREE_STRING + '' + local_root_name + ' : {' + local_root_id_str + ', ' + str(relevant_list)[1:-1] + '};' + os.linesep
        var_resume_from_node_string += (tab_indent(2) + LOCAL_ROOT_TREE_STRING + local_root_name + ' : {'
                                        + ', '.join([str(node_name_to_number[local_root_name])] + [str(node_name_to_number[node_name]) for node_name in relevant_list])
                                        + '};' + os.linesep)
        init_resume_from_node_string += tab_indent(2) + 'init(' + LOCAL_ROOT_TREE_STRING + local_root_name + ') := ' + local_root_id_str + ';' + os.linesep
        if -2 in relevant_list:
            # this means the parent is a synched parallel node, so it can skip the entire branch.
            inject_string = (tab_indent(4) + '(active_node = node_names.' + local_root_name + ') & (' + STATUS_STRING + local_root_name + ' = success) : -2;' + os.linesep  # if the local root returns success, this is skippable. note that this is checked after the reset condition, so we don't over-write the reset.
                             + tab_indent(4) + '(active_node = node_names.' + local_root_name + ') & (' + STATUS_STRING + local_root_name + ' = failure) : node_names.' + local_root_name + ';' + os.linesep  # failure is still a reset though
                             )
            relevant_list.remove(-2)  # don't actually want it in the relevant set going forward
        else:
            inject_string = tab_indent(4) + '(active_node = node_names.' + local_root_name + ') & ((' + STATUS_STRING + local_root_name + ' = success) | (' + STATUS_STRING + local_root_name + ' = failure)) : node_names.' + local_root_name + ';' + os.linesep  # reset since this isn't skippable.
        # we've manually handled the root case using inject_string
        cur_node_name = nodes[local_root_name]['parent']  # start from the parent.
        ancestor_string = ''
        while cur_node_name is not None:
            ancestor_string += tab_indent(4) + '(active_node = node_names.' + cur_node_name + ') & ((' + STATUS_STRING + cur_node_name + ' = success) | (' + STATUS_STRING + cur_node_name + ' = failure)) : node_names.' + local_root_name + ';' + os.linesep
            cur_node_name = nodes[cur_node_name]['parent']
        # go through and add all the ancestors of the local root to a set for the purpose of resetting.
        next_resume_from_node_string += (tab_indent(2) + 'next(' + LOCAL_ROOT_TREE_STRING + local_root_name + ') := ' + os.linesep
                                         + tab_indent(3) + 'case' + os.linesep
                                         + ancestor_string  # highest priority is reset
                                         + inject_string  # parallel_synch nodes have a special condition
                                         )
        if len(relevant_list) == 0:
            # this was solely for the purpose of skipping success nodes with parallel_synch nodes
            # since ancestor and inject_string already happened, we'll just exit with a default case
            next_resume_from_node_string += ('\t\t\t\tTRUE : ' + LOCAL_ROOT_TREE_STRING + local_root_name + ';' + os.linesep
                                             + '\t\t\tesac;' + os.linesep
                                             )
            continue
        next_resume_from_node_string += (
            ''.join(
                [
                    (tab_indent(4) + '(active_node = node_names.' + relevant_node + ') & (current_status = running) : node_names.' + relevant_node + ';' + os.linesep)
                    for relevant_node in relevant_list
                ]
            )
            + tab_indent(4) + 'TRUE : ' + LOCAL_ROOT_TREE_STRING + local_root_name + ';' + os.linesep
            + tab_indent(3) + 'esac;' + os.linesep
        )
    define_string = var_define_status_string  # + define_trace_running_source
    var_string = var_resume_from_node_string
    init_string = init_resume_from_node_string
    next_string = next_resume_from_node_string
    return (define_string, var_string, init_string, next_string)


def create_resume_point(nodes, node_to_local_root_name_map, local_root_to_relevant_list_map, node_to_descendants_map, node_name_to_number):
    '''
    create the resume_point variable that tells sequence nodes which child to start at
    --
    arguments
    @ nodes := dictionary, s -> n
      s := name of a node, string
      n := dictionary containing node informaion, dictionary
    @ node_to_local_root_name_map := s1 -> s2
      s1 := name of a node, string
      s2 := name of the local root, string
         local root := a node n such that n is the root or the parent of n is parallel
    @ local_root_to_relevant_list_map := dictionary, s -> l
      s := name of a local root, string
        local root := a node n such that n is the root or the parent of n is parallel
      l := nodes which can be resumed from, list
    @ node_to_descendants_map := s -> l
      s := name of a node, string
      l := descendants of the node, list
        descendant := for a node n, any node m such that m is not n
                      and there exists x >= 1 s.t.
                      n = parent^x(m) where ^x means repeat the operation x times
    --
    return
    @ define_string := a string with defintions
    @ init_string := a string with initializations
    @ next_string := a string with next conditions
    @ var_string := a string with variable declarations
    --
    effects
    purely functional from a black box perspective.
    '''
    resume_point_string = ''
    for node_name in nodes:
        node = nodes[node_name]
        if not node['category'] == 'composite':
            pass
        elif not has_memory(node):
            # doesn't have memory. we don't need to resume.
            pass
        elif len(node['children']) < 2:
            # print('few children. skipping')
            # we have 0 or 1 children
            # if there are no children, then resume_point really doesn't matter,
            # but we need to pass a value
            # if there is 1 child, then we never skip it, so resume_point really doesn't matter
            pass
        elif 'parallel' in node['type']:
            # the parallel skip case is already handled, because that's just "is resume tree = -2"
            pass
        else:
            # print('multiple children')
            # have an actual quantity of children
            local_root_name = node_to_local_root_name_map[node_name]
            relevant_list = local_root_to_relevant_list_map[local_root_name]
            # print(relevant_list)
            if len(relevant_list) == 0:
                # print('no real resume children. hard coding -2')
                resume_point_string += tab_indent(2) + CHILD_TRACK_STRING + node_name + ' := -2;' + os.linesep
            else:
                # print('real resume target present. initiating')
                resume_point_string += (tab_indent(2) + CHILD_TRACK_STRING + node_name + ' := ' + os.linesep
                                        + tab_indent(3) + 'case' + os.linesep
                                        )
                descendants = node_to_descendants_map[node_name]
                child_index_to_relevant_descendants_map = {}  # basically, we are going to use this to figure out where we need to point.
                # i.e., if resume_from_node is pointing to 400, which of our children, if any, needs to be resumed? this is what this map answers.
                # print(descendants)
                for relevant_node in relevant_list:
                    # print(relevant_node)
                    if relevant_node in descendants:
                        for child_index in range(len(node['children'])):
                            # so we're gonna map this based on relative children
                            # i.e, do i resume from my first child? second child?
                            # print('---------------------------')
                            # print(child_index)
                            # print(child_index_to_relevant_descendants_map)
                            child_name = node['children'][child_index]
                            # print(child)
                            if relevant_node in node_to_descendants_map[child_name]:
                                # if the relevant node is a descendant of this child,
                                # then we need to mark that down. if it's not, continue
                                if child_index in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(node_name_to_number[relevant_node])
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {node_name_to_number[relevant_node]}
                            elif child_name == relevant_node:
                                # unless of course, the relevant node IS the child,
                                # then we also need to mark that down.
                                if child_index in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(node_name_to_number[relevant_node])
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {node_name_to_number[relevant_node]}
                            # print(child_index_to_relevant_descendants_map)

                for child_index in child_index_to_relevant_descendants_map:
                    resume_point_string += tab_indent(4) + '(' + LOCAL_ROOT_TREE_STRING + local_root_name + ' in ' + str(child_index_to_relevant_descendants_map[child_index]) + ') : ' + str(child_index) + ';' + os.linesep
                resume_point_string += (tab_indent(4) + 'TRUE : -2;' + os.linesep
                                        # we have nothing to resume from
                                        + tab_indent(3) + 'esac;' + os.linesep
                                        )

    define_string = resume_point_string
    var_string = ''
    init_string = ''
    next_string = ''

    return (define_string, var_string, init_string, next_string)

##############################################################################
# Main
##############################################################################


def write_smv(nodes, variables, tick_condition, specifications, output_file = None, do_not_trim = False):

    STAGE_RE = re.compile(r'_stage_\d+')

    def remove_stage(condition):
        return STAGE_RE.sub('', condition)

    specifications = map(remove_stage, specifications)

    print('Number of nodes before pruning: ' + str(len(nodes)))

    root_node_name = get_root_node(nodes)
    refine_return_types(nodes, root_node_name)
    refine_invalid(nodes, root_node_name)

    if not do_not_trim:
        nodes = prune_nodes(nodes)
        root_node_name = get_root_node(nodes)

    print('Number of nodes after pruning: ' + str(len(nodes)))

    nodes_in_order = order_nodes(root_node_name, nodes)
    node_name_to_number = map_node_name_to_number(nodes, nodes_in_order)

    node_to_local_root_name_map = create_node_to_local_root_map(nodes, root_node_name)
    (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map) = create_local_root_to_relevant_list_map(nodes, node_to_local_root_name_map, nodes_in_order)
    node_to_descendants_map = create_node_to_descendants_map(nodes, root_node_name)

    depth_map = create_parallel_depth_map(nodes)
    inverse_map = create_inverse_depth_map(depth_map)

    add_depth(nodes, depth_map)  # bweh don't feel like making this functional.

    # ------------------------------------------------------------------------------------------------------------------------
    # done with variable decleration, moving into string building.

    define_string = ('MODULE main' + os.linesep
                     + '\tCONSTANTS' + os.linesep
                     + '\t\tsuccess, failure, running, invalid;' + os.linesep
                     + '\tDEFINE' + os.linesep
                     )

    # ------------------------------------------------------------------------------------------------------------------------
    var_string = ('\tVAR' + os.linesep
                  + '\t\tnode_names : define_nodes;' + os.linesep
                  )
    # ------------------------------------------------------------------------------------------------------------------------
    init_string = '\tASSIGN' + os.linesep
    next_string = ''
    # ------------------------------------------------------------------------------------------------------------------------

    (new_define, new_var, new_init, new_next) = create_active_node(nodes, root_node_name, tick_condition)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_previous_node(nodes)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_current_status(nodes)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_previous_status()
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_parallel_status(nodes, depth_map, inverse_map)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_resume_structure(nodes, local_root_to_relevant_list_map, node_name_to_number)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_resume_point(nodes, node_to_local_root_name_map, local_root_to_relevant_list_map, node_to_descendants_map, node_name_to_number)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_var, new_init, new_next) = create_next_child(nodes)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_frozen_var, new_var, new_init, new_next) = node_creator.create_blackboard(nodes, variables, root_node_name, tick_condition)
    define_string += ('\t\t--START OF BLACKBOARD DEFINITIONS' + os.linesep
                      + new_define
                      + '\t\t--END OF BLACKBOARD DEFINITIONS' + os.linesep
                      + (
                          (
                              '\tFROZENVAR' + os.linesep
                              + '\t\t--START OF BLACKBOARD FROZENVAR' + os.linesep
                              + new_frozen_var
                              + '\t\t--END OF BLACKBOARD FROZENVAR' + os.linesep) if len(new_frozen_var) > 0 else '')
                      )
    var_string += ('\t\t--START OF BLACKBOARD VARIABLES DECLARATION' + os.linesep
                   + new_var
                   + '\t\t--END OF BLACKBOARD VARIABLES DECLARATION' + os.linesep)
    init_string += ('\t\t--START OF BLACKBOARD VARIABLES INITIALIZATION' + os.linesep
                    + new_init
                    + '\t\t--END OF BLACKBOARD VARIABLES INITIALIZATION' + os.linesep)
    next_string += ('\t\t--START OF BLACKBOARD VARIABLES TRANSITION' + os.linesep
                    + new_next
                    + '\t\t--END OF BLACKBOARD VARIABLES TRANSITION' + os.linesep)

    nuxmv_string = define_string + var_string + init_string + next_string + os.linesep + (os.linesep).join(specifications) + os.linesep
    # ------------------------------------------------------------------------------------------------------------------------

    nuxmv_string += node_creator.create_names_module(node_name_to_number)

    nuxmv_string = remove_stage(nuxmv_string)

    if output_file is None:
        print(nuxmv_string)
    else:
        with open(output_file, 'w') as f:
            f.write(nuxmv_string)
    return


def main():
    '''
    basically a script to write the necessary information.
    --
    arguments
    NONE * -> there are no arguments, but there are command line arguments
    --
    command_line_arguments
    REQUIRED
    @ input_file -> the file containing the nodes and variables.
    OPTIONAL
    @ blackboard_input_file -> a file containing a blackboard. Overwrites
      the default blackbaord creation
    @ module_input_file -> a file containing additional modules. Overwrites
      the default additional module creation
    @ specs_input_file -> a file containing specifications.
    @ output_file -> a file where the entire nuXmv model will be written
      This includes the blackboard, modules, and specifications
    @ blackboard_output_file -> a file where the blackboard will be written
    @ module_output_file -> a file where the additional modules will be written
    @ do_not_trim -> if set, prevents the automatic removal of nodes that cannot run
    --
    return
    NONE
    --
    effects
    creates a string that can be used with nuXmv. Output printed either to a
    specified file, or to the terminal.
    '''
    arg_parser = argparse.ArgumentParser()
    # python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite
    arg_parser.add_argument('input_file')
    arg_parser.add_argument('--blackboard_input_file', default = None)
    arg_parser.add_argument('--module_input_file', default = None)
    arg_parser.add_argument('--specs_input_file', default = None)
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--blackboard_output_file', default = None)
    arg_parser.add_argument('--module_output_file', default = None)
    arg_parser.add_argument('--do_not_trim', action = 'store_true')
    # arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()

    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    tick_condition = temp['tick_condition']
    nodes = temp['nodes']
    variables = temp['variables']
    specifications = temp['specifications']

    write_smv(nodes, variables, tick_condition, specifications, args.output_file, args.do_not_trim)
    return


if __name__ == '__main__':
    main()
