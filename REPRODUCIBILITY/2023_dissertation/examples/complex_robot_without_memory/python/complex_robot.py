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
import serene_safe_assignment


def create_tree():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'zone', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'side', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'have_flag', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'need_side_reached', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'forward', access = py_trees.common.Access.WRITE)
    blackboard_reader.zone = serene_safe_assignment.zone('home')
    blackboard_reader.side = serene_safe_assignment.side(1)
    blackboard_reader.have_flag = serene_safe_assignment.have_flag(False)
    blackboard_reader.need_side_reached = serene_safe_assignment.need_side_reached(True)


    def forward():
        if blackboard_reader.have_flag:
            forward_return_val = -1
        else:
            forward_return_val = 1
        return forward_return_val

    blackboard_reader.forward = forward

    set_zone = set_zone_file.set_zone('set_zone')
    flag_not_returned = flag_not_returned_file.flag_not_returned('flag_not_returned')
    in_maze = in_maze_file.in_maze('in_maze')
    can_move_forward = can_move_forward_file.can_move_forward('can_move_forward')
    go_forward = go_forward_file.go_forward('go_forward')
    try_forward = py_trees.composites.Sequence(name = 'try_forward', memory = False, children = [can_move_forward, go_forward])
    can_move_side = can_move_side_file.can_move_side('can_move_side')
    go_side = go_side_file.go_side('go_side')
    try_side = py_trees.composites.Sequence(name = 'try_side', memory = False, children = [can_move_side, go_side])
    change_side = change_side_file.change_side('change_side')
    return_failure = py_trees.decorators.SuccessIsFailure(name = 'return_failure', child = change_side)
    try_side_or_change = py_trees.composites.Selector(name = 'try_side_or_change', memory = False, children = [try_side, return_failure])
    success_node = success_node_file.success_node('success_node')
    move_through_maze = py_trees.composites.Selector(name = 'move_through_maze', memory = False, children = [try_forward, try_side_or_change, success_node])
    move_through_maze_decorator = py_trees.decorators.SuccessIsRunning(name = 'move_through_maze_decorator', child = move_through_maze)
    navigate_maze = py_trees.composites.Sequence(name = 'navigate_maze', memory = False, children = [in_maze, move_through_maze_decorator])
    in_maze_1 = in_maze_file.in_maze('in_maze_1')
    maze_inverter = py_trees.decorators.Inverter(name = 'maze_inverter', child = in_maze_1)
    in_target = in_target_file.in_target('in_target')
    flag_found = flag_found_file.flag_found('flag_found')
    go_home = py_trees.composites.Sequence(name = 'go_home', memory = False, children = [in_target, flag_found])
    in_home = in_home_file.in_home('in_home')
    flag_found_1 = flag_found_file.flag_found('flag_found_1')
    flag_inverter = py_trees.decorators.Inverter(name = 'flag_inverter', child = flag_found_1)
    go_target = py_trees.composites.Sequence(name = 'go_target', memory = False, children = [in_home, flag_inverter])
    traversal_needed = py_trees.composites.Selector(name = 'traversal_needed', memory = False, children = [go_home, go_target])
    go_forward_1 = go_forward_file.go_forward('go_forward_1')
    enter_maze = py_trees.composites.Sequence(name = 'enter_maze', memory = False, children = [maze_inverter, traversal_needed, go_forward_1])
    in_target_1 = in_target_file.in_target('in_target_1')
    need_side = need_side_file.need_side('need_side')
    can_move_side_1 = can_move_side_file.can_move_side('can_move_side_1')
    go_side_1 = go_side_file.go_side('go_side_1')
    try_side_1 = py_trees.composites.Sequence(name = 'try_side_1', memory = False, children = [can_move_side_1, go_side_1])
    change_side_1 = change_side_file.change_side('change_side_1')
    return_failure_1 = py_trees.decorators.SuccessIsFailure(name = 'return_failure_1', child = change_side_1)
    try_side_or_change_1 = py_trees.composites.Selector(name = 'try_side_or_change_1', memory = False, children = [try_side_1, return_failure_1])
    side_reached = py_trees.decorators.FailureIsSuccess(name = 'side_reached', child = try_side_or_change_1)
    never_need_side = never_need_side_file.never_need_side('never_need_side')
    to_side = py_trees.composites.Sequence(name = 'to_side', memory = False, children = [in_target_1, need_side, side_reached, never_need_side])
    in_target_2 = in_target_file.in_target('in_target_2')
    flag_found_2 = flag_found_file.flag_found('flag_found_2')
    flag_inverter_1 = py_trees.decorators.Inverter(name = 'flag_inverter_1', child = flag_found_2)
    search_tile = search_tile_file.search_tile('search_tile')
    can_move_side_2 = can_move_side_file.can_move_side('can_move_side_2')
    go_side_2 = go_side_file.go_side('go_side_2')
    try_side_2 = py_trees.composites.Sequence(name = 'try_side_2', memory = False, children = [can_move_side_2, go_side_2])
    change_side_2 = change_side_file.change_side('change_side_2')
    return_failure_2 = py_trees.decorators.SuccessIsFailure(name = 'return_failure_2', child = change_side_2)
    try_side_or_change_2 = py_trees.composites.Selector(name = 'try_side_or_change_2', memory = False, children = [try_side_2, return_failure_2])
    go_forward_2 = go_forward_file.go_forward('go_forward_2')
    move_for_flag = py_trees.composites.Selector(name = 'move_for_flag', memory = False, children = [try_side_or_change_2, go_forward_2])
    search_for_flag = py_trees.composites.Selector(name = 'search_for_flag', memory = False, children = [search_tile, move_for_flag])
    search_target = py_trees.composites.Sequence(name = 'search_target', memory = False, children = [in_target_2, flag_inverter_1, search_for_flag])
    control_selector = py_trees.composites.Selector(name = 'control_selector', memory = False, children = [navigate_maze, enter_maze, to_side, search_target])
    control_sequence = py_trees.composites.Sequence(name = 'control_sequence', memory = False, children = [flag_not_returned, control_selector])
    control = py_trees.composites.Parallel(name = 'control', policy = py_trees.common.ParallelPolicy.SuccessOnAll(False), children = [set_zone, control_sequence])
    return control
