"""
verify_grid_world_contracts.py

Verifies A/G safety contracts for the grid-world NSBT using alpha-beta-CROWN.

Two verification modes are supported:

  CONTINUOUS (default): one CROWN call per contract.
    Drone position is fixed to an EPS-ball around the integer source cell.
    Goal ranges continuously over the full grid [GRID_MIN, GRID_MAX]^2 —
    38 calls total. Sound over all real-valued goals, not just integer ones.

  DISCRETE (--discrete flag): 49 CROWN calls per contract.
    For each of the 49 integer goal positions in {0,...,6}^2, the goal is
    fixed to an EPS-ball around that integer point. Short-circuits on the
    first UNSAT found. Bridges to the 2025_NEUS table approach: if all 38
    contracts are SAT in discrete mode, the NN is safe on every integer goal.

Class index mapping (matches DSL declaration order):
  We=0  Ea=1  No=2  So=3  XX=4

Configuration: grid_world_domain_config.yaml
Run from: REPRODUCIBILITY/2026_TBA/examples/grid_world/
"""

import argparse
import datetime
import json
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any

import torch
import yaml

_HERE = Path(__file__).parent.resolve()
_TBA  = (_HERE / "../../").resolve()
if str(_TBA) not in sys.path:
    sys.path.insert(0, str(_TBA))

from pipeline.neuro.crown.crown_verification import (
    build_crown_config,
    normalize_status,
    run_crown_verification,
)

from generate_grid_world_contracts import generate_contracts, load_config


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC: float = 5.0

# See note in original file: eps=0.0 is safe in practice because PGD resolves
# all contracts for 100%-accurate NNs before BaB. Use 1e-5 if inf/NaN crashes.
DISCRETE_GOAL_EPS: float = 0.0


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
) -> tuple[str, list[float] | None]:
    """
    Verify one A/G contract with a single CROWN call.

    Drone position: [cx-eps, cx+eps] x [cy-eps, cy+eps]
    Goal position:  [grid_min, grid_max]^2

    Returns (status, counterexample) where counterexample is
    [drone_x, drone_y, goal_x, goal_y] if UNSAT, else None.
    """
    lower = [cx - eps, cy - eps, grid_min, grid_min]
    upper = [cx + eps, cy + eps, grid_max, grid_max]

    status, result = run_crown_verification(
        onnx_path, lower, upper, forbidden_d, num_classes, crown_config
    )

    counterexample = None
    if status == "UNSAT":
        adv = result.stats.get("attack_examples")
        if adv is None:
            adv = result.stats.get("all_adv_candidates")
        if adv is not None:
            try:
                ce = adv.view(-1)[:4].tolist()
                counterexample = [round(v, 6) for v in ce]
            except Exception:
                pass

    return status, counterexample


# ---------------------------------------------------------------------------
# Discrete-mode contract verification
# ---------------------------------------------------------------------------

def verify_one_contract_discrete(
    onnx_path: str,
    cx: int,
    cy: int,
    forbidden_d: int,
    num_classes: int,
    grid_min: int,
    grid_max: int,
    eps: float,
    crown_config: Any,
) -> tuple[str, list[float] | None]:
    """
    Verify one A/G contract against all integer goal positions (discrete mode).

    Makes one CROWN call per integer goal in {grid_min,...,grid_max}^2,
    short-circuiting on the first UNSAT. Returns TIMEOUT only if no UNSAT was
    found but at least one call timed out.
    """
    timeout_seen = False

    for gx in range(grid_min, grid_max + 1):
        for gy in range(grid_min, grid_max + 1):
            lower = [cx - eps, cy - eps, gx - DISCRETE_GOAL_EPS, gy - DISCRETE_GOAL_EPS]
            upper = [cx + eps, cy + eps, gx + DISCRETE_GOAL_EPS, gy + DISCRETE_GOAL_EPS]

            status, result = run_crown_verification(
                onnx_path, lower, upper, forbidden_d, num_classes, crown_config
            )

            if status == "UNSAT":
                counterexample = None
                adv = result.stats.get("attack_examples")
                if adv is None:
                    adv = result.stats.get("all_adv_candidates")
                if adv is not None:
                    try:
                        ce = adv.view(-1)[:4].tolist()
                        counterexample = [round(v, 6) for v in ce]
                    except Exception:
                        pass
                return "UNSAT", counterexample

            if status == "TIMEOUT":
                timeout_seen = True

    return ("TIMEOUT" if timeout_seen else "SAT"), None


# ---------------------------------------------------------------------------
# CROWN configuration (thin wrapper over shared build_crown_config)
# ---------------------------------------------------------------------------

def _build_crown_cfg(cfg: dict[str, Any], timeout_override: float | None = None) -> Any:
    pgd_order = cfg.get("pgd_order", "before")
    timeout   = timeout_override if timeout_override is not None \
                else cfg["verification"]["timeout_sec"]
    return build_crown_config(
        timeout=timeout,
        pgd_order=pgd_order,
        device="cpu",
    )


# ---------------------------------------------------------------------------
# Console helpers
# ---------------------------------------------------------------------------

