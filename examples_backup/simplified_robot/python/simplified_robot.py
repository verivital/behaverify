import go_x_file
import go_y_file
import x_too_small_file
import x_too_big_file
import y_too_small_file
import y_too_big_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    return blackboard_reader


def create_tree(environment):
    x_too_small = x_too_small_file.x_too_small('x_too_small', environment)
    go_x = go_x_file.go_x('go_x', environment, 1)
    try_right = py_trees.composites.Sequence(name = 'try_right', memory = False, children = [x_too_small, go_x])
    x_too_big = x_too_big_file.x_too_big('x_too_big', environment)
    go_x_1 = go_x_file.go_x('go_x_1', environment, -1)
    try_left = py_trees.composites.Sequence(name = 'try_left', memory = False, children = [x_too_big, go_x_1])
    y_too_small = y_too_small_file.y_too_small('y_too_small', environment)
    go_y = go_y_file.go_y('go_y', environment, 1)
    try_up = py_trees.composites.Sequence(name = 'try_up', memory = False, children = [y_too_small, go_y])
    y_too_big = y_too_big_file.y_too_big('y_too_big', environment)
    go_y_1 = go_y_file.go_y('go_y_1', environment, -1)
    try_down = py_trees.composites.Sequence(name = 'try_down', memory = False, children = [y_too_big, go_y_1])
    move_robot = py_trees.composites.Selector(name = 'move_robot', memory = False, children = [try_right, try_left, try_up, try_down])
    return move_robot
