import in_home_file
import in_maze_file
import in_target_file
import flag_found_file
import need_side_file
import success_node_file
import change_side_file
import go_forward_file
import go_side_file
import never_need_side_file
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
    blackboard_reader.register_key(key = 'need_side_reached', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'forward', access = py_trees.common.Access.WRITE)
    blackboard_reader.zone = 'home'
    blackboard_reader.side = 1
    blackboard_reader.have_flag = False
    blackboard_reader.need_side_reached = True


    def forward():
        if blackboard_reader.have_flag:
            forward_return_val = -1
        else:
            forward_return_val = 1
        return forward_return_val

    blackboard_reader.forward = forward

    control = py_trees.composites.Parallel('control', py_trees.common.ParallelPolicy.SuccessOnAll(False))
    set_zone = set_zone_file.set_zone('set_zone')
    control_sequence = py_trees.composites.Sequence('control_sequence', False)
    flag_not_returned = flag_not_returned_file.flag_not_returned('flag_not_returned')
    control_selector = py_trees.composites.Selector('control_selector', False)
    navigate_maze = py_trees.composites.Sequence('navigate_maze', False)
    in_maze = in_maze_file.in_maze('in_maze')
    move_through_maze = py_trees.composites.Selector('move_through_maze', False)
    try_forward = py_trees.composites.Sequence('try_forward', False)
    can_move_forward = can_move_forward_file.can_move_forward('can_move_forward')
    go_forward = go_forward_file.go_forward('go_forward')
    try_forward.add_children([can_move_forward, go_forward])
    try_side_or_change = py_trees.composites.Selector('try_side_or_change', False)
    try_side = py_trees.composites.Sequence('try_side', False)
    can_move_side = can_move_side_file.can_move_side('can_move_side')
    go_side = go_side_file.go_side('go_side')
    try_side.add_children([can_move_side, go_side])
    change_side = change_side_file.change_side('change_side')
    return_failure = py_trees.decorators.SuccessIsFailure(name = 'return_failure', child = change_side)
    try_side_or_change.add_children([try_side, return_failure])
    success_node = success_node_file.success_node('success_node')
    move_through_maze.add_children([try_forward, try_side_or_change, success_node])
    move_through_maze_decorator = py_trees.decorators.SuccessIsRunning(name = 'move_through_maze_decorator', child = move_through_maze)
    navigate_maze.add_children([in_maze, move_through_maze_decorator])
    enter_maze = py_trees.composites.Sequence('enter_maze', False)
    in_maze_1 = in_maze_file.in_maze('in_maze_1')
    maze_inverter = py_trees.decorators.Inverter(name = 'maze_inverter', child = in_maze_1)
    traversal_needed = py_trees.composites.Selector('traversal_needed', False)
    go_home = py_trees.composites.Sequence('go_home', False)
    in_target = in_target_file.in_target('in_target')
    flag_found = flag_found_file.flag_found('flag_found')
    go_home.add_children([in_target, flag_found])
    go_target = py_trees.composites.Sequence('go_target', False)
    in_home = in_home_file.in_home('in_home')
    flag_found_1 = flag_found_file.flag_found('flag_found_1')
    flag_inverter = py_trees.decorators.Inverter(name = 'flag_inverter', child = flag_found_1)
    go_target.add_children([in_home, flag_inverter])
    traversal_needed.add_children([go_home, go_target])
    go_forward_1 = go_forward_file.go_forward('go_forward_1')
    enter_maze.add_children([maze_inverter, traversal_needed, go_forward_1])
    to_side = py_trees.composites.Sequence('to_side', False)
    in_target_1 = in_target_file.in_target('in_target_1')
    need_side = need_side_file.need_side('need_side')
    try_side_or_change_1 = py_trees.composites.Selector('try_side_or_change_1', False)
    try_side_1 = py_trees.composites.Sequence('try_side_1', False)
    can_move_side_1 = can_move_side_file.can_move_side('can_move_side_1')
    go_side_1 = go_side_file.go_side('go_side_1')
    try_side_1.add_children([can_move_side_1, go_side_1])
    change_side_1 = change_side_file.change_side('change_side_1')
    return_failure_1 = py_trees.decorators.SuccessIsFailure(name = 'return_failure_1', child = change_side_1)
    try_side_or_change_1.add_children([try_side_1, return_failure_1])
    side_reached = py_trees.decorators.FailureIsSuccess(name = 'side_reached', child = try_side_or_change_1)
    never_need_side = never_need_side_file.never_need_side('never_need_side')
    to_side.add_children([in_target_1, need_side, side_reached, never_need_side])
    search_target = py_trees.composites.Sequence('search_target', False)
    in_target_2 = in_target_file.in_target('in_target_2')
    flag_found_2 = flag_found_file.flag_found('flag_found_2')
    flag_inverter_1 = py_trees.decorators.Inverter(name = 'flag_inverter_1', child = flag_found_2)
    search_for_flag = py_trees.composites.Selector('search_for_flag', False)
    search_tile = search_tile_file.search_tile('search_tile')
    move_for_flag = py_trees.composites.Selector('move_for_flag', False)
    try_side_or_change_2 = py_trees.composites.Selector('try_side_or_change_2', False)
    try_side_2 = py_trees.composites.Sequence('try_side_2', False)
    can_move_side_2 = can_move_side_file.can_move_side('can_move_side_2')
    go_side_2 = go_side_file.go_side('go_side_2')
    try_side_2.add_children([can_move_side_2, go_side_2])
    change_side_2 = change_side_file.change_side('change_side_2')
    return_failure_2 = py_trees.decorators.SuccessIsFailure(name = 'return_failure_2', child = change_side_2)
    try_side_or_change_2.add_children([try_side_2, return_failure_2])
    go_forward_2 = go_forward_file.go_forward('go_forward_2')
    move_for_flag.add_children([try_side_or_change_2, go_forward_2])
    search_for_flag.add_children([search_tile, move_for_flag])
    search_target.add_children([in_target_2, flag_inverter_1, search_for_flag])
    control_selector.add_children([navigate_maze, enter_maze, to_side, search_target])
    control_sequence.add_children([flag_not_returned, control_selector])
    control.add_children([set_zone, control_sequence])
    return control
