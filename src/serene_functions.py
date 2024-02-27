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
    def evaluate_loop(references):
        return [
            value
            for loop_value in reverse_thing_if_true(function_call.reverse == 'reverse', (
                    range(build_meta_func(function_call.min_val)(references)[0],
                          build_meta_func(function_call.max_val)(references)[0] + 1)
                    if function_call.min_val is not None else
                    [loop_value_ref for loop_value_code in function_call.loop_variable_domain for loop_value_ref in build_meta_func(loop_value_code)(references)]
            ))
            for value in sub_func((references[0], update_dictionary(references[1], function_call.loop_variable, loop_value)))
        ]
    return evaluate_loop

def serene_case_loop(function_call):
    cond_func = build_meta_func(function_call.cond_value)
    sub_func = build_meta_func(function_call.values[0])
    default_func = build_meta_func(function_call.default_value)
    def evaluate_case_loop(references):
        domain_vals = reverse_thing_if_true(function_call.reverse == 'reverse', (
            range(build_meta_func(function_call.min_val)(references)[0],
                  build_meta_func(function_call.max_val)(references)[0] + 1)
            if function_call.min_val is not None else
            [loop_value_ref for loop_value_code in function_call.loop_variable_domain for loop_value_ref in build_meta_func(loop_value_code)(references)]
        ))
        for loop_value in domain_vals:
            if cond_func((references[0], update_dictionary(references[1], function_call.loop_variable, loop_value)))[0]:
                return sub_func((references[0], update_dictionary(references[1], function_call.loop_variable, loop_value)))
        return default_func((references[0], references[1]))
    return evaluate_case_loop

def serene_if(function_call):
    # since both return options return a list, we always return a list, so we don't have wo worry about that.
    def evaluate_if(references):
        return (
            build_meta_func(function_call.values[1])(references)  # this returns a list
            if build_meta_func(function_call.values[0])(references)[0] else
            build_meta_func(function_call.values[2])(references)  # this also returns a list
        )
    return evaluate_if

def create_lambda_to_apply_function(function, unpack, values):
    if unpack:
        def evaluate_function_unpack(references):
            return [
                function(
                    *[
                        value
                        for code in values
                        for value in build_meta_func(code)(references)
                    ]
                )
            ]
        return evaluate_function_unpack
    def evaluate_function(references):
        return [
            function(
                [
                    value
                    for code in values
                    for value in build_meta_func(code)(references)
                ]
            )
        ]
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
            constants[constant_or_reference.reference]
            if constant_or_reference.reference in constants else
            (
                loop_references[constant_or_reference.reference]
                if constant_or_reference.reference in loop_references else
                constant_or_reference.reference
            )
        )
    )

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
                        build_meta_func(code.function_call.to_index)  # this should only be used when doing neural network reachability stuff.
                        if code.function_call.function_name == 'index' else
                        create_lambda_to_apply_function(*FUNCTIONS[code.function_call.function_name], code.function_call.values)
                    )
                )
            )
        )
    )
