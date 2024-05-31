import sys
import random
from obstacle_file import OBSTACLES, OBSTACLE_SIZES, OBSTACLE_QUERY
import ctypes
import os
THIS_LOCATION = os.path.dirname(os.path.abspath(__file__))
collision_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'collision_monitor.so'))
collision_monitor_lib.user_interface.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
collision_monitor_lib.user_interface.restype = ctypes.c_int
loop_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'loop_monitor.so'))
loop_monitor_lib.user_interface.argtypes = [ctypes.c_int, ctypes.c_bool]
loop_monitor_lib.user_interface.restype = ctypes.c_int

MAX_VAL = int(sys.argv[2])
NEEDS_RESET = False
drone_x = 0
drone_y = 0
monitor_var = None
for _ in range(int(sys.argv[1])):
    speed = 2
    action = random.choice([0, 1, 2, 3, 4])
    delta_x = (-1 if action == 0 else (1 if action == 1 else 0))
    delta_y = (-1 if action == 3 else (1 if action == 2 else 0))
    if OBSTACLE_QUERY[(min(MAX_VAL, max(0, drone_x + delta_x)), min(MAX_VAL, max(0, drone_y + delta_y)))]:
        delta_x = 0
        delta_y = 0
        action = 4
    monitor_var = collision_monitor_lib.user_interface(drone_x, drone_y, speed, delta_x, delta_y)
    if monitor_var > 1:
        speed = 1
    monitor_var = loop_monitor_lib.user_interface(action, NEEDS_RESET)
    if monitor_var > 1:
        speed = 1
        NEEDS_RESET = True
    drone_x = min(MAX_VAL, max(0, drone_x + (speed * delta_x)))
    drone_y = min(MAX_VAL, max(0, drone_y + (speed * delta_y)))
