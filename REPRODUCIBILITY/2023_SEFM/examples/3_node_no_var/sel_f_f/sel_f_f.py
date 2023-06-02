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
    f_1 = f_file.f('f_1', environment)
    root = py_trees.composites.Selector(name = 'root', memory = False, children = [f, f_1])
    return root
