"""
pipeline.write_pipeline_report — Step 4: JSON report and console summary.

write_report() serialises all per-step metrics to pipeline_report.json and
prints a formatted summary table to stdout.
"""

from __future__ import annotations

import datetime
import json
from typing import Any


def write_report(ctx: dict[str, Any], steps: dict[str, dict], total_wall_sec: float) -> None:
    """Write pipeline_report.json and print the final pipeline summary."""
    invar   = steps["nuxmv_verification"].get("invarspec")
    ctl     = steps["nuxmv_verification"].get("ctlspec")
    verdict = f"INVAR={invar} CTL={ctl}"

    report = {
        "network":        ctx["network_name"],
        "onnx_path":      str(ctx["onnx_path"]),
        "tree_path":      str(ctx["tree_path"]),
        "timestamp":      datetime.datetime.now().isoformat(),
        "steps":          steps,
        "total_wall_sec": round(total_wall_sec, 3),
        "verdict":        verdict,
    }

    with open(ctx["report_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _print_summary(ctx, steps, verdict, total_wall_sec)


def _print_summary(
    ctx: dict[str, Any],
    steps: dict[str, dict],
    verdict: str,
    total_wall_sec: float,
) -> None:
    c = steps["contracts"]
    s = steps["smv_generation"]
    n = steps["nuxmv_verification"]

    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Network  : {ctx['network_name']}")
    print(f"  Contracts: SAT={c['sat']}  UNSAT={c['unsat']}  "
          f"TIMEOUT={c['timeout']}  (skipped={c['skipped']})")
    print(f"  SMV      : {s['sat_contracts_injected']} INVARs injected")
    print(f"  nuXmv    : INVARSPEC={n['invarspec']}  CTLSPEC={n['ctlspec']}")
    print(f"  Timing   : contracts={c['wall_sec']:.1f}s  "
          f"smv={s['wall_sec']:.1f}s  "
          f"nuxmv={n['wall_sec']:.1f}s  "
          f"total={total_wall_sec:.1f}s")
    print(f"  Verdict  : {verdict}")
    print(f"  Report   : {ctx['report_path']}")
    print("=" * 60)
