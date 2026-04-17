"""
verify_acas_contracts_parallel.py

Parallel wrapper for verify_acas_contracts.py.
Splits TIMEOUT contracts across N worker processes and merges results.

Thin wrapper: ACAS-specific logic (compute_nn_inputs, dangerous_xy iteration)
is kept here.  CROWN invocation is delegated to pipeline/neuro/crown/crown_verification.py
via lazy imports inside worker_fn (required for multiprocessing spawn context).

Usage:
    python verify_acas_contracts_parallel.py \\
        --timeout 3600 \\
        --retry-from contracts/crown/continuous_goals/enabled_pgd/aprev_clear_crown_results.json \\
        --workers 8 \\
        --device cpu
"""

import argparse
import datetime
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path
from typing import Any

_HERE = Path(__file__).parent.resolve()
_TBA  = (_HERE / "../../").resolve()
if str(_TBA) not in sys.path:
    sys.path.insert(0, str(_TBA))


def worker_fn(args_tuple):
    """Run in a child process — verifies one contract and returns a record dict."""
    (contract_spec, onnx_path, forbidden_idx, num_classes,
     timeout, device, worker_id, discrete, discrete_timeout) = args_tuple

    # Lazy imports so each process loads its own CROWN state.
    # crown_verification imports abcrown, which must load in each worker process.
    import sys
    from pathlib import Path as _Path
    _tba = _Path(__file__).resolve().parents[2]
    if str(_tba) not in sys.path:
        sys.path.insert(0, str(_tba))

    from pipeline.neuro.crown.crown_verification import (
        build_crown_config,
        run_crown_verification,
    )

    if discrete:
        from generate_acas_contracts import compute_nn_inputs

        crown_config = build_crown_config(
            timeout=discrete_timeout,
            pgd_order="before",
            device=device,
        )

        x_sign      = contract_spec["x_sign"]
        y_sign      = contract_spec["y_sign"]
        heading_var = contract_spec["heading_own_var"]
        timeout_seen = False
        status = "SAT"

        t0 = time.perf_counter()
        for x_mag, y_mag in contract_spec["dangerous_xy"]:
            exact = compute_nn_inputs(x_mag, y_mag, x_sign, y_sign, heading_var)
            try:
                per_status, _ = run_crown_verification(
                    onnx_path=onnx_path,
                    lower=exact,
                    upper=exact,
                    forbidden_idx=forbidden_idx,
                    num_classes=num_classes,
                    crown_config=crown_config,
                )
            except Exception:
                per_status = "TIMEOUT"

            if per_status == "UNSAT":
                status = "UNSAT"
                break
            if per_status == "TIMEOUT":
                timeout_seen = True

        if status != "UNSAT":
            status = "TIMEOUT" if timeout_seen else "SAT"
        wall_sec = time.perf_counter() - t0

    else:
        crown_config = build_crown_config(
            timeout=timeout,
            pgd_order="before",
            device=device,
            extra_settings={
                "bab__cut__enabled":      True,
                "bab__cut__cplex_cuts":   False,
                "bab__branching__method": "sb",
            },
        )

        t0 = time.perf_counter()
        try:
            status, _ = run_crown_verification(
                onnx_path=onnx_path,
                lower=contract_spec["nn_input_lower"],
                upper=contract_spec["nn_input_upper"],
                forbidden_idx=forbidden_idx,
                num_classes=num_classes,
                crown_config=crown_config,
            )
        except Exception as e:
            status = "TIMEOUT"
        wall_sec = time.perf_counter() - t0

    sign = lambda v: "+" if v == 1 else "-"
    quad = f"({sign(contract_spec['x_sign'])},{sign(contract_spec['y_sign'])})"

    return {
        "id":                     contract_spec["id"],
        "heading_own_var":        contract_spec["heading_own_var"],
        "x_sign":                 contract_spec["x_sign"],
        "y_sign":                 contract_spec["y_sign"],
        "forbidden_advisory":     contract_spec["forbidden_advisory"],
        "forbidden_advisory_idx": forbidden_idx,
        "n_states_covered":       contract_spec["n_states_covered"],
        "dangerous_xy":           contract_spec["dangerous_xy"],
        "wall_sec":               round(wall_sec, 3),
        "status":                 status,
        "quad":                   quad,
    }


