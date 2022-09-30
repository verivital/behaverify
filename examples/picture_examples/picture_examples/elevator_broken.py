import py_trees
import operator

def create_root(print_pic=False):
    GUARD_doors_are_closed = py_trees.behaviours.Dummy('GUARD_doors_are_closed')
    GUARD_doors_are_closed2 = py_trees.behaviours.Dummy('GUARD_doors_are_closed')
    GUARD_elevator_is_called = py_trees.behaviours.Dummy('GUARD_elevator_is_called')
    GUARD_at_rest_at_floor = py_trees.behaviours.Dummy('GUARD_at_rest_at_floor')

    ACTION_close_doors = py_trees.behaviours.Dummy('ACTION_close_doors')
    ACTION_open_doors = py_trees.behaviours.Dummy('ACTION_open_doors')
    ACTION_move = py_trees.behaviours.Dummy('ACTION_move')


    SEQUENCE_call = py_trees.composites.Sequence('SEQUENCE_call', memory = False)
    SELECTOR_closed_doors = py_trees.composites.Selector('SELECTOR_closed_doors', memory = False)
    SEQUENCE_open_doors = py_trees.composites.Sequence('SEQUENCE_open_doors', memory = False)
    SELECTOR_elevator = py_trees.composites.Selector('SELECTOR_elevator_1', memory = False)

    SELECTOR_closed_doors.add_children([GUARD_doors_are_closed, ACTION_close_doors])
    SEQUENCE_call.add_children([GUARD_elevator_is_called, SELECTOR_closed_doors, ACTION_move])
    SEQUENCE_open_doors.add_children([GUARD_at_rest_at_floor, GUARD_doors_are_closed2, ACTION_open_doors])
    SELECTOR_elevator.add_children([SEQUENCE_call, SEQUENCE_open_doors])
    
    if print_pic:
        py_trees.display.render_dot_tree(SELECTOR_elevator, with_blackboard_variables=True, target_directory = '../pictures')#works
    return SELECTOR_elevator

#create_root(True)
