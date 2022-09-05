
#python3 tree_parser.py root_file root_method --root_args ROOT_ARGS --string_args STRING_ARGS --output_file OUTPUT_FILE

#----------------------------------------------------------------------------------------------------------------
import argparse
import py_trees
import sys
import time
import os
import re
import inspect
import operator
#import json
import pprint
#----------------------------------------------------------------------------------------------------------------
import py_trees.console as console
#----------------------------------------------------------------------------------------------------------------
blackboard_needed = False
#----------------------------------------------------------------------------------------------------------------
#regex stuff
blackboard_name_pattern = re.compile(r"#*(?P<blackboard_name>[^\s= ]+)\s*= \s*py_trees\.blackboard\.Blackboard\(\s*\)")
#----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
'''
root : the root node of the tree being considered
file_name : the output file
--
returns nothing, but writes {'nodes' : nodes, 'variables' : variables} to the provided file, or prints them out if no file is provided

nodes : a map (dictionary) from node number to a dictionary of information. contains the following information
 'name' : the node's name
 'parent_id' : the node_id of the parent
 'children' : a list of children (node_id)
 'category' : leaf, decorator, or composite
 'type' : a string indicating the node type
 'variables' : a list of blackboard variables the node has access to (variable_name)
 'additional_arguments' : a list of additional arguments that the node will need,
 'additional_definitions' : a list of additional definitions needed by the node (declared in MAIN),
 'additional_declarations' : a list of additional variables to declare,
 'additional_initializations' : a list of assignments for variables,
 'additional_modules' : a list of additional modules to be created

variables : a map (dictionary) from variable name to information about the variable
 'variable_id' = the id (int) associated with the variable. used for ordering the blackboard
 'min_value' = the minimum value (int) the variable can be. default 0
 'max_value' = the maximum value (int) the variable can be. default 1
 'init_value' = the value used at the very start. default None
 'always_exist' = whether this variable always exists. default True
 'init_exist' = whether this variable initially exists. default True
 'global_next_mode' = whether this variable uses only on next statement for everything. default True
 'global_next_value' = what the next value for this variable is when using only one statement for everything. default True
 'global_next_exist' = whether this variable exists by default at the next step. default True,
 'next_value' = a map (dictionary) from node id to what value that node assign. each node maps to a list of pairs (condition, value). default, each node maps to None. 
 'next_exist' = a map (dictionary) from node id to if that node makes the variable exist. each node maps to a list of pairs (condition, value). default, each node maps to True
 'access' = a set of node_ids that have access to change the value of the variable
'''
def walk_tree(root, file_name = None):
    nodes = {-1 : {'children' : []}}
    variables = {}
    walk_tree_recursive(root, -1, 0, nodes, {}, variables)
    variable_name_cleanup(nodes, variables)
    nodes.pop(-1)
    if file_name:
        with open(file_name, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False)
        printer.pprint({'nodes' : nodes, 'variables' : variables})

