import argparse
import pprint
import copy
# ----------------------------------------------------------------------------------------------------------------
# todo: add a way to delete variables and change access


def create_stages(variable, variables, node_name_to_id):
    prev_stage_name = variable['variable_name']
    for stage_count in range(1, len(variable['stages']) + 1):
        stage_start = variable['stages'][stage_count - 1]
        try:
            stage_end = variable['stages'][stage_count]
        except KeyError:
            stage_end = len(node_name_to_id)
        variable_name = variable['variable_name'] + "_stage_" + str(stage_count)
        variable_number = len(variables)
        variables[variable_name] = copy.deepcopy(variable)
        variables[variable_name]['variable_name'] = variable_name
        variables[variable_name]['variable_id'] = variable_number
        new_access = set()
        for access_node_name in variables[variable_name]['access']:
            access_node_id = node_name_to_id[access_node_name]
            if stage_start <= access_node_id and access_node_id <= stage_end:
                new_access.add(access_node_name)
        variables[variable_name]['access'] = new_access
        variables[variable_name]['next_stage'] = None
        variables[prev_stage_name]['next_stage'] = variable_name
        variables[variable_name]['prev_stage'] = prev_stage_name

        prev_stage_name = variable_name
    new_access = set()
    stage_start = 0
    stage_end = variable['stages'][0]
    for access_node_name in variable['access']:
        access_node_id = node_name_to_id[access_node_name]
        if stage_start <= access_node_id and access_node_id <= stage_end:
            new_access.add(access_node_name)
    variable['access'] = new_access
    variable['prev_stage'] = None
    variable['last_stage'] = prev_stage_name
    # variable['next_value'] = [('TRUE', prev_stage_name)]
    # this is going to be handled in node_creator


def delete_stages(variable, variables):
    name_to_pop = variable['next_stage']
    while name_to_pop:
        popped = variables.pop(name_to_pop)
        name_to_pop = popped['next_stage']
        variable['access'].union(popped['access'])


def arg_modification(args, nodes, variables, node_name_to_id):
    if args.use_stages:
        variable_name_list = list(variables.keys())
        for variable_name in variable_name_list:
            variable = variables[variable_name]
            variable['use_stages'] = True
            try:
                if variable['next_stage'] in variables:
                    continue
            except KeyError:
                pass
            create_stages(variable, variables, node_name_to_id)
    if args.no_stages:
        variable_name_list = list(variables.keys())
        for variable_name in variable_name_list:
            variable = variables[variable_name]
            variable['use_stages'] = False
            delete_stages(variable, variables)
    for variable_name in variables:
        variable = variables[variable_name]
        if args.min_value:
            variable['min_val'] = int(args.min_value)
        if args.max_value:
            variable['max_val'] = int(args.max_value)
        if args.init_value:
            variable['init_val'] = int(args.init_value)
        if args.no_init_value:
            variable['init_val'] = None
        if args.always_exist:
            variable['always_exist'] = True
        if args.sometimes_exist:
            variable['always_exist'] = False
        if args.init_exist:
            variable['init_exist'] = bool(args.init_exist)
        if args.no_init_exist:
            variable['init_exist'] = None
        if args.next_exist:
            variable['next_exist'] = bool(args.next_exist)
        if args.no_next_exist:
            variable['no_next_exist'] = None
        if args.variables_auto_stay:
            variable['auto_change'] = False
        if args.variables_auto_change:
            variable['auto_change'] = True

    for node_id in nodes:
        node = nodes[node_id]
        if args.force_parallel_unsynch:
            if (((node['category'] == 'composite'
                  and 'parallel_synchronized' in node['type']))):
                node['type'] = node['type'].replace('_synchronized',
                                                    '_unsynchronized')
                node['type'] = node['type'].replace('success_on_one',
                                                    'success_on_all')
        if args.force_parallel_synch:
            if (((node['category'] == 'composite'
                  and 'parallel_unsynchronized' in node['type']))):
                node['type'] = node['type'].replace('_unsynchronized',
                                                    '_synchronized')
        if args.force_selector_memory:
            if (((node['category'] == 'composite'
                  and 'selector_without_memory' == node['type']))):
                node['type'] = 'selector_with_memory'
        if args.force_selector_memoryless:
            if (((node['category'] == 'composite'
                  and 'selector_with_memory' == node['type']))):
                node['type'] = 'selector_without_memory'
        if args.force_sequence_memory:
            if (((node['category'] == 'composite'
                  and 'sequence_without_memory' == node['type']))):
                node['type'] = 'sequence_with_memory'
        if args.force_sequence_memoryless:
            if (((node['category'] == 'composite'
                  and 'sequence_with_memory' == node['type']))):
                node['type'] = 'sequence_without_memory'
        if args.use_next_checks:
            if node['type'] == 'check_blackboard_variable_value':
                for module_sig in node['additional_modules']:
                    node['additional_modules'][module_sig]['use_next'] = True
        if args.use_current_checks:
            if node['type'] == 'check_blackboard_variable_value':
                for module_sig in node['additional_modules']:
                    node['additional_modules'][module_sig]['use_next'] = False
        if args.best_guess_checks:
            best_guess(node, node_id, variables)


