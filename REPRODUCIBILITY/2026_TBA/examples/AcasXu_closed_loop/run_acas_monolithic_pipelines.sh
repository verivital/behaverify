#!/usr/bin/env bash
#
# run_acas_monolithic_pipelines.sh
#
# Benchmark ACAS Xu monolithic verification vs. discrete compositional verification.
# This is the ACAS Xu equivalent of grid_world/run_all_monolithic_pipelines.sh.
#
# Stages:
#   1. [TREE]         Generate tree/acas_360.tree (if missing)
#   2. [SMV]          Generate smv/acas_360.smv via dsl_to_nuxmv (if missing)
#   3. [MONO-VERIFY]  Run nuXmv on the monolithic SMV; emit pipeline_report.json
#                     (or load pre-computed 2025_NEUS result via --skip-monolithic)
#   4. [MERGE]        Merge discrete contract results for all 5 NNs
#   5. [COMP-VERIFY]  Run discrete compositional pipeline; emit pipeline_report.json
#   6. [SUMMARY]      Print side-by-side comparison table
#
# Usage (from REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop/):
#   ./run_acas_monolithic_pipelines.sh
#   ./run_acas_monolithic_pipelines.sh --nuxmv /path/to/nuXmv
#   ./run_acas_monolithic_pipelines.sh --skip-monolithic   # use 2025_NEUS reference result
#
# WARNING: the monolithic nuXmv run requires ~9.6 GB RAM. If your machine has less
# than ~12 GB free, use --skip-monolithic to load the pre-computed reference result
# from REPRODUCIBILITY/2025_NEUS/examples/AcasXu_closed_loop/invar.txt instead.
#
# Output:
#   results/monolithic/nuxmv_output.txt       (skipped with --skip-monolithic)
#   results/monolithic/timing.txt             (skipped with --skip-monolithic)
#   results/monolithic/pipeline_report.json
#   results/compositional/discrete_goals/all_nns/pipeline_report.json
#
# Prerequisites:
#   pip install -e .
#   pip install -r REPRODUCIBILITY/2026_TBA/requirements.txt
#   nuXmv binary at ../../nuXmv_DL/bin/nuXmv (or override with --nuxmv)

set -euo pipefail

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NUXMV="${_HERE}/../../nuXmv_DL/bin/nuXmv"
SKIP_MONO=false
NUXMV_REFERENCE="${_HERE}/../../../2025_NEUS/examples/AcasXu_closed_loop/invar.txt"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --nuxmv)            NUXMV="$2"; shift 2 ;;
        --skip-monolithic)  SKIP_MONO=true; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done

NUXMV_CMD_ALL_INVAR="${_HERE}/../../scripts/nuxmv_commands/command_all_invar"
SRC_DIR="${_HERE}/../../src"
METAMODEL="${_HERE}/../../metamodel/behaverify.tx"
PYTHON="${PYTHON:-python3}"

# ---------------------------------------------------------------------------
# Stage 1: Generate tree (if missing)
# ---------------------------------------------------------------------------
echo "========================================"
echo "[1/6] TREE GENERATION"
echo "========================================"

if [[ -f "${_HERE}/tree/acas_360.tree" ]]; then
    echo "  Skipped — tree/acas_360.tree already exists"
else
    mkdir -p "${_HERE}/tree"
    cd "${_HERE}"
    "${PYTHON}" generate_acas_tree.py
    echo "  Generated tree/acas_360.tree"
fi

# ---------------------------------------------------------------------------
# Stage 2: Generate base SMV (if missing)
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "[2/6] BASE SMV GENERATION"
echo "========================================"

if [[ -f "${_HERE}/smv/acas_360.smv" ]]; then
    echo "  Skipped — smv/acas_360.smv already exists"
else
    mkdir -p "${_HERE}/smv"
    echo "  Calling dsl_to_nuxmv (this may take ~30s)..."
    cd "${_HERE}"
    "${PYTHON}" - <<PYEOF
import sys, pathlib
src_dir = "${SRC_DIR}"
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
import dsl_to_nuxmv as _dsl
_dsl.dsl_to_nuxmv(
    "${METAMODEL}",
    "tree/acas_360.tree",
    "smv/acas_360.smv",
    False, False, False, False,
    10000,  # recursion_limit
    False,  # keep_stage_0
    True,   # skip_grammar_check
    None,   # record_times
)
print("  Generated smv/acas_360.smv")
PYEOF
fi

# ---------------------------------------------------------------------------
# Stage 3: Monolithic nuXmv verification
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "[3/6] MONOLITHIC NUXMV VERIFICATION"
echo "========================================"

mkdir -p "${_HERE}/results/monolithic"
MONO_OUT="${_HERE}/results/monolithic/nuxmv_output.txt"
MONO_TIMING="${_HERE}/results/monolithic/timing.txt"
MONO_REPORT="${_HERE}/results/monolithic/pipeline_report.json"

if [[ "${SKIP_MONO}" == "true" ]]; then
    echo "  --skip-monolithic: loading reference result from 2025_NEUS..."
    if [[ ! -f "${NUXMV_REFERENCE}" ]]; then
        echo "ERROR: Reference file not found: ${NUXMV_REFERENCE}" >&2
        exit 1
    fi

    "${PYTHON}" - <<PYEOF
