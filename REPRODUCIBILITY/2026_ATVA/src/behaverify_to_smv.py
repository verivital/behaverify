'''
This module is primarily for internal use with BehaVerify.
It is called by dsl_to_behaverify.py.
It contains a variety of functions to format BehaVerify for use with nuXmv.
It can be called directly.


Author: Serena Serafina Serbinowska
First Created: 2022-01-01 (Date not correct)
Last Edit: 2023-09-08 
'''
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
# ----------------------------------------------------------------------------------------------------------------
# serene custom imports
import node_creator
from behaverify_common import (get_root_node,
                               refine_return_types,
                               refine_invalid,
                               prune_nodes, order_nodes,
                               map_node_name_to_number,
                               create_node_to_local_root_map,
                               create_local_root_to_relevant_list_map,
                               create_node_to_descendants_map,
                               indent,
                               format_node_type)
# -----------------------------------------------------------------------------------------------------------------------

LOCAL_ROOT_TREE_STRING = 'resume_from_here_in_subtree__'
CHILD_TRACK_STRING = 'child_index_to_resume_from__'
PARALLEL_SKIP_STRING = 'parallel_skip__'


def create_nodes(nodes, root_node_name, node_name_to_number, tick_condition):
    '''
    creates strings with necessary information based on nodes.
    --
    arguments
    @ nodes := dictionary, s -> n
      s := name of a node, string
      n := dictionary containing node informaion, dictionary
    @ root_node_name := string, name of the root
    @ node_name_to_number := dictionary, s -> i
      s := name of a node, string
      i := where the node appears in a depth first traversal
           of the tree, integer
    --
    return
    @ define_string := a string with defintions
    @ init_string := a string with initializations
    @ next_string := a string with next conditions
    @ var_string := a string with variable declarations
    --
    effects
    purely functional
    '''
    define_string = (indent(2) + root_node_name + '.active := ' + tick_condition + ';' + os.linesep
                     + ''.join([(indent(2) + PARALLEL_SKIP_STRING + node['name'] + ' := '
                                 + (
                                     '[-2]' if len(node['children']) < 2 else (
                                         '[' + ', '.join([(LOCAL_ROOT_TREE_STRING + child) for child in node['children']]) + ']'
                                     )
                                 )
                                 + ';' + os.linesep) for node in filter(lambda node: (node['type'] == 'parallel' and node['memory'] != ''), nodes.values())])
                     )
    # ^ for each node that is parallel with memory, create a parellel_skip_string.
    # if it doesn't really have children, set it to a constant. otherwise, it will track each of it's children local roots.
    # (also the base case of we need to make the root_node active).
    # print('hello?')

    def create_leaf(node):
        # print(node['name'] + ' : ' + str(node['internal_status_module_name']))
        return (
            indent(2) + node['name'] + ' : '
            + (
                (
                    '_'.join(
                        [
                            status
                            for (status, possible) in [('success', node['return_possibilities']['success']),
                                                       ('running', node['return_possibilities']['running']),
                                                       ('failure', node['return_possibilities']['failure'])]
                            if possible
                        ]
                    ) + '_DEFAULT_module();'
                )
                if node['internal_status_module_name'] is None else
                (
                    node['internal_status_module_name'] + '(' + ', '.join(node['additional_arguments']) + ');'
                )
            )
            + os.linesep
        )

    def create_decorator(node):
        return (
            indent(2) + node['name'] + ' : '
            + format_node_type(node, False)
            + '('
            + ', '.join(node['children'] + (node['additional_arguments'] if node['additional_arguments'] is not None else []))
            + ');' + os.linesep
        )

    def create_composite_with_memory(node):
        return (
            indent(2) + node['name'] + ' : '
            + format_node_type(node, True)
            + '('
            + ', '.join(
                node['children'] +
                [
                    (PARALLEL_SKIP_STRING + node['name'])
                    if node['type'] == 'parallel' else
                    (
                        '-2' if len(node['children']) < 2 else (CHILD_TRACK_STRING + node['name'])
                    )
                ]
            )
            + ');' + os.linesep
        )

    def create_composite_without_memory(node):
        return (
            indent(2) + node['name'] + ' : '
            + format_node_type(node, True)
            + '('
            + ', '.join(node['children'])
            + ');' + os.linesep
        )

    def create_composite(node):
        return (
            (
                indent(2) + node['name']
                + (
                    ' : running_DEFAULT_module;'
                    if node['type'] == 'parallel' else
                    (
                        ' : success_DEFAULT_module;'
                        if 'sequence' in node['type'] else
                        ' : failure_DEFAULT_module;'
                    )
                )
                + os.linesep
            )
            if len(node['children']) == 0 else
            (
                create_composite_without_memory(node)
                if node['memory'] == ''
                else
                create_composite_with_memory(node)
            )
        )

    var_string = ''.join(
        [
            create_leaf(node)
            if node['category'] == 'leaf' else
            (
                create_decorator(node)
                if node['category'] == 'decorator' else
                create_composite(node)
            )
            for node in nodes.values()
        ]
    )
    # ^ for each node, create it as a variable.
    # for leaf nodes: this means passing the internal status module as an argument
    # for decorator nodes: this means adding the additional arguments into the mix
    # for composite nodes: this means adding children, and potential memory tracking stuff.
    init_string = ''
    next_string = ''
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
    define_trace_running_source = ''  # this is storing for the propagation mechanism. rename everything later lmao.

    for local_root_name in local_root_to_relevant_list_map:
        local_root_id_str = str(node_name_to_number[local_root_name])
        relevant_list = local_root_to_relevant_list_map[local_root_name]
        if len(relevant_list) == 0:
            # there's nothing to resume from. if we have a sequence node, then it apparently only had 0 or 1 children, and we don't need any special resume for it.
            var_define_status_string += indent(2) + LOCAL_ROOT_TREE_STRING + local_root_name + ' := -3;' + os.linesep
            continue
        # var_resume_from_node_string += indent(2) + LOCAL_ROOT_TREE_STRING + local_root_name + ' : {' + local_root_id_str + ', ' + str(relevant_list)[1:-1] + '};' + os.linesep
        var_resume_from_node_string += (indent(2) + LOCAL_ROOT_TREE_STRING + local_root_name + ' : {'
                                        + ', '.join([str(node_name_to_number[local_root_name])] + [('-2' if node_name == -2 else str(node_name_to_number[node_name])) for node_name in relevant_list])
                                        + '};' + os.linesep)
        init_resume_from_node_string += indent(2) + 'init(' + LOCAL_ROOT_TREE_STRING + local_root_name + ') := ' + local_root_id_str + ';' + os.linesep
        if -2 in relevant_list:
            # this means the parent is a synched parallel node, so it can skip the entire branch.
            inject_string = (indent(4) + '(' + local_root_name + '.status = success) : -2;' + os.linesep  # if the local root returns success, this is skippable. note that this is checked after the reset condition, so we don't over-write the reset.
                             + indent(4) + '(' + local_root_name + '.status = failure) : node_names.' + local_root_name + ';' + os.linesep  # failure is still a reset though
                             )
            relevant_list.remove(-2)  # don't actually want it in the relevant set going forward
        else:
            inject_string = indent(4) + '(' + local_root_name + '.status in {success, failure}) : node_names.' + local_root_name + ';' + os.linesep  # reset since this isn't skippable.
        # we've manually handled the root case using inject_string
        cur_node_name = nodes[local_root_name]['parent']  # start from the parent.
        ancestor_string = ''
        while cur_node_name is not None:
            ancestor_string += indent(4) + '(' + cur_node_name + '.status in {success, failure}) : node_names.' + local_root_name + ';' + os.linesep
            cur_node_name = nodes[cur_node_name]['parent']
        # go through and add all the ancestors of the local root to a set for the purpose of resetting.
        next_resume_from_node_string += (indent(2) + 'next(' + LOCAL_ROOT_TREE_STRING + local_root_name + ') := ' + os.linesep
                                         + indent(3) + 'case' + os.linesep
                                         + ancestor_string  # highest priority is reset
                                         + inject_string  # parallel_synch nodes have a special condition
                                         + indent(4) + local_root_name + '.status = invalid : ' + LOCAL_ROOT_TREE_STRING + local_root_name + ';' + os.linesep  # don't change if the local root is invalid, and an ancestor didn't make us reset
                                         )
        if len(relevant_list) == 0:
            # this was solely for the purpose of skipping success nodes with parallel_synch nodes
            # since ancestor and inject_string already happened, we'll just exit with a default case
            next_resume_from_node_string += (indent(4) + 'TRUE : ' + local_root_id_str + ';' + os.linesep
                                             + indent(3) + 'esac;' + os.linesep
                                             )
            continue

        def trace_running_source(node_name):
            nonlocal define_trace_running_source
            cases = ''
            if len(nodes[node_name]['children']) == 0:
                pass
            else:
                for child_name in nodes[node_name]['children']:
                    if trace_running_source(child_name):
                        cases += indent(4) + '!(trace_running_source_' + child_name + ' = -2) : trace_running_source_' + child_name + ';' + os.linesep
            if cases == '':
                if node_name in relevant_list:
                    define_trace_running_source += indent(2) + 'trace_running_source_' + node_name + ' := (' + node_name + '.status = running) ? node_names.' + node_name + ' : -2;' + os.linesep
                    return True
                return False
            if node_name in relevant_list:
                cases += indent(4) + '(' + node_name + '.status = running) : node_names.' + node_name + ';' + os.linesep
            define_trace_running_source += (indent(2) + 'trace_running_source_' + node_name + ' := ' + os.linesep
                                            + indent(3) + 'case' + os.linesep
                                            + cases
                                            + indent(4) + 'TRUE : -2;' + os.linesep
                                            + indent(3) + 'esac;' + os.linesep
                                            )
            return True
        trace_running_source(local_root_name)
        next_resume_from_node_string += (indent(4) + 'TRUE : max(trace_running_source_' + local_root_name + ', node_names.' + local_root_name + ');' + os.linesep
                                         # we didn't encounter any reset triggers, so we use trace_running_source
                                         # note that if trace_running_source = -2, then we're just setting to local_root_name.
                                         # if something returned running, the value will be > = local_root_name, so we'll point to that
                                         # note that since we are always executing the entire tree, if we returned running last time we will definitely resume this time.
                                         + indent(3) + 'esac;' + os.linesep
                                         )
    define_string = var_define_status_string + define_trace_running_source
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
            continue
        if node['type'] == 'parallel':
            continue
        if node['memory'] == '':
            continue
        if len(node['children']) < 2:
            # print('few children. skipping')
            # we have 0 or 1 children
            # if there are no children, then resume_point really doesn't matter,
            # but we need to pass a value
            # if there is 1 child, then we never skip it, so resume_point really doesn't matter,
            # but we need to pass a value
            # so regardless, we need to pass a value.
            # hard code -2 into the node_with_memory in this case
            pass
        else:
            # print('multiple children')
            # have an actual quantity of children
            local_root_name = node_to_local_root_name_map[node_name]
            relevant_list = local_root_to_relevant_list_map[local_root_name]
            # print(relevant_list)
            if len(relevant_list) == 0:
                # print('no real resume children. hard coding -2')
                resume_point_string += indent(2) + CHILD_TRACK_STRING + node_name + ' := -2;' + os.linesep
            else:
                # print('real resume target present. initiating')
                resume_point_string += (indent(2) + CHILD_TRACK_STRING + node_name + ' := ' + os.linesep
                                        + indent(3) + 'case' + os.linesep
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
                    resume_point_string += indent(4) + '(' + LOCAL_ROOT_TREE_STRING + local_root_name + ' in ' + str(child_index_to_relevant_descendants_map[child_index]) + ') : ' + str(child_index) + ';' + os.linesep
                resume_point_string += (indent(4) + 'TRUE : -2;' + os.linesep
                                        # we have nothing to resume from
                                        + indent(3) + 'esac;' + os.linesep
                                        )

    define_string = resume_point_string
    var_string = ''
    init_string = ''
    next_string = ''

    return (define_string, var_string, init_string, next_string)


def write_smv(nodes, variables, enum_constants, tick_condition, specifications, hyper_mode, output_file = None, do_not_trim = False):
    '''
    basically a script to write the necessary information.
    --
    arguments
    @ nodes := a dictionary from node names to a dictionary with info
    @ variables := a dictionary from variable name to dict info
    @ tick_condition := a string containing tick_condition
    @ specifications := a string containing specifications
    @ output_file := if none, will print. else, writes to the file
    @ do_not_trim := if true, prevents the automatic removal of nodes that cannot run
    --
    return
    NONE
    --
    effects
    creates a string that can be used with nuXmv. Output printed either to a
    specified file, or to the terminal.
    '''
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

    # ------------------------------------------------------------------------------------------------------------------------
    # done with variable decleration, moving into string building.

    define_string = (
        'MODULE main' + os.linesep
        + indent(1) + 'VAR' + os.linesep
        + (
            (
                indent(2) + 'system_1 : system_module;' + os.linesep
                + indent(2) + 'system_2 : system_module;' + os.linesep
            )
            if hyper_mode
            else
            (
                indent(2) + 'system : system_module;' + os.linesep
            )
        )
        + '--------------SPECIFICATIONS' + os.linesep
        + os.linesep
        + (os.linesep).join(specifications) + os.linesep
        + os.linesep
        + '--------------END OF SPECIFICATIONS' + os.linesep
        + os.linesep
        + 'MODULE system_module' + os.linesep
        + indent(1) + 'CONSTANTS' + os.linesep
        + indent(2) + 'success, failure, running, invalid' + (', ' if len(enum_constants) > 0 else '') + ', '.join(enum_constants) + ';' + os.linesep
        + indent(1) + 'DEFINE' + os.linesep
        # + indent(2) + 'statuses := [' + ', '.join([(node_name + '.status') for node_name in nodes_in_order]) + '];' + os.linesep
        # + indent(2) + 'active := [' + ', '.join([(node_name + '.active') for node_name in nodes_in_order]) + '];' + os.linesep
    )

    # ------------------------------------------------------------------------------------------------------------------------
    var_string = (indent(1) + 'VAR' + os.linesep
                  + indent(2) + 'node_names : define_nodes;' + os.linesep
                  # + indent(2) + 'blackboard : blackboard_module(node_names, active);' + os.linesep
                  )
    # ------------------------------------------------------------------------------------------------------------------------
    init_string = indent(1) + 'ASSIGN' + os.linesep
    next_string = ''
    # ------------------------------------------------------------------------------------------------------------------------

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

    (new_define, new_var, new_init, new_next) = create_nodes(nodes, root_node_name, node_name_to_number, tick_condition)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    (new_define, new_frozen_var, new_var, new_init, new_next) = node_creator.create_blackboard(nodes, variables, root_node_name)
    define_string += (indent(2) + '--START OF BLACKBOARD DEFINITIONS' + os.linesep
                      + new_define
                      + indent(2) + '--END OF BLACKBOARD DEFINITIONS' + os.linesep
                      + (
                          (
                              indent(1) + 'FROZENVAR' + os.linesep
                              + indent(2) + '--START OF BLACKBOARD FROZENVAR' + os.linesep
                              + new_frozen_var
                              + indent(2) + '--END OF BLACKBOARD FROZENVAR' + os.linesep) if len(new_frozen_var) > 0 else '')
                      )
    var_string += (indent(2) + '--START OF BLACKBOARD VARIABLES DECLARATION' + os.linesep
                   + new_var
                   + indent(2) + '--END OF BLACKBOARD VARIABLES DECLARATION' + os.linesep)
    init_string += (indent(2) + '--START OF BLACKBOARD VARIABLES INITIALIZATION' + os.linesep
                    + new_init
                    + indent(2) + '--END OF BLACKBOARD VARIABLES INITIALIZATION' + os.linesep)
    next_string += (indent(2) + '--START OF BLACKBOARD VARIABLES TRANSITION' + os.linesep
                    + new_next
                    + indent(2) + '--END OF BLACKBOARD VARIABLES TRANSITION' + os.linesep)

    nuxmv_string = define_string + var_string + init_string + next_string  + os.linesep
    # ------------------------------------------------------------------------------------------------------------------------

    nuxmv_string += node_creator.create_names_module(node_name_to_number)
    # nuxmv_string += node_creator.create_leaf()
    nuxmv_string += ''.join([eval('node_creator.create_' + cur_thing[0] + '(' + cur_thing[1] + ')') for cur_thing in
                             [*set([(format_node_type(node, False), str(len(node['children'])))
                                    for node in nodes.values() if (node['category'] != 'leaf')])]])

    module_string = ''.join([node['internal_status_module_code']
                             for node in nodes.values() if ((node['category'] == 'leaf') and (node['internal_status_module_name'] is not None))])

    module_string += ''.join([node_creator.create_status_module(statuses) for statuses in [*set([('_'.join([status for (status, possible) in [('success', node['return_possibilities']['success']), ('running', node['return_possibilities']['running']), ('failure', node['return_possibilities']['failure'])] if possible])) for node in nodes.values() if ((node['category'] == 'leaf') and (node['internal_status_module_name'] is None))])]])

    nuxmv_string += module_string

    if output_file is None:
        print(nuxmv_string)
    else:
        with open(output_file, 'w') as f:
            f.write(nuxmv_string)
    return


##############################################################################
# Main
##############################################################################


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
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--do_not_trim', action = 'store_true')
    # arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()

    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']
    enum_constants = temp['enum_constants']
    tick_condition = temp['tick_condition']
    specifications = temp['specifications']
    hyper_mode = temp['hyper_mode']
    write_smv(nodes, variables, enum_constants, tick_condition, specifications, hyper_mode, args.output_file, args.do_not_trim)
    return


if __name__ == '__main__':
    main()
