import f_file
import r_file
import s_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    return blackboard_reader


def create_tree(environment):
    s = s_file.s('s', environment)
    s_1 = s_file.s('s_1', environment)
    sel = py_trees.composites.Selector(name = 'sel', memory = False, children = [s, s_1])
    return sel
