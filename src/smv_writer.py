
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
import compute_resume_info
# -----------------------------------------------------------------------------------------------------------------------


def create_nodes(nodes):
    '''
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
    '''
    define_string = ""
    init_string = ""
    next_string = ""
    var_string = ""
    for node_id in range(0, len(nodes)):
        node = nodes[node_id]
        # print(node_id)
        if node_id == 0:
            define_string += ("\t\t" + node['name'] + ".active := TRUE;"
                              + os.linesep)
        children_string = ''
        # if node_id in selector_without_memory_set or node_id in
        # sequence_without_memory_set or node_id in selector_with_memory_set
        # or node_id in sequence_with_memory_set or node_id in
        # parallel_synch_set or node_id in parallel_unsynch_set:
        if len(node['children']) == 0:
            # this node has no children
            children_string = ''
        else:
            children_string = ''
            for child in node['children']:
                children_string += ", " + nodes[child]['name']
            children_string = children_string[2:]
        # ---------------------------------
        if node['category'] == 'leaf':
            var_string += ("\t\t" + node['name'] + " : "
                           + node['category'] + '_' + node['type'] + "(")
        elif node['category'] == 'decorator':
            var_string += ("\t\t" + node['name'] + " : "
                           + node['category'] + '_' + node['type'] + "("
                           + children_string)
        elif node['category'] == 'composite':
            if 'without_memory' in node['type']:
                var_string += ("\t\t" + node['name'] + " : "
                               + node['category'] + '_' + node['type']
                               + "_" + str(len(node['children'])) + "("
                               + children_string)
            elif 'with_memory' in node['type']:
                if len(node['children']) < 2:
                    resume_point = "-2"
                else:
                    resume_point = "resume_point_" + str(node_id)
                if children_string == '':
                    pass
                else:
                    children_string = children_string + ', '
                var_string += ("\t\t" + node['name'] + " : "
                               + node['category'] + '_' + node['type']
                               + "_" + str(len(node['children'])) + "("
                               + children_string + resume_point)
            elif 'parallel' in node['type']:
                if 'unsynchronized' in node['type']:
                    var_string += ("\t\t" + node['name'] + " : "
                                   + node['category'] + '_' + node['type']
                                   + "_" + str(len(node['children'])) + "("
                                   + children_string)
                else:
                    if len(node['children']) < 2:
                        skip_string = "[-2]"
                    else:
                        skip_string = "["
                        for child in node['children']:
                            skip_string += ("resume_from_node_" + str(child) + ", ")
                        skip_string = skip_string[0:-2] + "]"
                    define_string += ("\t\tparallel_skip_" + str(node_id) + " := "
                                      + skip_string + ";" + os.linesep)

                    if children_string == "":
                        pass
                    else:
                        children_string = children_string + ', '
                    var_string += ("\t\t" + node['name'] + " : "
                                   + node['category'] + '_' + node['type']
                                   + "_" + str(len(node['children'])) + "("
                                   + children_string + " parallel_skip_" + str(node_id))
            else:
                print('composite node of unknown type. is not parallel.',
                      ' is not with_memory. is not without_memory.',
                      'Node infromation follows')
                print(node)
        else:
            print('ERROR: node is not leaf, decorator, or composite.',
                  'This should not be possible. Node information follows')
            print(node)
            var_string += "0"
        # ---------------------------------
        if node['category'] == 'leaf':
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


def create_additional_arguments(nodes):
    '''
    creates strings with additional neccessary information based on nodes.
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
    this is based on additional arguments
    '''
    define_string = ""
    var_string = ""
    init_string = ""
    next_string = ""
    for node_id in nodes:
        node = nodes[node_id]
        for arg in node['additional_definitions']:
            define_string += arg
        for arg in node['additional_declarations']:
            var_string += arg
        for arg in node['additional_initializations']:
            init_string += arg
    return (define_string, var_string, init_string, next_string)


