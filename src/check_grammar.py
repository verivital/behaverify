'''
This module is for internal use with BehaVerify.
It is used to verify that the provided DSL file is reasonable.
It contains a variety of utility functions.


Author: Serena Serafina Serbinowska
Last Edit: 2023-11-09
'''
import itertools
import re
import sys
from os.path import isfile
import textx
from serene_functions import build_meta_func
from behaverify_common import (create_node_name,
                               BTreeException,
                               handle_constant_or_reference,
                               resolve_potential_reference,
                               resolve_potential_reference_no_type,
                               constant_type,
                               dummy_value,
                               variable_type,
                               is_local,
                               is_env,
                               is_blackboard,
                               variable_scope,
                               is_array,
                               str_format)

# TODO : function category (TL/INVAR/reg) - DONE?
# TODO : node_types (idk what this means)
# TODO : instant declarations
# TODO : array updates
# TODO : read at/node_name in functions
# TODO : confirm enumerations are being enforced
# todo : make sure loop variables don't conflict
# todo : make sure define variables are deterministicly updated.

def validate_model(metamodel_file, model_file, recursion_limit):
    '''used to validate the model'''
    trace = []
    function_type_info = {
        'if' : {'return_type' : 'depends', 'min_arg' : 3, 'max_arg' : 3, 'arg_type' : 'any', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'loop' : {'return_type' : 'depends', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'any', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'abs' : {'return_type' : 'NUM', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'max' : {'return_type' : 'NUM', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'min' : {'return_type' : 'NUM', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        # 'sin' : serene_functions.serene_sin,
        # 'cos' : serene_functions.serene_cos,
        # 'tan' : serene_functions.serene_tan,
        # 'ln' : serene_functions.serene_log,
        'eq' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'depends', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'neq' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'depends', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'lt' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'gt' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'lte' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'gte' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'neg' : {'return_type' : 'NUM', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'add' : {'return_type' : 'NUM', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'sub' : {'return_type' : 'NUM', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'mult' : {'return_type' : 'NUM', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'idiv' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'mod' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'rdiv' : {'return_type' : 'NUM', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'floor' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'NUM', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'count' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : -1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
        'index' : {'return_type' : 'depends', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},

        'not' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'and' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'or' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'xor' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'xnor' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'implies' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
        'equivalent' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},

        'active' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},
        'success' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},
        'running' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},
        'failure' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},

        'exists_globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
        'exists_next' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
        'exists_finally' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
        'exists_until' :  {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
        'always_globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
        'always_next' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
        'always_finally' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
        'always_until' :  {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},

        'next' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'globally_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'finally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'finally_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'until' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'until_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'release' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'release_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'previous' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'not_previous_not' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'historically' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'historically_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'once' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'once_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'since' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'since_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'triggered' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
        'triggered_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}}
    }
    def validate_name(name):
        if name in declared_enumerations or name in all_node_names or name in variables or name in constants or name in loop_references:
            raise BTreeException(trace, 'Name ' + name + ' clashes with an existing name')

    def verify_min_max(min_code, max_code, bound):
        min_func = build_meta_func(min_code)
        max_func = build_meta_func(max_code)
        min_values = min_func((constants, loop_references))
        max_values = max_func((constants, loop_references))
        if len(min_values) != 1:
            raise BTreeException(trace, 'Must have exactly one value for min')
        if len(max_values) != 1:
            raise BTreeException(trace, 'Must have exactly one value for max')
        min_val = min_values[0]
        max_val = max_values[0]
        (min_class, min_type, min_val) = resolve_potential_reference(min_val, declared_enumerations, all_node_names, variables, constants, loop_references)
        if min_class != 'CONSTANT' or min_type != 'INT':
            raise BTreeException(trace, 'Min value must be a constant of type INT. Got: ' + min_class + ', ' + min_type + ', ' + str(min_val))
        if bound and max_val == '+oo':
            max_class = 'CONSTANT'
            max_type = 'INT'
            max_val = min_val + 1
        else:
            (max_class, max_type, max_val) = resolve_potential_reference(max_val, declared_enumerations, all_node_names, variables, constants, loop_references)
        if max_class != 'CONSTANT' or max_type != 'INT':
            raise BTreeException(trace, 'Max value must be a constant of type INT (or +oo for bound). Got: ' + max_class + ', ' + max_type + ', ' + str(max_val))
        if min_val > max_val:
            raise BTreeException(trace, 'min of bound statement cannot be greater than max')
        return ((min_type, min_val), (max_type, max_val))

    def var_checks(code, variable, scopes, variable_names):
        var_scope = variable_scope(variable)
        if var_scope not in scopes:
            raise BTreeException(trace, 'Expected a variable in one of the following scopes: [' + ', '.join(scopes) + '] but got ' + variable.name + ' in scope ' + var_scope)
        if var_scope != 'environment':
            if variable_names is not None:
                if variable.name not in variable_names:
                    raise BTreeException(trace, 'Expected only the following variables: [' + ', '.join(variable_names) + '] but got ' + variable.name)
        if var_scope == 'local':
            if code.node_name is not None:
                node_func = build_meta_func(code.node_name)
                node_name_vals = node_func((constants, loop_references))
                if len(node_name_vals) != 1:
                    raise BTreeException(trace, 'Expected exactly one node reference')
                if node_name_vals[0] not in all_node_names:
                    raise BTreeException(trace, 'Reference to a node that does not exist (maybe it was renamed): ' + node_name_vals[0])
                # TODO: add a check here which confirms that the node actually uses the local variable.
                # this will prevent the user from specificying a specification using a node that doesn't have this variable.
            else:
                # TODO: double check, we should make sure we're in a node doing this, and not from invar, and that the node uses the variable
                pass
        # todo: confirm read_at and trace_num are correct.
        return

    def validate_code(code, scopes, variable_names, allowed_functions):

        if code.atom is not None:
            (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, all_node_names, variables, constants, loop_references)
            if atom_class == 'CONSTANT':
                return [(atom_type, 'constant', str_format(atom))]
            if atom_class == 'NODE':
                raise BTreeException(trace, 'Received a node where it was not expected: ' + str(atom))
            var_checks(code, atom, scopes, variable_names)
            if is_array(atom):
                raise BTreeException(trace, 'Variable ' + atom.name + ' is an array but appears without being indexed')
            if require_trace_identifier == (code.trace_num is None):
                #print(require_trace_identifier)
                #print(code.trace_num)
                raise BTreeException(trace, 'Variable ' + atom.name + ' is being referenced ' + ('without' if require_trace_identifier else 'with') + ' a trace identifier.')
            return [(atom_type, 'variable', atom.name)]
        if code.code_statement is not None:
            return validate_code(code.code_statement, scopes, variable_names, allowed_functions)
        if code.function_call.function_name not in function_type_info:
            raise BTreeException(trace, 'Function ' + code.function_call.function_name + ' is not yet supported')
        func_info = function_type_info[code.function_call.function_name]
        if len(func_info['allowed_in'].intersection(allowed_functions)) == 0:
            raise BTreeException(trace, 'Function ' + code.function_call.function_name + ' is only allowed in ' + str(func_info['allowed_in']) + ' but we are in ' + str(allowed_functions))
        new_allowed_functions = func_info['allows'].intersection(allowed_functions)
        if code.function_call.function_name == 'if':
            if len(code.function_call.values) != 3:
                raise BTreeException(trace, 'if requires exactly 3 arguments')
            validate_condition(code.function_call.values[0], scopes, variable_names, allowed_functions)
            return_vals1 = validate_code(code.function_call.values[1], scopes, variable_names, allowed_functions)
            return_vals2 = validate_code(code.function_call.values[2], scopes, variable_names, allowed_functions)
            if len(return_vals1) != 1 or len(return_vals2) != 1:
                raise BTreeException(trace, 'currently, if must return exactly 1 argument (encoding issues down the line require this)')
            # we don't have a good way to verify that both halves work.
            # we could require that they be the same types?
            # TODO: think about this.
            return return_vals1
        if code.function_call.function_name == 'loop':
            loop_variable = code.function_call.loop_variable
            validate_name(loop_variable)
            return_vals = []
            all_domain_values = []
            if code.function_call.min_val is None:
                for domain_code in code.function_call.loop_variable_domain:
                    try:
                        domain_func = build_meta_func(domain_code)
                        # new_references = copy.deepcopy(loop_references)  # the meta function is guaranteed to not change this.
                        for domain_value in domain_func((constants, loop_references)):
                            all_domain_values.append(resolve_potential_reference(domain_value, declared_enumerations, all_node_names, variables, constants, loop_references)[2])
                    except Exception as error:
                        raise BTreeException(trace, 'Unknown error') from error
            else:
                ((_, min_val), (_, max_val)) = verify_min_max(code.function_call.min_val, code.function_call.max_val, False)
                all_domain_values = range(min_val, max_val + 1)
            cond_func = build_meta_func(code.function_call.loop_condition)
            for domain_member in all_domain_values:
                loop_references[loop_variable] = domain_member
                returned_vals = cond_func((constants, loop_references))
                if len(returned_vals) != 1:
                    raise BTreeException(trace, 'Loop Condition function is expected to return exactly 1 value')
                if returned_vals[0]:
                    return_vals.extend(validate_code(code.function_call.values[0], scopes, variable_names, allowed_functions))
                loop_references.pop(loop_variable)
            return return_vals
        # handle index specially, and return.
        if code.function_call.function_name == 'index':
            to_index_func = build_meta_func(code.function_call.to_index)
            indexed_vars = to_index_func((constants, loop_references))
            if len(indexed_vars) != 1:
                raise BTreeException(trace, 'Expected exactly 1 variable to index')
            (atom_class, atom_type, atom) = resolve_potential_reference(indexed_vars[0], declared_enumerations, all_node_names, variables, constants, loop_references)
            if atom_class != 'VARIABLE':
                raise BTreeException(trace, 'You can only index variables')
            var_checks(code.function_call, atom, scopes, variable_names)
            if len(code.function_call.values) != 1:
                raise BTreeException(trace, 'Index into variable ' + code.function_call.variable.name + ' should have exactly 1 argument')
            if code.function_call.constant_index == 'constant_index':
                index_func = build_meta_func(code.function_call.values[0])
                returned_vals = index_func((constants, loop_references))
                cur_arg_type = resolve_potential_reference(returned_vals[0], declared_enumerations, all_node_names, variables, constants, loop_references)[1]
            else:
                returned_vals = validate_code(code.function_call.values[0], scopes, variable_names, new_allowed_functions)
                (cur_arg_type, _, _) = returned_vals[0]
            if len(returned_vals) != 1:
                raise BTreeException(trace, 'Index expects exactly one value but got ' + str(len(returned_vals)))
            if cur_arg_type != 'INT':
                raise BTreeException(trace, 'Index into variable ' + code.function_call.variable.name + ' should be an integer')
            return [(atom_type, 'indexed variable', atom.name)]
        # handle bounded specially
        if 'bounded' in func_info:
            verify_min_max(code.function_call.bound.lower_bound, code.function_call.bound.upper_bound, True)
        returned_values = []
        return_type = func_info['return_type']
        arg_type = func_info['arg_type']
        if arg_type == 'node_name':
            node_func = build_meta_func(code.node_name)
            node_name_vals = node_func((constants, loop_references))
            if len(node_name_vals) != 1:
                raise BTreeException(trace, 'Expected exactly one node reference')
            if node_name_vals[0] not in all_node_names:
                raise BTreeException(trace, 'Reference to a node that does not exist ' + node_name_vals[0])
        if arg_type == 'depends':
            (arg_type, _, _) = validate_code(code.function_call.values[0], scopes, variable_names, new_allowed_functions)[0]
            arg_type = ('NUM' if arg_type in {'INT', 'REAL'} else arg_type)
        for value in code.function_call.values:
            returned_values.extend(validate_code(value, scopes, variable_names, new_allowed_functions))
        if func_info['max_arg'] != -1:
            if len(returned_values) > func_info['max_arg']:
                raise BTreeException(trace, 'Function ' + code.function_call.function_name + ' expected at most ' + str(func_info['max_arg']) + ' but got ' + str(len(returned_values)))
        if len(returned_values) < func_info['min_arg']:
            raise BTreeException(trace, 'Function ' + code.function_call.function_name + ' expected at least ' + str(func_info['min_arg']) + ' but got ' + str(len(returned_values)))
        for (cur_arg_type, cur_code_type, cur_code) in returned_values:
            if (cur_arg_type != arg_type) and ((arg_type != 'NUM') or (cur_arg_type not in {'INT', 'REAL'})):
                raise BTreeException(trace, 'Function ' + code.function_call.function_name + ' expected ' + arg_type + ' but got ' + cur_arg_type + ' from an argument which is ' + cur_code_type + ' ' + cur_code)
            return_type = ('REAL' if return_type == 'NUM' and cur_arg_type == 'REAL' else return_type)
        return_type = ('INT' if return_type == 'NUM' else return_type)
        return [(return_type, 'function', code.function_call.function_name)]

    def validate_condition(code, scopes, variable_names, allowed_functions):
        returned_values = validate_code(code, scopes, variable_names, allowed_functions)
        if len(returned_values) != 1:
            raise BTreeException(trace, 'Condition expects exactly one value but got ' + str(len(returned_values)))
        (cur_arg_type, cur_code_type, cur_code) = returned_values[0]
        if cur_arg_type != 'BOOLEAN':
            raise BTreeException(trace, 'Conditition expected BOOLEAN but got ' + cur_arg_type + ' from ' + cur_code_type + ' ' + cur_code)
        return

    def validate_variable_assignment(variable, assign, scopes, variable_names, deterministic = False, init_mode = None):
        trace.append('In variable assignment for: ' + variable.name)
        if sum([is_local(variable), is_env(variable), is_blackboard(variable)]) != 1:
            raise BTreeException(trace, 'marked as not exactly one type (this should be unreachable)')
        if init_mode is None and (variable.model_as in {'DEFINE', 'FROZENVAR'}):
            raise BTreeException(trace, 'updating variable modeled as ' + variable.model_as)
        if init_mode == 'node' and (not is_local(variable)):
            raise BTreeException(trace, 'initializes non_local variable')

        var_type = variable_type(variable, declared_enumerations, constants)

        def handle_case_result(case_result, is_default):
            if not is_default:
                validate_condition(case_result.condition, scopes, variable_names, {'reg'})
            # if deterministic and len(case_result.values) > 1:
            #     raise BTreeException(trace, 'needs to be updated deterministicly here but is being updated non-deterministicly')
            for value in case_result.values:
                returned_vals = validate_code(value, scopes, variable_names, {'reg'})
                for (cur_arg_type, cur_code_type, cur_code) in returned_vals:
                    if (cur_arg_type != var_type) and not (cur_arg_type == 'INT' and var_type == 'REAL'):
                        raise BTreeException(trace, 'type ' + var_type + ' is being updated with ' + cur_code_type + ' ' + cur_code + ' which is of type ' + cur_arg_type)
        for case_result in assign.case_results:
            handle_case_result(case_result, False)
        handle_case_result(assign.default_result, True)
        trace.pop()
        return

    def validate_loop_array_index(loop_array_index, assign_var, constant_index, scopes, variable_names, deterministic = True, init_mode = None):
        seen_constants = set()
        if loop_array_index.array_index is not None:
            for index in loop_array_index.array_index.index_expr:
                if constant_index == 'constant_index':
                    index_func = build_meta_func(index)
                    values = index_func((constants, {}))
                    for value in values:
                        cur_type = constant_type(value, declared_enumerations)
                        if cur_type != 'INT':
                            raise BTreeException(trace, 'indexed using type of ' + cur_type + ' instead of INT')
                        if value in seen_constants:
                            raise BTreeException(trace, 'array is being indexed with constants and a constant appears twice. New: ' + str(value) + '. Already seen: ' + str(seen_constants))
                        seen_constants.add(value)
                else:
                    returned_vals = validate_code(index, scopes, variable_names, {'reg'})
                    for (cur_type, _, _) in returned_vals:
                        if cur_type != 'INT':
                            raise BTreeException(trace, 'indexed using type of ' + cur_type + ' instead of INT')
            validate_variable_assignment(assign_var, loop_array_index.array_index.assign, scopes, variable_names, deterministic, init_mode)
            return seen_constants
        loop_variable = loop_array_index.loop_variable
        validate_name(loop_variable)
        all_domain_values = []
        if loop_array_index.min_val is None:
            for domain_code in loop_array_index.loop_variable_domain:
                try:
                    domain_func = build_meta_func(domain_code)
                    for domain_value in domain_func((constants, loop_references)):
                        all_domain_values.append(resolve_potential_reference(domain_value, declared_enumerations, all_node_names, variables, constants, loop_references)[2])
                except Exception as error:
                    raise BTreeException(trace, 'unknown error') from error
        else:
            ((_, min_val), (_, max_val)) = verify_min_max(loop_array_index.min_val, loop_array_index.max_val, False)
            all_domain_values = range(min_val, max_val + 1)
        cond_func = build_meta_func(loop_array_index.loop_condition)
        for domain_member in all_domain_values:
            loop_references[loop_variable] = domain_member
            returned_vals = cond_func((constants, loop_references))
            if len(returned_vals) != 1:
                raise BTreeException(trace, 'Loop Condition function is expected to return exactly 1 value')
            if returned_vals[0]:
                new_constants = validate_loop_array_index(loop_array_index.loop_array_index, assign_var, constant_index, scopes, variable_names, deterministic, init_mode)
                if constant_index:
                    if not seen_constants.isdisjoint(new_constants):
                        raise BTreeException(trace, 'array is being indexed with constants and a constant appears twice. New: ' + str(new_constants) + '. Already seen: ' + str(seen_constants))
                    seen_constants.update(new_constants)
            loop_references.pop(loop_variable)
        return seen_constants

    def validate_array_assign(statement, scopes, variable_names, deterministic = True, init_mode = None):
        assign_var = statement.variable if hasattr(statement, 'variable') else statement
        trace.append('In Array Assignment for: ' + assign_var.name)
        if not is_array(assign_var):
            raise BTreeException(trace, 'updated as array but is not an array')
        if hasattr(statement, 'default_value'):
            validate_variable_assignment(assign_var, statement.default_value, scopes, variable_names, deterministic, init_mode)
        seen_constants = set()
        for loop_array_index in statement.assigns:
            new_constants = validate_loop_array_index(loop_array_index, assign_var, statement.constant_index, scopes, variable_names, deterministic, init_mode)
            if statement.constant_index:
                if not seen_constants.isdisjoint(new_constants):
                    raise BTreeException(trace, 'array is being indexed with constants and a constant appears twice. New: ' + str(new_constants) + '. Already seen: ' + str(seen_constants))
                seen_constants.update(new_constants)
        trace.pop()
        return

    def validate_check(node):
        trace.append('In Check: ' + node.name)
        for arg_pair in node.arguments:
            loop_references[arg_pair.argument_name] = dummy_value(arg_pair.argument_type, declared_enumerations)
        read_variables = set(map(lambda x : x.name, node.read_variables))
        if len(read_variables) != len(node.read_variables):
            raise BTreeException(trace, 'duplicate read variables')
        validate_condition(node.condition, {'blackboard'}, read_variables, {'reg'})
        for arg_pair in node.arguments:
            loop_references.pop(arg_pair.argument_name)
        trace.pop()
        return


    def validate_check_env(node):
        trace.append('In Environment Check: ' + node.name)
        for arg_pair in node.arguments:
            loop_references[arg_pair.argument_name] = dummy_value(arg_pair.argument_type, declared_enumerations)
        read_variables = set(map(lambda x : x.name, node.read_variables))
        if len(read_variables) != len(node.read_variables):
            raise BTreeException(trace, 'duplicate read variables')
        validate_condition(node.condition, {'blackboard', 'environment'}, read_variables, {'reg'})
        for arg_pair in node.arguments:
            loop_references.pop(arg_pair.argument_name)
        trace.pop()
        return

    def validate_action(node):
        trace.append('In Action: ' + node.name)
        for arg_pair in node.arguments:
            loop_references[arg_pair.argument_name] = dummy_value(arg_pair.argument_type, declared_enumerations)

        all_vars = set(map(lambda x : x.name, itertools.chain(node.local_variables, node.read_variables, node.write_variables)))
        read_variables = set(map(lambda x : x.name, node.read_variables))
        write_variables = set(map(lambda x : x.name, node.write_variables))
        local_variables = set(map(lambda x : x.name, node.local_variables))
        if len(read_variables) != len(node.read_variables):
            raise BTreeException(trace, 'duplicate read variables')
        if len(write_variables) != len(node.write_variables):
            raise BTreeException(trace, 'has duplicate write variables')
        if len(local_variables) != len(node.local_variables):
            raise BTreeException(trace, 'duplicate local variables')

        if len(node.init_statements) != len(set(map(lambda x: x.variable.name, node.init_statements))):
            raise BTreeException(trace, 'initializes at least one variable at least twice')

        for var_statement in node.init_statements:
            # if var_statement.instant:
            #     raise BTreeException(trace, 'Action ' + node.name + ' marked a non-environment statement as instant')
            assign_var = var_statement.variable
            if assign_var.name not in local_variables:
                raise BTreeException(trace, 'initializing local variable ' + assign_var.name + ' but it it does not appear in the local variable list for the node: [' + ', '.join(local_variables) + ']')
            if is_array(assign_var):
                validate_array_assign(var_statement, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = 'node')
            else:
                if var_statement.assign is None:
                    raise BTreeException(trace, 'Variable is not an array, but has as an array like update: ' + assign_var.name)
                validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = 'node')

        for statement in itertools.chain(node.pre_update_statements, node.post_update_statements):
            if statement.variable_statement is not None:
                trace.append('Variable Statement for: ' + statement.variable_statement.variable.name)
                var_statement = statement.variable_statement
                if var_statement.instant:
                    raise BTreeException(trace, 'non-environment marked as instant')
                assign_var = var_statement.variable
                if assign_var.name not in local_variables and assign_var.name not in write_variables:
                    raise BTreeException(trace, 'updating variable ' + assign_var.name + ' but it is not listed in the local or write variables')
                if is_array(assign_var):
                    validate_array_assign(var_statement, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = None)
                else:
                    if var_statement.assign is None:
                        raise BTreeException(trace, 'Variable is not an array, but has as an array like update: ' + assign_var.name)
                    validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = None)
                trace.pop()
                #
                # END OF VARIABLE_STATEMENT
                #
            elif statement.read_statement is not None:
                trace.append('Read Statement: ' + statement.read_statement.name)
                read_statement = statement.read_statement
                cond_var = None
                if read_statement.condition_variable is not None:
                    cond_var = read_statement.condition_variable
                    if is_array(cond_var):
                        if read_statement.index_of is None:
                            raise BTreeException(trace, 'Action ' + node.name + ' is using array ' + cond_var.name + ' without an index as a condition variable')
                        if read_statement.is_const == 'index_of':
                            returned_vals = validate_code(read_statement.index_of, {'local', 'blackboard'}, all_vars, {'reg'})
                            if len(returned_vals) != 1:
                                raise BTreeException(trace, 'attempted to index read variable with multiple values (or no values)')
                            (cur_type, _, _) = returned_vals[0]
                        else:
                            index_func = build_meta_func(read_statement.index_of)
                            values = index_func((constants, {}))
                            if len(values) != 1:
                                raise BTreeException(trace, 'attempted to index read variable with multiple values (or no values)')
                            cur_type = constant_type(values[0], declared_enumerations)
                        if cur_type != 'INT':
                            raise BTreeException(trace, 'indexing into ' + cond_var.name + ' with something other than an int')
                    if not is_array(cond_var) and read_statement.index_of is not None:
                        raise BTreeException(trace, cond_var.name + ' used with an index as a condition variable but it is not an array')
                    if is_env(cond_var):
                        raise BTreeException(trace, cond_var.name + ' used as a condition variable but it is an Environment Variable')
                    if cond_var.name not in local_variables and cond_var.name not in write_variables:
                        raise BTreeException(trace, 'updating condition variable ' + cond_var.name + ' but it is not listed in the local or write variables')
                    temp_var_type = variable_type(cond_var, declared_enumerations, constants,)
                    if temp_var_type != 'BOOLEAN':
                        raise BTreeException(trace, 'Condition variable for read statement is ' + cond_var.name + ' but ' + cond_var.name + ' is of type ' + temp_var_type + ' and not BOOLEAN')
                    if cond_var.model_as != 'VAR':
                        raise BTreeException(trace, 'Condition variable for read statement is ' + cond_var.name + ' but ' + cond_var.name + ' is modeled as ' + cond_var.model_as)
                validate_condition(read_statement.condition, {'blackboard', 'local', 'environment'}, all_vars, {'reg'})
                if read_statement.non_determinism and cond_var is None:
                    raise BTreeException(trace, 'non-deterministic read statement but no condition variable')
                for var_statement in read_statement.variable_statements:
                    trace.append('Variable Statement for: ' + var_statement.variable.name)
                    if var_statement.instant:
                        raise BTreeException(trace, 'non-environment statement as instant')
                    assign_var = var_statement.variable
                    if cond_var is not None:
                        if cond_var.name == assign_var.name:
                            raise BTreeException(trace, cond_var.name + ' used as a condition variable and update variable in the same read statement')
                    if is_env(assign_var):
                        raise BTreeException(trace, 'updating ' + assign_var.name + ' as part of a read statement but it is an Environment Variable')
                    if assign_var.name not in write_variables and assign_var.name not in local_variables:
                        raise BTreeException(trace, 'updating ' + assign_var.name + ' but ' + assign_var.name + ' is not declared in write_variables: [' + ', '.join(write_variables) + '] or in local_variables: [' + ', '.join(local_variables) + ']')
                    if is_array(assign_var):
                        validate_array_assign(var_statement, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
                    else:
                        if var_statement.assign is None:
                            raise BTreeException(trace, 'Variable is not an array, but has as an array like update: ' + assign_var.name)
                        validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
                    trace.pop()
                trace.pop()
                #
                # END OF READ_STATEMENT
                #
            elif statement.write_statement is not None:
                trace.append('Write Statement: ' + statement.write_statement.name)
                write_statement = statement.write_statement
                for var_statement in write_statement.update:
                    trace.append('Variable Statement for: ' + var_statement.variable.name)
                    assign_var = var_statement.variable
                    if not is_env(assign_var):
                        raise BTreeException(trace, 'updating ' + assign_var.name + ' as part of a write statement but it is not an Environment Variable')
                    if is_array(assign_var):
                        validate_array_assign(var_statement, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
                    else:
                        if var_statement.assign is None:
                            raise BTreeException(trace, 'Variable is not an array, but has as an array like update: ' + assign_var.name)
                        validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
                    trace.pop()
                trace.pop()
                #
                # END OF WRITE_STATEMENT
                #
            else:
                raise BTreeException(trace, 'Action ' + node.name + ' has a statement of an unrecognized type (should be impossible)')

        for case_result in node.return_statement.case_results:
            validate_condition(case_result.condition, {'blackboard', 'local'}, all_vars, {'reg'})
        for arg_pair in node.arguments:
            loop_references.pop(arg_pair.argument_name)
        trace.pop()
        return

    def validate_variable(variable, scopes, variable_names):
        trace.append('In Variable: ' + variable.name)
        if variable.model_as == 'NEURAL':
            if not model.neural:
                raise BTreeException(trace, 'Model configuration did not include \'neural\' but uses neural networks')
            num_inputs = 0
            for input_code in variable.inputs:
                variable_func = build_meta_func(input_code)
                input_variables = variable_func((constants, {}))
                for input_variable in input_variables:
                    (atom_class, atom_type, _) = resolve_potential_reference(input_variable, declared_enumerations, all_node_names, variables, constants, {})
                    if atom_class not in ('VARIABLE', 'CONSTANT'):
                        raise BTreeException(trace, 'Neural Network has an input of class: ' + str(atom_class) + '. Neural network inputs must be of class VARIABLE or CONSTANT')
                    if atom_type != 'INT':
                        raise BTreeException(trace, 'Neural Network inputs must be of type INT')
                num_inputs += len(input_variables)
            output_func = build_meta_func(variable.num_outputs)
            output_vals = output_func((constants, {}))
            if len(output_vals) != 1:
                raise BTreeException(trace, 'Neural Network output size must resolve to a single integer value. Received: ' + str(len(output_vals)))
            num_outputs = output_vals[0]
            (atom_class, atom_type, num_outputs) = resolve_potential_reference(num_outputs, declared_enumerations, all_node_names, variables, constants, {})
            if atom_class != 'CONSTANT':
                raise BTreeException(trace, 'Neural Network output size must be a constant')
            if atom_type != 'INT':
                raise BTreeException(trace, 'Neural Network output size must be an INT')
            file_prefix = model_file.rsplit('/', 1)[0]
            source_func = build_meta_func(variable.source)
            source_vals = source_func((constants, {}))
            if len(source_vals) != 1:
                raise BTreeException(trace, 'Neural Networks must have exactly 1 source file. Received: ' + str(len(source_vals)))
            source = source_vals[0]
            (atom_class, source) = resolve_potential_reference_no_type(source, declared_enumerations, all_node_names, variables, constants, {})
            if atom_class != 'CONSTANT':
                raise BTreeException(trace, 'Neural Network source must be a constant')
            source = file_prefix + '/' + source
            if not isfile(source):
                raise BTreeException(trace, 'Neural Network source: ' + source + ' is not a file')
            try:
                session = onnxruntime.InferenceSession(source)
                input_name = session.get_inputs()[0].name
                results = session.run(None, {input_name : [[0] * num_inputs]})
                if len(results[0][0]) != num_outputs:
                    raise ValueError('Expected output to be of size ' + str(num_outputs))
            except Exception as error:
                raise BTreeException(trace, 'Encountered an error while running network from: ' + source) from error
            trace.pop()
            return
        if variable.model_as != 'DEFINE':
            if variable.domain.true_int is not None:
                pass
            elif variable.domain.min_val is not None:
                verify_min_max(variable.domain.min_val, variable.domain.max_val, False)
            elif variable.domain.boolean is not None:
                pass
            else:
                values = []
                for domain_code in variable.domain.domain_codes:
                    domain_func = build_meta_func(domain_code)
                    values.extend(domain_func((constants, {})))
                if len(values) == 0:
                    raise BTreeException(trace, 'Variable ' + variable.name + ' has an empty domain')
                value_type = constant_type(values[0], declared_enumerations)
                if value_type not in {'ENUM', 'INT'}:
                    raise BTreeException(trace, 'Variable ' + variable.name + ' must be ENUM or INT (loop domain)')
                for value in values:
                    cur_type = constant_type(value, declared_enumerations)
                    if cur_type != value_type:
                        raise BTreeException(trace, 'Variable ' + variable.name + ' has multiple types (cannot use reals here): ' + value_type + ', ' + cur_type)
        if is_array(variable):
            array_size_func = build_meta_func(variable.array_size)
            array_sizes = array_size_func((constants, {}))
            if len(array_sizes) != 1:
                raise BTreeException(trace, 'must have exactly 1 array size')
            array_size = array_sizes[0]
            array_size_type = constant_type(array_size, declared_enumerations)
            if array_size_type != 'INT':
                raise BTreeException(trace, 'Array size must be an INT')
            if array_size < 2:
                raise BTreeException(trace, 'Variable ' + variable.name + ' is an array of size ' + str(array_size))
            validate_array_assign(variable, scopes, variable_names, deterministic = not is_env(variable), init_mode = 'default')
        else:
            validate_variable_assignment(variable, variable.assign, scopes, variable_names, deterministic = not is_env(variable), init_mode = 'default')
        trace.pop()
        return

    def walk_tree(current_node, node_names, node_names_map, nodes_to_check):
        while True:
            if hasattr(current_node, 'sub_root'):
                current_node = current_node.sub_root
                continue
            current_name = current_node.leaf.name if current_node.name is None else current_node.name
            if hasattr(current_node, 'leaf'):
                current_args = current_node.arguments
                current_node = current_node.leaf
                all_current_args = []
                for cur_arg in current_args:
                    arg_func = build_meta_func(cur_arg)
                    all_current_args.extend(arg_func((constants, {})))
                if len(current_node.arguments) != len(all_current_args):
                    raise BTreeException(trace, 'Node ' + current_node.name + ' needs ' + str(len(current_node.arguments)) + ' arguments but was created with ' + str(len(all_current_args)))
                for (index, cur_arg) in enumerate(all_current_args):
                    cur_type = resolve_potential_reference(cur_arg, declared_enumerations, {}, {}, constants, {})[1]
                    if current_node.arguments[index].argument_type != cur_type:
                        raise BTreeException(trace, 'Node ' + current_node.name + ' argument ' + str(index) + ' named ' + current_node.arguments[index].argument_name + ' was declared to be of type ' + current_node.arguments[index].argument_type + ' but is being created with type ' + cur_type)
                nodes_to_check.add(current_node.name)
            break
        # next, we get the name of this node, and correct for duplication

        new_name = create_node_name(current_name, node_names, node_names_map)
        node_name = new_name[0]
        modifier = new_name[1]
        if node_name in constants or new_name in declared_enumerations:
            raise BTreeException(trace, 'Node name ' + node_name + ' clashes with existing constant or enumeration')

        node_names.add(node_name)
        node_names_map[node_name] = modifier

        if hasattr(current_node, 'memory'):
            if current_node.memory == 'with_true_memory':
                raise BTreeException(trace, 'True memory not yet implemented')
            if current_node.node_type == 'parallel':
                if current_node.parallel_policy == 'success_on_one' and current_node.memory != '':
                    raise BTreeException(trace, 'Node ' + current_node.name + ' is success_on_one and has memory. This combination does not make sense.')
        if current_node.node_type == 'X_is_Y':
            if current_node.x == current_node.y:
                raise BTreeException(trace, 'Node ' + current_node.name + ' is of type X_is_Y where X==Y')

        if hasattr(current_node, 'child'):
            (node_names, node_names_map, nodes_to_check) = walk_tree(current_node.child, node_names, node_names_map, nodes_to_check)
        if hasattr(current_node, 'children'):
            if len(current_node.children) < 2:
                raise BTreeException(trace, 'Node ' + current_node.name + ' has less than 2 children.')
            for child in current_node.children:
                (node_names, node_names_map, nodes_to_check) = walk_tree(child, node_names, node_names_map, nodes_to_check)
        return (node_names, node_names_map, nodes_to_check)

    def valid_enumeration(value):
        if not isinstance(value, str):
            raise BTreeException(trace, 'Value ' + str(value) + ' is not a valid enumeration (not a string)')
        if re.fullmatch(r'[^\d\W]\w*', value) is None:
            raise BTreeException(trace, 'Value ' + value + ' is not a valid enumeration')
        return value

    def valid_constant(value):
        if isinstance(value, str) and value not in declared_enumerations:
            raise BTreeException(trace, 'Value ' + value + ' is not a valid enumeration')
        return value

    def valid_constant_name(name):
        if name in declared_enumerations:
            raise BTreeException(trace, 'Constant ' + name + ' is already an enumeration')
        return name

    # END OF METHODS. START OF SCRIPT -------------------------------------------------------------------------------------------------------------
    if recursion_limit > 1000:
        sys.setrecursionlimit(recursion_limit)
    metamodel = textx.metamodel_from_file(metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(model_file)
    if model.neural:
        import onnxruntime

    trace.append('In Enumeration Validation')
    declared_enumerations = set(map(valid_enumeration, model.enumerations))
    trace.pop()
    trace.append('In Constant Validation')
    constants = {
        valid_constant_name(constant.name) : valid_constant(constant.val)
        for constant in model.constants
    }
    loop_references = {}
    trace.pop()
    (all_node_names, _, nodes_to_check) = walk_tree(model.root, set(), {}, set())

    require_trace_identifier = False

    variables_so_far = set()
    variables = {}
    trace.append('In Variable validation')
    for variable in model.variables:
        if variable.name in all_node_names or variable.name in declared_enumerations or variable.name in constants:
            raise BTreeException(trace, 'Variable name ' + variable.name + ' clashes with existing names')
        validate_variable(variable, {'blackboard', 'environment'} if is_env(variable) else {'blackboard'}, variables_so_far)
        variables_so_far.add(variable.name)
        variables[variable.name] = variable
    trace.pop()

    trace.append('In Environment Update Validation')
    for var_statement in model.update:
        # we allow local, blackboard, and environment variables to be referenced in between ticks for environment updates
        # TODO: make sure local variables are always referened with a node identifier here.
        assign_var = var_statement.variable
        if not is_env(assign_var):
            raise BTreeException(trace, 'A pre/post tick update is updating a non-environment variable: ' + assign_var.name)
        if is_array(assign_var):
            validate_array_assign(var_statement, {'local', 'blackboard', 'environment'}, None, deterministic = False, init_mode = None)
        else:
            if var_statement.assign is None:
                raise BTreeException(trace, 'Environment update :: Variable is not an array, but has as an array like update: ' + assign_var.name)
            validate_variable_assignment(assign_var, var_statement.assign, {'local', 'blackboard', 'environment'}, None, deterministic = False, init_mode = None)
    trace.pop()
    # no point in really checking nodes that aren't being used.
    # and checking them causes problems because we can't verify argument types.
    for check in filter(lambda node: node.name in nodes_to_check, model.check_nodes):
        validate_check(check)
    for check_env in filter(lambda node: node.name in nodes_to_check, model.environment_checks):
        validate_check_env(check_env)
    for action in filter(lambda node: node.name in nodes_to_check, model.action_nodes):
        validate_action(action)

    if model.tick_condition is not None:
        validate_condition(model.tick_condition, {'blackboard', 'local', 'environment'}, None, {'reg'})
    if model.hypersafety:
        require_trace_identifier = True
    for specification in model.specifications:
        if specification.spec_type == 'LTLSPEC':
            allowed = {'LTL', 'INVAR', 'reg'}
        elif specification.spec_type == 'CTLSPEC':
            allowed = {'CTL', 'INVAR', 'reg'}
        elif specification.spec_type == 'INVARSPEC':
            allowed = {'INVAR', 'reg'}
        else:
            raise BTreeException(trace, 'unknown specification type: ' + specification.spec_type)
        validate_condition(specification.code_statement, {'blackboard', 'local', 'environment'}, None, allowed)
    print('grammar check complete')
    return (model, variables, constants, declared_enumerations)
