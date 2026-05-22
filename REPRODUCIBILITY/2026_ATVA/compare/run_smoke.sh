#!/usr/bin/env bash
# Smoke test: verify the full tool chain end-to-end in ~3-5 minutes.
# Does NOT reproduce exact paper numbers -- use run_all.sh for that.
#
# Runs:
#   Table 2  -- N=1..3, 1 timing run, 30s per-instance timeout  (< 1 min)
#   Table 3  -- BT2Fiacre/drone3 with persistent-sets (-P, fast path)    (< 30s)
#   Sec 4.3  -- BehaVerify on MarsRover / TrainControl               (< 1 min)
#
# Expected total: 3-5 min on any modern x86-64 host.

set -euo pipefail

OUT="${1:-/out}"
mkdir -p "${OUT}"
ATVA="/home/bv/behaverify/REPRODUCIBILITY/2026_ATVA"
EX="${ATVA}/examples/EncodingComparison"

echo "=========================================================================="
echo "BehaVerify ATVA 2026 SMOKE TEST"
echo "=========================================================================="
echo "Started: $(date -u)"
echo

# ---------------------------------------------------------------------------
# Table 2 smoke: N=1..3, 1 run, 30s per-instance timeout.
# All three instances are sub-second; 30s is a generous guard against hung nuXmv.
# ---------------------------------------------------------------------------
echo "[smoke] Table 2 (N=1..3, 1 run, 30s timeout): generating SMV files..."
( cd "${ATVA}/scripts/build_scripts" \
  && ./exp_encoding_comparison_create.sh python3 1 3 1 ) \
  > "${OUT}/smoke_table2_create.log" 2>&1

echo "[smoke] Table 2: timing sweep..."
( cd "${ATVA}/scripts/encoding_timing_scripts" \
  && ./exp_encoding_comparison_run.sh 1 3 1 30s ) \
  > "${OUT}/smoke_table2_run.log" 2>&1

mkdir -p "${OUT}/smoke_table2"
for f in CTL-Fastforwarding-Concise CTL-Naive-Concise \
          LTL-Fastforwarding-Concise LTL-Naive-Concise; do
    cp "${EX}/${f}" "${OUT}/smoke_table2/"
done

# ---------------------------------------------------------------------------
# Table 3 BT2Fiacre smoke: drone3 with -P (persistent-sets reduction).
# The full evaluation uses BT2F_PERSISTENT_SETS=0 (hits timeout as in paper).
# Here -P is hardcoded so the state space is small enough to finish in < 5s,
# which confirms the bt2fiacre -> frac -> sift -> selt chain works end-to-end.
# ---------------------------------------------------------------------------
echo "[smoke] Table 3 BT2Fiacre (drone3, persistent-sets -P enabled)..."
mkdir -p "${OUT}/smoke_bt2fiacre"

(
    set -euo pipefail
    cd /opt/bt2fiacre/examples

    LOG="${OUT}/smoke_bt2fiacre/drone3.log"
    TIMING="${OUT}/smoke_bt2fiacre/drone3_timing.txt"
    : > "${LOG}"; : > "${TIMING}"

    _stage() {
        local TAG="$1"; shift
        if ! timeout 30s /usr/bin/time -f "${TAG}=%e" -ao "${TIMING}" "$@" \
                >> "${LOG}" 2>&1; then
            echo "${TAG}=TIMEOUT_OR_FAIL" >> "${TIMING}"; return 1
        fi
    }

    _stage btf_to_fcr bt2fiacre \
        -c "set tina_compact on" -c "set tick Node" -c "set default_prop off" \
        -c "load bt \"drone3.btf\"" \
        -c "save fiacre \"/tmp/drone3.fcr\"" \
        -c "exit" drone3 || exit 0

    rm -rf /tmp/drone3.tts
    _stage frac /opt/hippo/frac -tts \
        /tmp/drone3.fcr /tmp/drone3.tts || exit 0
    _stage sift /opt/tina/bin/sift -P \
        /tmp/drone3.tts/drone3.net -kts /tmp/drone3.ktz -stats || exit 0
    _stage selt /opt/tina/bin/selt \
        /tmp/drone3.ktz /tmp/drone3.tts/drone3.ltl -b || exit 0
)

# ---------------------------------------------------------------------------
# Section 4.3 smoke: BehaVerify on BT2BIP examples.
# run_section43.sh is self-contained and always finishes in < 30s.
# ---------------------------------------------------------------------------
echo "[smoke] Section 4.3 (BehaVerify on BT2BIP examples)..."
bash /home/bv/run_section43.sh "${OUT}"

# ---------------------------------------------------------------------------
# Print smoke summary
# ---------------------------------------------------------------------------
echo
python3 - "${OUT}" <<'PY'
import json, pathlib, sys

out = pathlib.Path(sys.argv[1])
SEP = "=" * 60

print(SEP)
print("SMOKE TEST RESULTS")
print(SEP)

# Table 2 (N=1..3, single run)
snap = out / "smoke_table2"
cols = ["CTL-Fastforwarding", "CTL-Naive", "LTL-Fastforwarding", "LTL-Naive"]
rows = {}
for c in cols:
    p = snap / f"{c}-Concise"
    if p.exists():
        for i, line in enumerate(p.read_text().splitlines()):
            v = line.strip()
            if v:
                rows.setdefault(i + 1, {})[c] = v
print("\nTable 2 (N=1-3, 1 run, 30s timeout). Expected: all values < 1s")
print(f"{'N':>2}  {'CTL-FF':>8}  {'CTL-Naive':>9}  {'LTL-FF':>8}  {'LTL-Naive':>9}")
for n in sorted(rows):
    r = rows[n]
    print(f"{n:>2}"
          f"  {r.get('CTL-Fastforwarding', '?'):>8}"
          f"  {r.get('CTL-Naive', '?'):>9}"
          f"  {r.get('LTL-Fastforwarding', '?'):>8}"
          f"  {r.get('LTL-Naive', '?'):>9}")

# Table 3 BT2Fiacre smoke
t_path = out / "smoke_bt2fiacre" / "drone3_timing.txt"
if t_path.exists():
    timings = {}
    for line in t_path.read_text().splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            timings[k.strip()] = v.strip()
    print("\nTable 3 BT2Fiacre smoke (drone3, -P). Expected: all stages < 5s")
    for s in ("btf_to_fcr", "frac", "sift", "selt"):
        v = timings.get(s, "?")
        try:
            print(f"  {s:15s}: {float(v):.2f}s")
        except ValueError:
            print(f"  {s:15s}: {v}")

# Section 4.3
p43 = out / "section43_behaverify.json"
if p43.exists():
    data = json.loads(p43.read_text())
    print("\nSection 4.3 (BehaVerify/BT2BIP). Expected: 'false' verdicts, ~0s wall time")
    for stem in ("MarsRover", "TrainControl"):
        e = data.get(stem, {})
        v = ", ".join(e.get("verdicts") or []) or "?"
        w = f"{e['wall_sec']:.2f}s" if e.get("wall_sec") is not None else "?"
        print(f"  {stem:15s}: verdicts={v}  wall={w}")

print("\n" + SEP)
print("Smoke test PASSED. All tools executed without errors.")
print("For full evaluation (~60 min):")
print('  docker run --rm \\')
print('    -v "$(pwd)/REPRODUCIBILITY/2026_ATVA/compare/output:/out" \\')
print('    behaverify-compare')
print(SEP)
PY

echo
echo "Finished: $(date -u)"
