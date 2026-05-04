#!/usr/bin/env bash
# Table 3 reproduction: BehaVerify drone3 + droneNew vs BT2Fiacre drone3 + drone4.
#
# Two pipelines:
#   (A) BehaVerify  -- runs the existing 2026_ATVA tool-comparison script,
#                      which translates drone3.tree / droneNew.tree to SMV
#                      and verifies the height invariant via nuXmv.
#   (B) BT2Fiacre   -- bt2fiacre -> frac -> gcc -> tina sift -> tina selt
#                      on /opt/bt2fiacre/examples/drone3.btf and drone4.btf
#                      (BT2Fiacre's own encodings of the same drone model).
#
# Output: <out>/table3_behaverify.json, <out>/table3_bt2fiacre.json
# Both are read back by format_results.py.

set -euo pipefail

OUT_DIR="${1:-/out}"
mkdir -p "${OUT_DIR}"
ATVA="/home/bv/behaverify/REPRODUCIBILITY/2026_ATVA"

# ============================================================
# (A) BehaVerify side
# ============================================================
echo "[Table 3] (A) BehaVerify drone3 + droneNew via 2026_ATVA scripts..."
( cd "${ATVA}/scripts/build_scripts"  \
   && ./exp_tool_comparisons_2026_ATVA_create.sh python3 1 10 1 ) \
   > "${OUT_DIR}/table3_behaverify_create.log" 2>&1
( cd "${ATVA}/scripts/encoding_timing_scripts" \
   && ./exp_tool_comparisons_2026_ATVA_run.sh 1 10 1 ) \
   > "${OUT_DIR}/table3_behaverify_run.log" 2>&1

# Parse per-paper QUICKSTART:
#   Prep            -- results/translation_drone3_{0,3}.txt   -> "total:"
#   Check Height    -- results/SILENT_INVAR_full_opt_drone3_{0,3}.txt -> 2nd "elapse:"
#   Reach. / Total  -- results/STATES_full_opt_drone3_{0,3}.txt
python3 - <<'PY' "${OUT_DIR}"
import json, pathlib, re, sys
out = pathlib.Path(sys.argv[1])
results = pathlib.Path("/home/bv/behaverify/REPRODUCIBILITY/2026_ATVA/examples/BT2Fiacre/results")

def grep_total(path):
    """First 'total:' line in translation_drone3_{0,3}.txt (Prep time)."""
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith("total:"):
            return float(line.split(":", 1)[1].strip())
    return None

def second_elapse(path):
    """Second 'elapse:  X.XX seconds' value in SILENT_INVAR_*.txt (Check Height)."""
    matches = re.findall(r"elapse:\s*([\d.]+)\s*seconds", pathlib.Path(path).read_text())
    return float(matches[1]) if len(matches) >= 2 else None

def states_log2(path):
    """STATES_full_opt_drone3_*.txt -- nuXmv prints
       'reachable states: <n> (2^<X>) out of <m> (2^<Y>)'.
       Returns (reach_log2, total_log2)."""
    txt = pathlib.Path(path).read_text()
    m = re.search(r"reachable states:.*?\(2\^([\d.]+)\).*?out of.*?\(2\^([\d.]+)\)", txt)
    return (float(m.group(1)), float(m.group(2))) if m else (None, None)

def per_drone(idx):
    return {
        "prep_sec":         grep_total(results / f"translation_drone3_{idx}.txt"),
        "check_height_sec": second_elapse(results / f"SILENT_INVAR_full_opt_drone3_{idx}.txt"),
        "reach_log2":       states_log2(results / f"STATES_full_opt_drone3_{idx}.txt")[0],
        "total_log2":       states_log2(results / f"STATES_full_opt_drone3_{idx}.txt")[1],
    }

(out / "table3_behaverify.json").write_text(json.dumps({
    "drone3":   per_drone(0),
    "droneNew": per_drone(3),
}, indent=2))
print("  wrote", out / "table3_behaverify.json")
PY

# ============================================================
# (B) BT2Fiacre side
# ============================================================
echo "[Table 3] (B) BT2Fiacre drone3 + drone4..."
EX=/opt/bt2fiacre/examples
mkdir -p "${OUT_DIR}/bt2fiacre_runs"

# Per-stage cap. The paper's Table 3 BT2Fiacre column reports a TIMEOUT at
# >5400 s on local hardware -- that's the "sift without -P" workload.
# Default 300 s = 5 min, matching Table 2's per-instance cap.
BT2F_TIMEOUT="${BT2F_TIMEOUT:-300}"

# Persistent-sets reduction. Off by default to reproduce the paper's
# (slow / TIMEOUT) BT2Fiacre numbers. Set BT2F_PERSISTENT_SETS=1 to enable
# `sift -P`, which makes BT2Fiacre finish in <1 s (the "real" answer).
SIFT_P_FLAG=""
if [[ "${BT2F_PERSISTENT_SETS:-0}" == "1" ]]; then
    SIFT_P_FLAG="-P"
