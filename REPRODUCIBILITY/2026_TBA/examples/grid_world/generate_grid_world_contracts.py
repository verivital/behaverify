"""
generate_grid_world_contracts.py

Generates A/G safety contracts for the grid-world NSBT from obstacle positions
and grid bounds. No neural network or CROWN dependency — pure Python logic.

Contract schema (per obstacle o=(ox,oy), per entry direction d):
  Assume : drone at adjacent cell (cx,cy)
  Guarantee: NN output != direction d
             (d would move the drone into the obstacle)

Run standalone to preview contracts without verifying them:
    python generate_grid_world_contracts.py
    python generate_grid_world_contracts.py --config grid_world_domain_config.yaml
"""

import argparse
from typing import Any

import yaml

# Direction index → (label, dx, dy).
# dx/dy is the movement applied when this direction is chosen.
# Not configurable: these are the fixed cardinal directions of the grid world.
DIRECTIONS = {
    0: ("We", -1,  0),   # West:  x decreases
    1: ("Ea", +1,  0),   # East:  x increases
    2: ("No",  0, +1),   # North: y increases
    3: ("So",  0, -1),   # South: y decreases
}


def generate_contracts(
    obstacles: list[tuple[int, int]],
    grid_min: int,
    grid_max: int,
) -> list[tuple[int, int, int, str, int, int, str]]:
    """
    Generate all A/G contracts from obstacle positions and grid bounds.

    For each obstacle and each cardinal direction, produces one contract:
        (cx, cy, forbidden_dir_idx, dir_label, ox, oy, description)

    cx, cy             = source cell the drone is standing on
    forbidden_dir_idx  = direction index the NN must NOT output

    Skips source cells that are outside the grid or are themselves obstacles.
    """
    obstacle_set = {tuple(o) for o in obstacles}
    contracts = []
    for (ox, oy) in obstacles:
        for d_idx, (label, dx, dy) in DIRECTIONS.items():
            cx, cy = ox - dx, oy - dy
            if not (grid_min <= cx <= grid_max and grid_min <= cy <= grid_max):
                continue
            if (cx, cy) in obstacle_set:
                continue
            desc = f"obstacle ({ox},{oy})  source ({cx},{cy})  forbid {label}"
            contracts.append((cx, cy, d_idx, label, ox, oy, desc))
    return contracts


def load_config(path: str = "grid_world_domain_config.yaml") -> dict[str, Any]:
    """Load grid-world configuration from a YAML file."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preview A/G contracts for the grid-world NSBT without running CROWN."
    )
    parser.add_argument("--config", default="grid_world_domain_config.yaml",
                        help="Path to YAML config (default: grid_world_domain_config.yaml)")
    args = parser.parse_args()

    cfg = load_config(args.config)
    obstacles = [tuple(obs) for obs in cfg["obstacles"]]
    grid_min  = cfg["grid"]["min"]
    grid_max  = cfg["grid"]["max"]

    contracts = generate_contracts(obstacles, grid_min, grid_max)
    print(f"Generated {len(contracts)} contracts  "
          f"(grid=[{grid_min},{grid_max}]^2, {len(obstacles)} obstacles)\n")
    print(f"{'#':<4} {'Description':<50}")
    print("-" * 56)
    for i, c in enumerate(contracts):
        print(f"{i+1:<4} {c[-1]}")
