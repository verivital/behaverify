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
# Constants
# ---------------------------------------------------------------------------

# Default per-goal timeout for discrete mode (seconds).
# Each of the 49 integer goal checks gets this budget independently.
DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC: float = 5.0

# Epsilon used for goal bounds in discrete mode.
# Set to 0.0 so each CROWN call checks the exact integer goal point, matching
# the 2025_NEUS table approach (which evaluates the NN at exact integer coordinates).
#
# NOTE: alpha-beta-CROWN divides by (upper - lower) in cut_ops.py (lines 319-322)
# without a zero-guard. eps=0.0 is safe here in practice because PGD resolves all
# contracts for 100%-accurate networks before BaB is invoked, so that division is
# never reached. If you see inf/NaN crashes, fall back to eps=1e-5.
DISCRETE_GOAL_EPS: float = 0.0


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
) -> tuple[str, list[float] | None]:
    """
    Verify one A/G contract with a single CROWN call.

    Drone position: [cx-eps, cx+eps] x [cy-eps, cy+eps]  (≈ integer point)
    Goal position:  [grid_min, grid_max]^2                (full continuous range)

    Returns (status, counterexample) where:
        status          — "SAT", "UNSAT", or "TIMEOUT"
        counterexample  — [drone_x, drone_y, goal_x, goal_y] if UNSAT, else None
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
    status = normalize_status(result.status)

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

    Makes one CROWN call per integer goal in {grid_min, ..., grid_max}^2,
    short-circuiting on the first UNSAT found. If all 49 calls return SAT the
    contract is SAT. If any call returns UNSAT the contract is immediately UNSAT.
    If no UNSAT is found but at least one call timed out, returns TIMEOUT.

    Drone position: [cx-eps, cx+eps] x [cy-eps, cy+eps]  (≈ integer source cell)
    Goal position:  [gx-eps, gx+eps] x [gy-eps, gy+eps]  (≈ one integer point)

    Returns (status, counterexample) where:
        status          — "SAT", "UNSAT", or "TIMEOUT"
        counterexample  — [drone_x, drone_y, goal_x, goal_y] if UNSAT, else None
    """
    timeout_seen = False

    for gx in range(grid_min, grid_max + 1):
        for gy in range(grid_min, grid_max + 1):
            x = input_vars((4,))
            lower = torch.tensor(
                [cx - eps, cy - eps, gx - DISCRETE_GOAL_EPS, gy - DISCRETE_GOAL_EPS],
                dtype=torch.float32,
            )
            upper = torch.tensor(
                [cx + eps, cy + eps, gx + DISCRETE_GOAL_EPS, gy + DISCRETE_GOAL_EPS],
                dtype=torch.float32,
            )
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
            status = normalize_status(result.status)

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
# CROWN configuration
# ---------------------------------------------------------------------------

def build_crown_config(cfg: dict[str, Any], timeout_override: float | None = None) -> Any:
    """
    Build the alpha-beta-CROWN solver configuration from the loaded YAML config.

    Args:
        cfg:              Loaded YAML config dict.
        timeout_override: If provided, overrides cfg["verification"]["timeout_sec"].
                          Used by discrete mode to set a short per-goal timeout.
    """
    pgd_order = cfg.get("pgd_order", "before")
    timeout = timeout_override if timeout_override is not None \
        else cfg["verification"]["timeout_sec"]
    builder = (
        ConfigBuilder.from_defaults()
        .set(general__device="cpu")
        .set(attack__pgd_order=pgd_order)
        .set(bab__timeout=timeout)
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

def save_report(records: list[dict[str, Any]], cfg: dict[str, Any], mode_str: str) -> None:
    """
    Write the full verification report to the JSON path set in cfg.

    Args:
        records:   List of per-contract result dicts.
        cfg:       Loaded YAML config dict (must contain output_path).
        mode_str:  Human-readable description of the verification mode,
                   written to the "mode" field of the JSON report.
    """
    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    report = {
        "onnx_path":  cfg["onnx_path"],
        "timestamp":  datetime.datetime.now().isoformat(),
        "mode":       mode_str,
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

    Dispatches to continuous or discrete mode based on cfg.get("discrete", False).
    Discrete mode reads cfg.get("discrete_timeout", DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC)
    as the per-goal timeout.

    Returns a metrics dict with SAT/UNSAT/TIMEOUT counts and wall time,
    in addition to writing the full report JSON to cfg['output_path'].
    """
    obstacles   = [tuple(obs) for obs in cfg["obstacles"]]
    grid_min    = cfg["grid"]["min"]
    grid_max    = cfg["grid"]["max"]
    num_classes = cfg["num_classes"]
    eps         = cfg["verification"]["eps"]
    discrete    = cfg.get("discrete", False)
    if discrete:
        eps = 0.0  # exact integer drone position in discrete mode

    contracts = generate_contracts(obstacles, grid_min, grid_max)

    if discrete:
        discrete_timeout = cfg.get("discrete_timeout", DISCRETE_GOAL_DEFAULT_TIMEOUT_SEC)
        crown_config = build_crown_config(cfg, timeout_override=discrete_timeout)
        mode_str = (f"discrete, {(grid_max - grid_min + 1) ** 2} integer goals, "
                    f"drone EPS={eps}, goal EPS={DISCRETE_GOAL_EPS}, "
                    f"timeout={discrete_timeout}s per goal")
        print(f"Generated {len(contracts)} contracts  "
              f"(discrete mode: {(grid_max - grid_min + 1) ** 2} integer goals, "
              f"timeout={discrete_timeout}s per goal)\n")
    else:
        timeout = cfg["verification"]["timeout_sec"]
        crown_config = build_crown_config(cfg)
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
    parser.add_argument("--discrete", action="store_true",
                        help=("Discrete verification mode: check each of the "
                              "(grid_max - grid_min + 1)^2 integer goal positions "
                              "individually instead of the full continuous range. "
                              "Bridges to the 2025_NEUS table approach."))
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
