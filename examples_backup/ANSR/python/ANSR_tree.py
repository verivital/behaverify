import not_at_destination_file
import y_too_small_file
import y_too_big_file
import x_too_small_file
import x_too_big_file
import call_xy_net_file
import move_file
import send_victory_file
import update_direction_file
import update_previous_destination_file
import target_in_sight_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'prev_dest_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'prev_dest_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'cur_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'cur_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dest_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dest_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dir', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'victory', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_1_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_1_2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_1_3', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_1_4', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_1_5', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_2_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_2_2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_2_3', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_2_4', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_3_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_3_2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_3_3', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_3_4', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_4_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_4_2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_4_3', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_net_output_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_1_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_1_2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_1_3', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_1_4', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_1_5', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_2_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_2_2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_2_3', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_2_4', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_3_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_3_2', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_3_3', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_net_output_1', access = py_trees.common.Access.WRITE)
    blackboard_reader.prev_dest_x = serene_safe_assignment.prev_dest_x(0)
    blackboard_reader.prev_dest_y = serene_safe_assignment.prev_dest_y((0 + 1))
    blackboard_reader.cur_x = serene_safe_assignment.cur_x(0)
    blackboard_reader.cur_y = serene_safe_assignment.cur_y(0)
    blackboard_reader.dest_x = serene_safe_assignment.dest_x(0)
    blackboard_reader.dest_y = serene_safe_assignment.dest_y(0)
    blackboard_reader.dir = serene_safe_assignment.dir(1)
    blackboard_reader.victory = serene_safe_assignment.victory(False)


    def x_net_1_1():
        return max(blackboard_reader.dest_x, 0)

    blackboard_reader.x_net_1_1 = x_net_1_1


    def x_net_1_2():
        return max((blackboard_reader.dest_x - blackboard_reader.prev_dest_x), 0)

    blackboard_reader.x_net_1_2 = x_net_1_2


    def x_net_1_3():
        return max((blackboard_reader.prev_dest_x - blackboard_reader.dest_x), 0)

    blackboard_reader.x_net_1_3 = x_net_1_3


    def x_net_1_4():
        return max((blackboard_reader.dest_x - (int(((0 + 10))/ (2)))), 0)

    blackboard_reader.x_net_1_4 = x_net_1_4


    def x_net_1_5():
        return max(((int(((0 + 10))/ (2))) - blackboard_reader.dest_x), 0)

    blackboard_reader.x_net_1_5 = x_net_1_5


    def x_net_2_1():
        return max(blackboard_reader.x_net_1_1(), 0)

    blackboard_reader.x_net_2_1 = x_net_2_1


    def x_net_2_2():
        return max((-(blackboard_reader.x_net_1_2()) + -(blackboard_reader.x_net_1_3()) + 1), 0)

    blackboard_reader.x_net_2_2 = x_net_2_2


    def x_net_2_3():
        return max((1 - blackboard_reader.x_net_1_4()), 0)

    blackboard_reader.x_net_2_3 = x_net_2_3


    def x_net_2_4():
        return max((1 - blackboard_reader.x_net_1_5()), 0)

    blackboard_reader.x_net_2_4 = x_net_2_4


    def x_net_3_1():
        return max((blackboard_reader.x_net_2_1() - (blackboard_reader.x_net_2_2() * 10)), 0)

    blackboard_reader.x_net_3_1 = x_net_3_1


    def x_net_3_2():
        return max((1 - blackboard_reader.x_net_2_2()), 0)

    blackboard_reader.x_net_3_2 = x_net_3_2


    def x_net_3_3():
        return max(blackboard_reader.x_net_2_3(), 0)

    blackboard_reader.x_net_3_3 = x_net_3_3


    def x_net_3_4():
        return max(blackboard_reader.x_net_2_4(), 0)

    blackboard_reader.x_net_3_4 = x_net_3_4


    def x_net_4_1():
        return max(blackboard_reader.x_net_3_1(), 0)

    blackboard_reader.x_net_4_1 = x_net_4_1


    def x_net_4_2():
        return max(((10 * blackboard_reader.x_net_3_3()) - (10 * blackboard_reader.x_net_3_2())), 0)

    blackboard_reader.x_net_4_2 = x_net_4_2


    def x_net_4_3():
        return max(((0 * blackboard_reader.x_net_3_4()) - (10 * blackboard_reader.x_net_3_2())), 0)

    blackboard_reader.x_net_4_3 = x_net_4_3


    def x_net_output_1():
        return max((blackboard_reader.x_net_4_1() + blackboard_reader.x_net_4_2() + blackboard_reader.x_net_4_3()), 0)

    blackboard_reader.x_net_output_1 = x_net_output_1


    def y_net_1_1():
        return max(blackboard_reader.dest_y, 0)

    blackboard_reader.y_net_1_1 = y_net_1_1


    def y_net_1_2():
        return max((blackboard_reader.dest_y - blackboard_reader.prev_dest_y), 0)

    blackboard_reader.y_net_1_2 = y_net_1_2


    def y_net_1_3():
        return max((blackboard_reader.prev_dest_y - blackboard_reader.dest_y), 0)

    blackboard_reader.y_net_1_3 = y_net_1_3


    def y_net_1_4():
        return max(blackboard_reader.dir, 0)

    blackboard_reader.y_net_1_4 = y_net_1_4


    def y_net_1_5():
        return max(-(blackboard_reader.dir), 0)

    blackboard_reader.y_net_1_5 = y_net_1_5


    def y_net_2_1():
        return max(blackboard_reader.y_net_1_1(), 0)

    blackboard_reader.y_net_2_1 = y_net_2_1


    def y_net_2_2():
        return max((-(blackboard_reader.y_net_1_2()) + -(blackboard_reader.y_net_1_3()) + 1), 0)

    blackboard_reader.y_net_2_2 = y_net_2_2


    def y_net_2_3():
        return max(blackboard_reader.y_net_1_4(), 0)

    blackboard_reader.y_net_2_3 = y_net_2_3


    def y_net_2_4():
        return max(blackboard_reader.y_net_1_5(), 0)

    blackboard_reader.y_net_2_4 = y_net_2_4


    def y_net_3_1():
        return max(blackboard_reader.y_net_2_1(), 0)

    blackboard_reader.y_net_3_1 = y_net_3_1


    def y_net_3_2():
        return max((blackboard_reader.y_net_2_2() + blackboard_reader.y_net_2_3() + -1), 0)

    blackboard_reader.y_net_3_2 = y_net_3_2


    def y_net_3_3():
        return max((blackboard_reader.y_net_2_2() + blackboard_reader.y_net_2_4() + -1), 0)

    blackboard_reader.y_net_3_3 = y_net_3_3


    def y_net_output_1():
        return max((blackboard_reader.y_net_3_1() + (2 * blackboard_reader.y_net_3_2()) + (-1 * 2 * blackboard_reader.y_net_3_3())), 0)

    blackboard_reader.y_net_output_1 = y_net_output_1
    return blackboard_reader


