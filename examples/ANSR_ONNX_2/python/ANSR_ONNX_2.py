from pathlib import Path
import py_trees
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
import onnxruntime


def create_blackboard(serene_randomizer):
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'prev_dest_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.prev_dest_x = None
    blackboard_reader.register_key(key = 'cur_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.cur_x = None
    blackboard_reader.register_key(key = 'cur_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.cur_y = None
    blackboard_reader.register_key(key = 'x_mid', access = py_trees.common.Access.WRITE)
    blackboard_reader.x_mid = None
    blackboard_reader.register_key(key = 'cur_x_bool', access = py_trees.common.Access.WRITE)
    blackboard_reader.cur_x_bool = None
    blackboard_reader.register_key(key = 'dest_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.dest_x = None
    blackboard_reader.register_key(key = 'dest_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.dest_y = None
    blackboard_reader.register_key(key = 'dir', access = py_trees.common.Access.WRITE)
    blackboard_reader.dir = None
    blackboard_reader.register_key(key = 'dir_int', access = py_trees.common.Access.WRITE)
    blackboard_reader.dir_int = None
    blackboard_reader.register_key(key = 'victory', access = py_trees.common.Access.WRITE)
    blackboard_reader.victory = None
    blackboard_reader.register_key(key = 'x_net', access = py_trees.common.Access.WRITE)
    blackboard_reader.x_net = None
    blackboard_reader.register_key(key = 'y_net', access = py_trees.common.Access.WRITE)
    blackboard_reader.y_net = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    blackboard_reader.prev_dest_x = blackboard_reader.serene_randomizer.r_10(None)
    blackboard_reader.cur_x = blackboard_reader.serene_randomizer.r_11(None)
    blackboard_reader.cur_y = blackboard_reader.serene_randomizer.r_12(None)


    def x_mid():
        return blackboard_reader.serene_randomizer.r_13(None)

    blackboard_reader.x_mid = x_mid


    def cur_x_bool():
        return (
            blackboard_reader.serene_randomizer.r_14(None)
            if (blackboard_reader.cur_x < blackboard_reader.x_mid()) else
            (
            blackboard_reader.serene_randomizer.r_15(None)
        ))

    blackboard_reader.cur_x_bool = cur_x_bool
    blackboard_reader.dest_x = blackboard_reader.serene_randomizer.r_16(None)
    blackboard_reader.dest_y = blackboard_reader.serene_randomizer.r_17(None)
    blackboard_reader.dir = blackboard_reader.serene_randomizer.r_18(None)


    def dir_int():
        return (
            blackboard_reader.serene_randomizer.r_19(None)
            if (blackboard_reader.dir == 'Up') else
            (
            blackboard_reader.serene_randomizer.r_20(None)
        ))

    blackboard_reader.dir_int = dir_int
    blackboard_reader.victory = blackboard_reader.serene_randomizer.r_21(None)


    x_net__session__ = onnxruntime.InferenceSession(str(Path(__file__).parent.resolve()) + '/./networks/x_net.onnx')
    x_net__previous_input__ = None
    x_net__previous_output__ = None
    def x_net(index):
        input_values = [blackboard_reader.prev_dest_x]
        nonlocal x_net__session__, x_net__previous_input__, x_net__previous_output__
        if input_values != x_net__previous_input__:
            temp = x_net__session__.run(None, {'my_inputs' : [input_values]})
            x_net__previous_input__ = input_values
            x_net__previous_output__ = temp[0][0]
        return int(x_net__previous_output__[index])
    blackboard_reader.x_net = x_net


    y_net__session__ = onnxruntime.InferenceSession(str(Path(__file__).parent.resolve()) + '/./networks/y_net.onnx')
    y_net__previous_input__ = None
    y_net__previous_output__ = None
    def y_net(index):
        input_values = [blackboard_reader.cur_x_bool(), blackboard_reader.prev_dest_x]
        nonlocal y_net__session__, y_net__previous_input__, y_net__previous_output__
        if input_values != y_net__previous_input__:
            temp = y_net__session__.run(None, {'my_inputs' : [input_values]})
            y_net__previous_input__ = input_values
            y_net__previous_output__ = temp[0][0]
        return int(y_net__previous_output__[index])
    blackboard_reader.y_net = y_net
    return


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
    go_up = move_file.move('go_up', environment, 0, 1)
    try_up = py_trees.composites.Sequence(name = 'try_up', memory = False, children = [y_too_small, go_up])
    y_too_big = y_too_big_file.y_too_big('y_too_big')
    go_down = move_file.move('go_down', environment, 0, (-1))
    try_down = py_trees.composites.Sequence(name = 'try_down', memory = False, children = [y_too_big, go_down])
    x_too_big = x_too_big_file.x_too_big('x_too_big')
    go_left = move_file.move('go_left', environment, (-1), 0)
    try_left = py_trees.composites.Sequence(name = 'try_left', memory = False, children = [x_too_big, go_left])
    x_too_small = x_too_small_file.x_too_small('x_too_small')
    go_right = move_file.move('go_right', environment, 1, 0)
    try_right = py_trees.composites.Sequence(name = 'try_right', memory = False, children = [x_too_small, go_right])
    movement = py_trees.composites.Selector(name = 'movement', memory = False, children = [try_up, try_down, try_left, try_right])
    destination_and_movement = py_trees.composites.Sequence(name = 'destination_and_movement', memory = False, children = [destination, movement])
    drone_control = py_trees.composites.Selector(name = 'drone_control', memory = False, children = [vision, destination_and_movement])
    return drone_control