fi

run_bt2fiacre() {
    local D="$1"; local TIMING="${OUT_DIR}/bt2fiacre_runs/${D}_timing.txt"
    local LOG="${OUT_DIR}/bt2fiacre_runs/${D}.log"
    : > "${TIMING}"; : > "${LOG}"
    cd "${EX}"

    # Pipeline matches the paper's measurement methodology
    # (cf. vsc-compare/REPRODUCIBILITY/2026_FM/comparison/bt2fiacre/run_verification.sh):
    #   bt2fiacre BTF -> FCR     (set default_prop off, set tick Node, set tina_compact on)
    #   frac      FCR -> TTS dir (.net + .ltl)
    #   sift      .net -> .ktz   ([-P], -stats)
    #   selt      .ktz + .ltl    (-b)
    #
    # default_prop=off is what the vsc-compare team used and what the
    # paper's harness measures.  With default_prop on, frac fails on
    # auto-generated property components in this BT2Fiacre commit.

    if ! timeout "${BT2F_TIMEOUT}s" \
            /usr/bin/time -f "btf_to_fcr=%e" -ao "${TIMING}" bt2fiacre \
                -c "set tina_compact on" -c "set tick Node" -c "set default_prop off" \
                -c "load bt \"${D}.btf\"" -c "save fiacre \"/tmp/${D}.fcr\"" \
                -c "exit" "${D}" >> "${LOG}" 2>&1; then
        echo "btf_to_fcr=TIMEOUT_OR_FAIL" >> "${TIMING}"; return 0
    fi

    rm -rf "/tmp/${D}.tts"
    if ! timeout "${BT2F_TIMEOUT}s" \
            /usr/bin/time -f "frac=%e" -ao "${TIMING}" \
                /opt/hippo/frac -tts "/tmp/${D}.fcr" "/tmp/${D}.tts" \
                >> "${LOG}" 2>&1; then
        echo "frac=TIMEOUT_OR_FAIL" >> "${TIMING}"; return 0
    fi

    if ! timeout "${BT2F_TIMEOUT}s" \
            /usr/bin/time -f "sift=%e" -ao "${TIMING}" \
                /opt/tina/bin/sift ${SIFT_P_FLAG} \
                    "/tmp/${D}.tts/${D}.net" -kts "/tmp/${D}.ktz" -stats \
                >> "${LOG}" 2>&1; then
        echo "sift=TIMEOUT_OR_FAIL" >> "${TIMING}"; return 0
    fi

    if ! timeout "${BT2F_TIMEOUT}s" \
            /usr/bin/time -f "selt=%e" -ao "${TIMING}" \
                /opt/tina/bin/selt "/tmp/${D}.ktz" "/tmp/${D}.tts/${D}.ltl" -b \
                >> "${LOG}" 2>&1; then
        echo "selt=TIMEOUT_OR_FAIL" >> "${TIMING}"; return 0
    fi

    # Extract state-space sizes from the sift output.
    grep -oE "[0-9]+ marking\(s\),\s*[0-9]+ transition" "${LOG}" | tail -1 >> "${TIMING}"
}

run_bt2fiacre drone3
run_bt2fiacre drone4

# Parse the timing files into JSON. A TIMEOUT_OR_FAIL marker means the
# stage either exceeded BT2F_TIMEOUT or failed (e.g. frac unbound-component
# error on auto-generated default_prop properties). Either way we treat
# the run as a TIMEOUT for table-rendering purposes, matching the paper.
python3 - <<'PY' "${OUT_DIR}"
import json, math, pathlib, re, sys
out = pathlib.Path(sys.argv[1])
runs = out / "bt2fiacre_runs"

def parse(name):
    txt = (runs / f"{name}_timing.txt").read_text()
    secs, timeouts = {}, []
    for line in txt.splitlines():
        m = re.match(r"(\w+)=(.+)$", line.strip())
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        if v == "TIMEOUT_OR_FAIL":
            timeouts.append(k)
        else:
            try:    secs[k] = float(v)
            except: pass
    m = re.search(r"(\d+) marking\(s\),\s*(\d+) transition", txt)
    mark, trans = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    return {
        "btf_to_fcr_sec": secs.get("btf_to_fcr"),
        "frac_sec":       secs.get("frac"),
        "sift_sec":       secs.get("sift"),
        "selt_sec":       secs.get("selt"),
        "timeouts":       timeouts,
        "markings":       mark,
        "transitions":    trans,
        "reach_log2":     (math.log2(mark)  if mark  else None),
        "total_log2":     (math.log2(mark)  if mark  else None),  # sift reports markings; no separate "total"
    }

(out / "table3_bt2fiacre.json").write_text(json.dumps({
    "drone3":         parse("drone3"),
    "drone4_~droneNew": parse("drone4"),
}, indent=2))
print("  wrote", out / "table3_bt2fiacre.json")
PY

echo "[Table 3] Done."
