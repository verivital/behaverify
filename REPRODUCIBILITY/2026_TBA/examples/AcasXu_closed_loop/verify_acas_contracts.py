"""
verify_acas_contracts.py

Verify A/G safety contracts for the ACAS Xu closed-loop NSBT using alpha-beta-CROWN.

Thin wrapper: ACAS-specific logic is limited to input-space construction
(compute_nn_inputs, dangerous_xy iteration).  All CROWN invocation, config
building, and status normalization are delegated to pipeline/neuro/crown/crown_verification.py.

Contract semantics (range-based, analogous to grid-world single-call contracts):
  - Input region : nn_input_lower[i] <= x[i] <= nn_input_upper[i]  (5 inputs)
  - Output property: forbidden_advisory score < max(all other scores)
  - If SAT (verified): NN never chooses the forbidden advisory from any state
    in this input region -- the A/G guarantee holds for all covered states.

Class index mapping (matches DSL enum order and generate_acas_contracts.py):
  clear=0  weak_left=1  weak_right=2  strong_left=3  strong_right=4

Configuration: verify_acas_contracts_config.yaml
Output: JSON report (path set in YAML or overridden via --output)

Run from:  REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop/
"""

import os
import sys
import json
import datetime
import time
import argparse
from pathlib import Path
from typing import Any

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

from generate_acas_contracts import compute_nn_inputs


# ---------------------------------------------------------------------------
# Configuration loading
# ---------------------------------------------------------------------------

def load_config(path: str = "verify_acas_contracts_config.yaml") -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Discrete-mode contract verification
# ---------------------------------------------------------------------------

def verify_contract_discrete(
    contract: dict[str, Any],
    onnx_path: str,
    forbidden_idx: int,
    num_classes: int,
    crown_config: Any,
) -> str:
    """
    Verify one contract in discrete mode: one CROWN call per dangerous state.

    Loops over contract["dangerous_xy"] (pre-computed integer (x_mag, y_mag) pairs),
    computes exact NN inputs for each, and calls CROWN with lower=upper=exact_inputs.
    Short-circuits on the first UNSAT. Returns TIMEOUT only if no UNSAT was found
    but at least one state timed out.
    """
    x_sign      = contract["x_sign"]
    y_sign      = contract["y_sign"]
    heading_var = contract["heading_own_var"]
    timeout_seen = False

    for x_mag, y_mag in contract["dangerous_xy"]:
        exact = compute_nn_inputs(x_mag, y_mag, x_sign, y_sign, heading_var)
        status, _ = run_crown_verification(
            onnx_path=onnx_path,
            lower=exact,
            upper=exact,
            forbidden_idx=forbidden_idx,
            num_classes=num_classes,
            crown_config=crown_config,
        )
        if status == "UNSAT":
            return "UNSAT"
        if status == "TIMEOUT":
            timeout_seen = True

    return "TIMEOUT" if timeout_seen else "SAT"


# ---------------------------------------------------------------------------
# CROWN config builder (ACAS-specific defaults)
# ---------------------------------------------------------------------------

def _build_crown_cfg(cfg: dict[str, Any], timeout_override: float | None = None) -> Any:
    timeout = timeout_override if timeout_override is not None \
        else cfg["verification"]["timeout_sec"]
    return build_crown_config(
        timeout=timeout,
        pgd_order="skip",
        device="cpu",
    )


# ---------------------------------------------------------------------------
# Console helpers
# ---------------------------------------------------------------------------

def result_marker(status: str) -> str:
    if status == "SAT":
        return "✓"
    if status == "UNSAT":
        return "✗  <- VIOLATION"
    return "?  <- TIMEOUT (inconclusive)"


def print_summary(records: list[dict[str, Any]]) -> None:
    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    print(f"\nSummary: {counts['SAT']} SAT, {counts['UNSAT']} UNSAT, "
          f"{counts['TIMEOUT']} TIMEOUT out of {len(records)} contracts")


