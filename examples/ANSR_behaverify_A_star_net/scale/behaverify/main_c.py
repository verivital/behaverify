import sys
import random
from obstacle_file import OBSTACLES, OBSTACLE_SIZES, OBSTACLE_QUERY
import ctypes
import os
THIS_LOCATION = os.path.dirname(os.path.abspath(__file__))
collision_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'collision_monitor.so'))
collision_monitor_lib.collision_monitor_transition.argtypes = [ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_bool), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
collision_monitor_lib.collision_monitor_transition.restype = ctypes.c_int
loop_monitor_lib = ctypes.CDLL(os.path.join(THIS_LOCATION, 'loop_monitor.so'))
loop_monitor_lib.loop_monitor_transition.argtypes = [ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_bool), ctypes.c_char_p]
loop_monitor_lib.loop_monitor_transition.restype = ctypes.c_int

COLLISION_MONITOR = (ctypes.c_bool * 1)(True)
LOOP_MONITOR = (ctypes.c_bool * 16)(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
obs_array = (ctypes.c_int * len(OBSTACLES))(*OBSTACLES)
obs_size_array = (ctypes.c_int * len(OBSTACLE_SIZES))(*OBSTACLE_SIZES)

MAX_VAL = int(sys.argv[2])
drone_x = 0
drone_y = 0
monitor_var = None
for _ in range(int(sys.argv[1])):
    speed = 2
    action = random.choice(['left', 'right', 'up', 'down', 'no_action'])
    delta_x = (-1 if action == 'left' else (1 if action == 'right' else 0))
    delta_y = (-1 if action == 'down' else (1 if action == 'up' else 0))
    if OBSTACLE_QUERY[(min(MAX_VAL, max(0, drone_x + delta_x)), min(MAX_VAL, max(0, drone_y + delta_y)))]:
        delta_x = 0
        delta_y = 0
        action = 'no_action'
    monitor_var = collision_monitor_lib.collision_monitor_transition(
        COLLISION_MONITOR,
        (ctypes.c_bool * 1)(),
        delta_x,
        delta_y,
        drone_x,
        drone_y,
        obs_size_array,
        obs_array
    )
    if monitor_var == 2:
        speed = 1
    loop_output = (ctypes.c_bool * 16)()
    monitor_var = loop_monitor_lib.loop_monitor_transition(
        LOOP_MONITOR,
        loop_output,
        action.encode('utf-8')
    )
    if monitor_var == 2:
        speed = 1
        LOOP_MONITOR = (ctypes.c_bool * 16)(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    else:
        LOOP_MONITOR = loop_output
    drone_x = min(MAX_VAL, max(0, drone_x + (speed * delta_x)))
    drone_y = min(MAX_VAL, max(0, drone_y + (speed * delta_y)))