def walk_tree_recursive(current_node, parent_id, next_available_id, nodes, node_names, variables):
    this_id = next_available_id #set what the current id is
    next_available_id = next_available_id + 1 #increment what is available
    nodes[parent_id]['children'].append(this_id) #update parent's list of children

    #next, we get the name of this node, and correct for duplication
    node_name = current_node.name
    if node_name in node_names:
        node_names[node_name] = node_names[node_name] + 1
        node_name = node_name + str(node_names[node_name])
    else:
        node_names[node_name] = 0


    def attempt_to_read_file():
        nonlocal nodes,  variables
        try:
            try:
                file_name = inspect.getfile(current_node.__class__)
                with open(file_name, 'r') as f:
                    code = f.read()
            except:
                code = inspect.getsource(current_node.__class__)
        except:
            return
        additional_arguments = []
        additional_initializations = []
        additional_declarations = []
        additional_modules = []
        
        blackboard_match = blackboard_name_pattern.search(code)
        invar_string = ""
        decl_string = ""
        local_variables = []
        if blackboard_match:
            blackboard_name = blackboard_match.groupdict()['blackboard_name'].strip()
            variable_name_pattern = re.compile(r"#*\s*" + blackboard_name + "\.(?P<variable_name>[_a-zA-Z][\w\.]+)")
            start_loc = 0
            done = False
            local_variable_set = set()
            while not done:
                variable_match = variable_name_pattern.search(code, start_loc)
                if variable_match:
                    start_loc = variable_match.span()[1]
                    variable_name = variable_match.groupdict()['variable_name'].strip()
                    variable_name = variable_name.replace('.', '_dot_')
                    if variable_name in local_variable_set:#already dealt with
                        continue
                    else:
                        local_variable_set.add(variable_name)
                    if variable_name in variables:
                        var_num = variables[variable_name]['variable_id']
                        variables[variable_name]['access'].add(this_id)
                        variables[variable_name]['next_value'][this_id] = None
                        variables[variable_name]['next_exist'][this_id] = True
                    else:
                        var_num = len(variables)
                        variables[variable_name] = {
                            'variable_id' : var_num,
                            'min_value' : 0,
                            'max_value' : 1,
                            'init_value' : None,
                            'always_exist' : True,
                            'init_exist' : True,
                            'global_next_mode' : True,
                            'global_next_value' : None,
                            'global_next_exist' : True,
                            'next_value' : {this_id : None},
                            'next_exist' : {this_id : True},
                            'access' : {this_id}
                        }
                    local_variables.append(variable_name)
                else:
                    done = True
        else:
            variable_name = current_node.variable_name
            variable_name = variable_name.replace('.', '_dot_')
            if variable_name in variables:
                var_num = variables[variable_name]['variable_id']
                variables[variable_name]['access'].add(this_id)
                variables[variable_name]['next_value'][this_id] = None
                variables[variable_name]['next_exist'][this_id] = True
            else:
                var_num = len(variables)
                variables[variable_name] = {
                    'variable_id' : var_num,
                    'min_value' : 0,
                    'max_value' : 1,
                    'init_value' : None,
                    'always_exist' : True,
                    'init_exist' : True,
                    'global_next_mode' : True,
                    'global_next_value' : None,
                    'global_next_exist' : True,
                    'next_value' : {this_id : None},
                    'next_exist' : {this_id : True},
                    'access' : {this_id}
                }
            local_variables.append(variable_name)

            
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'set_blackboard_variables',
            'variables' : local_variables,
            'additional_arguments' : [node_name + "_STATUS"],
            'additional_definitions' : [],
            'additional_declarations' : ['\t\t' + node_name + '_STATUS : ' + node_name + '_STATUS_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep],
            'additional_initializations' : [],
            'additional_modules' : [
                {
                    'name' : node_name + '_STATUS_module',
                    'type' : 'status',
                    'args' : ['variables', 'variable_exists', 'node_names', 'variable_names'],
                    'possible_values' : ['success', 'failure', 'running'],
                    'initial_value' : None,
                    'next_value' : None
                }
            ]
        }
        return
        
        
    dealt_with = False
    try:
        #this is to overwrite the later checks in order to directly create a specific type of node based on a variable
        if current_node.serene_info_variable == "BlueROV_Blackboard_Node" or current_node.serene_info_variable == "BlueROV_Task_Node":
            attempt_to_read_file()
        elif current_node.serene_info_variable == "non_blocking":
            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'leaf',
                'type' : 'node_non_blocking',
                'variables' : [],
                'additional_arguments' : [],
                'additional_definitions' : [],
                'additional_declarations' : [],
                'additional_initializations' : [],
                'additional_modules' : []
            }
        dealt_with = True
    except AttributeError as e:
        dealt_with = False


    try:
        #this attemptys to detect custom blackboard code.
        attempt_to_read_file()
        dealt_with = True
    except Exception:
        dealt_with = False


    

    if dealt_with:
        pass
    elif isinstance(current_node, py_trees.composites.Sequence):
        if current_node.memory:
            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'composite',
                'type' : 'sequence_with_memory',
                'variables' : [],
                'additional_arguments' : [],
                'additional_definitions' : [],
                'additional_declarations' : [],
                'additional_initializations' : [],
                'additional_modules' : []
            }
        else:
            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'composite',
                'type' : 'sequence_without_memory',
                'variables' : [],
                'additional_arguments' : [],
                'additional_definitions' : [],
                'additional_declarations' : [],
                'additional_initializations' : [],
                'additional_modules' : []
            }
    elif isinstance(current_node, py_trees.composites.Selector):
        if current_node.memory:
            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'composite',
                'type' : 'selector_with_memory',
                'variables' : [],
                'additional_arguments' : [],
                'additional_definitions' : [],
                'additional_declarations' : [],
                'additional_initializations' : [],
                'additional_modules' : []
            }
        else:
            nodes[this_id] = {
                'name' : node_name,
                'parent_id' : parent_id,
                'children' : [],
                'category' : 'composite',
                'type' : 'selector_without_memory',
                'variables' : [],
                'additional_arguments' : [],
                'additional_definitions' : [],
                'additional_declarations' : [],
                'additional_initializations' : [],
                'additional_modules' : []
            }
    elif isinstance(current_node, py_trees.composites.Parallel):
        cur_type = 'parallel'
        if current_node.policy.synchronise:
            cur_type += '_synchronized_success_on_all'
            if isinstance(current_node.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                #cur_type += '_success_on_all'
                pass

            elif isinstance(current_node.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                #cur_type += '_success_on_one'
                print('success on one with synchronised does not make sense. defaulted to success on all.')
            else:
                print('ERROR: the following parallel policy is not supported: ' + str(current_node.policy))
                sys.exit('Unsupported Parallel Policy')
        else:
            cur_type += '_unsynchronized'
            if isinstance(current_node.policy, py_trees.common.ParallelPolicy.SuccessOnAll):
                cur_type += '_success_on_all'
            elif isinstance(current_node.policy, py_trees.common.ParallelPolicy.SuccessOnOne):
                cur_type += '_success_on_one'
            else:
                print('ERROR: the following parallel policy is not supported: ' + str(current_node.policy))
                sys.exit('Unsupported Parallel Policy')
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'composite',
            'type' : cur_type,
            'variables' : [],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.Condition):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'condition',
            'variables' : [],
            'additional_arguments' : [current_node.succeed_status.name.lower()],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.Inverter):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'inverter',
            'variables' : [],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.OneShot):
        needed_nodes.add('decorator_one_shot')
        if current_node.policy.name == "ON_SUCCESSFUL_COMPLETION":
            policy = 'TRUE'
        else:
            policy = 'FALSE'
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'one_shot',
            'variables' : [],
            'additional_arguments' : [policy],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    #there's a solid argument for combining all the X is Y types into one module, and just having 2 additional arguments for that module.
    elif isinstance(current_node, py_trees.decorators.FailureIsRunning):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'variables' : [],
            'additional_arguments' : ['failure', 'running'],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.FailureIsSuccess):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'variables' : [],
            'additional_arguments' : ['failure', 'success'],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.RunningIsFailure):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'variables' : [],
            'additional_arguments' : ['running', 'failure'],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.RunningIsSuccess):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'variables' : [],
            'additional_arguments' : ['running', 'success'],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.SuccessIsFailure):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'variables' : [],
            'additional_arguments' : ['success', 'failure'],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.decorators.SuccessIsRunning):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'variables' : [],
            'additional_arguments' : ['success', 'running'],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
    elif isinstance(current_node, py_trees.behaviours.CheckBlackboardVariableExists):
        variable_name = current_node.variable_name
        variable_name = variable_name.replace('.', '_dot_')
        
        if (variable_name in variables):
            variables[variable_name]['always_exist'] = False
            var_num = variables[variable_name]['variable_id']
        else:
            var_num = len(variables)
            variables[variable_name] = {
                'variable_id' : var_num,
                'min_value' : 0,
                'max_value' : 1,
                'init_value' : None,
                'always_exist' : True,
                'init_exist' : True,
                'global_next_mode' : True,
                'global_next_value' : None,
                'global_next_exist' : True,
                'next_value' : {this_id : None},
                'next_exist' : {this_id : True},
                'access' : {this_id}
            }
            
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'check_blackboard_variable_exists',
            'variables' : [],
            'additional_arguments' : ['blackboard', variable_name],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
            
        
    elif isinstance(current_node, py_trees.behaviours.CheckBlackboardVariableValue):
        variable_name = current_node.check.variable
        variable_name = variable_name.replace('.', '_dot_')
        
        if (variable_name in variables):
            var_num = variables[variable_name]['variable_id']
        else:
            var_num = len(variables)
            variables[variable_name] = {
                'variable_id' : var_num,
                'min_value' : 0,
                'max_value' : 1,
                'init_value' : None,
                'always_exist' : True,
                'init_exist' : True,
                'global_next_mode' : True,
                'global_next_value' : None,
                'global_next_exist' : True,
                'next_value' : {this_id : None},
                'next_exist' : {this_id : True},
                'access' : {this_id}
            }
        try:
            rhs = str(int(current_node.check.value))
        except:
            rhs = '0'

        try:
            if current_node.check.operator is operator.eq:
                op = '='
            elif current_node.check.operator is operator.le:
                op = '<='
            elif current_node.check.operator is operator.lt:
                op = '<'
            elif current_node.check.operator is operator.ge:
                op = '>='
            elif current_node.check.operator is operator.gt:
                op = '>'
            elif current_node.check.operator is operator.ne:
                op = '!='
            else:
                op = '='
        except:
            op = '='
            
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'check_blackboard_variable_value',
            'variables' : [],
            'additional_arguments' : [node_name + '_CHECK_' + variable_name],
            'additional_definitions' : [],
            'additional_declarations' : ['\t\t' + node_name + '_CHECK_' + variable_name  + ' : '+ node_name + '_CHECK_' + variable_name + '_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep],
            'additional_initializations' : [],
            'additional_modules' : [
                {
                    'name' : node_name + '_CHECK_' + variable_name + '_module',
                    'type' : 'check',
                    'args' : ['variables', 'variable_exists', 'node_names', 'variable_names'],
                    'use_next' : False,
                    'left_hand_side' : 'variables[variable_names.' + variable_name + ']',
                    'operator' : op,
                    'right_hand_side' : rhs,
                    'variable_name' : variable_name
                }
            ]
        }
        
    elif isinstance(current_node, py_trees.behaviours.CheckBlackboardVariableValues):
        pass
        #leaf_node_exit(this_id)
        #not doing the below right now. it's way too much of a pain. don't know how to deal with operator
    elif isinstance(current_node, py_trees.behaviours.SetBlackboardVariable):
        variable_name = current_node.variable_name
        variable_name = variable_name.replace('.', '_dot_')
        if variable_name in variables:
            variables[variable_name]['access'].add(this_id)
            variables[variable_name]['next_value'][this_id] = None
            var_num = variables[variable_name]['variable_id']
        else:
            var_num = len(variables)
            variables[variable_name] = {
                'variable_id' : var_num,
                'min_value' : 0,
                'max_value' : 1,
                'init_value' : None,
                'always_exist' : True,
                'init_exist' : True,
                'global_next_mode' : True,
                'global_next_value' : None,
                'global_next_exist' : True,
                'next_value' : {this_id : None},
                'next_exist' : {this_id : True},
                'access' : {this_id}
            }

        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'set_blackboard_variables',
            'variables' : [variable_name],
            'additional_arguments' : [node_name + "_STATUS"],
            'additional_definitions' : [],
            'additional_declarations' : ['\t\t' + node_name + '_STATUS : ' + node_name + '_STATUS_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep],
            'additional_initializations' : [],
            'additional_modules' : [
                {
                    'name' : node_name + '_STATUS_module',
                    'type' : 'status',
                    'args' : ['variables', 'variable_exists', 'node_names', 'variable_names'],
                    'possible_values' : ['success', 'failure', 'running'],
                    'initial_value' : None,
                    'next_value' : None
                }
            ]
        }
        
    
    elif isinstance(current_node, py_trees.behaviours.UnsetBlackboardVariable):
        variable_name = current_node.key
        variable_name = variable_name.replace('.', '_dot_')
        if variable_name in variables:
            variables[variable_name]['access'].add(this_id)
            variables[variable_name]['next_value'][this_id] = None
            variables[variable_name]['always_exist'] = False
            variables[variable_name]['next_exist'][this_id] = False
            variables[variable_name]['global_next_exist'] = False
            var_num = variables[variable_name]['variable_id']
        else:
            var_num = len(variables)
            variables[variable_name] = {
                'variable_id' : var_num,
                'min_value' : 0,
                'max_value' : 1,
                'init_value' : None,
                'always_exist' : False,
                'init_exist' : True,
                'global_next_mode' : True,
                'global_next_value' : None,
                'global_next_exist' : False,
                'next_value' : {this_id : None},
                'next_exist' : {this_id : False},
                'access' : {this_id}
            }

        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'unset_blackboard_variables',
            'variables' : [(var_num, variable_name)],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.WaitForBlackboardVariable):
        variable_name = current_node.variable_name
        variable_name = variable_name.replace('.', '_dot_')
        
        if (variable_name in variables):
            variables[variable_name]['always_exist'] = False
            var_num = variables[variable_name]['variable_id']
        else:
            var_num = len(variables)
            variables[variable_name] = {
                'variable_id' : var_num,
                'min_value' : 0,
                'max_value' : 1,
                'init_value' : None,
                'always_exist' : True,
                'init_exist' : True,
                'global_next_mode' : True,
                'global_next_value' : None,
                'global_next_exist' : True,
                'next_value' : {this_id : None},
                'next_exist' : {this_id : True},
                'access' : {this_id}
            }
            
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'wait_for_blackboard_variable',
            'variables' : [],
            'additional_arguments' : ['blackboard', var_num],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
            
        
    elif isinstance(current_node, py_trees.behaviours.WaitForBlackboardVariableValue):
        variable_name = current_node.check.variable
        variable_name = variable_name.replace('.', '_dot_')
        if (variable_name in variables):
            var_num = variables[variable_name]['variable_id']
        else:
            var_num = len(variables)
            variables[variable_name] = {
                'variable_id' : var_num,
                'min_value' : 0,
                'max_value' : 1,
                'init_value' : None,
                'always_exist' : True,
                'init_exist' : True,
                'global_next_mode' : True,
                'global_next_value' : None,
                'global_next_exist' : True,
                'next_value' : {},
                'next_exist' : {},
                'access' : {}
            }
        try:
            rhs = str(int(current_node.check.value))
        except:
            rhs = '0'

        try:
            if current_node.check.operator is operator.eq:
                op = ' = '
            elif current_node.check.operator is operator.le:
                op = ' <= '
            elif current_node.check.operator is operator.lt:
                op = ' < '
            elif current_node.check.operator is operator.ge:
                op = ' >= '
            elif current_node.check.operator is operator.gt:
                op = ' > '
            elif current_node.check.operator is operator.ne:
                op = ' != '
            else:
                op = ' = '
        except:
            op = ' = '
            
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'wait_for_blackboard_variable_value',
            'variables' : [],
            'additional_arguments' : ['blackboard', str(var_num), '\t\t' + node_name + '_CHECK_' + variable_name],
            'additional_definitions' : [],
            'additional_declarations' : ['\t\t' + node_name + '_CHECK_' + variable_name  + ' : '+ node_name + '_CHECK_' + variable_name + '_module(blackboard.variables, blackboard.variable_exists, node_names, variable_names);' + os.linesep],
            'additional_initializations' : [],
            'additional_modules' : [
                {
                    'name' : node_name + '_CHECK_' + variable_name + '_module',
                    'type' : 'check', 
                    'args' : ['variables', 'variable_exists', 'node_names', 'variable_names'],
                    'variable_name' : variable_name,
                    'left_hand_side' : 'variables[variable_names.' + variable_name + ']',
                    'operator' : op,
                    'right_hand_side' : rhs,
                    'variable_name' : variable_name
                }
            ]
        }
        
    elif isinstance(current_node, py_trees.behaviours.Count):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'count',
            'variables' : [],
            'additional_arguments' : [str(current_node.fail_until), str(current_node.running_until), str(current_node.success_until), str(current_node.reset).upper()],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.Failure):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'failure',
            'variables' : [],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.Periodic):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'periodic',
            'variables' : [],
            'additional_arguments' : [str(current_node.period)],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.Running):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'running',
            'variables' : [],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.StatusSequence):
        sequence_definition = "\t\tsequence_for_" + node_name + '_' + str(this_id) + " := " + str(current_node.sequence) + ";" + os.linesep
        if current_node.eventually is None:
            eventually = 'invalid'
        else:
            eventually = current_node.eventually.name.lower()
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'status_sequence',
            'variables' : [],
            'additional_arguments' : ['sequence_for_' + node_name + '_' + str(this_id), str(len(current_node.sequence)), eventually],
            'additional_definitions' : [sequence_definition],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.Success):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'success',
            'variables' : [],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.SuccessEveryN):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'success_every_n',
            'variables' : [],
            'additional_arguments' : [str(current_node.every_n)],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.behaviours.TickCounter):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'tick_counter',
            'variables' : [],
            'additional_arguments' : [str(current_node.duration), current_node.completion_status.name.lower()],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    elif isinstance(current_node, py_trees.timers.Timer):
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'timer',
            'variables' : [],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        
    else:#currently defaulting to default. will rework this later probably
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'default',
            'variables' : [],
            'additional_arguments' : [],
            'additional_definitions' : [],
            'additional_declarations' : [],
            'additional_initializations' : [],
            'additional_modules' : []
        }
        

    if nodes[this_id]['type'] == 'leaf':
        pass
    else:
        for child in current_node.children:
            next_available_id = walk_tree_recursive(child, this_id, next_available_id, nodes, node_names,  variables)
    return next_available_id


