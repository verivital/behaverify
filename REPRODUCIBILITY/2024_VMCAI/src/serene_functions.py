'''
This module is for internal use with BehaVerify.
It contains utility functions for computations.


Author: Serena Serafina Serbinowska
Created: 2022-01-01 (Date not correct)
Last Edit: 2023-01-01 (Date not correct)
'''
import operator
import math


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


def serene_truediv(values, x):
    return values[0](x) / values[1](x)


def serene_mod(values, x):
    return values[0](x) % values[1](x)


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