def create_tree(environment):
    target_in_sight = target_in_sight_file.target_in_sight('target_in_sight', environment)
    send_victory = send_victory_file.send_victory('send_victory', environment)
    vision = py_trees.composites.Sequence(name = 'vision', memory = False, children = [target_in_sight, send_victory])
    not_at_destination = not_at_destination_file.not_at_destination('not_at_destination')
    update_direction = update_direction_file.update_direction('update_direction', environment)
    call_xy_net = call_xy_net_file.call_xy_net('call_xy_net', environment)
    update_previous_destination = update_previous_destination_file.update_previous_destination('update_previous_destination', environment)
    new_destination = py_trees.composites.Sequence(name = 'new_destination', memory = False, children = [update_direction, call_xy_net, update_previous_destination])
    destination = py_trees.composites.Selector(name = 'destination', memory = False, children = [not_at_destination, new_destination])
    y_too_small = y_too_small_file.y_too_small('y_too_small')
    move = move_file.move('move', environment, 0, 1)
    try_up = py_trees.composites.Sequence(name = 'try_up', memory = False, children = [y_too_small, move])
    y_too_big = y_too_big_file.y_too_big('y_too_big')
    move_1 = move_file.move('move_1', environment, 0, -1)
    try_down = py_trees.composites.Sequence(name = 'try_down', memory = False, children = [y_too_big, move_1])
    x_too_big = x_too_big_file.x_too_big('x_too_big')
    move_2 = move_file.move('move_2', environment, -1, 0)
    try_left = py_trees.composites.Sequence(name = 'try_left', memory = False, children = [x_too_big, move_2])
    x_too_small = x_too_small_file.x_too_small('x_too_small')
    move_3 = move_file.move('move_3', environment, 1, 0)
    try_right = py_trees.composites.Sequence(name = 'try_right', memory = False, children = [x_too_small, move_3])
    movement = py_trees.composites.Selector(name = 'movement', memory = False, children = [try_up, try_down, try_left, try_right])
    destination_and_movement = py_trees.composites.Sequence(name = 'destination_and_movement', memory = False, children = [destination, movement])
    drone_control = py_trees.composites.Selector(name = 'drone_control', memory = False, children = [vision, destination_and_movement])
    return drone_control
