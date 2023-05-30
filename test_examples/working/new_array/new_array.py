import y_do_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    return blackboard_reader


def create_tree(environment):
    y_do = y_do_file.y_do('y_do', environment)
    return y_do
