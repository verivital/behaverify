import py_trees
import ebt.bt.not_near_goal_index_file as not_near_goal_index_file
import ebt.bt.not_near_path_segment_end_file as not_near_path_segment_end_file
import ebt.bt.obstacle_map_exists_check_file as obstacle_map_exists_check_file
import ebt.bt.path_exists_check_file as path_exists_check_file
import ebt.bt.path_segment_exists_check_file as path_segment_exists_check_file
import ebt.bt.path_valid_check_file as path_valid_check_file
import ebt.bt.sent_path_segment_check_file as sent_path_segment_check_file
import ebt.bt.compute_path_file as compute_path_file
import ebt.bt.compute_path_segment_file as compute_path_segment_file
import ebt.bt.handle_error_file as handle_error_file
import ebt.bt.read_goals_file as read_goals_file
import ebt.bt.read_initial_obstacle_map_file as read_initial_obstacle_map_file
import ebt.bt.read_obstacle_map_file as read_obstacle_map_file
import ebt.bt.read_position_file as read_position_file
import ebt.bt.send_path_segment_file as send_path_segment_file
import ebt.bt.remake_cost_graph_file as remake_cost_graph_file
import ebt.bt.update_goal_index_file as update_goal_index_file


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'goals', access = py_trees.common.Access.WRITE)
    blackboard_reader.goals = None
    blackboard_reader.register_key(key = 'goal_index', access = py_trees.common.Access.WRITE)
    blackboard_reader.goal_index = None
    blackboard_reader.register_key(key = 'obstacle_map', access = py_trees.common.Access.WRITE)
    blackboard_reader.obstacle_map = None
    blackboard_reader.register_key(key = 'map_info', access = py_trees.common.Access.WRITE)
    blackboard_reader.map_info = None
    blackboard_reader.register_key(key = 'cost_graph', access = py_trees.common.Access.WRITE)
    blackboard_reader.cost_graph = None
    blackboard_reader.register_key(key = 'path', access = py_trees.common.Access.WRITE)
    blackboard_reader.path = None
    blackboard_reader.register_key(key = 'path_segment', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_segment = None # pair (start, end) marking the slice of the path. start is inclusive, end is not.
    blackboard_reader.register_key(key = 'path_segment_sent', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_segment_sent = None
    blackboard_reader.register_key(key = 'position', access = py_trees.common.Access.WRITE)
    blackboard_reader.position = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    blackboard_reader.goals = []
    blackboard_reader.goal_index = 0
    blackboard_reader.obstacle_map = None
    blackboard_reader.map_info = None #{'origin' : None, 'x_size' : None, 'y_size' : None}
    blackboard_reader.cost_graph = None
    blackboard_reader.path = []
    blackboard_reader.path_segment = (0, 0)
    blackboard_reader.path_segment_sent = False
    blackboard_reader.position = None
    return


def create_tree(
        environment,
        convert_planner_to_bt,
        convert_odometry_to_bt,
        convert_bt_to_a_star,
        convert_bt_to_waypoint,
        near_goal_function,
        near_path_segment_end_function,
        obstacle_at_point_function,
        reformat_obstacle_map_function,
        create_cost_graph_function,
        update_cost_graph_function
):
    obstacle_map_exists_check = obstacle_map_exists_check_file.obstacle_map_exists_check('obstacle_map_exists_check')
    read_initial_obstacle_map = read_initial_obstacle_map_file.read_initial_obstacle_map('read_initial_obstacle_map', environment, reformat_obstacle_map_function, create_cost_graph_function)
    initial_map_selector = py_trees.composites.Selector(name = 'initial_map_selector', memory = False, children = [obstacle_map_exists_check, read_initial_obstacle_map])
    read_goals = read_goals_file.read_goals('read_goals', environment, convert_planner_to_bt)
    read_position = read_position_file.read_position('read_position', environment, convert_odometry_to_bt)
    read_obstacle_map = read_obstacle_map_file.read_obstacle_map('read_obstacle_map', environment, reformat_obstacle_map_function, update_cost_graph_function)
    not_near_goal_index = not_near_goal_index_file.not_near_goal_index('not_near_goal_index', near_goal_function)
    update_goal_index = update_goal_index_file.update_goal_index('update_goal_index', environment)
    update_goal_index_selector = py_trees.composites.Selector(name = 'update_goal_index_selector', memory = False, children = [not_near_goal_index, update_goal_index])
    path_exists_check = path_exists_check_file.path_exists_check('path_exists_check')
    path_valid_check_0 = path_valid_check_file('path_valid_check_0', obstacle_at_point_function)
    path_exists_sequence = py_trees.composites.Sequence(name = 'path_exists_sequence', memory = False, children = [path_exists_check, path_valid_check_0])
    compute_path_0 = compute_path_file.compute_path('compute_path_0', environment, convert_bt_to_a_star)
    path_valid_check_1 = path_valid_check_file.path_valid_check('path_valid_check_1', obstacle_at_point_function)
    compute_path_sequence = py_trees.composites.Sequence(name = 'compute_path_sequence', memory = False, children = [compute_path_0, path_valid_check_1])
    remake_cost_graph = remake_cost_graph_file.remake_cost_graph('remake_cost_graph', environment, create_cost_graph_function)
    compute_path_1 = compute_path_file.compute_path('compute_path_1', environment, convert_bt_to_a_star)
    path_valid_check_2 = path_valid_check_file.path_valid_check('path_valid_check_2', obstacle_at_point_function)
    compute_path_with_map_update_sequence = py_trees.composites.Sequence(name = 'compute_path_with_map_update_sequence', memory = False, children = [remake_cost_graph, compute_path_1, path_valid_check_2])
    handle_error = handle_error_file.handle_error('handle_error', environment)
    compute_path_selector = py_trees.composites.Selector(name = 'compute_path_selector', memory = False, children = [path_exists_sequence, compute_path_sequence, compute_path_with_map_update_sequence, handle_error])
    path_segment_exists_check = path_segment_exists_check_file.path_segment_exists_check('path_segment_exists_check')
    not_near_path_segment_end = not_near_path_segment_end_file.not_near_path_segment_end('not_near_path_segment_end', near_path_segment_end_function)
    compute_path_segment_sequence = py_trees.composites.Sequence(name = 'compute_path_segment_sequence', memory = False, children = [path_segment_exists_check, not_near_path_segment_end])
    compute_path_segment = compute_path_segment_file.compute_path_segment('compute_path_segment', environment)
    compute_path_segment_selector = py_trees.composites.Selector(name = 'compute_path_segment_selector', memory = False, children = [compute_path_segment_sequence, compute_path_segment])
    sent_path_segment_check = sent_path_segment_check_file.sent_path_segment_check('sent_path_segment_check')
    send_path_segment = send_path_segment_file.send_path_segment('send_path_segment', environment, convert_bt_to_waypoint)
    send_path_segment_selector = py_trees.composites.Selector(name = 'send_path_segment_selector', memory = False, children = [sent_path_segment_check, send_path_segment])
    drone_control = py_trees.composites.Sequence(name = 'drone_control', memory = False, children = [initial_map_selector, read_goals, read_position, read_obstacle_map, update_goal_index_selector, compute_path_selector, compute_path_segment_selector, send_path_segment_selector])
    return drone_control
