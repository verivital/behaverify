# networks/

ONNX neural network models for the 7×7 grid world NSBT verification experiments.

## Naming Convention

```
{accuracy}__{max_val}_{obstacles}_{obs_size}__{episodes}_{seed}.onnx
```

| Field        | Meaning                                                      |
|--------------|--------------------------------------------------------------|
| `accuracy`   | Test accuracy out of 1000 (e.g. `1000` = 100%, `0995` = 99.5%) |
| `max_val`    | Grid upper bound — grid runs from 0 to max_val inclusive (6 → 7×7) |
| `obstacles`  | Number of static obstacles on the map (18)                   |
| `obs_size`   | Obstacle size parameter (0 = unit cells)                     |
| `episodes`   | Training episode count at which this checkpoint was saved    |
| `seed`       | Training seed / run variant (1)                              |

## Networks in this folder

| File                          | Accuracy | Episodes |
|-------------------------------|----------|----------|
| `1000__6_18_0__0100_1.onnx`   | 100%     | 100      |
| `1000__6_18_0__0150_1.onnx`   | 100%     | 150      |
| `1000__6_18_0__0200_1.onnx`   | 100%     | 200      |
| `1000__6_18_0__0250_1.onnx`   | 100%     | 250      |
| `1000__6_18_0__0300_1.onnx`   | 100%     | 300      |
| `0996__6_18_0__200_1.onnx`    | 99.6%    | 200      |
| `0995__6_18_0__200_1.onnx`    | 99.5%    | 200      |

These 7 networks are the subset used in the 2026_TBA experiments. The full set of
trained checkpoints (episodes 100–5000) and their raw PyTorch `.pth` weights live in
`REPRODUCIBILITY/2025_NEUS/examples/grid_world/networks_all/` and `networks_pth/`.

## Network Architecture

- **Input:** `(drone_x, drone_y, goal_x, goal_y)` — all in `[0, 6]`
- **Output:** one of `{left, right, up, down, no_action}`
- Trained via reinforcement learning on the 7×7 grid world navigation task.
