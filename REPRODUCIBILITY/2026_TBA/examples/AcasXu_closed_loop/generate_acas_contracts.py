"""
generate_acas_contracts.py

Enumerate dangerous (state, advisory) pairs for the ACAS Xu closed-loop NSBT and
produce a JSON contract specification file for CROWN verification.

A contract says: "from any state in input region R, NN_k must NOT output advisory F",
where R covers all states for which applying F causes distance < 200.

Contract grouping (analogous to the grid-world approach):
  Fix  : (x_sign, y_sign, heading_own_var)  --  discrete; determines inputs 3/4/5 exactly
  Range: (x_mag, y_mag)                     --  bounding box over dangerous values

For each non-empty (heading_own_var, x_sign, y_sign, forbidden_advisory) group:
  - Compute [lower, upper] bounding box over the NN inputs of all dangerous states
  - One CROWN call per NN covers all those dangerous states at once

This yields at most 40 headings × 4 sign-quadrants × 5 advisories × 5 NNs = 4,000 contracts,
but only non-empty groups are emitted (typically a few hundred in practice).

Compare to the per-state approach: 2,830 dangerous pairs × 5 NNs = 14,150 per-point CROWN calls.

Physics model (from acas_template_360.tree / environment_update):
  - heading_own_var updated first (advisory applied)
  - position (x_mag, y_mag, x_sign, y_sign) computed using the NEW heading
  - State domain: x_mag,y_mag in [0,10], x_sign,y_sign in {-1,1}, heading_own_var in [0,39]
  - Safety invariant: distance = round(sqrt(x_mag^2 + y_mag^2)) * 100 >= 200

NN selection (from tree selector):
  a_prev = 'clear'        -> network_idx=1  (aprev_clear.onnx)
  a_prev = 'weak_right'   -> network_idx=2  (aprev_weak_right.onnx)
  a_prev = 'weak_left'    -> network_idx=3  (aprev_weak_left.onnx)
  a_prev = 'strong_right' -> network_idx=4  (aprev_strong_right.onnx)
  a_prev = 'strong_left'  -> network_idx=5  (aprev_strong_left.onnx)

NN inputs (normalized, from template):
  1. (distance - 19791.091) / 60261
  2. relative_angle_adjusted / 360   [degrees -> normalized]
  3. intersect_angle_adjusted / 360  [degrees -> normalized; CONSTANT for fixed heading]
  4. (speed_own - 650) / 1100        [constant: (20-650)/1100]
  5. (speed_int - 600) / 1200        [constant: (30-600)/1200]

Output: JSON file with range-based contract specs.
"""

import math
import json
import itertools
import argparse
from collections import defaultdict
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Model parameters (single source of truth: acas_model_params.yaml)
# ---------------------------------------------------------------------------

def _load_params() -> dict:
    path = Path(__file__).parent / "acas_model_params.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

_P = _load_params()

DISTANCE_MODIFIER  = _P["physics"]["distance_modifier"]
MAX_DIST           = _P["physics"]["max_dist"]
MAX_DIST_VAR       = MAX_DIST // DISTANCE_MODIFIER
SPEED_OWN          = _P["physics"]["speed_own"]
SPEED_INT          = _P["physics"]["speed_int"]
SECONDS_PER_UPDATE = _P["physics"]["seconds_per_update"]
DEGREE_MULTIPLIER  = _P["physics"]["degree_multiplier"]
MAX_HEADING_VAR    = 360 // DEGREE_MULTIPLIER
HEADING_INT        = _P["physics"]["heading_int_degrees"]
HEADING_INT_VAR    = HEADING_INT // DEGREE_MULTIPLIER
SAFETY_THRESHOLD   = _P["physics"]["safety_threshold"]

DISTANCE_MEAN      = _P["nn_normalization"]["distance_mean"]
DISTANCE_RANGE     = _P["nn_normalization"]["distance_range"]
SPEED_OWN_MEAN     = _P["nn_normalization"]["speed_own_mean"]
SPEED_OWN_RANGE    = _P["nn_normalization"]["speed_own_range"]
SPEED_INT_MEAN     = _P["nn_normalization"]["speed_int_mean"]
SPEED_INT_RANGE    = _P["nn_normalization"]["speed_int_range"]

ADVISORIES   = _P["advisories"]
ADV_IDX      = {a: i for i, a in enumerate(ADVISORIES)}
A_PREV_TO_NN = {name: (net["idx"], net["onnx"]) for name, net in _P["networks"].items()}

# Fixed speed inputs (constant across all states)
_NN_INPUT_SPEED_OWN = (SPEED_OWN - SPEED_OWN_MEAN) / SPEED_OWN_RANGE  # -0.5727...
_NN_INPUT_SPEED_INT = (SPEED_INT - SPEED_INT_MEAN) / SPEED_INT_RANGE   # -0.4750

