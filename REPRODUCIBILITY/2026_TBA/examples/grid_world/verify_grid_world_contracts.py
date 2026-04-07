"""
verify_grid_world_contracts.py

Verifies A/G safety contracts for the grid-world NSBT using alpha-beta-CROWN.

Verification mode: SINGLE-CALL (one CROWN call per contract).
  Drone position is fixed to an EPS-ball around the integer source cell.
  Goal ranges continuously over the full grid [GRID_MIN, GRID_MAX]^2 in a
  single CROWN call — 38 calls total instead of 38 × 49 = 1,862.

  This is sound: if the property holds for all real-valued goals in [0, 6]^2,
  it certainly holds for the 49 integer goals that arise during BT execution.

Class index mapping (matches DSL declaration order):
  We=0  Ea=1  No=2  So=3  XX=4

Configuration: grid_world_config.yaml
Run from: REPRODUCIBILITY/2026_TBA/examples/grid_world/
"""

import argparse
import datetime
import functools
import json
import sys
import time
import tracemalloc
from typing import Any

import torch
import yaml
from abcrown import ABCrownSolver, ConfigBuilder, VerificationSpec, input_vars, output_vars

from generate_grid_world_contracts import generate_contracts, load_config


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
# Single-call contract verification
# ---------------------------------------------------------------------------

def verify_one_contract(
    onnx_path: str,
    cx: int,
    cy: int,
    forbidden_d: int,
    num_classes: int,
    grid_min: float,
    grid_max: float,
    eps: float,
    crown_config: Any,
) -> str:
    """
    Verify one A/G contract with a single CROWN call.

    Drone position: [cx-eps, cx+eps] x [cy-eps, cy+eps]  (≈ integer point)
    Goal position:  [grid_min, grid_max]^2                (full continuous range)

    Returns "SAT", "UNSAT", or "TIMEOUT".
    """
    x = input_vars((4,))
    lower = torch.tensor([cx - eps, cy - eps, grid_min, grid_min], dtype=torch.float32)
    upper = torch.tensor([cx + eps, cy + eps, grid_max, grid_max], dtype=torch.float32)
    input_constraint = (x >= lower) & (x <= upper)

    y = output_vars(num_classes)
    other = [j for j in range(num_classes) if j != forbidden_d]
    output_constraint = functools.reduce(
        lambda a, b: a | b, [y[j] > y[forbidden_d] for j in other]
    )

    spec = VerificationSpec.build_spec(
        input_vars=x, output_vars=y,
        input_constraint=input_constraint, output_constraint=output_constraint,
    )
    result = ABCrownSolver(spec, onnx_path, config=crown_config).solve()
    return normalize_status(result.status)


# ---------------------------------------------------------------------------
# CROWN configuration
# ---------------------------------------------------------------------------

def build_crown_config(cfg: dict[str, Any]) -> Any:
    """Build the alpha-beta-CROWN solver configuration from the loaded YAML config."""
    pgd_order = cfg.get("pgd_order", "before")
    builder = (
        ConfigBuilder.from_defaults()
        .set(general__device="cpu")
        .set(attack__pgd_order=pgd_order)
        .set(bab__timeout=cfg["verification"]["timeout_sec"])
    )
    if pgd_order == "before":
        builder = builder.set(attack__pgd_restarts=50)
    return builder()


# ---------------------------------------------------------------------------
# Console helpers
# ---------------------------------------------------------------------------

def result_marker(status: str) -> str:
    """Return the console marker string for a contract result."""
    if status == "SAT":
        return "✓"
    if status == "UNSAT":
        return "✗  ← VIOLATION"
    return "?  ← TIMEOUT (inconclusive)"


