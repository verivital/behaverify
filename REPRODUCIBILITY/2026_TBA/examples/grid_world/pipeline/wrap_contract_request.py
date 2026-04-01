"""
pipeline.wrap_contract_request — Step 1: timing wrapper around A/G contract verification.

Temporary file: will be removed once verify_contracts.py is split into
generate_grid_world_contracts.py and verify_grid_world_contracts.py. At that
point, the pipeline will call verify_grid_world_contracts directly.

run_contracts()  — calls verify_contracts.run_verification() and records timing/memory metrics.
skip_contracts() — loads an existing contracts JSON and returns skipped metrics.
"""

from __future__ import annotations

import json
import os
import time
import tracemalloc
from typing import Any

from pipeline.resolve_pipeline_paths import self_rss_kb


def run_contracts(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Verify A/G contracts via alpha-beta-CROWN.

    Imports verify_contracts lazily so the module-level load_config() in that
    script finds verify_contracts.yaml relative to CWD (must be grid_world/).
    """
    print("\n" + "=" * 60)
    print("[1/3] CONTRACT VERIFICATION")
    print("=" * 60)

    import verify_contracts as _vc  # noqa: PLC0415

    cfg = _vc.load_config(str(ctx["config_path"]))
    # CROWN concatenates paths with string ops — absolute paths produce doubled
    # slashes.  Provide CWD-relative paths instead.
    cfg["onnx_path"]   = os.path.relpath(ctx["onnx_path"])
    cfg["output_path"] = os.path.relpath(ctx["contracts_path"])

    tracemalloc.start()
    rss_before = self_rss_kb()
    t0 = time.perf_counter()

    _vc.run_verification(cfg)

    wall_sec = time.perf_counter() - t0
    rss_after = self_rss_kb()
    _, peak_traced = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    summary = _read_summary(ctx["contracts_path"])
    metrics = _build_metrics(wall_sec, rss_after, peak_traced, summary, skipped=False)
    print(f"\n[contracts] {wall_sec:.1f}s  |  peak RSS ≥{rss_after} KB  |  "
          f"SAT={metrics['sat']} UNSAT={metrics['unsat']} TIMEOUT={metrics['timeout']}")
    return metrics


def skip_contracts(ctx: dict[str, Any]) -> dict[str, Any]:
    """Load existing contracts JSON and return zero-cost skipped metrics."""
    print("\n[1/3] CONTRACT VERIFICATION — skipped (using existing JSON)")
    summary = _read_summary(ctx["contracts_path"])
    return _build_metrics(0.0, 0, 0, summary, skipped=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_summary(contracts_path) -> dict[str, Any]:
    with open(contracts_path, encoding="utf-8") as f:
        return json.load(f).get("summary", {})


def _build_metrics(
    wall_sec: float,
    rss_kb: int,
    peak_traced: int,
    summary: dict[str, Any],
    skipped: bool,
) -> dict[str, Any]:
    return {
        "wall_sec":          round(wall_sec, 3),
        "peak_rss_kb":       rss_kb,
        "peak_traced_bytes": peak_traced,
        "sat":               summary.get("SAT", 0),
        "unsat":             summary.get("UNSAT", 0),
        "timeout":           summary.get("TIMEOUT", 0),
        "total":             summary.get("total", 0),
        "skipped":           skipped,
    }
