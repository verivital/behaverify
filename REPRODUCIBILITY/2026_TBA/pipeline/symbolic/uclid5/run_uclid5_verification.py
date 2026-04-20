"""
pipeline.symbolic.uclid5.run_uclid5_verification — UCLID5 subprocess runner.

run_uclid5(ctx)      — runs UCLID5 on a .ucl file; returns timing + verdict.
parse_verdict(text)  — extracts pass/fail from UCLID5 stdout.

ctx keys consumed:
    uclid5_bin      Path  — UCLID5 binary (typically 'uclid')
    ucl_path        Path  — .ucl model file to verify
    uclid5_out_path Path  — where to write combined stdout+stderr
"""

from __future__ import annotations

import re
import subprocess
import time
from typing import Any

from pipeline.resolve_pipeline_paths import children_rss_kb


# UCLID5 prints results like:
#   UCLID5 finished with 1 verified, 0 failed
#   or: 0 verified, 1 failed
_VERIFIED_RE = re.compile(r"(\d+)\s+verified")
_FAILED_RE   = re.compile(r"(\d+)\s+failed")

# Individual property lines:
#   [PASSED] invariant safety_0
#   [FAILED] invariant safety_0
_PROP_RE = re.compile(r"\[(PASSED|FAILED)\]\s+invariant\s+(\w+)")


def parse_verdict(output_text: str) -> dict[str, str | None]:
    """
    Extract verification verdict from UCLID5 stdout.

    Returns:
        invarspec: "true" if all invariants passed, "false" if any failed, None if unclear
        verified:  number of verified properties (str)
        failed:    number of failed properties (str)
    """
    verified_m = _VERIFIED_RE.search(output_text)
    failed_m   = _FAILED_RE.search(output_text)

    verified_count = int(verified_m.group(1)) if verified_m else None
    failed_count   = int(failed_m.group(1))   if failed_m   else None

    if failed_count is not None and verified_count is not None:
        invarspec = "false" if failed_count > 0 else "true"
    else:
        invarspec = None

    return {
        "invarspec": invarspec,
        "verified":  str(verified_count) if verified_count is not None else None,
        "failed":    str(failed_count)   if failed_count   is not None else None,
    }


def run_uclid5(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Run UCLID5 on ctx["ucl_path"] and record timing, RSS, and verdict.

    Captures both stdout and stderr; writes combined output to ctx["uclid5_out_path"].
    Returns a metrics dict suitable for a pipeline steps dict.
    """
    print("\n" + "=" * 60)
    print("[UCLID5] SYMBOLIC VERIFICATION")
    print("=" * 60)

    cmd = [str(ctx["uclid5_bin"]), str(ctx["ucl_path"])]
    print(f"  Command: {' '.join(cmd)}")

    rss_before = children_rss_kb()
    t0 = time.perf_counter()

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    wall_sec  = time.perf_counter() - t0
    rss_after = children_rss_kb()

    output_text = result.stdout + result.stderr
    ctx["uclid5_out_path"].write_text(output_text, encoding="utf-8")

    verdict = parse_verdict(output_text)
    metrics = {
        "wall_sec":    round(wall_sec, 3),
        "peak_rss_kb": rss_after - rss_before,
        "returncode":  result.returncode,
        **verdict,
    }
    print(f"\n  [{wall_sec:.1f}s]  INVARSPEC={verdict['invarspec']}  "
          f"(verified={verdict['verified']}, failed={verdict['failed']})")
    print(f"  Output saved to: {ctx['uclid5_out_path']}")
    return metrics
