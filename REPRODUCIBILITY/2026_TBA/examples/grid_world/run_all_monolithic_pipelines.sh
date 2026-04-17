#!/usr/bin/env bash
# run_all_monolithic_pipelines.sh
#
# Monolithic verification pipeline for grid-world NSBTs (table approach only).
#
# This replicates the 2025_NEUS paper baseline: BehaVerify embeds the full
# NN lookup table into a nuXmv SMV file, then nuXmv verifies INVARSPEC and
# CTLSPEC on the resulting monolithic model.
#
# Stages (derived from REPRODUCIBILITY/2025_NEUS/BehaVerify_2025_NEUS.sh):
#   1. [TREE]   Generate .tree files from 2025_NEUS template (table mode only)
#   2. [SMV]    Convert .tree -> .smv via BehaVerify with timing
#   3. [VERIFY] Run nuXmv (INVAR + CTL) on table SMVs for 1000-series networks
#
# Results go to: REPRODUCIBILITY/2026_TBA/examples/grid_world/results/monolithic/
#
# Usage (from REPRODUCIBILITY/2026_TBA/examples/grid_world/):
#
#   ./run_all_monolithic_pipelines.sh
#
# Prerequisites:
#   - BehaVerify installed and on PATH (run: pip install -e . from repo root)
#   - nuXmv binary at REPRODUCIBILITY/2026_TBA/nuXmv_DL/bin/nuXmv

set -euo pipefail

_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NUXMV="${_HERE}/../../nuXmv_DL/bin/nuXmv"
NUXMV_CMD="${_HERE}/../../commands/nuxmv_commands/command_combo_invar_ctl"
# Template lives in 2025_NEUS — the .tree format and obstacle config are shared.
TEMPLATE="${_HERE}/../../../2025_NEUS/examples/grid_world/template.tree"
OUT="${_HERE}/results/monolithic"
PYTHON="${PYTHON:-python3}"

NETWORKS=(
    "1000__6_18_0__0100_1"
    "1000__6_18_0__0150_1"
    "1000__6_18_0__0200_1"
    "1000__6_18_0__0250_1"
    "1000__6_18_0__0300_1"
    "0996__6_18_0__200_1"
    "0995__6_18_0__200_1"
)

mkdir -p "${OUT}/tree"
mkdir -p "${OUT}/smv"

# ---------------------------------------------------------------------------
# Stage 1 + 2: Generate .tree and .smv for each network (table mode, with timing)
# ---------------------------------------------------------------------------
echo "========================================"
echo "[1-2/3] Generating .tree and .smv files"
echo "========================================"

for NAME in "${NETWORKS[@]}"; do
    # ONNX path must be relative to _HERE (CWD when behaverify runs).
    # BehaVerify passes the source string directly to onnxruntime, which resolves
    # it relative to CWD, not the tree file location.
    ONNX="./networks/${NAME}.onnx"
    TREE="${OUT}/tree/table_${NAME}.tree"
    SMV="${OUT}/smv/table_${NAME}.smv"
    TIMING="${OUT}/timing_table_${NAME}.txt"

    echo "  ${NAME}"

    # Generate .tree from 2025_NEUS template (table mode).
    sed -e "s/REPLACE_CONFIG/table/g" \
        -e "s|REPLACE_SOURCE|${ONNX}|g" \
        "${TEMPLATE}" > "${TREE}"

    # Convert .tree -> .smv with timing.
    # Must run from _HERE so onnxruntime resolves ./networks/ relative to CWD.
    # behaverify nuxmv --generate writes to <outdir>/nuxmv/<name>.smv.
    { time ( cd "${_HERE}" && "${PYTHON}" -m behaverify nuxmv \
        "${TREE}" "${OUT}/smv" \
        --generate \
        --no_checks \
        --recursion_limit 10000 \
        --overwrite ) ; } 2> "${TIMING}"
    mv "${OUT}/smv/nuxmv/table_${NAME}.smv" "${SMV}"
done

# ---------------------------------------------------------------------------
# Stage 3: Run nuXmv (INVAR + CTL)
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "[3/3] Running nuXmv (INVAR + CTL)"
echo "========================================"

for NAME in "${NETWORKS[@]}"; do
    SMV="$(realpath "${OUT}/smv/table_${NAME}.smv")"
    OUTFILE="${OUT}/table_${NAME}_invar_ctl.txt"
    echo "  ${NAME}"
    { time "${NUXMV}" -source "${NUXMV_CMD}" "${SMV}" ; } > "${OUTFILE}" 2>&1
done

echo ""
echo "All done. Results in ${OUT}/"
