import is_path_computed_file
import is_waypoint_reached_file
import is_close_to_landmark_file
import compute_path_file
import get_next_landmark_file
import get_next_subgoal_file
import move_action_file
import py_trees
import serene_safe_assignment
import random
import onnxruntime


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'path_computed_bool', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'drone_location', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'drone_velocity', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'waypoint_location', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'path_storage_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'path_storage_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'landmark_index', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'current_landmark', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'subgoal', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_computed_bool = serene_safe_assignment.path_computed_bool(False)
    blackboard_reader.drone_location = [0 for _ in range(2)]
    __temp_var__ = serene_safe_assignment.drone_location([])
    for (index, val) in __temp_var__:
        blackboard_reader.drone_location[index] = val
    blackboard_reader.drone_velocity = [0 for _ in range(2)]
    __temp_var__ = serene_safe_assignment.drone_velocity([])
    for (index, val) in __temp_var__:
        blackboard_reader.drone_velocity[index] = val
    blackboard_reader.waypoint_location = [1 for _ in range(2)]
    __temp_var__ = serene_safe_assignment.waypoint_location([])
    for (index, val) in __temp_var__:
        blackboard_reader.waypoint_location[index] = val
    blackboard_reader.path_storage_x = [0 for _ in range(25)]
    __temp_var__ = serene_safe_assignment.path_storage_x([])
    for (index, val) in __temp_var__:
        blackboard_reader.path_storage_x[index] = val
    blackboard_reader.path_storage_y = [0 for _ in range(25)]
    __temp_var__ = serene_safe_assignment.path_storage_y([])
    for (index, val) in __temp_var__:
        blackboard_reader.path_storage_y[index] = val
    blackboard_reader.landmark_index = serene_safe_assignment.landmark_index(0)


    def current_landmark(index):
        if type(index) is not int:
            raise TypeError('Index must be an int when accessing current_landmark: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing current_landmark: ' + str(index))
        current_landmark = [0 for _ in range(2)]
        seen_indices = set()
        for (new_index, new_value) in [(0, blackboard_reader.path_storage_x[serene_safe_assignment.index_func(blackboard_reader.landmark_index, 25)]), (1, blackboard_reader.path_storage_y[serene_safe_assignment.index_func(blackboard_reader.landmark_index, 25)])]:
            if new_index in seen_indices:
                continue
            seen_indices.add(new_index)
            if type(new_index) is not int:
                raise TypeError('Index must be an int when accessing current_landmark: ' + str(type(new_index)))
            if new_index < 0 or new_index >= 2:
                raise ValueError('Index out of bounds when accessing current_landmark: ' + str(new_index))
            if type(new_value) not in {int, float}:
                raise ValueError('Variable current_landmark is type float. Got ' + str(type(new_value)))
            current_landmark[new_index] = new_value
        return current_landmark[index]

    blackboard_reader.current_landmark = current_landmark
    blackboard_reader.subgoal = [0 for _ in range(2)]
    __temp_var__ = serene_safe_assignment.subgoal([])
    for (index, val) in __temp_var__:
        blackboard_reader.subgoal[index] = val
    return blackboard_reader


def create_tree(environment):
    is_path_computed = is_path_computed_file.is_path_computed('is_path_computed')
    compute_path = compute_path_file.compute_path('compute_path', environment)
    path_selector = py_trees.composites.Selector(name = 'path_selector', memory = False, children = [is_path_computed, compute_path])
    is_waypoint_reached = is_waypoint_reached_file.is_waypoint_reached('is_waypoint_reached')
    is_close_to_landmark = is_close_to_landmark_file.is_close_to_landmark('is_close_to_landmark')
    get_next_landmark = get_next_landmark_file.get_next_landmark('get_next_landmark', environment)
    landmark_sequence = py_trees.composites.Sequence(name = 'landmark_sequence', memory = False, children = [is_close_to_landmark, get_next_landmark])
    get_next_subgoal = get_next_subgoal_file.get_next_subgoal('get_next_subgoal', environment)
    move_action = move_action_file.move_action('move_action', environment)
    movement_sequence = py_trees.composites.Sequence(name = 'movement_sequence', memory = False, children = [get_next_subgoal, move_action])
    main_selector = py_trees.composites.Selector(name = 'main_selector', memory = False, children = [is_waypoint_reached, landmark_sequence, movement_sequence])
    ebt_root = py_trees.composites.Sequence(name = 'ebt_root', memory = False, children = [path_selector, main_selector])
    return ebt_root
