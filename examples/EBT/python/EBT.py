from pathlib import Path
import py_trees
import is_path_computed_file
import is_waypoint_reached_file
import is_close_to_landmark_file
import compute_path_file
import get_next_landmark_file
import get_next_subgoal_file
import move_action_file
import onnxruntime
import user_blackboard_generator


def create_blackboard(serene_randomizer):
    blackboard_reader = user_blackboard_generator.create_blackboard()
    # blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'path_computed_bool', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_computed_bool = None
    blackboard_reader.register_key(key = 'drone_location', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_location = None
    blackboard_reader.register_key(key = 'drone_velocity', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_velocity = None
    blackboard_reader.register_key(key = 'waypoint_location', access = py_trees.common.Access.WRITE)
    blackboard_reader.waypoint_location = None
    blackboard_reader.register_key(key = 'path_storage_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_storage_x = None
    blackboard_reader.register_key(key = 'path_storage_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.path_storage_y = None
    blackboard_reader.register_key(key = 'landmark_index', access = py_trees.common.Access.WRITE)
    blackboard_reader.landmark_index = None
    blackboard_reader.register_key(key = 'current_landmark', access = py_trees.common.Access.WRITE)
    blackboard_reader.current_landmark = None
    blackboard_reader.register_key(key = 'subgoal', access = py_trees.common.Access.WRITE)
    blackboard_reader.subgoal = None
    
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    blackboard_reader.path_computed_bool = blackboard_reader.serene_randomizer.r_2(None)
    blackboard_reader.drone_location = [blackboard_reader.serene_randomizer.r_3(None) for _ in range(2)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.drone_location[index] = val
    blackboard_reader.drone_velocity = [blackboard_reader.serene_randomizer.r_4(None) for _ in range(2)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.drone_velocity[index] = val
    blackboard_reader.waypoint_location = [blackboard_reader.serene_randomizer.r_5(None) for _ in range(2)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.waypoint_location[index] = val
    blackboard_reader.path_storage_x = [blackboard_reader.serene_randomizer.r_6(None) for _ in range(25)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.path_storage_x[index] = val
    blackboard_reader.path_storage_y = [blackboard_reader.serene_randomizer.r_7(None) for _ in range(25)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.path_storage_y[index] = val
    blackboard_reader.landmark_index = blackboard_reader.serene_randomizer.r_8(None)


    def current_landmark(index):
        current_landmark = [blackboard_reader.serene_randomizer.r_9(None) for _ in range(2)]
        seen_indices = set()
        for (new_index, new_value) in [(0, blackboard_reader.serene_randomizer.r_10(None)), (1, blackboard_reader.serene_randomizer.r_11(None))]:
            if new_index in seen_indices:
                continue
            seen_indices.add(new_index)
            current_landmark[new_index] = new_value
        return current_landmark[index]

    blackboard_reader.current_landmark = current_landmark
    blackboard_reader.subgoal = [blackboard_reader.serene_randomizer.r_12(None) for _ in range(2)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.subgoal[index] = val
    return


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
