#python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 


#---------------------------------------------------------------------
import argparse
import py_trees
import sys
import time
import os
import re
import inspect
#----------------------------------------------------------------------------------------------------------------
import py_trees.console as console
import node_creator_BTCompiler as node_creator

def walk_tree(t, parent_id, next_available_id, children, nodes, needed_nodes, node_names, leaf_set, fallback_set, sequence_set, parallel_set, parallel_threshold):
    global blackboard_needed
    this_id=next_available_id
    next_available_id = next_available_id + 1
    children[parent_id].append(this_id)

    node_name=t.name
    if node_name in node_names:
        node_names[node_name]=node_names[node_name]+1
        node_name=node_name+str(node_names[node_name])
    else:
        node_names[node_name]=0

    try:
        #this is to overwrite the later checks in order to directly create a specific type of node.
        if t.serene_info_variable == "non_blocking":
            nodes[this_id]=('bt_non_blocking_skill', parent_id, node_name)
            needed_nodes.add('bt_non_blocking_skill')
            leaf_set.add(this_id)
            return next_available_id
    except AttributeError as e:
        #print(e)
        #print(node_name+ " ERROR?")
        pass

    if isinstance(t, py_trees.composites.Sequence):
        nodes[this_id]=('bt_sequence_with_memory', parent_id, node_name)
        needed_nodes.add('bt_sequence_with_memory')
        sequence_set.add(this_id)
    elif isinstance(t, py_trees.composites.Selector):
        nodes[this_id]=('bt_fallback', parent_id, node_name)
        needed_nodes.add('bt_fallback')
        fallback_set.add(this_id)
    elif isinstance(t, py_trees.composites.Parallel):
        nodes[this_id]=('bt_parallel', parent_id, node_name)
        needed_nodes.add('bt_parallel')
        parallel_set.add(this_id)
        if isinstance(t.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
            parallel_threshold[this_id] = 2
        else:
            parallel_threshold[this_id] = 1
    elif isinstance(t, py_trees.behaviours.Success):
        #nodes[this_id] = ('bt_placeholder', parent_id, node_name)
        #needed_nodes.add('bt_placeholder')
        nodes[this_id] = ('bt_success', parent_id, node_name)
        needed_nodes.add('bt_success')
        leaf_set.add(this_id)
        return next_available_id
    else:#currently defaulting to default. will rework this later probably
        nodes[this_id]=('bt_skill', parent_id, node_name)
        needed_nodes.add('bt_skill')
        leaf_set.add(this_id)
        return next_available_id
    
    children[this_id] = []#if we've reached this point, then this node has children, and we are going to set up an empty list for it.
    for child in t.children:
        next_available_id = walk_tree(child, this_id, next_available_id, children, nodes, needed_nodes, node_names, leaf_set, fallback_set, sequence_set, parallel_set, parallel_threshold)
    return next_available_id


#-----------------------------------------------------------------------------------------------------------------------

#fixes some _dot_ variable nesting problems
def create_nodes(nodes, children, leaf_set, fallback_set, sequence_set, parallel_set, parallel_threshold):
    #print(nodes)
    #print(children)
    #print(leaf_set)
    define_string = ""
    init_string = ""
    next_string = ""
    var_string = ""
    for node_id in range(0, len(nodes)):
        #print(node_id)
        var_string += "\t\t" + nodes[node_id][2] + " : " + nodes[node_id][0]
        if node_id in leaf_set:
            pass
        elif node_id in parallel_set:
            var_string += "(" + str(parallel_threshold[node_id]) + ", " + nodes[children[node_id][0]][2] + ", " + nodes[children[node_id][1]][2] + ")"
        else:
            var_string += "(" + nodes[children[node_id][0]][2] + ", " + nodes[children[node_id][1]][2] + ")"
            #all nodes are guaranteed to have 2 children. 
        var_string += ";" + os.linesep
        #---------------------------------
    var_string += "\t\ttick_generator : bt_tick_generator(" + nodes[0][2] + ");" + os.linesep
    return (define_string, var_string, init_string, next_string)

##############################################################################
# Main
##############################################################################

def main():
    global blackboard_needed

    arg_parser=argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('root_file')
    arg_parser.add_argument('root_method')
    arg_parser.add_argument('--root_args', default='', nargs='*')
    arg_parser.add_argument('--string_args', default='', nargs='*')
    arg_parser.add_argument('--specs_input_file')
    arg_parser.add_argument('--output_file', default=None)
    arg_parser.add_argument('--overwrite', action='store_true')
    args=arg_parser.parse_args()

    module = __import__(args.root_file.replace('.py', ''))

    root_string = 'module.' + args.root_method + '('
    first = True
    for root_arg in args.root_args:
        if first:
            root_string += root_arg
            first=False
        else:
            root_string += ', ' + root_arg
    for string_arg in args.string_args:
        if first:
            root_string += '\'' + string_arg + '\''
            first=False
        else:
            root_string += ', ' + '\'' + string_arg + '\''
    root_string += ')'
    root = eval(root_string)

    #tracking variables
    children={-1:[]}#stores a list of children ID. is indexed via node id
    nodes={}#stores a tuple, (type, parent_id, node_name), where type informs us of the node type, and parent of the parent id, and node_name. it's indexed via node id
    node_names={}#a list of node names. each name is also associated with an integer that indicates how many times it has been seen, allowing us to automatically create a new name.
    parallel_threshold = {} #map from parallel nodes to threshold
    #-------------------------------------------------------------------------------
    #sets
    sequence_set = set()
    fallback_set = set()
    leaf_set = set()
    parallel_set = set()
    #-------------------------------------------------------------------------------
    needed_nodes=set()#the set of node types needed
    
    next_available_id = walk_tree(root, -1, 0, children, nodes, needed_nodes, node_names, leaf_set, fallback_set, sequence_set, parallel_set, parallel_threshold)
        
    define_string = ("MODULE main" + os.linesep
    )
    var_string = (""
                  + "\tVAR" + os.linesep
    )
    init_string = (""
    )
    next_string = ""

    (new_define, new_var, new_init, new_next) = create_nodes(nodes, children, leaf_set, fallback_set, sequence_set, parallel_set, parallel_threshold)
    define_string += new_define
    var_string += new_var
    init_string += new_init
    next_string += new_next

    nuxmv_string = define_string + var_string + init_string + next_string
    #------------------------------------------------------------------------------------------------------------------------
    if args.specs_input_file:
        nuxmv_string += open(args.specs_input_file).read() + os.linesep + os.linesep


    for needed in needed_nodes:
        nuxmv_string +=  eval('node_creator.create_'+needed+'()')
    nuxmv_string += node_creator.create_bt_tick_generator()

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