def main():
    parser = argparse.ArgumentParser(description="Parallel ACAS Xu contract verification")
    parser.add_argument("--config", default="verify_acas_contracts_config.yaml")
    parser.add_argument("--retry-from", dest="retry_from", required=True,
                        help="Previous results JSON — re-verify TIMEOUT contracts")
    parser.add_argument("--timeout", type=int, default=3600,
                        help="Timeout per contract in seconds (default: 3600)")
    parser.add_argument("--workers", type=int, default=None,
                        help="Number of parallel workers (default: CPU count)")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"],
                        help="Device for CROWN (default: cpu)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Only verify first N TIMEOUT contracts")
    parser.add_argument(
        "--discrete", action="store_true",
        help="Discrete mode: verify each dangerous (x_mag, y_mag) state individually.",
    )
    parser.add_argument(
        "--discrete-timeout", type=float, default=None,
        dest="discrete_timeout",
        help="Per-state timeout in seconds for discrete mode.",
    )
    args = parser.parse_args()

    import yaml
    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    nn_idx = cfg["network_idx"]
    num_classes = cfg["num_classes"]

    discrete_timeout = (
        args.discrete_timeout
        if args.discrete_timeout is not None
        else cfg["verification"].get("discrete_timeout_sec", 5.0)
    )
    discrete_eps = cfg["verification"].get("discrete_state_eps", 0.0)

    with open(cfg["contracts_path"], encoding="utf-8") as f:
        spec_data = json.load(f)
    all_specs = {c["id"]: c for c in spec_data["contracts"] if c["network_idx"] == nn_idx}

    with open(args.retry_from, encoding="utf-8") as f:
        prev = json.load(f)
    previous_records = {r["id"]: r for r in prev["contracts"]}
    timeout_ids = [r["id"] for r in prev["contracts"] if r["status"] == "TIMEOUT"]

    if args.limit:
        timeout_ids = timeout_ids[:args.limit]

    if args.discrete:
        mode_str = f"discrete, EPS={discrete_eps}, timeout={discrete_timeout}s per state"
    else:
        mode_str = "continuous"

    print(f"Parallel verification: {len(timeout_ids)} TIMEOUT contracts")
    print(f"Mode: {mode_str}")
    print(f"Workers: {args.workers or mp.cpu_count()}, Device: {args.device}, Timeout: {args.timeout}s\n")

    worker_args = []
    for i, cid in enumerate(timeout_ids):
        spec = all_specs[cid]
        worker_args.append((
            spec,
            spec["onnx"],
            spec["forbidden_advisory_idx"],
            num_classes,
            args.timeout,
            args.device,
            i,
            args.discrete,
            discrete_timeout,
        ))

    n_workers = args.workers or mp.cpu_count()
    if args.device == "cuda":
        n_workers = min(n_workers, 1)
        print("Note: CUDA mode limited to 1 worker (GPU contention)")

    print(f"Starting {n_workers} workers for {len(worker_args)} contracts...\n")
    print(f"{'#':<5} {'ID':>5} {'Heading':>7} {'Quad':>6} {'Forbidden':<14} {'Sec':>8} {'Status':<10}")
    print("-" * 70)
    sys.stdout.flush()

    run_start = time.perf_counter()
    completed = 0

    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=n_workers) as pool:
        for result in pool.imap_unordered(worker_fn, worker_args):
            completed += 1
            quad = result.pop("quad")
            marker = "OK" if result["status"] == "SAT" else ("X" if result["status"] == "UNSAT" else "?")
            print(
                f"{completed:<5} {result['id']:>5} {result['heading_own_var']:>7} {quad:>6} "
                f"{result['forbidden_advisory']:<14} {result['wall_sec']:>8.1f} {result['status']:<10} {marker}"
            )
            sys.stdout.flush()
            previous_records[result["id"]] = result

    total_wall = time.perf_counter() - run_start
    records = sorted(previous_records.values(), key=lambda r: r["id"])

    counts = {s: sum(1 for r in records if r["status"] == s) for s in ("SAT", "UNSAT", "TIMEOUT")}
    improved = sum(1 for cid in timeout_ids if previous_records[cid]["status"] == "SAT")

    print("-" * 70)
    print(f"\nRetry improved {improved}/{len(timeout_ids)} contracts to SAT")
    print(f"Summary: {counts['SAT']} SAT, {counts['UNSAT']} UNSAT, "
          f"{counts['TIMEOUT']} TIMEOUT out of {len(records)} contracts")
    print(f"Total wall time: {total_wall:.1f}s  ({total_wall/60:.1f} min)")

    cfg["verification"]["timeout_sec"] = args.timeout
    sat_times = [r["wall_sec"] for r in records if r["status"] == "SAT"]
    report = {
        "network_idx":     nn_idx,
        "onnx_path":       worker_args[0][1] if worker_args else "",
        "mode":            mode_str,
        "timestamp":       datetime.datetime.now().isoformat(),
        "timeout_sec":     args.timeout,
        "total_wall_sec":  round(total_wall, 3),
        "avg_sat_sec":     round(sum(sat_times) / len(sat_times), 3) if sat_times else None,
        "summary":         {**counts, "total": len(records)},
        "contracts":       records,
    }
    with open(cfg["output_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Results saved to {cfg['output_path']}")


if __name__ == "__main__":
    main()