# ---------------------------------------------------------------------------
# Physics functions
# ---------------------------------------------------------------------------

def _vel_x(heading_degrees: int, speed: int) -> int:
    return round(math.cos(math.radians(heading_degrees)) * speed)

def _vel_y(heading_degrees: int, speed: int) -> int:
    return round(math.sin(math.radians(heading_degrees)) * speed)

# Precompute fixed intruder velocities (heading_int = 225 degrees, speed_int = 30)
_VEL_X_INT = _vel_x(HEADING_INT, SPEED_INT)
_VEL_Y_INT = _vel_y(HEADING_INT, SPEED_INT)


def apply_advisory(heading_own_var: int, advisory: str) -> int:
    """Return new heading_own_var after applying advisory."""
    n = MAX_HEADING_VAR
    if advisory == 'strong_left':
        return (heading_own_var + 2) % n
    if advisory == 'weak_left':
        return (heading_own_var + 1) % n
    if advisory == 'weak_right':
        return (n + heading_own_var - 1) % n
    if advisory == 'strong_right':
        return (n + heading_own_var - 2) % n
    return heading_own_var  # clear


def compute_distance(x_mag: int, y_mag: int) -> int:
    """distance = round(sqrt(x_mag^2 + y_mag^2)) * DISTANCE_MODIFIER."""
    return round(math.sqrt(x_mag * x_mag + y_mag * y_mag)) * DISTANCE_MODIFIER


