import safe_battery_file
import read_battery_file
import execute_file
import py_trees


def create_tree():
    robot = py_trees.composites.Sequence('robot', False)
    read_battery = read_battery_file.read_battery('read_battery')
    safe_battery = safe_battery_file.safe_battery('safe_battery')
    execute = execute_file.execute('execute')
    robot.add_children([read_battery, safe_battery, execute])
    return robot
