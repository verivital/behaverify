
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
# import sys
# ----------------------------------------------------------------------------------------------------------------
# serene custom imports
import node_creator
import compute_resume_info
# -----------------------------------------------------------------------------------------------------------------------


def create_nodes(nodes):
    """
    creates strings with neccessary information based on nodes.
    --
    arguments
    @ nodes -> a map (dictionary) from integers (node_id) to node information
    --
    return
    @ define_string -> a string with defintions
    @ init_string -> a string with initializations
    @ next_string -> a string with next conditions
    @ var_string -> a string with variable declarations
    --
    effects
    returns 4 strings, each for a specific section which each node requires.
    """
    define_string = ('\t\t' + nodes[0]['name'] + '.active := TRUE;' + os.linesep
                     + ''.join([('\t\tparallel_skip_' + str(node['node_id']) + ' := '
                                 + ('[-2]' if len(node['children']) < 2 else (
                                     '[' + ', '.join(['resume_from_node_' + str(child) for child in node['children']]) + ']')
                                    )
                                 + ';' + os.linesep) for node in filter(lambda node: 'parallel_with_memory' in node['type'] , nodes.values())])
                     )
    init_string = ''
    next_string = ''
    var_string = ''.join([('\t\t' + node['name'] + ' : '
                           + ((('_'.join([status for (status, possible) in [('success', node['return_arguments']['success']), ('running', node['return_arguments']['running']), ('failure', node['return_arguments']['failure'])] if possible]) + '_DEFAULT_module(') if node['internal_status_module_name'] is None else (
                                   node['internal_status_module_name'] + '(blackboard')) if node['category'] == 'leaf' else (
                                       node['category'] + '_' + node['type']
                                       + ('_' + (str(len(node['children']))) if node['category'] == 'composite' else '')
                                       + '('
                                       + ((', '.join([nodes[node['children'][0]]['name']] + node['additional_arguments'])) if node['category'] == 'decorator' else (
                                           ', '.join([(nodes[child_id]['name']) for child_id in node['children']] + (
                                               ([] if 'without_memory' in node['type'] else (
                                                   [
                                                       ('parallel_skip_' + str(node['node_id'])) if 'parallel' in node['type'] else (
                                                           '-2' if len(node['children']) < 2 else (', resume_point_' + str(node['node_id']))
                                                       )
                                                   ]
                                               ))))))))
                           + ');' + os.linesep
                           )
                          for node in nodes.values()]
                         )
    return (define_string, var_string, init_string, next_string)


def create_resume_structure(nodes, local_root_to_relevant_list_map):
    """
    responsible for creating the resume structure
    --
    arguments
    @ nodes -> a map (dictionary) from integers (node_id) to node information
    @ local_root_to_relevant_list_map
      -> a map (dictionary) from local roots to list of relevant nodes
      @@ local roots -> nodes that are the root or whose parents are synchronized parallel nodes
      @@ relevant nodes -> nodes which can be resumed from
    --
    return
    @ define_string -> a string with defintions
    @ init_string -> a string with initializations
    @ next_string -> a string with next conditions
    @ var_string -> a string with variable declarations
    --
    effects
    returns 4 strings, each for a specific section.
    these are used to allow nodes to resume after running was returned.
    """
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
    for local_root in local_root_to_relevant_list_map:
        relevant_list = local_root_to_relevant_list_map[local_root]
        if len(relevant_list) == 0:
            # there's nothing to resume from. if we have a sequence node, then it apparently only had 0 or 1 children, and we don't need any special resume for it.
            var_define_status_string += "\t\tresume_from_node_" + str(local_root) + " := -3;" + os.linesep
            continue
        var_resume_from_node_string += "\t\tresume_from_node_" + str(local_root) + " : {" + str(local_root) + ", " + str(relevant_list)[1:-1] + "};" + os.linesep
        init_resume_from_node_string += "\t\tinit(resume_from_node_" + str(local_root) + ") := " + str(local_root) + ";" + os.linesep
        if -2 in relevant_list:
            inject_string = ("\t\t\t\t(statuses[" + str(local_root) + "] = success) : -2;" + os.linesep  # if the local root returns success, this is skippable. note that this is checked after the reset condition, so we don't over-write the reset.
                             + "\t\t\t\t(statuses[" + str(local_root) + "] = failure) : " + str(local_root) + ";" + os.linesep  # failure is still a reset though
                             )
            relevant_list.remove(-2)  # don't actually want it in the relevant set going forward
        else:
            inject_string = "\t\t\t\t(statuses[" + str(local_root) + "] in {success, failure}) : " + str(local_root) + ";" + os.linesep  # reset since this isn't skippable.
        # we've manually handled the root case using inject_string
        cur_node = nodes[local_root]['parent_id']  # start from the parent.
        ancestor_string = ""
        while not cur_node == -1:
            ancestor_string += "\t\t\t\t(statuses[" + str(cur_node) + "] in {success, failure}) : " + str(local_root) + ";" + os.linesep
            cur_node = nodes[cur_node]['parent_id']
        # go through and add all the ancestors of the local root to a set for the purpose of resetting.
        next_resume_from_node_string += ("\t\tnext(resume_from_node_" + str(local_root) + ") := " + os.linesep
                                         + "\t\t\tcase" + os.linesep
                                         + ancestor_string  # highest priority is reset
                                         + inject_string  # parallel_synch nodes have a special condition
                                         )
        if len(relevant_list) == 0:
            # this was solely for the purpose of skipping success nodes with parallel_synch nodes
            # since ancestor and inject_string already happened, we'll just exit with a default case
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
        next_resume_from_node_string += ("\t\t\t\tTRUE : max(trace_running_source_" + str(local_root) + ", " + str(local_root) + ");" + os.linesep
                                         # we didn't encounter any reset triggers, so we use trace_running_source
                                         # note that if trace_running_source = -2, then we're just setting to local_root.
                                         # if something returned running, the value will be > = local_root, so we'll point to that
                                         # note that since we are always executing the entire tree, if we returned running last time we will definitely resume this time.
                                         + "\t\t\tesac;" + os.linesep
                                         )
    define_string = var_define_status_string + define_trace_running_source
    var_string = var_resume_from_node_string
    init_string = init_resume_from_node_string
    next_string = next_resume_from_node_string
    return (define_string, var_string, init_string, next_string)