def simulate_step(
    x_mag: int, y_mag: int, x_sign: int, y_sign: int, heading_own_var: int,
    advisory: str,
) -> tuple[int, int, int, int, int]:
    """
    Simulate one environment_update tick.

    Heading is updated first (per the sequential order in environment_update),
    then position is computed using the new heading via velocity_x_own / velocity_y_own
    (DEFINE variables that read heading_own_var after it is updated).

    Returns (next_x_var, next_y_var, next_x_sign, next_y_sign, next_heading_own_var).
    """
    new_heading_var = apply_advisory(heading_own_var, advisory)
    new_heading     = new_heading_var * DEGREE_MULTIPLIER

    vel_x_own = _vel_x(new_heading, SPEED_OWN)
    vel_y_own = _vel_y(new_heading, SPEED_OWN)

    x = x_mag * DISTANCE_MODIFIER
    y = y_mag * DISTANCE_MODIFIER

    next_x = x * x_sign + SECONDS_PER_UPDATE * (_VEL_X_INT - vel_x_own)
    next_y = y * y_sign + SECONDS_PER_UPDATE * (_VEL_Y_INT - vel_y_own)

    next_x_sign = -1 if next_x < 0 else 1
    next_y_sign = -1 if next_y < 0 else 1
    next_x_var  = int(min(MAX_DIST, abs(next_x)) // DISTANCE_MODIFIER)
    next_y_var  = int(min(MAX_DIST, abs(next_y)) // DISTANCE_MODIFIER)

    return next_x_var, next_y_var, next_x_sign, next_y_sign, new_heading_var


# ---------------------------------------------------------------------------
# Angle computations (matching DSL DEFINE logic)
# ---------------------------------------------------------------------------

def _arctan_xy(x_mag: int, y_mag: int) -> int:
    """round(degrees(atan(x_mag / y_mag))); 0 when y_mag == 0."""
    return 0 if y_mag == 0 else round(math.degrees(math.atan(x_mag / y_mag)))


def _arctan_yx(x_mag: int, y_mag: int) -> int:
    """round(degrees(atan(y_mag / x_mag))); 0 when x_mag == 0."""
    return 0 if x_mag == 0 else round(math.degrees(math.atan(y_mag / x_mag)))


def _arctan_val(x_mag: int, y_mag: int, x_sign: int, y_sign: int) -> int:
    """
    Matches arctan_val DEFINE in template:
      (x_sign=1,  y_sign=1)  -> arctan_yx
      (x_sign=1,  y_sign=-1) -> arctan_xy
      (x_sign=-1, y_sign=1)  -> arctan_yx
      (x_sign=-1, y_sign=-1) -> arctan_xy  [default/last case]
    """
    if y_sign == 1:
        return _arctan_yx(x_mag, y_mag)
    return _arctan_xy(x_mag, y_mag)


def _normalize_angle(angle_degrees: int) -> int:
    """
    Apply mod/pos/adjusted normalization from the DSL:
      mod = angle % 360
      pos = mod if mod >= 0 else mod + 360
      adjusted = pos - 360 if pos > 180 else pos
    Returns adjusted angle in [-180, 180].
    """
    mod = angle_degrees % 360
    pos = mod if mod >= 0 else mod + 360
    return pos - 360 if pos > 180 else pos


def compute_relative_angle_adjusted(
    x_mag: int, y_mag: int, x_sign: int, y_sign: int, heading_own_var: int
) -> int:
    """
    Matches relative_angle DEFINE + normalization chain in the template.
    Case priority follows DSL sequential case order (first match wins).
    """
    heading_own = heading_own_var * DEGREE_MULTIPLIER
    x = x_mag * DISTANCE_MODIFIER  # only used for == 0 checks
    y = y_mag * DISTANCE_MODIFIER

    av = _arctan_val(x_mag, y_mag, x_sign, y_sign)

    if x_sign == 1 and y == 0:
        rel = 270 - heading_own
    elif x_sign == -1 and y == 0:
        rel = 90 - heading_own
    elif x == 0 and y_sign == 1:
        rel = 360 - heading_own
    elif x == 0 and y_sign == -1:
        rel = 180 - heading_own
    elif x_sign == 1 and y_sign == 1:
        rel = (270 - heading_own) + av
    elif x_sign == 1 and y_sign == -1:
        rel = (180 - heading_own) + av
    elif x_sign == -1 and y_sign == 1:
        rel = (90 - heading_own) - av
    else:  # x_sign == -1 and y_sign == -1
        rel = (180 - heading_own) - av

    return _normalize_angle(rel)


def compute_intersect_angle_adjusted(heading_own_var: int) -> int:
    """intersect_angle = heading_own - heading_int, then normalized."""
    heading_own = heading_own_var * DEGREE_MULTIPLIER
    return _normalize_angle(heading_own - HEADING_INT)


def compute_nn_inputs(
    x_mag: int, y_mag: int, x_sign: int, y_sign: int, heading_own_var: int
) -> list[float]:
    """
    Compute the 5 normalized NN input values for a given state.
    Matches the DSL rdiv expressions for network_k_1 variables.
    """
    dist    = compute_distance(x_mag, y_mag)
    rel_adj = compute_relative_angle_adjusted(x_mag, y_mag, x_sign, y_sign, heading_own_var)
    int_adj = compute_intersect_angle_adjusted(heading_own_var)

    return [
        (dist    - DISTANCE_MEAN)    / DISTANCE_RANGE,   # input 1: distance
        rel_adj  / 360.0,                                  # input 2: relative angle
        int_adj  / 360.0,                                  # input 3: intersect angle (CONSTANT for fixed heading)
        _NN_INPUT_SPEED_OWN,                               # input 4: speed_own (constant)
        _NN_INPUT_SPEED_INT,                               # input 5: speed_int (constant)
    ]


# ---------------------------------------------------------------------------
# Dangerous-pair enumeration
# ---------------------------------------------------------------------------

def enumerate_dangerous_pairs() -> list[dict]:
    """
    Return list of (state, forbidden_advisory) dicts for states where
    current distance >= SAFETY_THRESHOLD and some advisory causes
    next distance < SAFETY_THRESHOLD.
    """
    pairs = []
    for x_mag, y_mag, x_sign, y_sign, h in itertools.product(
        range(MAX_DIST_VAR + 1),  # x_mag: 0..10
        range(MAX_DIST_VAR + 1),  # y_mag: 0..10
        (-1, 1),                  # x_sign
        (-1, 1),                  # y_sign
        range(MAX_HEADING_VAR),   # heading_own_var: 0..39
    ):
        if compute_distance(x_mag, y_mag) < SAFETY_THRESHOLD:
            continue  # already unsafe; invariant already violated

        for advisory in ADVISORIES:
            nx, ny, _, _, _ = simulate_step(x_mag, y_mag, x_sign, y_sign, h, advisory)
            if compute_distance(nx, ny) < SAFETY_THRESHOLD:
                pairs.append({
                    'state': {
                        'x_mag': x_mag, 'y_mag': y_mag,
                        'x_sign': x_sign, 'y_sign': y_sign,
                        'heading_own_var': h,
                    },
                    'forbidden_advisory':     advisory,
                    'forbidden_advisory_idx': ADV_IDX[advisory],
                    'nn_inputs': compute_nn_inputs(x_mag, y_mag, x_sign, y_sign, h),
                })
    return pairs


# ---------------------------------------------------------------------------
# Range-based contract grouping
# ---------------------------------------------------------------------------

def group_range_contracts(pairs: list[dict], eps: float = 1e-4) -> list[dict]:
    """
    Group dangerous pairs by (heading_own_var, x_sign, y_sign, forbidden_advisory).

    For each non-empty group, compute a bounding box over the NN inputs of all
    dangerous states in the group, then emit one contract per NN (a_prev value).

    This is the range-based analog of the grid-world contracts:
      - Fixed: heading + sign quadrant  (determines inputs 3/4/5 exactly)
      - Ranged: (x_mag, y_mag)          (gives bounding box on inputs 1/2)

    Args:
        pairs: output of enumerate_dangerous_pairs()
        eps:   small margin added to each side of the bounding box

    Returns:
        List of range-based contract dicts, one per (group, NN).
    """
    # Accumulate inputs and state lists per group
    groups: dict[tuple, dict] = {}
    for pair in pairs:
        s   = pair['state']
        key = (s['heading_own_var'], s['x_sign'], s['y_sign'], pair['forbidden_advisory'])
        if key not in groups:
            groups[key] = {'inputs': [], 'states': []}
        groups[key]['inputs'].append(pair['nn_inputs'])
        groups[key]['states'].append([s['x_mag'], s['y_mag']])

    contracts = []
    contract_id = 1

    for key in sorted(groups):
        h, xm, ym, adv = key
        inp_list = groups[key]['inputs']
        states   = groups[key]['states']
        n        = len(inp_list[0])  # = 5

        lower = [min(inp[i] for inp in inp_list) - eps for i in range(n)]
        upper = [max(inp[i] for inp in inp_list) + eps for i in range(n)]

        # Inputs 3/4/5 are constants for fixed heading; verify the box is tight there
        # (both bounds should be equal up to 2*eps — just a sanity note, not enforced here)

        sign = lambda v: '+' if v == 1 else '-'

        for a_prev, (nn_idx, onnx) in A_PREV_TO_NN.items():
            contracts.append({
                'id':               contract_id,
                'type':             'range',
                'heading_own_var':  h,
                'x_sign':           xm,
                'y_sign':           ym,
                'a_prev':           a_prev,
                'network_idx':      nn_idx,
                'onnx':             onnx,
                'nn_input_lower':   lower,
                'nn_input_upper':   upper,
                'n_states_covered': len(states),
                'dangerous_xy':     states,
                'forbidden_advisory':     adv,
                'forbidden_advisory_idx': ADV_IDX[adv],
                'description': (
                    f"NN_{nn_idx} (a_prev={a_prev}) "
                    f"h={h} ({sign(xm)},{sign(ym)}) "
                    f"covers {len(states)} state(s), "
                    f"must not choose {adv}"
                ),
            })
            contract_id += 1

    return contracts


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate ACAS Xu A/G contract specs (range-based) for CROWN."
    )
    parser.add_argument(
        '--output', default='contracts/continuous_goals/contract_specs_eps1e4.json',
        help='Output JSON path (default: contracts/continuous_goals/contract_specs_eps1e4.json)',
    )
    parser.add_argument(
        '--eps', type=float, default=1e-4,
        help='Bounding-box margin added to each input dimension (default: 1e-4)',
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Print counts only; do not write output file',
    )
    args = parser.parse_args()

    print("Enumerating dangerous (state, advisory) pairs...")
    pairs = enumerate_dangerous_pairs()
    print(f"  {len(pairs)} dangerous pairs across "
          f"{len({(p['state']['heading_own_var'], p['state']['x_sign'], p['state']['y_sign'], p['forbidden_advisory']) for p in pairs})} "
          f"(heading, sign, advisory) groups")

    contracts = group_range_contracts(pairs, eps=args.eps)
    n_groups  = len(contracts) // len(A_PREV_TO_NN)
    print(f"  {n_groups} non-empty groups x {len(A_PREV_TO_NN)} NNs = {len(contracts)} range contracts")
    print(f"  (vs {len(pairs) * len(A_PREV_TO_NN)} per-state contracts)")

    if args.dry_run:
        print("Dry run -- no file written.")
        return

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        'description': 'ACAS Xu closed-loop A/G contract specs (range-based)',
        'physics': {
            'degree_multiplier':    DEGREE_MULTIPLIER,
            'seconds_per_update':   SECONDS_PER_UPDATE,
            'speed_own':            SPEED_OWN,
            'speed_int':            SPEED_INT,
            'heading_int_degrees':  HEADING_INT,
            'safety_threshold':     SAFETY_THRESHOLD,
            'heading_update_order': (
                'heading updated first (sequential env_update), '
                'then position computed with new heading'
            ),
        },
        'contract_type': 'range-based: bounding box over (x_mag,y_mag) for fixed (heading,sign,advisory)',
        'nn_mapping': {
            a_prev: {'network_idx': nn_idx, 'onnx': onnx}
            for a_prev, (nn_idx, onnx) in A_PREV_TO_NN.items()
        },
        'total_dangerous_pairs': len(pairs),
        'total_groups': n_groups,
        'total_contracts': len(contracts),
        'contracts': contracts,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"Saved to {output_path}")


if __name__ == '__main__':
    main()
