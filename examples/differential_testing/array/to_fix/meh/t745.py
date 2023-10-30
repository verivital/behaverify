import c1_file
import c2_file
import a1_file
import a2_file
import a3_file
import a4_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'blVAR0', access = py_trees.common.Access.WRITE)
    blackboard_reader.blVAR0 = serene_safe_assignment.blVAR0((
        'both'
        if True else
        (
        'yes'
    )))
    return blackboard_reader


def create_tree(environment):
    a4 = a4_file.a4('a4', environment)
    a3 = a3_file.a3('a3', environment)
    a3_1 = a3_file.a3('a3_1', environment)
    seq0 = py_trees.composites.Sequence(name = 'seq0', memory = True, children = [a4, a3, a3_1])
    return seq0
