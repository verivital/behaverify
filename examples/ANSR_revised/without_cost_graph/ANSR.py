import py_trees
from ebt.bt.check_near_path_file import check_near_path
from ebt.bt.check_not_near_goal_index_file import check_not_near_goal_index
from ebt.bt.check_not_near_path_segment_end_file import check_not_near_path_segment_end
from ebt.bt.check_obstacle_map_exists_file import check_obstacle_map_exists
from ebt.bt.check_path_exists_file import check_path_exists
from ebt.bt.check_path_segment_exists_file import check_path_segment_exists
from ebt.bt.check_path_valid_file import check_path_valid
from ebt.bt.check_sent_path_segment_file import check_sent_path_segment
from ebt.bt.action_compute_path_file import action_compute_path
from ebt.bt.action_compute_path_segment_file import action_compute_path_segment
from ebt.bt.action_handle_error_file import action_handle_error
from ebt.bt.action_read_goals_file import action_read_goals
from ebt.bt.action_read_initial_obstacle_map_file import action_read_initial_obstacle_map
from ebt.bt.action_read_obstacle_map_file import action_read_obstacle_map
from ebt.bt.action_read_position_file import action_read_position
from ebt.bt.action_send_path_segment_file import action_send_path_segment
from ebt.bt.action_update_goal_index_file import action_update_goal_index


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'flight_heights', access = py_trees.common.Access.WRITE)
    blackboard_reader.flight_heights = []
    blackboard_reader.register_key(key = 'goals', access = py_trees.common.Access.WRITE)
    blackboard_reader.goals = None
    blackboard_reader.register_key(key = 'goal_index', access = py_trees.common.Access.WRITE)
    blackboard_reader.goal_index = None
    blackboard_reader.register_key(key = 'obstacle_map', access = py_trees.common.Access.WRITE)
    blackboard_reader.obstacle_map = None
    blackboard_reader.register_key(key = 'map_info', access = py_trees.common.Access.WRITE)
    blackboard_reader.map_info = None
    blackboard_reader.register_key(key = 'path', access = py_trees.common.Access.WRITE)
    blackboard_reader.path = None
    blackboard_reader.register_key(key = 'path_segment', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_segment = None # end index, not inclusive.
    blackboard_reader.register_key(key = 'path_segment_sent', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_segment_sent = None
    blackboard_reader.register_key(key = 'position', access = py_trees.common.Access.WRITE)
    blackboard_reader.position = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader, flight_heights):
    blackboard_reader.flight_heights = flight_heights
    blackboard_reader.goals = []
    blackboard_reader.goal_index = 0
    blackboard_reader.obstacle_map = None
    blackboard_reader.map_info = None #{'origin' : None, 'x_size' : None, 'y_size' : None}
    blackboard_reader.path = []
    blackboard_reader.path_segment = 0
    blackboard_reader.path_segment_sent = False
    blackboard_reader.position = None
    return


def create_tree(
        environment,
        function_convert_bt_to_a_star,
        function_convert_bt_to_waypoint,
        function_convert_planner_to_bt,
        function_convert_odometry_to_bt,
        function_cost,
        function_near_goal,
        function_near_path_point,
        function_near_path_segment_end,
        function_obstacle_at_point,
        function_reformat_obstacle_map
):


    return py_trees.composites.Sequence(
        name = 'sequence_drone_control',
        memory = False,
        children = [
            py_trees.composites.Selector(
                name = 'selector_initial_map',
                memory = False,
                children = [
                    check_obstacle_map_exists('check_obstacle_map_exists'),
                    action_read_initial_obstacle_map('action_read_initial_obstacle_map', environment, function_reformat_obstacle_map)
                ]
            ),
            action_read_goals('action_read_goals', environment, function_convert_planner_to_bt),
            action_read_position('action_read_position', environment, function_convert_odometry_to_bt),
            action_read_obstacle_map('action_read_obstacle_map', environment, function_reformat_obstacle_map),
            py_trees.composites.Selector(
                name = 'selector_update_goal_index',
                memory = False,
                children = [
                    check_not_near_goal_index('check_not_near_goal_index', function_near_goal),
                    action_update_goal_index('action_update_goal_index', environment)
                ]
            ),
            py_trees.composites.Selector(
                name = 'selector_compute_path',
                memory = False,
                children = [
                    py_trees.composites.Sequence(
                        name = 'sequence_path_valid',
                        memory = False,
                        children = [
                            check_path_exists('check_path_exists'),
                            check_path_valid('check_path_valid_0', function_obstacle_at_point),
                            check_near_path('check_near_path', function_near_path_point)
                        ]
                    ),
                    py_trees.composites.Sequence(
                        name = 'sequence_compute_path',
                        memory = False,
                        children = [
                            action_compute_path('action_compute_path', environment, function_convert_bt_to_a_star, function_obstacle_at_point, function_cost),
                            check_path_valid('check_path_valid_1', function_obstacle_at_point)
                        ]
                    ),
                    py_trees.composites.Sequence(
                        name = 'sequence_in_obstacle',
                        memory = False,
                        children = [
                            check_in_obstacle('check_in_obstacle', function_obstacle_at_point),
                            action_elevate_drone('action_elevate_drone', environment)
                        ]
                    ),
                    action_handle_error('action_handle_error', environment)
                ]
            ),
            py_trees.composites.Selector(
                name = 'selector_compute_path_segment',
                memory = False,
                children = [
                    py_trees.composites.Sequence(
                        name = 'sequence_valid_path_segment',
                        memory = False,
                        children = [
                            check_path_segment_exists('check_path_segment_exists'),
                            check_not_near_path_segment_end('check_not_near_path_segment_end', function_near_path_segment_end)
                        ]
                    ),
                    action_compute_path_segment('action_compute_path_segment', environment)
                ]
            ),
            py_trees.composites.Selector(
                name = 'selector_send_path_segment',
                memory = False,
                children = [
                    check_sent_path_segment('check_sent_path_segment'),
                    action_send_path_segment('action_send_path_segment', environment, function_convert_bt_to_waypoint)
                ]
            )
        ]
    )
