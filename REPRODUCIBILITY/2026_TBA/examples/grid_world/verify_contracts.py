"""
Verify A/G safety contracts for the grid-world NSBT using alpha-beta-CROWN.

Contract schema (per obstacle o=(ox,oy), per entry direction d):
  Assume : drone at adjacent cell (cx,cy) ± EPS  (tiny neighborhood of the integer)
  Guarantee: NN output != direction d  (d would move drone into obstacle)
             for ALL goal positions (x_g, y_g) in [GRID_MIN, GRID_MAX]^2

Verification mode: SINGLE-CALL (one CROWN call per contract)
  The drone position is fixed to an EPS-ball around the integer source cell.
  The goal ranges continuously over the full grid [GRID_MIN, GRID_MAX]^2 in a
  single CROWN call — 38 calls total instead of 38 × 49 = 1,862.

  This is sound: if the property holds for all real-valued goals in [0, 6]^2,
  it certainly holds for the 49 integer goals that arise during BT execution.

  Note on EPS: CROWN requires a proper interval (no point queries). EPS=0.001
  is a tiny neighborhood around the integer source cell; the NN's large logit
  margins at training points mean no decision boundary is crossed within it.

Class index mapping (from draw_network.py CODES, matches DSL declaration order):
  We=0  Ea=1  No=2  So=3  XX=4

Configuration: verify_contracts.yaml
Output: JSON file (path set in YAML)
"""

import sys
import json
import functools
import datetime
from typing import Any
import yaml
import torch
from abcrown import ABCrownSolver, VerificationSpec, ConfigBuilder, input_vars, output_vars

# ---------------------------------------------------------------------------
# Configuration loading
# ---------------------------------------------------------------------------

