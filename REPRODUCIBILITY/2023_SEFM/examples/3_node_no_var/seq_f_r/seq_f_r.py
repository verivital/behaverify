import f_file
import r_file
import s_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    return blackboard_reader


def create_tree(environment):
    f = f_file.f('f', environment)
    r = r_file.r('r', environment)
    seq = py_trees.composites.Sequence(name = 'seq', memory = False, children = [f, r])
    return seq