"""
does not return anything. simply modifies the existing structures.
this segment is to detect and create sub-variables
i.e., if a variable in the original was just "meh = Object"
but other places use meh.val1, meh.val2, etc, then the original "meh" needs to handle those.
"""
def variable_name_cleanup(nodes, variables):
    #print(variables)
    for variable in variables:
        #print(variable)
        variable_regex = re.compile(r""+variable+"_dot_")#if out variable is meh, we are now matching meh_dot_
        for child_variable in variables:
            if variable_regex.match(child_variable):#if this is true, then is means we are looking at meh_dot_something
                for access_node in variables[variable]['access']:#we are now going to tell everything that can change meh, that it can change meh_dot_something
                    nodes[access_node]['variables'].append((variables[child_variable]['variable_id'], child_variable))#told the node it can access this variable
                    variables[child_variable]['access'].add(access_node)#told the variable it can be accessed by this node
                    variables[child_variable]['next_value'][access_node] = None#updated what the next value for this specific node is
                    variables[child_variable]['next_exist'][access_node] = True #updated what the next exist value is for this specific node


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('root_file')
    arg_parser.add_argument('root_method')
    arg_parser.add_argument('--root_args', default='', nargs='*')
    arg_parser.add_argument('--string_args', default='', nargs='*')
    arg_parser.add_argument('--output_file', default = None)
    args=arg_parser.parse_args()

    if '/' in args.root_file:
        sys.path.append( re.sub(r'/[^/]*$', '', args.root_file))
        args.root_file = re.sub(r'.*/', '', args.root_file)
        #print(args.root_file)

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
    walk_tree(root, args.output_file)

main()