def load_config(path: str = "verify_contracts.yaml") -> dict[str, Any]:
    """Load verification parameters from a YAML file."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

_cfg        = load_config()
GRID_MIN    = _cfg["grid"]["min"]
GRID_MAX    = _cfg["grid"]["max"]
NUM_CLASSES = _cfg["num_classes"]
EPS         = _cfg["verification"]["eps"]
TIMEOUT_SEC = _cfg["verification"]["timeout_sec"]
OBSTACLES   = [tuple(obs) for obs in _cfg["obstacles"]]
OBSTACLE_SET = set(OBSTACLES)

# Direction index → (label, dx, dy). Not externalized: fixed cardinal directions.
#   dx/dy is the movement applied when this direction is chosen.
DIRECTIONS = {
    0: ("We", -1,  0),   # West:  x decreases
    1: ("Ea", +1,  0),   # East:  x increases
    2: ("No",  0, +1),   # North: y increases
    3: ("So",  0, -1),   # South: y decreases
}

# ---------------------------------------------------------------------------
# Status normalization
# ---------------------------------------------------------------------------

def normalize_status(raw: str) -> str:
    """Map CROWN result.status to SAT / UNSAT / TIMEOUT."""
    if raw in ("safe", "verified", "safe-incomplete"):
        return "SAT"
    if raw.startswith("unsafe"):
        return "UNSAT"
    return "TIMEOUT"

# ---------------------------------------------------------------------------
# Contract generation
# ---------------------------------------------------------------------------

def generate_contracts() -> list[tuple[int, int, int, str, int, int, str]]:
    """
    For each obstacle and each cardinal direction, produce one contract:
      (cx, cy, forbidden_dir_idx, dir_label, ox, oy, description_string)

    cx, cy  = source cell the drone is standing on
    forbidden_dir_idx = direction index the NN must NOT output
    """
    contracts = []
    for (ox, oy) in OBSTACLES:
        for d_idx, (label, dx, dy) in DIRECTIONS.items():
            cx, cy = ox - dx, oy - dy          # source = one step opposite to d
            if not (GRID_MIN <= cx <= GRID_MAX and GRID_MIN <= cy <= GRID_MAX):
                continue
            if (cx, cy) in OBSTACLE_SET:
                continue
            desc = f"obstacle ({ox},{oy})  source ({cx},{cy})  forbid {label}"
            contracts.append((cx, cy, d_idx, label, ox, oy, desc))
    return contracts

# ---------------------------------------------------------------------------
# Single-call contract verification
# ---------------------------------------------------------------------------

def verify_contract(onnx_path: str, cx: int, cy: int, forbidden_d: int, config: Any) -> str:
    """
    Verify one contract with a single CROWN call.

    Drone position: [cx-EPS, cx+EPS] x [cy-EPS, cy+EPS]  (≈ integer point)
    Goal position:  [GRID_MIN, GRID_MAX]^2                 (full continuous range)

    Returns "SAT", "UNSAT", or "TIMEOUT".
    """
    x = input_vars((4,))
    lower = torch.tensor([cx - EPS, cy - EPS, GRID_MIN, GRID_MIN], dtype=torch.float32)
    upper = torch.tensor([cx + EPS, cy + EPS, GRID_MAX, GRID_MAX], dtype=torch.float32)
    input_constraint = (x >= lower) & (x <= upper)
    y = output_vars(NUM_CLASSES)
    other = [j for j in range(NUM_CLASSES) if j != forbidden_d]
    output_constraint = functools.reduce(
        lambda a, b: a | b, [y[j] > y[forbidden_d] for j in other]
    )
    spec = VerificationSpec.build_spec(
        input_vars=x, output_vars=y,
        input_constraint=input_constraint, output_constraint=output_constraint,
    )
    result = ABCrownSolver(spec, onnx_path, config=config).solve()
    return normalize_status(result.status)

# ---------------------------------------------------------------------------
# Helpers for run_verification
# ---------------------------------------------------------------------------

def build_crown_config(cfg: dict[str, Any]) -> Any:
    """Build the alpha-beta-CROWN solver configuration from loaded YAML config."""
    return (
        ConfigBuilder.from_defaults()
        .set(general__device="cpu")
        .set(attack__pgd_order="skip")   # skip PGD, go straight to BaB
        .set(bab__timeout=cfg["verification"]["timeout_sec"])
        ()
    )

def result_marker(overall: str) -> str:
    """Return the console marker string for a contract result."""
    if overall == "SAT":
        return "✓"
    if overall == "UNSAT":
        return "✗  ← VIOLATION"
    return "?  ← TIMEOUT (inconclusive)"

def contract_record(i: int, contract: tuple[int, int, int, str, int, int, str], overall: str) -> dict[str, Any]:
    """Build the JSON record for one contract."""
    cx, cy, d_idx, label, ox, oy, desc = contract
    return {
        "id": i,
        "obstacle": [ox, oy],
        "source": [cx, cy],
        "forbidden_dir": label,
        "forbidden_dir_idx": d_idx,
        "description": desc,
        "status": overall,
    }

def print_summary(records: list[dict[str, Any]]) -> None:
    """Print the final SAT / UNSAT / TIMEOUT tally."""
    counts = {s: sum(1 for r in records if r["status"] == s) for s in ("SAT", "UNSAT", "TIMEOUT")}
    print(f"\nSummary: {counts['SAT']} SAT, {counts['UNSAT']} UNSAT, "
          f"{counts['TIMEOUT']} TIMEOUT out of {len(records)} contracts")

def save_report(records: list[dict[str, Any]], cfg: dict[str, Any]) -> None:
    """Write the full verification report to the JSON path set in cfg."""
    counts = {s: sum(1 for r in records if r["status"] == s) for s in ("SAT", "UNSAT", "TIMEOUT")}
    report = {
        "onnx_path": cfg["onnx_path"],
        "timestamp": datetime.datetime.now().isoformat(),
        "mode": f"single-call, goal=[{GRID_MIN},{GRID_MAX}]^2, drone EPS={cfg['verification']['eps']}",
        "timeout_sec": cfg["verification"]["timeout_sec"],
        "summary": {**counts, "total": len(records)},
        "contracts": records,
    }
    with open(cfg["output_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Results saved to {cfg['output_path']}")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_verification(cfg: dict[str, Any]) -> None:
    """Run A/G contract verification for every contract in the grid world."""
    eps, timeout = cfg["verification"]["eps"], cfg["verification"]["timeout_sec"]
    crown_config = build_crown_config(cfg)
    contracts = generate_contracts()
    print(f"Generated {len(contracts)} contracts  "
          f"(drone EPS={eps}, goal=[{GRID_MIN},{GRID_MAX}]^2, timeout={timeout}s)\n")
    print(f"{'#':<4} {'Description':<45} {'Status':<10} {'Marker'}")
    print("-" * 75)
    records = []
    for i, contract in enumerate(contracts):
        cx, cy, d_idx, *_ = contract
        overall = verify_contract(cfg["onnx_path"], cx, cy, d_idx, crown_config)
        print(f"{i+1:<4} {contract[-1]:<45} {overall:<10} {result_marker(overall)}")
        sys.stdout.flush()
        records.append(contract_record(i + 1, contract, overall))
    print("-" * 75)
    print_summary(records)
    save_report(records, cfg)


if __name__ == "__main__":
    run_verification(load_config())
