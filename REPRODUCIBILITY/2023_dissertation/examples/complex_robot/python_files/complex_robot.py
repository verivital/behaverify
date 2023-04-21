import in_maze_file
import in_target_file
import flag_found_file
import change_side_file
import go_forward_file
import go_side_file
import search_tile_file
import set_zone_file
import flag_not_returned_file
import can_move_forward_file
import can_move_side_file
import py_trees


def create_tree():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'zone', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'side', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'have_flag', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'forward', access = py_trees.common.Access.WRITE)
    blackboard_reader.zone = 'home'
    blackboard_reader.side = 1
    blackboard_reader.have_flag = False


    def forward():
        if blackboard_reader.have_flag:
            forward_return_val = -1
        else:
            forward_return_val = 1
        return forward_return_val

    blackboard_reader.forward = forward

    control = py_trees.composites.Parallel('control', py_trees.common.ParallelPolicy.SuccessOnAll(False))
    set_zone = set_zone_file.set_zone('set_zone')
    control_sequence = py_trees.composites.Sequence('control_sequence', True)
    flag_not_returned = flag_not_returned_file.flag_not_returned('flag_not_returned')
    enter_maze = py_trees.composites.Selector('enter_maze', False)
    in_maze = in_maze_file.in_maze('in_maze')
    go_forward = go_forward_file.go_forward('go_forward')
    enter_maze.add_children([in_maze, go_forward])
    navigate_maze = py_trees.composites.Selector('navigate_maze', False)
    in_maze_1 = in_maze_file.in_maze('in_maze_1')
    maze_inverter = py_trees.decorators.Inverter(name = 'maze_inverter', child = in_maze_1)
    move_through_maze = py_trees.composites.Selector('move_through_maze', False)
    try_forward = py_trees.composites.Sequence('try_forward', False)
    can_move_forward = can_move_forward_file.can_move_forward('can_move_forward')
    go_forward_1 = go_forward_file.go_forward('go_forward_1')
    try_forward.add_children([can_move_forward, go_forward_1])
    try_side = py_trees.composites.Sequence('try_side', False)
    can_move_side = can_move_side_file.can_move_side('can_move_side')
    go_side = go_side_file.go_side('go_side')
    try_side.add_children([can_move_side, go_side])
    change_side = change_side_file.change_side('change_side')
    move_through_maze.add_children([try_forward, try_side, change_side])
    move_through_maze_decorator = py_trees.decorators.SuccessIsRunning(name = 'move_through_maze_decorator', child = move_through_maze)
    navigate_maze.add_children([maze_inverter, move_through_maze_decorator])
    navigate_maze_decorator = py_trees.decorators.FailureIsRunning(name = 'navigate_maze_decorator', child = navigate_maze)
    in_target = in_target_file.in_target('in_target')
    try_side_1 = py_trees.composites.Sequence('try_side_1', False)
    can_move_side_1 = can_move_side_file.can_move_side('can_move_side_1')
    go_side_1 = go_side_file.go_side('go_side_1')
    try_side_1.add_children([can_move_side_1, go_side_1])
    to_side_decorator = py_trees.decorators.FailureIsSuccess(name = 'to_side_decorator', child = try_side_1)
    change_side_1 = change_side_file.change_side('change_side_1')
    have_or_find_flag = py_trees.composites.Selector('have_or_find_flag', False)
    flag_found = flag_found_file.flag_found('flag_found')
    search_for_flag = py_trees.composites.Selector('search_for_flag', False)
    search_tile = search_tile_file.search_tile('search_tile')
    move_for_flag = py_trees.composites.Selector('move_for_flag', False)
    try_side_2 = py_trees.composites.Sequence('try_side_2', False)
    can_move_side_2 = can_move_side_file.can_move_side('can_move_side_2')
    go_side_2 = go_side_file.go_side('go_side_2')
    try_side_2.add_children([can_move_side_2, go_side_2])
    change_side_2 = change_side_file.change_side('change_side_2')
    change_side_decorator = py_trees.decorators.SuccessIsFailure(name = 'change_side_decorator', child = change_side_2)
    go_forward_2 = go_forward_file.go_forward('go_forward_2')
    move_for_flag.add_children([try_side_2, change_side_decorator, go_forward_2])
    search_for_flag.add_children([search_tile, move_for_flag])
    have_or_find_flag.add_children([flag_found, search_for_flag])
    control_sequence.add_children([flag_not_returned, enter_maze, navigate_maze_decorator, in_target, to_side_decorator, change_side_1, have_or_find_flag])
    control.add_children([set_zone, control_sequence])
    return control