def create_resume_structure(nodes, local_root_to_relevant_list_map):
    '''
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

    var_resume_from_node_string = ""  # this is a variable that actually stores what running state we're in
    init_resume_from_node_string = ""
    next_resume_from_node_string = ""
    var_define_status_string = ""  # this is for storing the define versions that are constants.
    define_trace_running_source = ""  # this is storing for the propagation mechanism. rename everything later lmao.
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
    '''
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
    '''
    resume_point_string = ""
    for node_id in nodes:
        node = nodes[node_id]
        if not node['category'] == 'composite':
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
    '''
    basically a script to write the necessary information.
    --
    arguments
    NONE * -> there are no arguments, but there are command line arguments
    --
    command_line_arguments
    REQUIRED
    @ input_file -> the file containing the nodes and variables.
    optional
    @ blackboard_input_file -> a file containing a blackboard. Overwrites
      the default blackbaord creation
    @ module_input_file -> a file containing additional modules. Overwrites
      the default additional module creation
    @ specs_input_file -> a file containing specifications.
    @ output_file -> a file where the entire nuXmv model will be written
      This includes the blackboard, modules, and specifications
    @ blackboard_output_file -> a file where the blackboard will be written
    @ module_output_file -> a file where the additional modules will be written
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
    # arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()

    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']

    compute_resume_info.refine_return_types(nodes, 0)

    node_to_local_root_map = compute_resume_info.create_node_to_local_root_map(nodes)
    (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map) = compute_resume_info.create_local_root_to_relevant_list_map(nodes, node_to_local_root_map)
    node_to_descendants_map = compute_resume_info.create_node_to_descendants_map(nodes)

    # ------------------------------------------------------------------------------------------------------------------------
    # done with variable decleration, moving into string building.

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

    # ------------------------------------------------------------------------------------------------------------------------
    var_string = (""
                  + "\tVAR" + os.linesep
                  )
    # var_string += "\t\tvariable_names : define_variables;" + os.linesep
    var_string += "\t\tnode_names : define_nodes;" + os.linesep
    # var_string += "\t\tblackboard : blackboard_module(node_names, variable_names, statuses);" + os.linesep
    var_string += "\t\tblackboard : blackboard_module(node_names, statuses);" + os.linesep
    # ------------------------------------------------------------------------------------------------------------------------
    init_string = "\tASSIGN" + os.linesep
    next_string = ""
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

    (new_define, new_var, new_init, new_next) = create_additional_arguments(nodes)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    nuxmv_string = define_string + var_string + init_string + next_string
    # ------------------------------------------------------------------------------------------------------------------------
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
            if cur_type not in created_types:
                created_types.add(cur_type)
                nuxmv_string += eval('node_creator.create_' + nodes[node]['category'] + '_' + nodes[node]['type'] + '(' + str(len(nodes[node]['children'])) + ')')
        else:
            print('unknown node category')
            print(nodes[node])

    nuxmv_string += node_creator.create_names_module(nodes, variables)

    # print a blackboard variable chart
    for variable in variables:
        nuxmv_string += ('--' + variable + ' : ' + str(variables[variable]['variable_id']) + os.linesep)
        for access_node in variables[variable]['access']:
            nuxmv_string += ('----' + access_node + os.linesep)

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

    module_string = ''
    status_module_string = ''
    check_module_string = ''
    other_module_string = ''
    if args.module_input_file:
        nuxmv_string = nuxmv_string + open(args.module_input_file).read()
    else:
        for node_id in nodes:
            for module_sig in nodes[node_id]['additional_modules']:
                module = nodes[node_id]['additional_modules'][module_sig]
                if module['type'] == 'status':
                    possible_values = []
                    for status in nodes[node_id]['return_arguments']:
                        if nodes[node_id]['return_arguments'][status]:
                            possible_values.append(status)
                    if len(possible_values) == 1:
                        status_module_string += ("MODULE " + module['name']
                                                 + '(' + str(module['args'])[1:-1].replace("'", "") + ')' + os.linesep
                                                 + "\tCONSTANTS" + os.linesep
                                                 + "\t\tsuccess, failure, running;" + os.linesep
                                                 + "\tDEFINE" + os.linesep
                                                 + "\t\tstatus := " + possible_values[0].replace("'", "") + ";"
                                                 + os.linesep
                                                 )
                    else:
                        if len(possible_values) == 0:
                            print('no possible values for module,',
                                  'defaulting to all values acceptable')
                            print(nodes[node_id])
                            possible_values = [
                                'success',
                                'failure',
                                'running']
                        possible_values = "{" + str(possible_values)[1:-1].replace("'", "") + "}"
                        status_module_string += ("MODULE " + module['name']
                                                 + '(' + str(module['args'])[1:-1].replace("'", "") + ')' + os.linesep
                                                 + "\tCONSTANTS" + os.linesep
                                                 + "\t\tsuccess, failure, running;" + os.linesep
                                                 + "\tVAR" + os.linesep
                                                 + "\t\tstatus : " + possible_values + ";" + os.linesep
                                                 )
                        assigned = False
                        if not module['initial_value'] is None:
                            if not assigned:
                                status_module_string += "\tASSIGN" + os.linesep
                                assigned = True
                            status_module_string += ("\t\tinit(status) := " + os.linesep
                                                     + "\t\t\tcase" + os.linesep
                                                     )
                            for condition_pair in module['init_value']:
                                status_module_string += "\t\t\t\t" + condition_pair[0] + " : " + condition_pair[1] + ";" + os.linesep
                            status_module_string += ("\t\t\t\tTRUE : " + possible_values + ";" + os.linesep
                                                     + "\t\t\tesac;" + os.linesep
                                                     )
                        if not module['next_value'] is None:
                            if not assigned:
                                status_module_string += "\tASSIGN" + os.linesep
                                assigned = True
                            status_module_string += ("\t\tnext(status) := " + os.linesep
                                                     + "\t\t\tcase" + os.linesep
                                                     )
                            for condition_pair in module['next_value']:
                                status_module_string += "\t\t\t\t" + condition_pair[0] + " : " + condition_pair[1] + ";" + os.linesep
                            status_module_string += ("\t\t\t\tTRUE : " + possible_values + ";" + os.linesep
                                                     + "\t\t\tesac;" + os.linesep
                                                     )
                        if not module['current_value'] is None:
                            if not assigned:
                                status_module_string += "\tASSIGN" + os.linesep
                                assigned = True
                            status_module_string += ("\t\tstatus := " + os.linesep
                                                     + "\t\t\tcase" + os.linesep
                                                     )
                            for condition_pair in module['current_value']:
                                status_module_string += "\t\t\t\t" + condition_pair[0] + " : " + condition_pair[1] + ";" + os.linesep
                            status_module_string += ("\t\t\t\tTRUE : " + possible_values + ";" + os.linesep
                                                     + "\t\t\tesac;" + os.linesep
                                                     )
                    status_module_string += os.linesep
                elif module['type'] == 'check':

                    check_module_string += ("MODULE " + module['name'] + '(' + str(module['args'])[1:-1].replace("'", "") + ')' + os.linesep
                                            + "\tDEFINE" + os.linesep
                                            + "\t\tresult := "
                                            )
                    if module['left_hand_side']:
                        # user provided a left hand side, using that.
                        check_module_string += module['left_hand_side'] + module['operator'] + module['right_hand_side'] + ';' + os.linesep
                    else:
                        # gotta default it
                        if variables[module['variable_name']]['use_stages']:
                            stage = 0
                            for stage_end in variables[module['variable_name']]['stages']:
                                if stage_end > node_id:
                                    break
                                stage = stage + 1
                            if stage == 0:
                                # check_module_string += ("variable_exists[variable_names." + module['variable_name'] + "]"
                                #                         + " & (variables[variable_names." + module['variable_name'] + "]" + module['operator'] + module['right_hand_side'] + ');' + os.linesep
                                #                         )
                                check_module_string += ("blackboard." + module['variable_name'] + "_exists"
                                                        + " & (blackboard." + module['variable_name'] + module['operator'] + module['right_hand_side'] + ');' + os.linesep
                                                        )
                            else:
                                stage = str(stage)
                                # check_module_string += ("variable_exists[variable_names." + module['variable_name'] + "_stage_" + stage + "]"
                                #                         + " & (variables[variable_names." + module['variable_name'] + "_stage_" + stage + "]" + module['operator'] + module['right_hand_side'] + ');' + os.linesep
                                #                         )
                                check_module_string += ("blackboard." + module['variable_name'] + "_stage_" + stage + "_exists"
                                                        + " & (blackboard." + module['variable_name'] + "_stage_" + stage + module['operator'] + module['right_hand_side'] + ');' + os.linesep
                                                        )
                        else:
                            if module['use_next']:
                                check_module_string += "next("
                            # check_module_string += "variable_exists[variable_names." + module['variable_name'] + "]"
                            check_module_string += "blackboard." + module['variable_name'] + "_exists"
                            if module['use_next']:
                                check_module_string += ")"
                            check_module_string += " & ("
                            if module['use_next']:
                                check_module_string += 'next('
                            # check_module_string += "variables[variable_names." + module['variable_name'] + "]"
                            check_module_string += "blackboard." + module['variable_name']
                            if module['use_next']:
                                check_module_string += ') '
                            check_module_string += module['operator'] + module['right_hand_side'] + ");" + os.linesep
                            check_module_string += os.linesep
                else:
                    other_module_string += module['custom_module']
                    other_module_string += os.linesep
        module_string = (status_module_string
                         + check_module_string
                         + other_module_string)
        nuxmv_string += module_string
        if args.module_output_file is None:
            pass
        else:
            with open(args.module_output_file, 'w') as f:
                f.write(module_string)
            # if args.overwrite:
            #     with open(args.module_output_file, 'w') as f:
            #         f.write(module_string)
            # else:
            #     try:
            #         with open(args.module_output_file, 'x') as f:
            #             f.write(module_string)
            #     except FileExistsError:
            #         print('The specified module file already exists. To overwrite the file, rerun the command with --overwrite True')
    if args.output_file is None:
        print(nuxmv_string)
    else:
        with open(args.output_file, 'w') as f:
            f.write(nuxmv_string)
        # if args.overwrite:
        #     with open(args.output_file, 'w') as f:
        #         f.write(nuxmv_string)
        # else:
        #     try:
        #         with open(args.output_file, 'x') as f:
        #             f.write(nuxmv_string)
        #     except FileExistsError:
        #         print('The specified output file already exists. To overwrite the file, rerun the command with --overwrite True')
    return


if __name__ == '__main__':
    main()
