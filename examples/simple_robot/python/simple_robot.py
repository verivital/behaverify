import move_file
import x_too_small_file
import x_too_big_file
import y_too_small_file
import y_too_big_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'x_true', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_true', access = py_trees.common.Access.WRITE)
    blackboard_reader.x_true = serene_safe_assignment.x_true((0 if ((temp := random.randint(0, 20)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10 if temp == 10 else (11 if temp == 11 else (12 if temp == 12 else (13 if temp == 13 else (14 if temp == 14 else (15 if temp == 15 else (16 if temp == 16 else (17 if temp == 17 else (18 if temp == 18 else (19 if temp == 19 else (20))))))))))))))))))))))
    blackboard_reader.y_true = serene_safe_assignment.y_true((0 if ((temp := random.randint(0, 20)) == 0) else (1 if temp == 1 else (2 if temp == 2 else (3 if temp == 3 else (4 if temp == 4 else (5 if temp == 5 else (6 if temp == 6 else (7 if temp == 7 else (8 if temp == 8 else (9 if temp == 9 else (10 if temp == 10 else (11 if temp == 11 else (12 if temp == 12 else (13 if temp == 13 else (14 if temp == 14 else (15 if temp == 15 else (16 if temp == 16 else (17 if temp == 17 else (18 if temp == 18 else (19 if temp == 19 else (20))))))))))))))))))))))
    return blackboard_reader


def create_tree(environment):
    x_too_small = x_too_small_file.x_too_small('x_too_small', environment)
    move = move_file.move('move', environment, 1, 0)
    try_right = py_trees.composites.Sequence(name = 'try_right', memory = False, children = [x_too_small, move])
    x_too_big = x_too_big_file.x_too_big('x_too_big', environment)
    move_1 = move_file.move('move_1', environment, (-1), 0)
    try_left = py_trees.composites.Sequence(name = 'try_left', memory = False, children = [x_too_big, move_1])
    y_too_small = y_too_small_file.y_too_small('y_too_small', environment)
    move_2 = move_file.move('move_2', environment, 0, 1)
    try_up = py_trees.composites.Sequence(name = 'try_up', memory = False, children = [y_too_small, move_2])
    y_too_big = y_too_big_file.y_too_big('y_too_big', environment)
    move_3 = move_file.move('move_3', environment, 0, (-1))
    try_down = py_trees.composites.Sequence(name = 'try_down', memory = False, children = [y_too_big, move_3])
    move_robot = py_trees.composites.Selector(name = 'move_robot', memory = False, children = [try_right, try_left, try_up, try_down])
    return move_robot
