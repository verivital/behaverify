'''
Greedy rollout of the RETRAINED neural A* planner on the city tracking
mission (SIMULATION ONLY -- the verified model uses the exact symbolic table;
this network is its learned surrogate, 95.1%% training accuracy, so
conformance with the verified behavior is NOT guaranteed).

Replays the same scripted target as the verified model from the same start
as city_track_sim.tree, but the drone action comes from
argmax(onnx([x_d, y_d, tar_x, tar_y])) over [We, Ea, No, So, XX].
Moves that would enter an obstacle or leave the map are clamped to hover
(the deployed BT would equally reject unsafe primitive moves).

usage: python3 neural_rollout.py <meta.json> <model.onnx> <out.json>
'''
import json
import sys

import numpy as np
import onnxruntime

MOVES = {0: (-1, 0), 1: (1, 0), 2: (0, 1), 3: (0, -1), 4: (0, 0)}  # We, Ea, No, So, XX


def main(meta_path, onnx_path, out_path):
    meta = json.load(open(meta_path, 'r', encoding='utf-8'))
    grid = meta['grid']
    n = len(grid)
    path = [tuple(p) for p in meta['path']]
    tpw = meta['ticks_per_waypoint']
    (x, y) = meta['sim_start']
    session = onnxruntime.InferenceSession(onnx_path)

    def target_of(step):
        return path[min(len(path) - 1, step // tpw)]

    states = []
    clamped = 0
    first_found = None
    for step in range(meta['step_max'] + 1):
        (tx, ty) = target_of(step)
        found = abs(x - tx) + abs(y - ty) <= meta['sensor_range']
        states.append([x, y, step])
        if found and first_found is None:
            first_found = step
        if found:
            continue  # hover while target in sensor range (mirrors the BT FoundSeq)
        logits = session.run(None, {'input': np.array([[x, y, tx, ty]], dtype=np.float32)})[0]
        (dx, dy) = MOVES[int(np.argmax(logits[0]))]
        (nx, ny) = (x + dx, y + dy)
        if not (0 <= nx < n and 0 <= ny < n) or grid[nx][ny] == 1:
            clamped += 1  # unsafe network output: reject move, hover
        else:
            (x, y) = (nx, ny)
    result = {'states': states, 'first_found': first_found, 'unsafe_moves_clamped': clamped,
              'start': meta['sim_start'], 'onnx': onnx_path}
    json.dump(result, open(out_path, 'w', encoding='utf-8'))
    print('neural rollout: first_found tick =', first_found, '| unsafe moves clamped =', clamped)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
