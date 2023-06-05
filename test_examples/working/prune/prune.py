import y_do_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'test', access = py_trees.common.Access.WRITE)
    blackboard_reader.test = serene_safe_assignment.test(0)
    return blackboard_reader


def create_tree(environment):
    y_do = y_do_file.y_do('y_do', environment)
    y_do_1 = y_do_file.y_do('y_do_1', environment)
    bad = py_trees.composites.Selector(name = 'bad', memory = False, children = [y_do, y_do_1])
    return bad