def save_report(
    records: list[dict[str, Any]],
    cfg: dict[str, Any],
    nn_idx: int,
    onnx_path: str,
    total_wall_sec: float,
    mode: str = "continuous",
) -> None:
    counts = {s: sum(1 for r in records if r["status"] == s)
              for s in ("SAT", "UNSAT", "TIMEOUT")}
    sat_times = [r["wall_sec"] for r in records if r["status"] == "SAT"]
    report = {
        "network_idx":     nn_idx,
        "onnx_path":       onnx_path,
        "mode":            mode,
        "timestamp":       datetime.datetime.now().isoformat(),
        "timeout_sec":     cfg["verification"]["timeout_sec"],
        "total_wall_sec":  round(total_wall_sec, 3),
        "avg_sat_sec":     round(sum(sat_times) / len(sat_times), 3) if sat_times else None,
        "summary":         {**counts, "total": len(records)},
        "contracts":       records,
    }
    os.makedirs(os.path.dirname(cfg["output_path"]) or ".", exist_ok=True)
    with open(cfg["output_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Results saved to {cfg['output_path']}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_verification(
    cfg: dict[str, Any],
    limit: int | None = None,
    retry_from: str | None = None,
    timeout_override: int | None = None,
) -> None:
    nn_idx      = cfg["network_idx"]
    num_classes = cfg["num_classes"]
    if timeout_override is not None:
        cfg["verification"]["timeout_sec"] = timeout_override
    timeout = cfg["verification"]["timeout_sec"]

    with open(cfg["contracts_path"], encoding="utf-8") as f:
        spec_data = json.load(f)

    all_contracts = spec_data["contracts"]
    contracts = [c for c in all_contracts if c["network_idx"] == nn_idx]

    if not contracts:
        print(f"No contracts found for network_idx={nn_idx}. Check contracts_path.")
        sys.exit(1)

    previous_records: dict[int, dict] = {}
    if retry_from:
        with open(retry_from, encoding="utf-8") as f:
            prev = json.load(f)
        previous_records = {r["id"]: r for r in prev["contracts"]}
        timeout_ids = {r["id"] for r in prev["contracts"] if r["status"] == "TIMEOUT"}
        contracts = [c for c in contracts if c["id"] in timeout_ids]
        print(f"Retry mode: {len(contracts)} TIMEOUT contracts from {retry_from}")

    if limit is not None:
        contracts = contracts[:limit]

    onnx_path = contracts[0]["onnx"]
    discrete  = cfg.get("discrete", False)

    if discrete:
        dt = cfg.get("discrete_timeout",
                     cfg["verification"].get("discrete_timeout_sec", 5.0))
        crown_config = _build_crown_cfg(cfg, timeout_override=dt)
        eps      = cfg["verification"].get("discrete_state_eps", 0.0)
        mode_str = f"discrete, EPS={eps}, timeout={dt}s per state"
        print(f"Verifying {len(contracts)} contracts for NN_{nn_idx} ({onnx_path})")
        print(f"Mode: {mode_str}\n")
    else:
        crown_config = _build_crown_cfg(cfg, timeout_override=timeout_override)
        mode_str = "continuous"
        print(f"Verifying {len(contracts)} contracts for NN_{nn_idx} ({onnx_path})")
        print(f"Timeout: {timeout}s per contract\n")

    print(f"{'#':<5} {'Heading':>7} {'Quad':>6} {'Forbidden':<14} {'States':>6} {'Sec':>6} {'Status':<10} Marker")
    print("-" * 80)

    new_records = []
    run_start = time.perf_counter()

    for i, contract in enumerate(contracts):
        t0 = time.perf_counter()
        if discrete:
            status = verify_contract_discrete(
                contract=contract,
                onnx_path=onnx_path,
                forbidden_idx=contract["forbidden_advisory_idx"],
                num_classes=num_classes,
                crown_config=crown_config,
            )
        else:
            status, _ = run_crown_verification(
                onnx_path=onnx_path,
                lower=contract["nn_input_lower"],
                upper=contract["nn_input_upper"],
                forbidden_idx=contract["forbidden_advisory_idx"],
                num_classes=num_classes,
                crown_config=crown_config,
            )
        wall_sec = time.perf_counter() - t0

        sign = lambda v: "+" if v == 1 else "-"
        quad = f"({sign(contract['x_sign'])},{sign(contract['y_sign'])})"

        print(
            f"{i+1:<5} {contract['heading_own_var']:>7} {quad:>6} "
            f"{contract['forbidden_advisory']:<14} {contract['n_states_covered']:>6} "
            f"{wall_sec:>6.1f} {status:<10} {result_marker(status)}"
        )
        sys.stdout.flush()

        new_records.append({
            "id":                     contract["id"],
            "heading_own_var":        contract["heading_own_var"],
            "x_sign":                 contract["x_sign"],
            "y_sign":                 contract["y_sign"],
            "forbidden_advisory":     contract["forbidden_advisory"],
            "forbidden_advisory_idx": contract["forbidden_advisory_idx"],
            "n_states_covered":       contract["n_states_covered"],
            "dangerous_xy":           contract["dangerous_xy"],
            "wall_sec":               round(wall_sec, 3),
            "status":                 status,
        })

    total_wall = time.perf_counter() - run_start

    if retry_from:
        updated = {r["id"]: r for r in new_records}
        previous_records.update(updated)
        records = sorted(previous_records.values(), key=lambda r: r["id"])
        improved = sum(1 for r in new_records if r["status"] == "SAT")
        print(f"\nRetry improved {improved}/{len(new_records)} contracts to SAT")
    else:
        records = new_records

    print("-" * 80)
    print_summary(records)
    print(f"Total wall time: {total_wall:.1f}s  ({total_wall/60:.1f} min)")
    save_report(records, cfg, nn_idx, onnx_path, total_wall, mode=mode_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify ACAS Xu A/G contracts via alpha-beta-CROWN."
    )
    parser.add_argument(
        "--config", default="verify_acas_contracts_config.yaml",
        help="Path to YAML config (default: verify_acas_contracts_config.yaml)",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Verify only the first N contracts (useful for pilot runs)",
    )
    parser.add_argument(
        "--retry-from", default=None, dest="retry_from",
        help="Path to a previous results JSON; re-verify only TIMEOUT contracts",
    )
    parser.add_argument(
        "--timeout", type=int, default=None,
        help="Override timeout_sec from YAML for this run",
    )
    parser.add_argument(
        "--network-idx", type=int, default=None, dest="network_idx",
        help="Override network_idx from YAML (1=clear, 2=weak_right, 3=weak_left, "
             "4=strong_right, 5=strong_left)",
    )
    parser.add_argument(
        "--output", default=None,
        help="Override output_path from YAML",
    )
    parser.add_argument(
        "--discrete", action="store_true",
        help="Discrete mode: verify each dangerous (x_mag, y_mag) state individually "
             "(lower=upper=exact NN inputs, EPS=0). Short-circuits on first UNSAT.",
    )
    parser.add_argument(
        "--discrete-timeout", type=float, default=None,
        dest="discrete_timeout",
        help=("Per-state timeout in seconds for discrete mode. "
              "Default: verification.discrete_timeout_sec from YAML. "
              "Ignored if --discrete not set."),
    )
    args = parser.parse_args()
    cfg = load_config(args.config)
    if args.network_idx is not None:
        cfg["network_idx"] = args.network_idx
    if args.output is not None:
        cfg["output_path"] = args.output
    if args.discrete:
        cfg["discrete"] = True
        if args.discrete_timeout is not None:
            cfg["discrete_timeout"] = args.discrete_timeout
    run_verification(
        cfg,
        limit=args.limit,
        retry_from=args.retry_from,
        timeout_override=args.timeout,
    )
