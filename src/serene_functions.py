'''
This module is for internal use with BehaVerify.
It contains utility functions for computations.
Each function 


Author: Serena Serafina Serbinowska
Last Edit: 2024-02-26
'''
import operator
import math
import copy

def update_dictionary(dictionary, key, value):
    new_dictionary = copy.copy(dictionary) # don't need to deep copy; we don't modify objects
    new_dictionary[key] = value
    return new_dictionary

def reverse_thing_if_true(bool_val, thing):
    return reversed(thing) if bool_val else thing

def serene_loop(function_call):
    sub_func = build_meta_func(function_call.values[0])
    min_val_func = None
    max_val_func = None
    domain_funcs = None
    if function_call.min_val is None:
        domain_funcs = [build_meta_func(loop_value_code) for loop_value_code in function_call.loop_variable_domain]
    else:
        min_val_func = build_meta_func(function_call.min_val)
        max_val_func = build_meta_func(function_call.max_val)
    def evaluate_loop(references):
        return [
            value
            for loop_value in reverse_thing_if_true(function_call.reverse == 'reverse', (
                    range(min_val_func(references)[0], max_val_func(references)[0] + 1)
                    if function_call.min_val is not None else
                    [loop_value_ref for domain_func in domain_funcs for loop_value_ref in domain_func(references)]
            ))
            for value in sub_func((references[0], update_dictionary(references[1], function_call.loop_variable, loop_value)))
        ]
    return evaluate_loop

def serene_case_loop(function_call):
    cond_func = build_meta_func(function_call.cond_value)
    sub_func = build_meta_func(function_call.values[0])
    default_func = build_meta_func(function_call.default_value)
    min_val_func = None
    max_val_func = None
    domain_funcs = None
    if function_call.min_val is None:
        domain_funcs = [build_meta_func(loop_value_code) for loop_value_code in function_call.loop_variable_domain]
    else:
        min_val_func = build_meta_func(function_call.min_val)
        max_val_func = build_meta_func(function_call.max_val)
    def evaluate_case_loop(references):
        domain_vals = reverse_thing_if_true(function_call.reverse == 'reverse', (
            range(min_val_func(references)[0], max_val_func(references)[0] + 1)
            if function_call.min_val is not None else
            [loop_value_ref for domain_func in domain_funcs for loop_value_ref in domain_func(references)]
        ))
        for loop_value in domain_vals:
            if cond_func((references[0], update_dictionary(references[1], function_call.loop_variable, loop_value)))[0]:
                return sub_func((references[0], update_dictionary(references[1], function_call.loop_variable, loop_value)))
        return default_func((references[0], references[1]))
    return evaluate_case_loop

def serene_if(function_call):
    # since both return options return a list, we always return a list, so we don't have wo worry about that.
    cond_func = build_meta_func(function_call.values[0])
    true_func = build_meta_func(function_call.values[1])
    false_func = build_meta_func(function_call.values[2])
    def evaluate_if(references):
        return (true_func(references) if cond_func(references) else false_func(references))
    return evaluate_if

def create_lambda_to_apply_function(function, unpack, values):
    value_funcs = [build_meta_func(code) for code in values]
    if unpack:
        def evaluate_function_unpack(references):
            return [function(*[value for value_func in value_funcs for value in value_func(references)])]
        return evaluate_function_unpack
    def evaluate_function(references):
        return [function([value for value_func in value_funcs for value in value_func(references)])]
    return evaluate_function

FUNCTIONS = {
    # 'if' : serene_if,  # handled seperately
    # 'loop' : serene_loop,  # handled seperately
    'abs' : (abs, True),
    'max' : (max, True),
    'min' : (min, True),
    'sin' : (math.sin, True),
    'cos' : (math.cos, True),
    'tan' : (math.tan, True),
    'ln' : (math.log, True),
    'not' : (operator.not_, True),
    'and' : (all, False),
    'or' : (any, False),
    'xor' : (operator.xor, True),
    'xnor' : (lambda x : operator.not_(operator.xor(x[0], x[1])), False),
    'implies' : (lambda x : (not x[0]) or x[1], False),
    'equivalent' : (operator.eq, True),
    'eq' : (operator.eq, True),
    'neq' : (operator.ne, True),
    #'neq' : (lambda x : operator.ne(x[0], x[1]), False),
    'lt' : (operator.lt, True),
    'gt' : (operator.gt, True),
    # 'gt' : (gt_override, True),
    'lte' : (operator.le, True),
    'gte' : (operator.ge, True),
    'neg' : (operator.neg, True),
    'add' : (sum, False),
    'sub' : (operator.sub, True),
    'mult' : (math.prod, False),
    'idiv' : (lambda x : int(x[0]/x[1]), False),
    'mod' : (operator.mod, True),
    'rdiv' : (operator.truediv, True),
    'floor' : (math.floor, True),
    'count' : (sum, False)  # sum of booleans is exactly what we want.
}

def handle_constant_or_reference_meta(constant_or_reference, constants, loop_references):
    return (
        constant_or_reference.constant
        if constant_or_reference.constant is not None else
        (
            constants[constant_or_reference.reference][0]  # use first value of constant if it's not indexed!
            if constant_or_reference.reference in constants else
            (
                loop_references[constant_or_reference.reference]
                if constant_or_reference.reference in loop_references else
                constant_or_reference.reference
            )
        )
    )

# def handle_index(function_call):
#     to_index_func = build_meta_func(function_call.to_index)
#     if function_call.constant_index != 'constant_index':
#         # this should only occur if we are doing reachability analysis for a neural network.
#         # otherwise, we have a problem because metacode needs to be resolvable at compile time, and if the index isn't constant that's impossible.
#         return to_index_func
#     index_func = build_meta_func(function_call.values[0])
#     def to_index_dependant(references):
#         to_index = to_index_func(references)[0]
#         if to_index in references[0]:
#             # we got a constant!
#             # we should be able to index!
#             return references[0][to_index]['values'][index_func(references)]
#         return to_index # It's a variable. Pass it back! We can't index a variable here, which meanse we better be doing network reachability right now.
#     return to_index_dependant

def build_meta_func(code):
    '''
    builds the meta func.
    return lambda references : s a function which takes a single parameter: references
    references is (constants, loop_references).
    the function returns a list of values.
    each value returned can be be a Constant or a Reference.
    Note that string overlaps both Constant and Reference. It is up to the subsequent user to distinguish them.
    '''
    return (
        (lambda references : [handle_constant_or_reference_meta(code.atom, references[0], references[1])])
        if code.atom is not None
        else
        (
            build_meta_func(code.code_statement)
            if code.code_statement is not None
            else
            (
                serene_loop(code.function_call)
                if code.function_call.function_name == 'loop' else
                (
                    serene_if(code.function_call)
                    if code.function_call.function_name == 'if' else
                    (
                        build_meta_func(code.function_call.to_index)  # network analysis only! Cannot index constants, and indexing variables doesn't make sense in metacode
                        if code.function_call.function_name == 'index' else
                        create_lambda_to_apply_function(*FUNCTIONS[code.function_call.function_name], code.function_call.values)
                    )
                )
            )
        )
    )