def result_marker(status: str) -> str:
    if status == "SAT":
        return "✓"
    if status == "UNSAT":
        return "✗  ← VIOLATION"
    return "?  ← TIMEOUT (inconclusive)"


def print_summary(records: list[dict[str, Any]]) -> None:
    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    print(f"\nSummary: {counts['SAT']} SAT, {counts['UNSAT']} UNSAT, "
          f"{counts['TIMEOUT']} TIMEOUT out of {len(records)} contracts")


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def save_report(records: list[dict[str, Any]], cfg: dict[str, Any], mode_str: str) -> None:
    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    report = {
        "onnx_path":   cfg["onnx_path"],
        "timestamp":   datetime.datetime.now().isoformat(),
        "mode":        mode_str,
        "timeout_sec": cfg["verification"]["timeout_sec"],
        "summary":     {**counts, "total": len(records)},
        "contracts":   records,
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

    Dispatches to continuous or discrete mode based on cfg.get("discrete", False).
    Returns a metrics dict (SAT/UNSAT/TIMEOUT counts + wall time).
    """
    obstacles   = [tuple(obs) for obs in cfg["obstacles"]]
    grid_min    = cfg["grid"]["min"]
    grid_max    = cfg["grid"]["max"]
    num_classes = cfg["num_classes"]
    eps         = cfg["verification"]["eps"]
    discrete    = cfg.get("discrete", False)
    if discrete:
        eps = 0.0

    contracts = generate_contracts(obstacles, grid_min, grid_max)

    if discrete:
        discrete_timeout = cfg.get("discrete_timeout", DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC)
        crown_config = _build_crown_cfg(cfg, timeout_override=discrete_timeout)
        mode_str = (f"discrete, {(grid_max - grid_min + 1) ** 2} integer goals, "
                    f"drone EPS={eps}, goal EPS={DISCRETE_GOAL_EPS}, "
                    f"timeout={discrete_timeout}s per goal")
        print(f"Generated {len(contracts)} contracts  "
              f"(discrete mode: {(grid_max - grid_min + 1) ** 2} integer goals, "
              f"timeout={discrete_timeout}s per goal)\n")
    else:
        timeout = cfg["verification"]["timeout_sec"]
        crown_config = _build_crown_cfg(cfg)
        mode_str = (f"single-call, goal=[{grid_min},{grid_max}]^2, "
                    f"drone EPS={eps}")
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

        if discrete:
            status, counterexample = verify_one_contract_discrete(
                cfg["onnx_path"], cx, cy, d_idx,
                num_classes, grid_min, grid_max, eps, crown_config,
            )
        else:
            status, counterexample = verify_one_contract(
                cfg["onnx_path"], cx, cy, d_idx,
                num_classes, grid_min, grid_max, eps, crown_config,
            )

        print(f"{i+1:<4} {desc:<45} {status:<10} {result_marker(status)}")
        if counterexample is not None:
            gx, gy = counterexample[2], counterexample[3]
            is_int = abs(gx - round(gx)) < 0.01 and abs(gy - round(gy)) < 0.01
            print(f"       CE: drone=({counterexample[0]:.4f},{counterexample[1]:.4f}) "
                  f"goal=({gx:.4f},{gy:.4f})  goal_is_integer={is_int}")
        sys.stdout.flush()

        record = {
            "id":                i + 1,
            "obstacle":          [ox, oy],
            "source":            [cx, cy],
            "forbidden_dir":     label,
            "forbidden_dir_idx": d_idx,
            "description":       desc,
            "status":            status,
            "counterexample":    counterexample,
        }
        records.append(record)

    wall_sec  = time.perf_counter() - t0
    rss_after = _self_rss_kb()
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("-" * 75)
    print_summary(records)
    save_report(records, cfg, mode_str)

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
    import resource  # noqa: PLC0415
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify grid-world A/G contracts via alpha-beta-CROWN."
    )
    parser.add_argument("--config",  default="grid_world_domain_config.yaml",
                        help="Path to YAML config (default: grid_world_domain_config.yaml)")
    parser.add_argument("--onnx",    required=True, help="Path to the ONNX network file")
    parser.add_argument("--output",  required=True, help="Path to write the contracts JSON")
    parser.add_argument("--no-pgd",  action="store_true",
                        help="Disable PGD attack (BaB only); sets pgd_order=skip")
    parser.add_argument("--discrete", action="store_true",
                        help=("Discrete verification mode: check each of the "
                              "(grid_max - grid_min + 1)^2 integer goal positions "
                              "individually instead of the full continuous range."))
    parser.add_argument("--discrete-timeout", type=float,
                        default=DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC,
                        help=(f"Per-goal timeout in seconds for discrete mode "
                              f"(default: {DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC}s). "
                              f"Ignored when --discrete is not set."))
    args = parser.parse_args()

    cfg = load_config(args.config)
    cfg["onnx_path"]   = args.onnx
    cfg["output_path"] = args.output
    if args.no_pgd:
        cfg["pgd_order"] = "skip"
    if args.discrete:
        cfg["discrete"]         = True
        cfg["discrete_timeout"] = args.discrete_timeout

    run_verification(cfg)
