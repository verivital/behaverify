import is_even_file
import divide_by_2_file
import multiply_and_add_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'value', access = py_trees.common.Access.WRITE)
    blackboard_reader.value = serene_safe_assignment.value(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]))
    return blackboard_reader


def create_tree(environment):
    is_even = is_even_file.is_even('is_even')
    divide_by_2 = divide_by_2_file.divide_by_2('divide_by_2', environment)
    even_case = py_trees.composites.Sequence(name = 'even_case', memory = False, children = [is_even, divide_by_2])
    multiply_and_add = multiply_and_add_file.multiply_and_add('multiply_and_add', environment)
    collatz = py_trees.composites.Selector(name = 'collatz', memory = False, children = [even_case, multiply_and_add])
    return collatz