import json, re, pathlib, datetime

ref_text = pathlib.Path("${NUXMV_REFERENCE}").read_text()

m = re.search(r'\[Invar\s+(True|False)\b', ref_text, re.IGNORECASE)
invarspec = m.group(1).lower() if m else None

m = re.search(r'User time\s+(\S+)\s+seconds', ref_text)
user_sec = float(m.group(1)) if m else None

m = re.search(r'Maximum resident size\s+=\s+(\d+)\s*K', ref_text)
peak_rss_kb = int(m.group(1)) if m else None

report = {
    "mode":           "monolithic",
    "source":         "2025_NEUS reference (--skip-monolithic)",
    "smv_path":       "smv/acas_360.smv",
    "timestamp":      datetime.datetime.utcnow().isoformat() + "Z",
    "steps": {
        "nuxmv": {
            "wall_sec":    round(user_sec, 3) if user_sec    is not None else None,
            "user_sec":    round(user_sec, 3) if user_sec    is not None else None,
            "peak_rss_kb": peak_rss_kb,
            "invarspec":   invarspec,
        }
    },
    "total_wall_sec": round(user_sec, 3) if user_sec is not None else None,
    "verdict":        f"INVAR={invarspec}" if invarspec else "UNKNOWN",
}

pathlib.Path("${MONO_REPORT}").write_text(json.dumps(report, indent=2))
print(f"  INVARSPEC : {invarspec}")
if user_sec    is not None: print(f"  User time : {user_sec:.1f}s")
if peak_rss_kb is not None: print(f"  Peak RSS  : {peak_rss_kb / 1024**2:.2f} GB")
print(f"  Source    : ${NUXMV_REFERENCE}")
print(f"  Report    : ${MONO_REPORT}")
PYEOF

else
    echo "  Running nuXmv on smv/acas_360.smv..."
    echo "  WARNING: requires ~9.6 GB RAM. Use --skip-monolithic if machine has <12 GB free."
    echo "  (Expected: ~49s, ~9.6 GB peak RSS)"

    cd "${_HERE}"
    { time "${NUXMV}" -source "${NUXMV_CMD_ALL_INVAR}" smv/acas_360.smv \
        > "${MONO_OUT}" 2>&1 ; } 2> "${MONO_TIMING}"

    echo "  nuXmv done. Parsing results..."

    "${PYTHON}" - <<PYEOF
import json, re, pathlib, datetime

out_text  = pathlib.Path("${MONO_OUT}").read_text()
time_text = pathlib.Path("${MONO_TIMING}").read_text()

m = re.search(r'-- invariant .+ is (true|false)', out_text, re.IGNORECASE)
invarspec = m.group(1).lower() if m else None

m = re.search(r'User time\s+(\S+)\s+seconds', out_text)
user_sec = float(m.group(1)) if m else None

m = re.search(r'Maximum resident size\s+=\s+(\d+)\s*K', out_text)
peak_rss_kb = int(m.group(1)) if m else None

m = re.search(r'real\s+(\d+)m([\d.]+)s', time_text)
wall_sec = float(m.group(1)) * 60 + float(m.group(2)) if m else user_sec

report = {
    "mode":           "monolithic",
    "smv_path":       "smv/acas_360.smv",
    "timestamp":      datetime.datetime.utcnow().isoformat() + "Z",
    "steps": {
        "nuxmv": {
            "wall_sec":    round(wall_sec, 3)    if wall_sec    is not None else None,
            "user_sec":    round(user_sec, 3)    if user_sec    is not None else None,
            "peak_rss_kb": peak_rss_kb,
            "invarspec":   invarspec,
        }
    },
    "total_wall_sec": round(wall_sec, 3) if wall_sec is not None else None,
    "verdict":        f"INVAR={invarspec}" if invarspec else "UNKNOWN",
}

pathlib.Path("${MONO_REPORT}").write_text(json.dumps(report, indent=2))
print(f"  INVARSPEC : {invarspec}")
if user_sec    is not None: print(f"  User time : {user_sec:.1f}s")
if peak_rss_kb is not None: print(f"  Peak RSS  : {peak_rss_kb / 1024**2:.2f} GB")
print(f"  Report    : ${MONO_REPORT}")
PYEOF

fi

# ---------------------------------------------------------------------------
# Stage 4: Merge discrete contract results for all 5 NNs
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "[4/6] MERGING DISCRETE CONTRACT RESULTS"
echo "========================================"

DISCRETE_DIR="${_HERE}/contracts/discrete_goals"
MERGED_JSON="${DISCRETE_DIR}/.merged.json"

"${PYTHON}" - <<PYEOF
import json, pathlib

files = [
    "${DISCRETE_DIR}/aprev_clear_crown_results.json",
    "${DISCRETE_DIR}/aprev_weak_right_crown_results.json",
    "${DISCRETE_DIR}/aprev_weak_left_crown_results.json",
    "${DISCRETE_DIR}/aprev_strong_right_crown_results.json",
    "${DISCRETE_DIR}/aprev_strong_left_crown_results.json",
]

