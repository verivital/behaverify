"""
verify_acas_contracts_parallel.py

Parallel wrapper for verify_acas_contracts.py.
Splits TIMEOUT contracts across N worker processes and merges results.

Usage:
    python verify_acas_contracts_parallel.py \
        --timeout 3600 \
        --retry-from contracts/continuous_goals/enabled_pgd/aprev_clear_crown_results.json \
        --workers 8 \
        --device cpu
"""

import argparse
import datetime
import json
import multiprocessing as mp
import os
import sys
import time
from typing import Any


def worker_fn(args_tuple):
    """Run in a child process — verifies one contract and returns a record dict."""
    contract_spec, onnx_path, forbidden_idx, num_classes, timeout, device, worker_id = args_tuple

    # Lazy imports so each process loads its own CROWN state
    import functools
    import torch
    from abcrown import ABCrownSolver, VerificationSpec, ConfigBuilder, input_vars, output_vars

    crown_config = (
        ConfigBuilder.from_defaults()
        .set(general__device=device)
        .set(attack__pgd_order="before")
        .set(attack__pgd_restarts=50)
        .set(bab__timeout=timeout)
        .set(bab__cut__enabled=True)
        .set(bab__cut__cplex_cuts=False)
        .set(bab__branching__method="sb")
        ()
    )

    x = input_vars((5,))
    lower_t = torch.tensor(contract_spec["nn_input_lower"], dtype=torch.float32)
    upper_t = torch.tensor(contract_spec["nn_input_upper"], dtype=torch.float32)
    input_constraint = (x >= lower_t) & (x <= upper_t)

    y = output_vars(num_classes)
    others = [j for j in range(num_classes) if j != forbidden_idx]
    output_constraint = functools.reduce(
        lambda a, b: a | b,
        [y[j] > y[forbidden_idx] for j in others],
    )

    spec = VerificationSpec.build_spec(
        input_vars=x, output_vars=y,
        input_constraint=input_constraint, output_constraint=output_constraint,
    )

    t0 = time.perf_counter()
    try:
        result = ABCrownSolver(spec, onnx_path, config=crown_config).solve()
        raw_status = result.status
    except Exception as e:
        raw_status = f"error: {e}"
    wall_sec = time.perf_counter() - t0

    # Normalize status
    if raw_status in ("safe", "verified", "safe-incomplete"):
        status = "SAT"
    elif isinstance(raw_status, str) and raw_status.startswith("unsafe"):
        status = "UNSAT"
    else:
        status = "TIMEOUT"

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
    parser.add_argument("--config", default="acas_config.yaml")
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
    args = parser.parse_args()

    import yaml
    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    nn_idx = cfg["network_idx"]
    num_classes = cfg["num_classes"]

    # Load contract specs
    with open(cfg["contracts_path"], encoding="utf-8") as f:
        spec_data = json.load(f)
    all_specs = {c["id"]: c for c in spec_data["contracts"] if c["network_idx"] == nn_idx}

    # Load previous results
    with open(args.retry_from, encoding="utf-8") as f:
        prev = json.load(f)
    previous_records = {r["id"]: r for r in prev["contracts"]}
    timeout_ids = [r["id"] for r in prev["contracts"] if r["status"] == "TIMEOUT"]

    if args.limit:
        timeout_ids = timeout_ids[:args.limit]

    print(f"Parallel verification: {len(timeout_ids)} TIMEOUT contracts")
    print(f"Workers: {args.workers or mp.cpu_count()}, Device: {args.device}, Timeout: {args.timeout}s\n")

    # Build worker arguments
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
        ))

    n_workers = args.workers or mp.cpu_count()
    # For CUDA, limit to 1 worker per GPU to avoid contention
    if args.device == "cuda":
        n_workers = min(n_workers, 1)
        print("Note: CUDA mode limited to 1 worker (GPU contention)")

    print(f"Starting {n_workers} workers for {len(worker_args)} contracts...\n")
    print(f"{'#':<5} {'ID':>5} {'Heading':>7} {'Quad':>6} {'Forbidden':<14} {'Sec':>8} {'Status':<10}")
    print("-" * 70)
    sys.stdout.flush()

    run_start = time.perf_counter()
    completed = 0

    # Use spawn context on Windows for clean process creation
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

            # Update and save incrementally
            previous_records[result["id"]] = result

    total_wall = time.perf_counter() - run_start

    # Build final records
    records = sorted(previous_records.values(), key=lambda r: r["id"])

    # Summary
    counts = {s: sum(1 for r in records if r["status"] == s) for s in ("SAT", "UNSAT", "TIMEOUT")}
    improved = sum(1 for cid in timeout_ids
                   if previous_records[cid]["status"] == "SAT")

    print("-" * 70)
    print(f"\nRetry improved {improved}/{len(timeout_ids)} contracts to SAT")
    print(f"Summary: {counts['SAT']} SAT, {counts['UNSAT']} UNSAT, "
          f"{counts['TIMEOUT']} TIMEOUT out of {len(records)} contracts")
    print(f"Total wall time: {total_wall:.1f}s  ({total_wall/60:.1f} min)")

    # Save
    cfg["verification"]["timeout_sec"] = args.timeout
    sat_times = [r["wall_sec"] for r in records if r["status"] == "SAT"]
    report = {
        "network_idx":     nn_idx,
        "onnx_path":       worker_args[0][1] if worker_args else "",
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
