'''
This module is for internal use with BehaVerify.
It contains utility functions for computations.
Each function 


Author: Serena Serafina Serbinowska
Last Edit: 2023-09-19
'''
import operator
import math
from behaverify_common import handle_constant

def serene_abs(values, x):
    return abs(values[0](x))

def serene_max(values, x):
    return max([value(x) for value in values])

def serene_min(values, x):
    return min([value(x) for value in values])

def serene_sin(values, x):
    return math.sin(values[0](x))

def serene_cos(values, x):
    return math.cos(values[0](x))

def serene_tan(values, x):
    return math.tan(values[0](x))

def serene_log(values, x):
    return math.log(values[0](x))

def serene_not(values, x):
    return not values[0](x)

def serene_xor(values, x):
    return operator.xor(values[0](x), values[1](x))

def serene_eq(values, x):
    return values[0](x) == values[1](x)

def serene_ne(values, x):
    return values[0](x) != values[1](x)

def serene_lt(values, x):
    return values[0](x) < values[1](x)

def serene_gt(values, x):
    return values[0](x) > values[1](x)

def serene_lte(values, x):
    return values[0](x) <= values[1](x)

def serene_gte(values, x):
    return values[0](x) >= values[1](x)

def serene_neg(values, x):
    return (-1)*values[0](x)

def serene_sub(values, x):
    return values[0](x) - values[1](x)

def serene_integer_div(values, x):
    return int(values[0](x) / values[1](x))

def serene_mod(values, x):
    return values[0](x) % values[1](x)

def serene_real_div(values, x):
    return values[0](x) / values[1](x)

def serene_floor(values, x):
    return math.floor(values[0](x))

def serene_and(values, x):
    return (values[0](x) and serene_and(values[1:], x)) if values else True

def serene_or(values, x):
    return (values[0](x) or serene_or(values[1:], x)) if values else False

def serene_xnor(values, x):
    return (not (operator.xor(values[0](x), values[1](x))))

def serene_implies(values, x):
    return (not (values[0](x)) or values[1](x))

def serene_sum(values, x):
    return (values[0](x) + serene_sum(values[1:], x)) if values else 0

def serene_mult(values, x):
    return (values[0](x) * serene_mult(values[1:], x)) if values else 1

def serene_count(values, x):
    return (int(bool(values[0](x))) + serene_count(values[1:], x)) if values else 0


RANGE_FUNCTION = {
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
    'add' : serene_sum,
    'sub' : serene_sub,
    'mult' : serene_mult,
    'idiv' : serene_integer_div,
    'mod' : serene_mod,
    'rdiv' : serene_real_div,
    'floor' : serene_floor,
    'count' : serene_count
}

def build_range_func(code, constants):
    '''builds the range func'''
    return (
        (lambda x : handle_constant(code.constant, constants)) if code.constant is not None else (
            (lambda x : x) if code.value else (
                build_range_func(code.code_statement, constants) if code.code_statement is not None else (
                    (lambda x : RANGE_FUNCTION[code.function_call.function_name]([build_range_func(value, constants) for value in code.function_call.values], x))
                )
            )
        )
    )
