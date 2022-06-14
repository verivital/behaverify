import py_trees
import operator
import random

def create_root(print_pic = False, val1 = -2, val2 = -2):

    robot = py_trees.composites.Selector('robot')
    
    battery_seq = py_trees.composites.Sequence('battery_seq')
    battery_level_good = py_trees.behaviours.Dummy('battery_level_good')
    recharge_seq = py_trees.composites.Sequence('recharge_seq')
    nav_to_station = py_trees.composites.Selector('nav_to_station')
    station_reached = py_trees.behaviours.Dummy('station_reached')
    move_to_station = py_trees.behaviours.Dummy('move_to_station')
    recharge = py_trees.behaviours.Dummy('recharge')

    confirm_mission = 
    mission_ = py_trees.composites.??()
    nav_to_target = py_trees.composites.Selector('nav_to_target')
    target_reached = py_trees.behaviours.Dummy('target_reached')
    move_to_target = py_trees.behaviours.Dummy('move_to_target')
    
    interact
    if print_pic:
        py_trees.display.render_dot_tree(gcd_root, with_blackboard_variables=True)

    return gcd_root