def create_resume_point(nodes, node_to_local_root_map, local_root_to_relevant_list_map, node_to_descendants_map):
    """
    create the resume_point variable that tells sequence nodes which child to start at
    --
    arguments
    @ nodes -> a map (dictionary) from integers (node_id) to node information
    @ node_to_local_root_map -> a map (dictionary) from a node to it's local root
      @@ local roots -> nodes that are the root or whose parents are synchronized parallel nodes
    @ local_root_to_relevant_list_map
      -> a map (dictionary) from local roots to list of relevant nodes
      @@ local roots -> nodes that are the root or whose parents are synchronized parallel nodes
      @@ relevant nodes -> nodes which can be resumed from
    @ node_to_descendants_map -> a map (dictionary) from a node_id to a set of node_ids
      @@ descendants -> does not include the node itself. all descendants, not just direct children
    --
    return
    @ define_string -> a string with defintions
    @ init_string -> a string with initializations
    @ next_string -> a string with next conditions
    @ var_string -> a string with variable declarations
    --
    effects
    returns 4 strings, each for a specific section.
    these are used to allow nodes to resume after running was returned.
    """
    resume_point_string = ""
    for node_id in nodes:
        node = nodes[node_id]
        if not node['category'] == 'composite':
            continue
        if 'parallel' in node['type']:
            continue
        if 'with_memory' not in node['type']:
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
            local_root = node_to_local_root_map[node_id]
            relevant_list = local_root_to_relevant_list_map[local_root]
            # print(relevant_list)
            if len(relevant_list) == 0:
                # print('no real resume children. hard coding -2')
                resume_point_string += "\t\tresume_point_" + str(node_id) + " := -2;" + os.linesep
            else:
                # print('real resume target present. initiating')
                resume_point_string += ("\t\tresume_point_" + str(node_id) + " := " + os.linesep
                                        + "\t\t\tcase" + os.linesep
                                        )
                descendants = node_to_descendants_map[node_id]
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
                            child = node['children'][child_index]
                            # print(child)
                            if relevant_node in node_to_descendants_map[child]:
                                # if the relevant node is a descendant of this child,
                                # then we need to mark that down. if it's not, continue
                                if child_index in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(relevant_node)
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {relevant_node}
                            elif child == relevant_node:
                                # unless of course, the relevant node IS the child,
                                # then we also need to mark that down.
                                if child_index in child_index_to_relevant_descendants_map:
                                    child_index_to_relevant_descendants_map[child_index].add(relevant_node)
                                else:
                                    child_index_to_relevant_descendants_map[child_index] = {relevant_node}
                            # print(child_index_to_relevant_descendants_map)

                for child_index in child_index_to_relevant_descendants_map:
                    resume_point_string += "\t\t\t\t(resume_from_node_" + str(local_root) + " in " + str(child_index_to_relevant_descendants_map[child_index]) + ") : " + str(child_index) + ";" + os.linesep
                resume_point_string += ("\t\t\t\tTRUE : -2;" + os.linesep
                                        # we have nothing to resume from
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
    """
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
    """
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
    nodes = temp['nodes']
    variables = temp['variables']

    compute_resume_info.refine_return_types(nodes, 0)
    compute_resume_info.refine_invalid(nodes, 0, True)

    # if not args.do_not_trim:
    #     node_ids = list(nodes.keys())
    #     deletion_modifier = 0
    #     for node_id in node_ids:
    #         node = nodes[node_id]
    #         if node['always_invalid']:
    #             print(node_id)
    #             if node['parent_id'] in nodes:
    #                 nodes[node['parent_id']]['children'].remove(node_id)
    #             nodes.pop(node_id)
    # print(nodes.keys())

    node_to_local_root_map = compute_resume_info.create_node_to_local_root_map(nodes)
    (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map) = compute_resume_info.create_local_root_to_relevant_list_map(nodes, node_to_local_root_map)
    node_to_descendants_map = compute_resume_info.create_node_to_descendants_map(nodes)

    # ------------------------------------------------------------------------------------------------------------------------
    # done with variable decleration, moving into string building.

    define_string = ('MODULE main' + os.linesep
                     + '\tCONSTANTS' + os.linesep
                     + '\t\tsuccess, failure, running, invalid;' + os.linesep
                     + '\tDEFINE' + os.linesep
                     + '\t\tstatuses := [' + ', '.join([(node['name'] + '.status') for node in nodes.values()]) + '];' + os.linesep
                     )

    # ------------------------------------------------------------------------------------------------------------------------
    var_string = ('\tVAR' + os.linesep
                  + '\t\tnode_names : define_nodes;' + os.linesep
                  + '\t\tblackboard : blackboard_module(node_names, statuses);' + os.linesep
                  )
    # ------------------------------------------------------------------------------------------------------------------------
    init_string = '\tASSIGN' + os.linesep
    next_string = ''
    # ------------------------------------------------------------------------------------------------------------------------

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

    nuxmv_string = define_string + var_string + init_string + next_string
    # ------------------------------------------------------------------------------------------------------------------------
    if args.specs_input_file:
        nuxmv_string += open(args.specs_input_file).read() + os.linesep + os.linesep

    nuxmv_string += node_creator.create_names_module(nodes)
    nuxmv_string += node_creator.create_leaf()
    nuxmv_string += ''.join([eval('node_creator.create_' + cur_thing[0] + '(' + cur_thing[1] + ')') for cur_thing in
                             [*set([('composite_' + node['type'], str(len(node['children']))) if node['category'] == 'composite' else (
                                 ('decorator_' + node['type'], '0'))
                                    for node in nodes.values() if (node['category'] != 'leaf')])]])

    if args.module_input_file:
        nuxmv_string = nuxmv_string + open(args.module_input_file).read()
    else:

        module_string = ''.join([node['internal_status_module_code']
                                 for node in nodes.values() if ((node['category'] == 'leaf') and (node['internal_status_module_name'] is not None))])

        module_string += ''.join([node_creator.create_status_module(statuses) for statuses in [*set([('_'.join([status for (status, possible) in [('success', node['return_arguments']['success']), ('running', node['return_arguments']['running']), ('failure', node['return_arguments']['failure'])] if possible])) for node in nodes.values() if ((node['category'] == 'leaf') and (node['internal_status_module_name'] is None))])]])

        nuxmv_string += module_string
        if args.module_output_file is None:
            pass
        else:
            with open(args.module_output_file, 'w') as f:
                f.write(module_string)

    # print a blackboard variable chart
    # for variable in variables:
    #     nuxmv_string += ('--' + variable + ' : ' + str(variables[variable]['variable_id']) + os.linesep)
    #     for access_node in variables[variable]['stages']:
    #         nuxmv_string += ('----' + access_node + os.linesep)

    if args.blackboard_input_file:
        nuxmv_string += open(args.blackboard_input_file).read()
    else:
        blackboard_string = ''
        blackboard_string += node_creator.create_blackboard(nodes, variables)
        nuxmv_string += blackboard_string
        if args.blackboard_output_file is None:
            pass
        else:
            with open(args.blackboard_output_file, 'w') as f:
                f.write(blackboard_string)

    if args.output_file is None:
        print(nuxmv_string)
    else:
        with open(args.output_file, 'w') as f:
            f.write(nuxmv_string)
    return


if __name__ == '__main__':
    main()
