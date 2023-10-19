import check_enum_file
import check_int_file
import check_boolean_file
import check_all_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    return blackboard_reader


def create_tree(environment):
    check_enum = check_enum_file.check_enum('check_enum', 'yes')
    check_enum_1 = check_enum_file.check_enum('check_enum_1', 'Hello')
    check_int = check_int_file.check_int('check_int', 55)
    check_int_1 = check_int_file.check_int('check_int_1', 1)
    check_boolean = check_boolean_file.check_boolean('check_boolean', True)
    check_boolean_1 = check_boolean_file.check_boolean('check_boolean_1', False)
    check_all = check_all_file.check_all('check_all', 'yes', 'Hello', 55, 1, True, False)
    root_node = py_trees.composites.Parallel(name = 'root_node', policy = py_trees.common.ParallelPolicy.SuccessOnAll(False), children = [check_enum, check_enum_1, check_int, check_int_1, check_boolean, check_boolean_1, check_all])
    return root_node
