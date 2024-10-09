import sys
import random
from obstacle_file import OBSTACLES, OBSTACLE_SIZES, OBSTACLE_QUERY

MAX_VAL = int(sys.argv[2])
drone_x = 0
drone_y = 0
for _ in range(int(sys.argv[1])):
    speed = 1
    action = random.choice(['left', 'right', 'up', 'down', 'no_action'])
    delta_x = (-1 if action == 'left' else (1 if action == 'right' else 0))
    delta_y = (-1 if action == 'down' else (1 if action == 'up' else 0))
    if OBSTACLE_QUERY[(min(MAX_VAL, max(0, drone_x + delta_x)), min(MAX_VAL, max(0, drone_y + delta_y)))]:
        delta_x = 0
        delta_y = 0
        action = 'no_action'
    drone_x = min(MAX_VAL, max(0, drone_x + (speed * delta_x)))
    drone_y = min(MAX_VAL, max(0, drone_y + (speed * delta_y)))
