'''
Overnight fixes (2026-07-02): sanity-checker for an exported A*-net ONNX model.

Rolls the network out greedily on the obstacle grid (input [x_d, y_d, x_g, y_g]
-> argmax over [We, Ea, No, So, XX] = [x-1, x+1, y+1, y-1, stop]) and compares
the resulting path against the symbolic planner (mass_basic_a_star_2.mass_a_star,
the same planner that generated the training labels).

usage:
    python3 eval_onnx_path.py <obstacles.txt> <model.onnx> [num_trials=200] [seed=0]

Prints per-trial success + path-length vs optimal-cost statistics and renders
one example rollout as ASCII.
'''
import random
import sys

import numpy as np
import onnxruntime

from create_grid import create_grid
from mass_basic_a_star_2 import mass_a_star
from misc_util import extract_info

MOVES = {0: (-1, 0), 1: (1, 0), 2: (0, 1), 3: (0, -1)}  # We, Ea, No, So
MOVE_NAMES = ['We', 'Ea', 'No', 'So', 'XX']


def rollout(session, grid, min_val, max_val, start, goal, max_steps):
    path = [start]
    (x, y) = start
    for _ in range(max_steps):
        if (x, y) == goal:
            return (True, path)
        logits = session.run(
            None,
            {'input': np.array([[float(x), float(y), float(goal[0]), float(goal[1])]], dtype=np.float32)}
        )[0]
        move = int(np.argmax(logits[0]))
        if move == 4:  # XX before reaching the goal: net says "stop"
            return (False, path)
        (dx, dy) = MOVES[move]
        (x, y) = (x + dx, y + dy)
        if not (min_val <= x <= max_val and min_val <= y <= max_val) or grid[x][y] == 1:
            return (False, path + [(x, y)])  # walked off the map / into an obstacle
        path.append((x, y))
    return ((x, y) == goal, path)


def draw_ascii(grid, min_val, max_val, path, start, goal):
    cells = {(x, y): '#' if grid[x][y] == 1 else '.' for x in range(min_val, max_val + 1) for y in range(min_val, max_val + 1)}
    for point in path:
        if point in cells and cells[point] == '.':
            cells[point] = '*'
    cells[start] = 'S'
    cells[goal] = 'G'
    lines = []
    for y in range(max_val, min_val - 1, -1):  # y up = North
        lines.append(''.join(cells[(x, y)] for x in range(min_val, max_val + 1)))
    return '\n'.join(lines)


def main():
    obstacles_path = sys.argv[1]
    onnx_path = sys.argv[2]
    num_trials = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    (min_val, max_val, _, _, _) = extract_info(obstacles_path)
    grid = create_grid(obstacles_path, min_val, max_val)
    free_cells = [(x, y) for x in range(min_val, max_val + 1) for y in range(min_val, max_val + 1) if grid[x][y] == 0]
    session = onnxruntime.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
    rng = random.Random(seed)
    cost_cache = {}
    successes = 0
    optimal_count = 0
    length_ratios = []
    reachable_trials = 0
    example = None
    for _ in range(num_trials):
        start = rng.choice(free_cells)
        goal = rng.choice(free_cells)
        if start not in cost_cache:
            cost_cache[start] = mass_a_star(grid, min_val, max_val, start)
        optimal = cost_cache[start][goal[0]][goal[1]]['cost']
        if optimal <= 0:  # unreachable goal or start == goal; skip
            continue
        reachable_trials += 1
        (success, path) = rollout(session, grid, min_val, max_val, start, goal,
                                  max_steps=4 * (max_val - min_val + 1) ** 2)
        if success:
            successes += 1
            steps = len(path) - 1
            length_ratios.append(steps / optimal)
            if steps == optimal:
                optimal_count += 1
            if example is None or len(path) > len(example[0]):
                example = (path, start, goal, optimal)
    print('obstacles: ' + obstacles_path)
    print('onnx     : ' + onnx_path)
    print('grid     : ' + str(max_val - min_val + 1) + 'x' + str(max_val - min_val + 1)
          + ' (' + str(len(free_cells)) + ' free cells)')
    print('trials   : ' + str(reachable_trials) + ' (reachable start/goal pairs, seed ' + str(seed) + ')')
    if reachable_trials == 0:
        print('no reachable pairs -- degenerate map?')
        return
    print('reached goal      : ' + str(successes) + '/' + str(reachable_trials)
          + ' (' + format(100.0 * successes / reachable_trials, '.1f') + '%)')
    if successes > 0:
        print('exactly optimal   : ' + str(optimal_count) + '/' + str(successes)
              + ' of successful paths')
        print('mean length/opt   : ' + format(sum(length_ratios) / len(length_ratios), '.4f'))
        print('worst length/opt  : ' + format(max(length_ratios), '.4f'))
    if example is not None:
        (path, start, goal, optimal) = example
        print('\nexample rollout: start=' + str(start) + ' goal=' + str(goal)
              + ' net_steps=' + str(len(path) - 1) + ' optimal=' + str(optimal))
        print(draw_ascii(grid, min_val, max_val, path, start, goal))


if __name__ == '__main__':
    main()
