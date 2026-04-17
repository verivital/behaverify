"""
pipeline.write_pipeline_report — generic JSON report writer and console summary.

write_report() serialises per-step metrics to pipeline_report.json and prints
a formatted summary table.  It is example-agnostic: step names, extra report
fields, and the nuxmv step key are all caller-supplied.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any


def write_report(
    report_path: Path | str,
    steps: dict[str, dict],
    total_wall_sec: float,
    extra: dict[str, Any] | None = None,
) -> str:
    """
    Write pipeline_report.json and print a pipeline summary.

    Args:
        report_path:    Destination JSON path.
        steps:          Ordered dict mapping step_name -> metrics dict.
                        The first step whose metrics contain "invarspec" is
                        used for the verdict.
        total_wall_sec: Total elapsed wall time for the entire pipeline.
        extra:          Optional extra top-level fields to include in the JSON
                        (e.g. {"network": "1000__0200_1", "onnx_path": "..."}).

    Returns:
        The verdict string written to the report.
    """
    invar = None
    ctl   = None
    for metrics in steps.values():
        if "invarspec" in metrics:
            invar = metrics["invarspec"]
            ctl   = metrics.get("ctlspec")
            break

    verdict = f"INVAR={invar} CTL={ctl}" if ctl is not None else f"INVAR={invar}"

    report: dict[str, Any] = {
        "timestamp":      datetime.datetime.now().isoformat(),
        "steps":          steps,
        "total_wall_sec": round(total_wall_sec, 3),
        "verdict":        verdict,
        **(extra or {}),
    }

    Path(report_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    _print_summary(steps, verdict, total_wall_sec, report_path)
    return verdict


def _print_summary(
    steps: dict[str, dict],
    verdict: str,
    total_wall_sec: float,
    report_path: Any,
) -> None:
    timing_parts = [
        f"{name}={m.get('wall_sec', 0.0):.1f}s"
        for name, m in steps.items()
    ]
    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Timing  : {' | '.join(timing_parts)}")
    print(f"            total={total_wall_sec:.1f}s")
    print(f"  Verdict : {verdict}")
    print(f"  Report  : {report_path}")
    print("=" * 60)