def best_guess(node, node_id, variables):
    if node['type'] == 'check_blackboard_variable_value':
        for module_sig in node['additional_modules']:
            module = node['additional_modules'][module_sig]
            variable = variables[module['variable_name']]
            try:
                if node_id < variable['stages'][0]:
                    node['additional_modules'][module_sig]['use_next'] = False
                else:
                    node['additional_modules'][module_sig]['use_next'] = True
            except KeyError:
                node['additional_modules'][module_sig]['use_next'] = False


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_file')
    arg_parser.add_argument('--output_file', default = None)

    arg_parser.add_argument('--interactive_mode',
                            action = 'store_true')
    arg_parser.add_argument('--instruction_file',
                            default = None)

    arg_parser.add_argument('--force_parallel_unsynch',
                            action = 'store_true')
    arg_parser.add_argument('--force_parallel_synch',
                            action = 'store_true')
    arg_parser.add_argument('--force_selector_memory',
                            action = 'store_true')
    arg_parser.add_argument('--force_selector_memoryless',
                            action = 'store_true')
    arg_parser.add_argument('--force_sequence_memory',
                            action = 'store_true')
    arg_parser.add_argument('--force_sequence_memoryless',
                            action = 'store_true')
    arg_parser.add_argument('--use_next_checks',
                            action = 'store_true')
    arg_parser.add_argument('--use_current_checks',
                            action = 'store_true')
    arg_parser.add_argument('--best_guess_checks',
                            action = 'store_true')

    arg_parser.add_argument('--min_value',
                            default = None)
    arg_parser.add_argument('--max_value',
                            default = None)
    arg_parser.add_argument('--init_value',
                            default = None)
    arg_parser.add_argument('--no_init_value',
                            action = 'store_true')
    arg_parser.add_argument('--always_exist',
                            action = 'store_true')
    arg_parser.add_argument('--sometimes_exist',
                            action = 'store_true')
    arg_parser.add_argument('--init_exist',
                            default = None)
    arg_parser.add_argument('--no_init_exist',
                            action = 'store_true')
    arg_parser.add_argument('--next_exist',
                            default = None)
    arg_parser.add_argument('--no_next_exist',
                            action = 'store_true')
    arg_parser.add_argument('--variables_auto_stay',
                            action = 'store_true')
    arg_parser.add_argument('--variables_auto_change',
                            action = 'store_true')
    arg_parser.add_argument('--use_stages',
                            action = 'store_true')
    arg_parser.add_argument('--no_stages',
                            action = 'store_true')

    args = arg_parser.parse_args()

    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']

    node_name_to_id = {}
    for node_id in nodes:
        # print(node_id)
        node_name_to_id[nodes[node_id]['name']] = node_id

    if (((args.force_parallel_synch
          or args.force_parallel_unsynch
          or args.force_selector_memory
          or args.force_selector_memoryless
          or args.force_sequence_memory
          or args.force_sequence_memoryless
          or args.min_value
          or args.max_value
          or args.init_value
          or args.no_init_value
          or args.always_exist
          or args.sometimes_exist
          or args.init_exist
          or args.no_init_exist
          or args.next_exist
          or args.no_next_exist
          or args.variables_auto_stay
          or args.variables_auto_change
          or args.use_stages
          or args.no_stages
          or args.best_guess_checks))):
        arg_modification(args, nodes, variables, node_name_to_id)

    # deletions = False
    if args.interactive_mode:
        done = False
        while not done:
            modify_nodes = input("Modify nodes? (Enter y for yes, n for no)")
            if modify_nodes == "y":
                done = True
                for node_id in nodes:
                    done2 = False
                    while not done2:
                        print(nodes[node_id])
                        modify_node = input("Modify this node?"
                                            + " (Enter y for yes, n for no)")
                        if modify_node == 'y':
                            modify_key = input("Enter key to modify: ")
                            try:
                                print("current value: "
                                      + str(nodes[node_id][modify_key]))
                                modify_value = input("Enter new value: ")
                                nodes[node_id][modify_key] = modify_value
                            except KeyError:
                                print(modify_key + " is not a valid key")
                        elif modify_node == 'n':
                            done2 = True
                        else:
                            print('input was not y or n')
            elif modify_nodes == "n":
                done = True
            else:
                print('input was not y or n')

        done = False
        while not done:
            modify_variables = input("Modify variables?"
                                     + "(Enter y for yes, n for no)")
            if modify_variables == "y":
                done = True
                for variable_name in variables:
                    done2 = False
                    while not done2:
                        print(variable_name)
                        print(variables[variable_name])
                        modify_variable = input("Modify this variable? "
                                                + "(Enter y for yes, n for no)")
                        if modify_variable == 'y':
                            modify_key = input("Enter key to modify: ")
                            modify_key = modify_key.strip()
                            if modify_key == 'delete':
                                variable = variables.pop(variable_name)
                                for node_name in variable['access']:
                                    nodes[node_name_to_id[node_name]]['variables'].remove(variable_name)
                                # deletions = True
                            else:
                                try:
                                    print("current value: "
                                          + str(variables[variable_name][modify_key]))
                                    modify_value = input("Enter new value: ")
                                    variables[variable][modify_key] = modify_value
                                except KeyError:
                                    print(modify_key + " is not a valid key")
                        elif modify_variable == 'n':
                            done2 = True
                        else:
                            print('input was not y or n')
            elif modify_variables == "n":
                done = True
            else:
                print('input was not y or n')

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--force_parallel_unsynch',
                            action = 'store_true')
    arg_parser.add_argument('--force_parallel_synch',
                            action = 'store_true')
    arg_parser.add_argument('--force_selector_memory',
                            action = 'store_true')
    arg_parser.add_argument('--force_selector_memoryless',
                            action = 'store_true')
    arg_parser.add_argument('--force_sequence_memory',
                            action = 'store_true')
    arg_parser.add_argument('--force_sequence_memoryless',
                            action = 'store_true')
    arg_parser.add_argument('--use_next_checks',
                            action = 'store_true')
    arg_parser.add_argument('--use_current_checks',
                            action = 'store_true')
    arg_parser.add_argument('--best_guess_checks',
                            action = 'store_true')

    arg_parser.add_argument('--min_value',
                            default = None)
    arg_parser.add_argument('--max_value',
                            default = None)
    arg_parser.add_argument('--init_value',
                            default = None)
    arg_parser.add_argument('--no_init_value',
                            action = 'store_true')
    arg_parser.add_argument('--always_exist',
                            action = 'store_true')
    arg_parser.add_argument('--sometimes_exist',
                            action = 'store_true')
    arg_parser.add_argument('--init_exist',
                            default = None)
    arg_parser.add_argument('--no_init_exist',
                            action = 'store_true')
    arg_parser.add_argument('--next_exist',
                            default = None)
    arg_parser.add_argument('--no_next_exist',
                            action = 'store_true')
    arg_parser.add_argument('--variables_auto_stay',
                            action = 'store_true')
    arg_parser.add_argument('--variables_auto_change',
                            action = 'store_true')
    arg_parser.add_argument('--use_stages',
                            action = 'store_true')
    arg_parser.add_argument('--no_stages',
                            action = 'store_true')

    if args.instruction_file:
        modifications = []
        with open(args.instruction_file, 'r') as f:
            modifications = eval(f.read())
        for modification in modifications:
            if modification['target'].strip().lower() == 'global_flags':
                args2 = arg_parser.parse_args(modification['instructions'])
                arg_modification(args2, nodes, variables, node_name_to_id)
            elif modification['target'].strip().lower() == 'variable':
                try:
                    if modification['delete']:
                        variable = variables.pop(modification['name'])
                        delete_stages(variable, variables)
                except KeyError:
                    try:
                        if modification['create']:
                            variables[modification['name']] = {
                                'variable_id' : -1,
                                'variable_name' : modification['name'],
                                'non-variable' : False,
                                'mode' : 'VAR',
                                'custom_value_range' : None,
                                'min_value' : 0,
                                'max_value' : 1,
                                'init_value' : None,
                                'always_exist' : True,
                                'init_exist' : True,
                                'auto_change' : False,
                                'next_value' : None,
                                'next_exist' : {},
                                'access' : {},
                                'use_stages' : False,
                                'stages' : []
                            }
                    except KeyError:
                        pass
                    finally:
                        # print('modded variable: ' + modification['name'])
                        try:
                            instructions = modification['instructions']
                            for key_to_mod in instructions:
                                if key_to_mod.strip() == "use_stages":
                                    if instructions[key_to_mod.strip()]:
                                        variable = variables[modification['name']]
                                        variable['use_stages'] = True
                                        try:
                                            if variable['next_stage'] in variables:
                                                continue
                                        except KeyError:
                                            pass
                                        create_stages(variable, variables, node_name_to_id)
                                    else:
                                        variable = variables[modification['name']]
                                        variable['use_stages'] = False
                                        delete_stages(variable, variables)
                                elif key_to_mod.strip() in variables[modification['name']]:
                                    variables[modification['name']][key_to_mod.strip()] = instructions[key_to_mod.strip()]
                                else:
                                    print("unknown modification key while trying to modify variables. Variable: " + modification['name'] + ". Key: " + str(key_to_mod))
                        except KeyError:
                            pass
            elif modification['target'].strip().lower() == 'node':
                instructions = modification['instructions']
                for key_to_mod in instructions:
                    # TODO-add best guess here, and also fix this.
                    key_to_mod_list = key_to_mod.split('::')
                    to_modify = nodes[node_name_to_id[modification['name']]]
                    final_key = key_to_mod_list.pop().strip()
                    for key in key_to_mod_list:
                        to_modify = to_modify[key.strip()]
                    to_modify[final_key] = instructions[key_to_mod]
            else:
                print('modification file contains '
                      + 'unknown modification target: '
                      + str(modification['target']))
        pass

    count = 0
    for variable_name in variables:
        if variables[variable_name]['non-variable']:
            variables[variable_name]['variable_id'] = -1
        else:
            variables[variable_name]['variable_id'] = count
            count = count + 1
        if variables[variable_name]['use_stages']:
            if variables[variable_name]['next_stage']:
                variables[variables[variable_name]['next_stage']]['min_value'] = variables[variable_name]['min_value']
                variables[variables[variable_name]['next_stage']]['max_value'] = variables[variable_name]['max_value']
                variables[variables[variable_name]['next_stage']]['init_value'] = variables[variable_name]['init_value']
                variables[variables[variable_name]['next_stage']]['custom_value_range'] = variables[variable_name]['custom_value_range']

    if args.output_file:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4,
                                           sort_dicts = False, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False)
        printer.pprint({'nodes' : nodes, 'variables' : variables})


main()
