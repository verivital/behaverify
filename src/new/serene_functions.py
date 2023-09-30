'''
This module is for internal use with BehaVerify.
It contains utility functions for computations.
Each function 


Author: Serena Serafina Serbinowska
Last Edit: 2023-09-27
'''
import operator
import math
import copy


def serene_if(function_call):
    # this one returns an array by directly returning a build_meta_func result.
    return lambda references : (
        build_meta_func(function_call.values[1])(references)
        if build_meta_func(function_call.values[0])(references)[0][1] else
        build_meta_func(function_call.values[2])(references)
    )

def update_dictionary(dictionary, key, value):
    new_dictionary = copy.deepcopy(dictionary)
    new_dictionary[key] = value
    return new_dictionary

def serene_loop(function_call):
    sub_func = build_meta_func(function_call.values[0])
    return lambda references : [
        sub_func((references[0], update_dictionary(references[1], function_call.loop_variable, loop_value)))
        for loop_value in (
                range(build_meta_func(function_call.min_val)(references)[0],
                      build_meta_func(function_call.max_val)(references)[1] + 1)
                if function_call.min_val is not None else
                [loop_value_ref for loop_value_code in function_call.loop_variable_domain for loop_value_ref in build_meta_func(loop_value_code)(references)]
        )
    ]

def serene_abs(function_call):
    return lambda references : [abs(build_meta_func(function_call.values[0])(references)[0])]

def serene_max(function_call):
    return lambda references : [max(max(build_meta_func(value)(references)) for value in function_call.values)]

def serene_min(function_call):
    return lambda references : [min(min(build_meta_func(value)(references)) for value in function_call.values)]

def serene_sin(function_call):
    return lambda references : [math.sin(build_meta_func(function_call.values[0])(references)[0])]

def serene_cos(function_call):
    return lambda references : [math.cos(build_meta_func(function_call.values[0])(references)[0])]

def serene_tan(function_call):
    return lambda references : [math.tan(build_meta_func(function_call.values[0])(references)[0])]

def serene_log(function_call):
    return lambda references : [math.log(build_meta_func(function_call.values[0])(references)[0])]

def serene_not(function_call):
    return lambda references : [not build_meta_func(function_call.values[0])(references)[0]]

def serene_xor(function_call):
    return lambda references : [operator.xor(build_meta_func(function_call.values[0])(references)[0],
                                             build_meta_func(function_call.values[1])(references)[0])]

def serene_eq(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] ==
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_ne(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] !=
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_lt(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] <
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_gt(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] >
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_lte(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] <=
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_gte(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] >=
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_neg(function_call):
    return lambda references : [(-1)*build_meta_func(function_call.values[0])(references)[0]]

def serene_sub(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] -
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_integer_div(function_call):
    return lambda references : [int(build_meta_func(function_call.values[0])(references)[0] /
                                    build_meta_func(function_call.values[1])(references)[0])]

def serene_mod(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] %
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_real_div(function_call):
    return lambda references : [build_meta_func(function_call.values[0])(references)[0] /
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_floor(function_call):
    return lambda references : [math.floor(build_meta_func(function_call.values[0])(references)[0])]

def serene_and(function_call):
    return lambda references : [all(all(build_meta_func(value)(references)) for value in function_call.values)]

def serene_or(function_call):
    return lambda references : [any(any(build_meta_func(value)(references)) for value in function_call.values)]

def serene_xnor(function_call):
    return lambda references : [not (operator.xor(build_meta_func(function_call.values[0])(references)[0],
                                                   build_meta_func(function_call.values[1])(references)[0]))]

def serene_implies(function_call):
    return lambda references : [(not (build_meta_func(function_call.values[0])(references)[0])) or
                                build_meta_func(function_call.values[1])(references)[0]]

def serene_add(function_call):
    return lambda references : [sum(sum(build_meta_func(value)(references)) for value in function_call.values)]

def serene_mult(function_call):
    return lambda references : [math.prod(math.prod(build_meta_func(value)(references)) for value in function_call.values)]


RANGE_FUNCTION = {
    'if' : serene_if,
    'loop' : serene_loop,
    'abs' : serene_abs,
    'max' : serene_max,
    'min' : serene_min,
    'sin' : serene_sin,
    'cos' : serene_cos,
    'tan' : serene_tan,
    'ln' : serene_log,
    'not' : serene_not,
    'and' : serene_and,
    'or' : serene_or,
    'xor' : serene_xor,
    'xnor' : serene_xnor,
    'imply' : serene_implies,
    'equiv' : serene_eq,
    'eq' : serene_eq,
    'neq' : serene_ne,
    'lt' : serene_lt,
    'gt' : serene_gt,
    'lte' : serene_lte,
    'gte' : serene_gte,
    'neg' : serene_neg,
    'add' : serene_add,
    'sub' : serene_sub,
    'mult' : serene_mult,
    'idiv' : serene_integer_div,
    'mod' : serene_mod,
    'rdiv' : serene_real_div,
    'floor' : serene_floor,
    'count' : serene_add
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
            RANGE_FUNCTION[code.function_call.function_name]((code.function_call))
        )
    )
