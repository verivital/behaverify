import sys
import random
from obstacle_file import OBSTACLES, OBSTACLE_SIZES, OBSTACLE_QUERY

from collision_monitor import transition as collision_transition, reset as collision_reset
from loop_monitor import transition as loop_transition, reset as loop_reset
COLLISION_MONITOR = collision_reset()
LOOP_MONITOR = loop_reset()

MAX_VAL = int(sys.argv[2])
drone_x = 0
drone_y = 0
delta_x = 0
delta_y = 0
def delta_x_func():
    return delta_x
def delta_y_func():
    return delta_y
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
    (_, monitor_var) = collision_transition(
        COLLISION_MONITOR,
        {
            'drone_x' : drone_x,
            'drone_y' : drone_y,
            'delta_x' : delta_x_func,
            'delta_y' : delta_y_func,
            'obstacles' : OBSTACLES,
            'obstacle_sizes' : OBSTACLE_SIZES
        }
    )
    if monitor_var == 'unsafe':
        speed = 1
    (LOOP_MONITOR, monitor_var) = loop_transition(
        LOOP_MONITOR,
        {
            'current_action' : action
        }
    )
    if monitor_var == 'unsafe':
        speed = 1
        LOOP_MONITOR = loop_reset()
    drone_x = min(MAX_VAL, max(0, drone_x + (speed * delta_x)))
    drone_y = min(MAX_VAL, max(0, drone_y + (speed * delta_y)))
