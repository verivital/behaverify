

import sys
import os
import textx

from serene_functions import build_range_func
from behaverify_common import indent, handle_constant

def meta_to_dsl(meta_grammar_file, behaverify_file, save_temporary = None):
    def symbol_to_string(symbol):
        return (
            str(symbol.is_num) if symbol.is_num is not None else
            (
                str(symbol.is_bool) if symbol.is_bool is not None else
                (
                    str(symbol.other) if symbol.other is not None else
                    (
                        symbol.is_id if symbol.is_id is not None else
                        (
                            '\'' + symbol.is_string + '\''
                        )
                    )
                )
            )
        )
    def handle_variable_domain(domain, loop_variables):
        if domain.min_value is not None:
            range_function = build_range_func(domain.condition, constants)
            return list(map(str, filter(range_function, range(handle_constant(domain.min_value, constants), handle_constant(domain.max_value, constants) + 1)))) 
        return map(symbol_to_string, domain.symbols)
    def handle_object(cur_object, loop_variables = None):
        loop_variables = ({} if loop_variables is None else loop_variables)
        if cur_object.symbol_object is not None:
            return (loop_variables[cur_object.symbol_object] if cur_object.symbol_object in loop_variables else symbol_to_string(cur_object.symbol_object))
        loop = cur_object.loop_object
        if len(loop.loop_variables) != len(loop.loop_variable_domains):
            raise ValueError('Mismatched number of loop variables and loop variable domains for ' + str(loop.loop_variables))
        condition_function = build_range_func(loop.loop_condition, constants)
        variable_domains = {
            loop.loop_variables[index] : handle_variable_domain(loop.loop_variable_domains[index], loop_variables)
            for index in range(loop.loop_variables)
        }
        domain_size = len(variable_domains[loop.loop_variables[0]])
        for variable in variable_domains:
            if len(variable_domains[variable]) != domain_size:
                raise ValueError('Mismatched domain size for loop variables ' + str(loop.loop_variables))
        for domain_index in range(domain_size):
            for variable in variable_domains:
                
        
    metamodel = textx.metamodel_from_file(meta_grammar_file, auto_init_attributes = False)
    model = metamodel.model_from_file(behaverify_file)
    constants = {constant.name : constant.val for constant in model.constants}
    new_model = (
        'configuration {' + ('hypersafety ' if model.hypersafety else '') + ('use_reals' if model.use_reals else '') + '}' + os.linesep
        + 'enumerations {' + os.linesep
        + indent(1) + ', '.join(map(lambda x: '\'' + x + '\'', model.enumerations)) + os.linesep
        + '}' + os.linesep
        + 'constants {' + os.linesep
        + indent(1) + ', '.join(map(lambda x: '\'' + x.name + '\'' + ' := ' + symbol_to_string(x.val), model.constants)) + os.linesep
        + '}' + os.linesep
        + ' '.join(map(handle_object, model.objects))
    )
        
meta_to_dsl(sys.argv[1], None)
