# ACAS Xu Networks

## Files

| File | Previous advisory (`a_prev`) | `network_idx` | Legacy name |
|------|------------------------------|---------------|-------------|
| `aprev_clear.onnx`        | `clear`        | 1 | `ACASXU_run2a_1_1_batch_2000.onnx` |
| `aprev_weak_right.onnx`   | `weak_right`   | 2 | `ACASXU_run2a_2_1_batch_2000.onnx` |
| `aprev_weak_left.onnx`    | `weak_left`    | 3 | `ACASXU_run2a_3_1_batch_2000.onnx` |
| `aprev_strong_right.onnx` | `strong_right` | 4 | `ACASXU_run2a_4_1_batch_2000.onnx` |
| `aprev_strong_left.onnx`  | `strong_left`  | 5 | `ACASXU_run2a_5_1_batch_2000.onnx` |

## What each network does

The ACAS Xu closed-loop system uses **5 networks**, one per previous advisory (`a_prev`).
At each tick, the behavior tree selects which network to run based on the last-issued
advisory, then queries that network for the next advisory.

The `network_idx` (1–5) is used internally as a compact filter key in
`contract_specs_eps1e4.json` and the verification scripts. It is derived from `a_prev`
and does not appear in the filename.

## Legacy naming convention

The original filenames (`ACASXU_run2a_i_j_batch_2000.onnx`) follow the naming scheme
from the Reluplex paper (Katz et al., 2017), which trained 45 networks indexed by
previous advisory (`i` = 1–5) and speed ratio (`j` = 1–9). This directory uses only
speed ratio `j=1`. The `run2a` prefix and `batch_2000` suffix are training run
identifiers from the original researchers and carry no meaning for verification purposes.

Files in `REPRODUCIBILITY/2025_NEUS/examples/AcasXu_closed_loop/networks/` still use
the legacy names — use the table above to cross-reference.

## Architecture

- **Inputs:** 5 (normalized distance, relative angle, intersect angle, speed_own, speed_int)
- **Outputs:** 5 class scores (`clear`, `weak_left`, `weak_right`, `strong_left`, `strong_right`)
- **Hidden layers:** 6 × 50 ReLU neurons (300 total ReLU nodes)
- **Output interpretation:** argmax → selected advisory
