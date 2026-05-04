#!/usr/bin/env bash
# Table 2 reproduction: BehaVerify FF vs Naive ablation, N = 1..10,
# 3 runs averaged, 5 min per-instance timeout.
#
# Inputs:
#   $1  -- output directory (default /out)
# Side-effects:
#   Writes <out>/table2_run_{1,2,3}/ snapshots (raw timing) and the
#   averaged values to <out>/table2_avg.csv (parsed by format_results.py).

set -euo pipefail

OUT_DIR="${1:-/out}"
mkdir -p "${OUT_DIR}"
ATVA="/home/bv/behaverify/REPRODUCIBILITY/2026_ATVA"
EX="${ATVA}/examples/EncodingComparison"

# Build SMV files (FF + naive encodings) for N=1..10 — done once, reused
# across all three timing runs.
echo "[Table 2] Generating binary-tree SMV files (N=1..10)..."
( cd "${ATVA}/scripts/build_scripts" \
  && ./exp_encoding_comparison_create.sh python3 1 10 1 ) > "${OUT_DIR}/table2_create.log" 2>&1

# Run the timing experiment 3 times, snapshot the four "Concise" files.
for run in 1 2 3; do
    echo "[Table 2] Timing run ${run}/3 (5m timeout per instance)..."
    ( cd "${ATVA}/scripts/encoding_timing_scripts" \
      && ./exp_encoding_comparison_run.sh 1 10 1 5m ) \
        > "${OUT_DIR}/table2_run${run}.log" 2>&1

    SNAP="${OUT_DIR}/table2_run_${run}"
    mkdir -p "${SNAP}"
    cp "${EX}/CTL-Fastforwarding-Concise" "${SNAP}/"
    cp "${EX}/CTL-Naive-Concise"          "${SNAP}/"
    cp "${EX}/LTL-Fastforwarding-Concise" "${SNAP}/"
    cp "${EX}/LTL-Naive-Concise"          "${SNAP}/"
done

# Generate state-space counts (single run is fine — exact integer sizes,
# not timed). Uses extract_states.sh which reads the per-N STATES output.
if [ -x "${EX}/extract_states.sh" ]; then
    echo "[Table 2] Extracting reachable / total state-space sizes..."
    ( cd "${EX}" && ./extract_states.sh 1 10 1 ) > "${OUT_DIR}/table2_states.log" 2>&1 || true
fi

# Average the 3 runs and emit a single CSV that format_results.py renders.
echo "[Table 2] Averaging 3 runs..."
python3 - <<'PY' "${OUT_DIR}"
import sys, pathlib, statistics
out = pathlib.Path(sys.argv[1])

def parse_concise(p):
    """Each line is either a float (seconds) or 'TIMEOUT'."""
    vals = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            vals.append(float(line))
        except ValueError:
            vals.append(None)   # TIMEOUT sentinel
    return vals

def avg(triples):
    """Average across 3 runs per N. If any run is TIMEOUT (None), report TIMEOUT."""
    if any(v is None for v in triples):
        return "TIMEOUT"
    return f"{statistics.mean(triples):.2f}"

cols = ["CTL-Fastforwarding", "CTL-Naive", "LTL-Fastforwarding", "LTL-Naive"]
runs = [parse_concise(out / f"table2_run_{r}" / f"{c}-Concise")
        for r in (1, 2, 3) for c in cols]
# runs now has 12 lists of 10 entries each, in row-major (run, col) order.

n_rows = max(len(r) for r in runs)
csv = ["N," + ",".join(cols)]
for i in range(n_rows):
    row = [str(i + 1)]
    for c_idx, _ in enumerate(cols):
        triple = [runs[r * len(cols) + c_idx][i] for r in range(3) if i < len(runs[r * len(cols) + c_idx])]
        row.append(avg(triple))
    csv.append(",".join(row))

(out / "table2_avg.csv").write_text("\n".join(csv) + "\n")
print(f"  wrote {out / 'table2_avg.csv'}")
PY

echo "[Table 2] Done."