def print_summary(records: list[dict[str, Any]]) -> None:
    """Print the final SAT / UNSAT / TIMEOUT tally."""
    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    print(f"\nSummary: {counts['SAT']} SAT, {counts['UNSAT']} UNSAT, "
          f"{counts['TIMEOUT']} TIMEOUT out of {len(records)} contracts")


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def save_report(records: list[dict[str, Any]], cfg: dict[str, Any]) -> None:
    """Write the full verification report to the JSON path set in cfg."""
    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    report = {
        "onnx_path":  cfg["onnx_path"],
        "timestamp":  datetime.datetime.now().isoformat(),
        "mode":       (f"single-call, goal=[{cfg['grid']['min']},{cfg['grid']['max']}]^2, "
                       f"drone EPS={cfg['verification']['eps']}"),
        "timeout_sec": cfg["verification"]["timeout_sec"],
        "summary":    {**counts, "total": len(records)},
        "contracts":  records,
    }
    with open(cfg["output_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Results saved to {cfg['output_path']}")


# ---------------------------------------------------------------------------
# Main verification loop
# ---------------------------------------------------------------------------

def run_verification(cfg: dict[str, Any]) -> dict[str, Any]:
    """
    Run A/G contract verification for every contract in the grid world.

    Returns a metrics dict with SAT/UNSAT/TIMEOUT counts and wall time,
    in addition to writing the full report JSON to cfg['output_path'].
    """
    obstacles  = [tuple(obs) for obs in cfg["obstacles"]]
    grid_min   = cfg["grid"]["min"]
    grid_max   = cfg["grid"]["max"]
    num_classes = cfg["num_classes"]
    eps        = cfg["verification"]["eps"]
    timeout    = cfg["verification"]["timeout_sec"]

    crown_config = build_crown_config(cfg)
    contracts    = generate_contracts(obstacles, grid_min, grid_max)

    print(f"Generated {len(contracts)} contracts  "
          f"(drone EPS={eps}, goal=[{grid_min},{grid_max}]^2, timeout={timeout}s)\n")
    print(f"{'#':<4} {'Description':<45} {'Status':<10} {'Marker'}")
    print("-" * 75)

    tracemalloc.start()
    rss_before = _self_rss_kb()
    t0 = time.perf_counter()

    records = []
    for i, contract in enumerate(contracts):
        cx, cy, d_idx, label, ox, oy, desc = contract
        status = verify_one_contract(
            cfg["onnx_path"], cx, cy, d_idx,
            num_classes, grid_min, grid_max, eps, crown_config,
        )
        print(f"{i+1:<4} {desc:<45} {status:<10} {result_marker(status)}")
        sys.stdout.flush()
        records.append({
            "id":               i + 1,
            "obstacle":         [ox, oy],
            "source":           [cx, cy],
            "forbidden_dir":    label,
            "forbidden_dir_idx": d_idx,
            "description":      desc,
            "status":           status,
        })

    wall_sec  = time.perf_counter() - t0
    rss_after = _self_rss_kb()
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("-" * 75)
    print_summary(records)
    save_report(records, cfg)

    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    return {
        "wall_sec":          round(wall_sec, 3),
        "peak_rss_kb":       rss_after,
        "peak_traced_bytes": peak_traced,
        "sat":               counts["SAT"],
        "unsat":             counts["UNSAT"],
        "timeout":           counts["TIMEOUT"],
        "total":             len(records),
        "skipped":           False,
    }


def _self_rss_kb() -> int:
    """Peak RSS of this process so far (KB)."""
    import resource  # noqa: PLC0415
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify grid-world A/G contracts via alpha-beta-CROWN."
    )
    parser.add_argument("--config",  default="grid_world_config.yaml",
                        help="Path to YAML config (default: grid_world_config.yaml)")
    parser.add_argument("--onnx",    required=True, help="Path to the ONNX network file")
    parser.add_argument("--output",  required=True, help="Path to write the contracts JSON")
    parser.add_argument("--no-pgd",  action="store_true",
                        help="Disable PGD attack (BaB only); sets pgd_order=skip")
    args = parser.parse_args()

    cfg = load_config(args.config)
    cfg["onnx_path"]   = args.onnx
    cfg["output_path"] = args.output
    if args.no_pgd:
        cfg["pgd_order"] = "skip"

    run_verification(cfg)
