import inspect
import re

blackboard_name_pattern = re.compile(r'#*(?P<blackboard_name>[^\s= ]+)'
                                     r'\s*= \s*'
                                     r'py_trees\.blackboard\.Blackboard\(\s*\)')


def attempt_to_find_variables(node):
    """
    return: True if success, False otherwise.
    arguments: none
    This method uses nodes, variables, and this_id in order to check
    if a file exists with a custom definition. If such a file exists,
    then we attempt to parse it to determine blackboard variable info.
    """
    # nonlocal nodes, variables, this_id
    # the nonlocal explicitly doesn't work with python2, and I don't
    # think it's actually necessary in the python3 version, since
    # nothing is actually assigned, just referenced
    try:
        # this is to catch attribute exceptions
        try:
            # this is a backup try in case we fail to get the file
            # then we attempt to get source
            try:
                # this try corresponds to the attempt
                # to actually get the file and read it
                file_name = inspect.getfile(node.__class__)
                with open(file_name, 'r') as f:
                    code = f.read()
            except (FileNotFoundError, TypeError):
                code = inspect.getsource(node.__class__)
        except OSError:
            # we couldn't get the code, return False
            return {}

        # code acquired, at this point we will either succeed
        # or we will run into something like an attribute error
        # and trigger an exception causing a false return.

        blackboard_match = blackboard_name_pattern.search(code)
        local_variables = []
        if blackboard_match:
            blackboard_name = \
                blackboard_match.groupdict()['blackboard_name'].strip()
            variable_name_pattern = re.compile(r'#*\s*' + blackboard_name
                                               + r'\.'
                                               r'(?P<variable_name>[_a-zA-Z][\w\.]+)')
            start_loc = 0
            done = False
            local_variable_set = set()
            while not done:
                variable_match = variable_name_pattern.search(code, start_loc)
                if variable_match:
                    start_loc = variable_match.span()[1]
                    variable_name = variable_match.groupdict()['variable_name'].strip()
                    variable_name = variable_name.replace('.', '_dot_')
                    if variable_name in local_variable_set:
                        # already dealt with
                        continue
                    else:
                        local_variable_set.add(variable_name)
                    if variable_name in variables:
                        var_num = variables[variable_name]['variable_id']
                        variables[variable_name]['next_exist'][node_name] = True
                        variables[variable_name]['stages'].append(node_name)
                    else:
                        var_num = len(variables)
                        variables[variable_name] = {
                            'variable_id' : var_num,
                            'variable_name' : variable_name,
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
                            'next_exist' : {node_name : True},
                            'use_separate_stages' : False,
                            'stages' : [node_name]
                        }
                    local_variables.append(variable_name)
                else:
                    done = True
        else:
            # if we don't find blackboard info, then just continue normally. don't use this.
            return False
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'set_blackboard_variables',
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : [node_name + "_STATUS"],
            'additional_definitions' : [],
            'additional_declarations' : [
                '\t\t' + node_name + '_STATUS : '
                + node_name
                + '_STATUS_module(blackboard, node_names);'
                + os.linesep],
            'additional_initializations' : [],
            'additional_modules' : {
                'status' : {
                    'name' : node_name + '_STATUS_module',
                    'type' : 'status',
                    'args' : ['blackboard', 'node_names'],
                    # 'possible_values' : ['success', 'failure', 'running'],
                    'initial_value' : None,
                    'current_value' : None,
                    'next_value' : None
                }
            }
        }
        return True
    except AttributeError:
        return False


def attempt_to_read_file(node):
    """
    return: True if success, False otherwise.
    arguments: none
    This method uses nodes, variables, and this_id in order to check
    if a file exists with a custom definition. If such a file exists,
    then we attempt to parse it to determine blackboard variable info.
    """
    # nonlocal nodes, variables, this_id
    # the nonlocal explicitly doesn't work with python2, and I don't
    # think it's actually necessary in the python3 version, since
    # nothing is actually assigned, just referenced
    try:
        # this is to catch attribute exceptions
        try:
            # this is a backup try in case we fail to get the file
            # then we attempt to get source
            try:
                # this try corresponds to the attempt
                # to actually get the file and read it
                file_name = inspect.getfile(node.__class__)
                with open(file_name, 'r') as f:
                    code = f.read()
            except (FileNotFoundError, TypeError):
                code = inspect.getsource(node.__class__)
        except OSError:
            # we couldn't get the code, return False
            return False

        # code acquired, at this point we will either succeed
        # or we will run into something like an attribute error
        # and trigger an exception causing a false return.

        blackboard_match = blackboard_name_pattern.search(code)
        local_variables = []
        if blackboard_match:
            blackboard_name = \
                blackboard_match.groupdict()['blackboard_name'].strip()
            variable_name_pattern = re.compile(r'#*\s*' + blackboard_name
                                               + r'\.'
                                               r'(?P<variable_name>[_a-zA-Z][\w\.]+)')
            start_loc = 0
            done = False
            local_variable_set = set()
            while not done:
                variable_match = variable_name_pattern.search(code, start_loc)
                if variable_match:
                    start_loc = variable_match.span()[1]
                    variable_name = variable_match.groupdict()['variable_name'].strip()
                    variable_name = variable_name.replace('.', '_dot_')
                    if variable_name in local_variable_set:
                        # already dealt with
                        continue
                    else:
                        local_variable_set.add(variable_name)
                    if variable_name in variables:
                        var_num = variables[variable_name]['variable_id']
                        variables[variable_name]['next_exist'][node_name] = True
                        variables[variable_name]['stages'].append(node_name)
                    else:
                        var_num = len(variables)
                        variables[variable_name] = {
                            'variable_id' : var_num,
                            'variable_name' : variable_name,
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
                            'next_exist' : {node_name : True},
                            'use_separate_stages' : False,
                            'stages' : [node_name]
                        }
                    local_variables.append(variable_name)
                else:
                    done = True
        else:
            # if we don't find blackboard info, then just continue normally. don't use this.
            return False
        nodes[this_id] = {
            'name' : node_name,
            'parent_id' : parent_id,
            'children' : [],
            'category' : 'leaf',
            'type' : 'set_blackboard_variables',
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : [node_name + "_STATUS"],
            'additional_definitions' : [],
            'additional_declarations' : [
                '\t\t' + node_name + '_STATUS : '
                + node_name
                + '_STATUS_module(blackboard, node_names);'
                + os.linesep],
            'additional_initializations' : [],
            'additional_modules' : {
                'status' : {
                    'name' : node_name + '_STATUS_module',
                    'type' : 'status',
                    'args' : ['blackboard', 'node_names'],
                    # 'possible_values' : ['success', 'failure', 'running'],
                    'initial_value' : None,
                    'current_value' : None,
                    'next_value' : None
                }
            }
        }
        return True
    except AttributeError:
        return False
