import x_strategy_file
import y_strategy_file
import get_info_file
import request_hold_file
import request_reset_file
import request_up_file
import request_down_file
import request_left_file
import request_right_file
import set_new_subgoal_file
import change_strategy_file
import sometimes_change_strategy_file
import fell_in_hole_file
import up_bad_file
import down_bad_file
import left_bad_file
import right_bad_file
import up_unknown_file
import down_unknown_file
import left_unknown_file
import right_unknown_file
import need_new_subgoal_file
import need_up_file
import need_down_file
import need_left_file
import need_right_file
import reached_goal_file
import subgoal_unreachable_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'tiles', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'action', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'sometimes', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'strategy', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'subgoal', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_subgoal', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_subgoal', access = py_trees.common.Access.WRITE)
    blackboard_reader.tiles = [None] * 16
    __temp_var__ = serene_safe_assignment.tiles([(0, 'unknown'), (1, 'unknown'), (2, 'unknown'), (3, 'unknown'), (4, 'unknown'), (5, 'unknown'), (6, 'unknown'), (7, 'unknown'), (8, 'unknown'), (9, 'unknown'), (10, 'unknown'), (11, 'unknown'), (12, 'unknown'), (13, 'unknown'), (14, 'unknown'), (15, 'unknown')])
    for (index, val) in __temp_var__:
        blackboard_reader.tiles[index] = val
    blackboard_reader.action = serene_safe_assignment.action(-2)
    blackboard_reader.sometimes = serene_safe_assignment.sometimes(False)
    blackboard_reader.strategy = serene_safe_assignment.strategy('x_first')
    blackboard_reader.subgoal = serene_safe_assignment.subgoal(0)


    def x_subgoal():
        return (blackboard_reader.subgoal % 4)

    blackboard_reader.x_subgoal = x_subgoal


    def y_subgoal():
        return ((blackboard_reader.subgoal - blackboard_reader.x_subgoal()) // 4)

    blackboard_reader.y_subgoal = y_subgoal
    return blackboard_reader


def create_tree(environment):
    get_info = get_info_file.get_info('get_info', environment)
    reached_goal = reached_goal_file.reached_goal('reached_goal', environment)
    request_hold = request_hold_file.request_hold('request_hold', environment)
    at_goal_sequence = py_trees.composites.Sequence(name = 'at_goal_sequence', memory = False, children = [reached_goal, request_hold])
    fell_in_hole = fell_in_hole_file.fell_in_hole('fell_in_hole', environment)
    request_reset = request_reset_file.request_reset('request_reset', environment)
    reset_sequence = py_trees.composites.Sequence(name = 'reset_sequence', memory = False, children = [fell_in_hole, request_reset])
    up_unknown = up_unknown_file.up_unknown('up_unknown', environment)
    request_up = request_up_file.request_up('request_up', environment)
    up_unknown_seq = py_trees.composites.Sequence(name = 'up_unknown_seq', memory = False, children = [up_unknown, request_up])
    down_unknown = down_unknown_file.down_unknown('down_unknown', environment)
    request_down = request_down_file.request_down('request_down', environment)
    down_unknown_seq = py_trees.composites.Sequence(name = 'down_unknown_seq', memory = False, children = [down_unknown, request_down])
    left_unknown = left_unknown_file.left_unknown('left_unknown', environment)
    request_left = request_left_file.request_left('request_left', environment)
    left_unknown_seq = py_trees.composites.Sequence(name = 'left_unknown_seq', memory = False, children = [left_unknown, request_left])
    right_unknown = right_unknown_file.right_unknown('right_unknown', environment)
    request_right = request_right_file.request_right('request_right', environment)
    right_unknown_seq = py_trees.composites.Sequence(name = 'right_unknown_seq', memory = False, children = [right_unknown, request_right])
    adjacent_unknown = py_trees.composites.Selector(name = 'adjacent_unknown', memory = False, children = [up_unknown_seq, down_unknown_seq, left_unknown_seq, right_unknown_seq])
    need_new_subgoal = need_new_subgoal_file.need_new_subgoal('need_new_subgoal', environment)
    set_new_subgoal = set_new_subgoal_file.set_new_subgoal('set_new_subgoal', environment)
    subgoal_seq = py_trees.composites.Sequence(name = 'subgoal_seq', memory = False, children = [need_new_subgoal, set_new_subgoal])
    subgoal_failure_is_success = py_trees.decorators.FailureIsSuccess(name = 'subgoal_failure_is_success', child = subgoal_seq)
    x_strategy = x_strategy_file.x_strategy('x_strategy')
    need_left = need_left_file.need_left('need_left', environment)
    left_bad = left_bad_file.left_bad('left_bad', environment)
    left_bad_inverter = py_trees.decorators.Inverter(name = 'left_bad_inverter', child = left_bad)
    request_left_1 = request_left_file.request_left('request_left_1', environment)
    try_left = py_trees.composites.Sequence(name = 'try_left', memory = False, children = [need_left, left_bad_inverter, request_left_1])
    need_right = need_right_file.need_right('need_right', environment)
    right_bad = right_bad_file.right_bad('right_bad', environment)
    right_bad_inverter = py_trees.decorators.Inverter(name = 'right_bad_inverter', child = right_bad)
    request_right_1 = request_right_file.request_right('request_right_1', environment)
    try_right = py_trees.composites.Sequence(name = 'try_right', memory = False, children = [need_right, right_bad_inverter, request_right_1])
    try_x = py_trees.composites.Selector(name = 'try_x', memory = False, children = [try_left, try_right])
    opt_x_movement = py_trees.composites.Sequence(name = 'opt_x_movement', memory = False, children = [x_strategy, try_x])
    y_strategy = y_strategy_file.y_strategy('y_strategy')
    need_up = need_up_file.need_up('need_up', environment)
    up_bad = up_bad_file.up_bad('up_bad', environment)
    up_bad_inverter = py_trees.decorators.Inverter(name = 'up_bad_inverter', child = up_bad)
    request_up_1 = request_up_file.request_up('request_up_1', environment)
    try_up = py_trees.composites.Sequence(name = 'try_up', memory = False, children = [need_up, up_bad_inverter, request_up_1])
    need_down = need_down_file.need_down('need_down', environment)
    down_bad = down_bad_file.down_bad('down_bad', environment)
    down_bad_inverter = py_trees.decorators.Inverter(name = 'down_bad_inverter', child = down_bad)
    request_down_1 = request_down_file.request_down('request_down_1', environment)
    try_down = py_trees.composites.Sequence(name = 'try_down', memory = False, children = [need_down, down_bad_inverter, request_down_1])
    try_y = py_trees.composites.Selector(name = 'try_y', memory = False, children = [try_up, try_down])
    opt_y_movement = py_trees.composites.Sequence(name = 'opt_y_movement', memory = False, children = [y_strategy, try_y])
    x_or_y_movement_selector = py_trees.composites.Selector(name = 'x_or_y_movement_selector', memory = False, children = [opt_x_movement, opt_y_movement])
    need_left_1 = need_left_file.need_left('need_left_1', environment)
    left_bad_1 = left_bad_file.left_bad('left_bad_1', environment)
    left_bad_inverter_1 = py_trees.decorators.Inverter(name = 'left_bad_inverter_1', child = left_bad_1)
    request_left_2 = request_left_file.request_left('request_left_2', environment)
    try_left_1 = py_trees.composites.Sequence(name = 'try_left_1', memory = False, children = [need_left_1, left_bad_inverter_1, request_left_2])
    need_right_1 = need_right_file.need_right('need_right_1', environment)
    right_bad_1 = right_bad_file.right_bad('right_bad_1', environment)
    right_bad_inverter_1 = py_trees.decorators.Inverter(name = 'right_bad_inverter_1', child = right_bad_1)
    request_right_2 = request_right_file.request_right('request_right_2', environment)
    try_right_1 = py_trees.composites.Sequence(name = 'try_right_1', memory = False, children = [need_right_1, right_bad_inverter_1, request_right_2])
    try_x_1 = py_trees.composites.Selector(name = 'try_x_1', memory = False, children = [try_left_1, try_right_1])
    need_up_1 = need_up_file.need_up('need_up_1', environment)
    up_bad_1 = up_bad_file.up_bad('up_bad_1', environment)
    up_bad_inverter_1 = py_trees.decorators.Inverter(name = 'up_bad_inverter_1', child = up_bad_1)
    request_up_2 = request_up_file.request_up('request_up_2', environment)
    try_up_1 = py_trees.composites.Sequence(name = 'try_up_1', memory = False, children = [need_up_1, up_bad_inverter_1, request_up_2])
    need_down_1 = need_down_file.need_down('need_down_1', environment)
    down_bad_1 = down_bad_file.down_bad('down_bad_1', environment)
    down_bad_inverter_1 = py_trees.decorators.Inverter(name = 'down_bad_inverter_1', child = down_bad_1)
    request_down_2 = request_down_file.request_down('request_down_2', environment)
    try_down_1 = py_trees.composites.Sequence(name = 'try_down_1', memory = False, children = [need_down_1, down_bad_inverter_1, request_down_2])
    try_y_1 = py_trees.composites.Selector(name = 'try_y_1', memory = False, children = [try_up_1, try_down_1])
    subgoal_unreachable = subgoal_unreachable_file.subgoal_unreachable('subgoal_unreachable', environment)
    request_hold_1 = request_hold_file.request_hold('request_hold_1', environment)
    new_subgoal_strategy = py_trees.composites.Sequence(name = 'new_subgoal_strategy', memory = False, children = [subgoal_unreachable, request_hold_1])
    x_strategy_1 = x_strategy_file.x_strategy('x_strategy_1')
    up_bad_2 = up_bad_file.up_bad('up_bad_2', environment)
    up_bad_inverter_2 = py_trees.decorators.Inverter(name = 'up_bad_inverter_2', child = up_bad_2)
    request_up_3 = request_up_file.request_up('request_up_3', environment)
    sometimes_change_strategy = sometimes_change_strategy_file.sometimes_change_strategy('sometimes_change_strategy', environment)
    navi_up = py_trees.composites.Sequence(name = 'navi_up', memory = False, children = [x_strategy_1, up_bad_inverter_2, request_up_3, sometimes_change_strategy])
    x_strategy_2 = x_strategy_file.x_strategy('x_strategy_2')
    down_bad_2 = down_bad_file.down_bad('down_bad_2', environment)
    down_bad_inverter_2 = py_trees.decorators.Inverter(name = 'down_bad_inverter_2', child = down_bad_2)
    request_down_3 = request_down_file.request_down('request_down_3', environment)
    sometimes_change_strategy_1 = sometimes_change_strategy_file.sometimes_change_strategy('sometimes_change_strategy_1', environment)
    navi_down = py_trees.composites.Sequence(name = 'navi_down', memory = False, children = [x_strategy_2, down_bad_inverter_2, request_down_3, sometimes_change_strategy_1])
    y_strategy_1 = y_strategy_file.y_strategy('y_strategy_1')
    left_bad_2 = left_bad_file.left_bad('left_bad_2', environment)
    left_bad_inverter_2 = py_trees.decorators.Inverter(name = 'left_bad_inverter_2', child = left_bad_2)
    request_left_3 = request_left_file.request_left('request_left_3', environment)
    sometimes_change_strategy_2 = sometimes_change_strategy_file.sometimes_change_strategy('sometimes_change_strategy_2', environment)
    navi_left = py_trees.composites.Sequence(name = 'navi_left', memory = False, children = [y_strategy_1, left_bad_inverter_2, request_left_3, sometimes_change_strategy_2])
    y_strategy_2 = y_strategy_file.y_strategy('y_strategy_2')
    right_bad_2 = right_bad_file.right_bad('right_bad_2', environment)
    right_bad_inverter_2 = py_trees.decorators.Inverter(name = 'right_bad_inverter_2', child = right_bad_2)
    request_right_3 = request_right_file.request_right('request_right_3', environment)
    sometimes_change_strategy_3 = sometimes_change_strategy_file.sometimes_change_strategy('sometimes_change_strategy_3', environment)
    navi_right = py_trees.composites.Sequence(name = 'navi_right', memory = False, children = [y_strategy_2, right_bad_inverter_2, request_right_3, sometimes_change_strategy_3])
    request_hold_2 = request_hold_file.request_hold('request_hold_2', environment)
    change_strategy = change_strategy_file.change_strategy('change_strategy', environment)
    hold_and_change = py_trees.composites.Sequence(name = 'hold_and_change', memory = False, children = [request_hold_2, change_strategy])
    new_navigation_strategy = py_trees.composites.Selector(name = 'new_navigation_strategy', memory = False, children = [navi_up, navi_down, navi_left, navi_right, hold_and_change])
    failure_plan = py_trees.composites.Selector(name = 'failure_plan', memory = False, children = [new_subgoal_strategy, new_navigation_strategy])
    move_selector = py_trees.composites.Selector(name = 'move_selector', memory = False, children = [x_or_y_movement_selector, try_x_1, try_y_1, failure_plan])
    navigation_sequence = py_trees.composites.Sequence(name = 'navigation_sequence', memory = False, children = [subgoal_failure_is_success, move_selector])
    pick_action = py_trees.composites.Selector(name = 'pick_action', memory = False, children = [at_goal_sequence, reset_sequence, adjacent_unknown, navigation_sequence])
    execution_sequence = py_trees.composites.Sequence(name = 'execution_sequence', memory = False, children = [get_info, pick_action])
    return execution_sequence
