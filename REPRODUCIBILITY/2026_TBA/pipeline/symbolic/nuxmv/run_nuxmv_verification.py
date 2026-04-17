"""
pipeline.symbolic.nuxmv.run_nuxmv_verification — nuXmv subprocess runner.

run_nuxmv(ctx)   — runs nuXmv as a subprocess and returns timing + verdicts.
parse_verdicts() — extracts INVARSPEC and CTLSPEC verdicts from nuXmv stdout.

ctx keys consumed:
    nuxmv_bin       Path  — nuXmv binary
    nuxmv_cmd       Path  — nuXmv command file (-source argument)
    smv_path        Path  — SMV model file to verify
    nuxmv_out_path  Path  — where to write combined stdout+stderr
"""

from __future__ import annotations

import re
import subprocess
import time
from typing import Any

from pipeline.resolve_pipeline_paths import children_rss_kb


_INVAR_RE = re.compile(r"-- invariant .+ is (true|false)")
_CTL_RE   = re.compile(r"-- specification .+ is (true|false)")


def parse_verdicts(output_text: str) -> dict[str, str | None]:
    """Extract INVARSPEC and CTLSPEC verdicts from nuXmv stdout."""
    invar_match = _INVAR_RE.search(output_text)
    ctl_match   = _CTL_RE.search(output_text)
    return {
        "invarspec": invar_match.group(1) if invar_match else None,
        "ctlspec":   ctl_match.group(1)   if ctl_match   else None,
    }


def run_nuxmv(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Run nuXmv on ctx["smv_path"] and record timing, RSS, and verdicts.

    Captures both stdout and stderr; writes combined output to ctx["nuxmv_out_path"].
    Returns a metrics dict suitable for inclusion in a pipeline steps dict.
    """
    print("\n" + "=" * 60)
    print("[nuXmv] SYMBOLIC VERIFICATION")
    print("=" * 60)

    cmd = [str(ctx["nuxmv_bin"]), "-source", str(ctx["nuxmv_cmd"]), str(ctx["smv_path"])]
    print(f"  Command: {' '.join(cmd)}")

    rss_before = children_rss_kb()
    t0 = time.perf_counter()

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    wall_sec  = time.perf_counter() - t0
    rss_after = children_rss_kb()

    output_text = result.stdout + result.stderr
    ctx["nuxmv_out_path"].write_text(output_text, encoding="utf-8")

    verdicts = parse_verdicts(output_text)
    metrics  = {
        "wall_sec":    round(wall_sec, 3),
        "peak_rss_kb": rss_after - rss_before,
        "returncode":  result.returncode,
        **verdicts,
    }
    print(f"\n  [{wall_sec:.1f}s]  INVARSPEC={verdicts['invarspec']}  "
          f"CTLSPEC={verdicts['ctlspec']}")
    print(f"  Output saved to: {ctx['nuxmv_out_path']}")
    return metrics
