#!/usr/bin/env bash
# Section 4.3 reproduction: BehaVerify on BT2BIP's MarsRover and TrainControl.
#
# Note: BT2BIP itself (Wang et al. 2024) is not bundled in this image. The
# paper's Section 4.3 just notes "Both tools agree the Mars Rover spec is
# false and the Train Control spec is false; BT2BIP timed out on LTL
# specifications on the larger trees while BehaVerify completed verification."
# We reproduce only the BehaVerify side here, and report the verdicts from
# the INVAR runs.
#
# The 2026_ATVA tool-comparison script already runs MarsRover_0 and
# TrainControl_0 (see exp_tool_comparisons_2026_ATVA_run.sh). Table 3 reuses
# the same pre-build step, so this script only re-parses the existing
# results files.

set -euo pipefail

OUT_DIR="${1:-/out}"
mkdir -p "${OUT_DIR}"
ATVA="/home/bv/behaverify/REPRODUCIBILITY/2026_ATVA"

# If Table 3 was not run first, kick off the build/run for the BT2BIP
# examples ourselves.
if [ ! -d "${ATVA}/examples/BT2BIP/results" ]; then
    echo "[Sec 4.3] Build & run BT2BIP examples..."
    ( cd "${ATVA}/scripts/build_scripts" \
       && ./exp_tool_comparisons_2026_ATVA_create.sh python3 1 1 1 ) \
       > "${OUT_DIR}/section43_create.log" 2>&1
    ( cd "${ATVA}/scripts/encoding_timing_scripts" \
       && ./exp_tool_comparisons_2026_ATVA_run.sh 1 1 1 ) \
       > "${OUT_DIR}/section43_run.log" 2>&1
fi

# Parse INVAR results: verdict + total wall time for each example.
python3 - <<'PY' "${OUT_DIR}"
import json, pathlib, re, sys
out = pathlib.Path(sys.argv[1])
results = pathlib.Path("/home/bv/behaverify/REPRODUCIBILITY/2026_ATVA/examples/BT2BIP/results")

def verdict_and_time(stem):
    """Verdicts come from INVAR_full_opt_<stem>_0.txt (non-silent shows the
    'is true/false' line). Wall time comes from SILENT_INVAR_*_0.txt."""
    verdict_p = results / f"INVAR_full_opt_{stem}_0.txt"
    silent_p  = results / f"SILENT_INVAR_full_opt_{stem}_0.txt"
    if not silent_p.exists():
        return {"found": False}
    truths = []
    if verdict_p.exists():
        truths = re.findall(r"-- (?:invariant|specification).*?\bis\s+(true|false)\b",
                            verdict_p.read_text())
    elapses = re.findall(r"elapse:\s*([\d.]+)\s*seconds", silent_p.read_text())
    return {
        "found":    True,
        "verdicts": truths,                                          # one per spec
        "wall_sec": float(elapses[-1]) if elapses else None,
    }

(out / "section43_behaverify.json").write_text(json.dumps({
    "MarsRover":    verdict_and_time("MarsRover"),
    "TrainControl": verdict_and_time("TrainControl"),
}, indent=2))
print("  wrote", out / "section43_behaverify.json")
PY

echo "[Sec 4.3] Done."