missing = [f for f in files if not pathlib.Path(f).exists()]
if missing:
    print("ERROR: Missing discrete contract result files:")
    for f in missing:
        print(f"  {f}")
    print("Run verify_all_discrete_contracts.sh first.")
    raise SystemExit(1)

all_contracts = []
for f in files:
    data = json.loads(pathlib.Path(f).read_text())
    all_contracts.extend(data["contracts"])

pathlib.Path("${MERGED_JSON}").write_text(json.dumps({"contracts": all_contracts}))

sat   = sum(1 for c in all_contracts if c.get("status") == "SAT")
unsat = sum(1 for c in all_contracts if c.get("status") == "UNSAT")
other = len(all_contracts) - sat - unsat
print(f"  Merged {len(all_contracts)} contracts: {sat} SAT, {unsat} UNSAT, {other} other")
print(f"  Written to {('${MERGED_JSON}')}")
PYEOF

# ---------------------------------------------------------------------------
# Stage 5: Discrete compositional pipeline
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "[5/6] DISCRETE COMPOSITIONAL PIPELINE"
echo "========================================"

COMP_OUT_DIR="${_HERE}/results/compositional/discrete_goals/all_nns"

cd "${_HERE}"
"${PYTHON}" run_acas_compositional_pipeline.py \
    --contracts "${MERGED_JSON}" \
    --output    "${COMP_OUT_DIR}" \
    --nuxmv     "${NUXMV}" \
    --skip-tree \
    --skip-smv

# ---------------------------------------------------------------------------
# Stage 6: Side-by-side comparison summary
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "[6/6] BENCHMARK SUMMARY"
echo "========================================"

"${PYTHON}" - <<PYEOF
import json, pathlib

mono_path = pathlib.Path("${MONO_REPORT}")
comp_path = pathlib.Path("${COMP_OUT_DIR}/pipeline_report.json")

if not mono_path.exists():
    print("  WARNING: monolithic report not found:", mono_path)
    mono = {}
else:
    mono = json.loads(mono_path.read_text())

if not comp_path.exists():
    print("  WARNING: compositional report not found:", comp_path)
    comp = {}
else:
    comp = json.loads(comp_path.read_text())

def get(d, *keys, default="N/A"):
    for k in keys:
        if not isinstance(d, dict): return default
        d = d.get(k, {})
    return d if d != {} else default

mono_nuxmv   = mono.get("steps", {}).get("nuxmv", {})
comp_nuxmv   = comp.get("steps", {}).get("nuxmv", {})
comp_patch   = comp.get("steps", {}).get("smv_patch", {})

mono_invar   = mono_nuxmv.get("invarspec", "N/A")
comp_invar   = comp_nuxmv.get("invarspec", "N/A")
mono_wall    = mono_nuxmv.get("wall_sec", "N/A")
comp_total   = comp.get("total_wall_sec", "N/A")
mono_rss     = mono_nuxmv.get("peak_rss_kb")
sat_count    = comp_patch.get("sat_contracts", "N/A")
invar_count  = comp_patch.get("invar_lines", "N/A")
total_c      = comp_patch.get("total_contracts", "N/A")

mono_rss_str = f"{mono_rss / 1024**2:.1f} GB" if mono_rss else "N/A"
mono_wall_str = f"{mono_wall:.1f}s" if isinstance(mono_wall, (int, float)) else str(mono_wall)
comp_wall_str = f"{comp_total:.1f}s" if isinstance(comp_total, (int, float)) else str(comp_total)
sat_str = f"{sat_count} / {total_c}" if total_c != "N/A" else str(sat_count)

SEP = "=" * 72
COL = 30

print(SEP)
print("  BENCHMARK SUMMARY: ACAS Xu Monolithic vs. Discrete Compositional")
print(SEP)
print(f"  {'':30s}  {'Monolithic':>20s}  {'Discrete Compositional':>22s}")
print(f"  {'-'*30}  {'-'*20}  {'-'*22}")
print(f"  {'INVARSPEC':30s}  {str(mono_invar):>20s}  {str(comp_invar):>22s}")
print(f"  {'nuXmv wall time':30s}  {mono_wall_str:>20s}  {comp_wall_str:>22s}")
print(f"  {'Peak RSS':30s}  {mono_rss_str:>20s}  {'N/A':>22s}")
print(f"  {'SAT contracts':30s}  {'N/A':>20s}  {sat_str:>22s}")
print(f"  {'INVAR constraints injected':30s}  {'N/A':>20s}  {str(invar_count):>22s}")
print(SEP)
print()
print("  Reports:")
print(f"    {mono_path}")
print(f"    {comp_path}")
print()
print("  NOTE: INVARSPEC=false with UNSAT/TIMEOUT contracts is expected —")
print("  discrete contracts cover unreachable states. The monolithic INVAR=true")
print("  is the ground truth (nuXmv evaluates only reachable states).")
PYEOF

echo ""
echo "Done. All results in results/monolithic/ and results/compositional/discrete_goals/all_nns/"
