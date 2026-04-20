#!/usr/bin/env bash
# run_all_compositional_pipelines.sh
#
# Run the compositional pipeline for every contract JSON in a given folder,
# using pre-computed contracts (--skip-contracts).
#
# Usage (from REPRODUCIBILITY/2026_TBA/examples/grid_world/):
#
#   ./run_all_compositional_pipelines.sh                                              # defaults
#   ./run_all_compositional_pipelines.sh contracts/crown/continuous_goals/disabled_pgd/
#   ./run_all_compositional_pipelines.sh contracts/crown/continuous_goals/enabled_pgd/ --symbolic uclid5
#   ./run_all_compositional_pipelines.sh contracts/crown/discrete_goals/ --symbolic nuXmv
#
# Flags:
#   <contracts_dir>      (positional, default: contracts/crown/continuous_goals/enabled_pgd)
#   --symbolic <checker> Symbolic checker to use: nuXmv | uclid5 (default: nuXmv)
#   --bmc-steps <N>      BMC depth for uclid5 (default: 50; ignored for nuXmv)
#
# Outputs go to:
#   results/compositional/<goals_dir>/<neuro>_<symbolic>/<network_stem>/
#
# Examples (contracts/crown/continuous_goals/enabled_pgd/ with defaults):
#   --symbolic nuXmv  -> results/compositional/continuous_goals/enabled_pgd/crown_nuXmv/<stem>/
#   --symbolic uclid5 -> results/compositional/continuous_goals/enabled_pgd/crown_uclid5/<stem>/

set -euo pipefail

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
CONTRACTS_DIR=""
SYMBOLIC="nuXmv"
BMC_STEPS=50

while [[ $# -gt 0 ]]; do
    case "$1" in
        --symbolic)  SYMBOLIC="$2";  shift 2 ;;
        --bmc-steps) BMC_STEPS="$2"; shift 2 ;;
        --*) echo "Unknown flag: $1" >&2; exit 1 ;;
        *)   CONTRACTS_DIR="$1"; shift ;;
    esac
done

CONTRACTS_DIR="${CONTRACTS_DIR:-contracts/crown/continuous_goals/enabled_pgd}"
CONTRACTS_DIR="${CONTRACTS_DIR%/}"  # strip trailing slash if present

# Validate --symbolic
if [[ "${SYMBOLIC}" != "nuXmv" && "${SYMBOLIC}" != "uclid5" ]]; then
    echo "Unknown --symbolic '${SYMBOLIC}'. Choose: nuXmv, uclid5." >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Derived paths
# ---------------------------------------------------------------------------
# Extract <neuro> and <goals_dir> from contracts/<neuro>/<goals_dir>/
_TMP="${CONTRACTS_DIR#contracts/}"
NEURO="${_TMP%%/*}"          # e.g. "crown"
RELATIVE="${_TMP#${NEURO}/}" # e.g. "continuous_goals/enabled_pgd"
RELATIVE="${RELATIVE%/}"     # strip trailing slash if present

# Both checkers land under results/compositional/; distinguished by <neuro>_<symbolic>
OUTPUT_BASE="results/compositional/${RELATIVE}/${NEURO}_${SYMBOLIC}"

echo "Contracts folder : ${CONTRACTS_DIR}"
echo "Neuro verifier   : ${NEURO}"
echo "Symbolic checker : ${SYMBOLIC}"
echo "Output base      : ${OUTPUT_BASE}/"
echo ""

# ---------------------------------------------------------------------------
# Read config paths (needed for uclid5 tree/model generation)
# ---------------------------------------------------------------------------
if [[ "${SYMBOLIC}" == "uclid5" ]]; then
    METAMODEL=$(python3 -c "
import yaml
d = yaml.safe_load(open('pipeline_filepaths_config.yaml'))
print(d['paths']['metamodel'])
")
    COUNTER_TEMPLATE=$(python3 -c "
import yaml
d = yaml.safe_load(open('pipeline_filepaths_config.yaml'))
print(d['paths']['counter_template'])
")
    NEURAL_VAR=$(python3 -c "
import yaml
d = yaml.safe_load(open('pipeline_filepaths_config.yaml'))
print(d['smv']['neural_var'])
")
    POS_X=$(python3 -c "
import yaml
d = yaml.safe_load(open('pipeline_filepaths_config.yaml'))
print(d['smv']['pos_x'])
")
    POS_Y=$(python3 -c "
import yaml
d = yaml.safe_load(open('pipeline_filepaths_config.yaml'))
print(d['smv']['pos_y'])
")
    DOMAIN=$(python3 -c "
import yaml
d = yaml.safe_load(open('pipeline_filepaths_config.yaml'))
print(' '.join(d['smv']['domain']))
")
fi

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
for CONTRACT_JSON in "${CONTRACTS_DIR}"/*.json; do
    STEM="$(basename "${CONTRACT_JSON}" .json)"
    ONNX=$(python3 -c "import json; print(json.load(open('${CONTRACT_JSON}'))['onnx_path'])")
    OUTPUT="${OUTPUT_BASE}/${STEM}"
    mkdir -p "${OUTPUT}"

    echo "========================================"
    echo "Network  : ${STEM}"
    echo "ONNX     : ${ONNX}"
    echo "Symbolic : ${SYMBOLIC}"
    echo "Output   : ${OUTPUT}"
    echo "========================================"

    if [[ "${SYMBOLIC}" == "nuXmv" ]]; then
        python3 run_compositional_pipeline.py \
            --onnx       "${ONNX}" \
            --contracts  "${CONTRACT_JSON}" \
            --output     "${OUTPUT}" \
            --skip-contracts

    elif [[ "${SYMBOLIC}" == "uclid5" ]]; then
        # Generate a network-specific .tree by substituting the ONNX path
        TREE_PATH="${OUTPUT}/${STEM}.tree"
        ONNX_REL=$(python3 -c "import os; print(os.path.relpath('${ONNX}', '${OUTPUT}'))")
        sed "s|REPLACE_SOURCE|${ONNX_REL}|g" "${COUNTER_TEMPLATE}" > "${TREE_PATH}"

        # Generate the UCLID5 model
        UCL_PATH="${OUTPUT}/${STEM}_contracts.ucl"
        # shellcheck disable=SC2086
        python3 ../../src/dsl_with_contracts_to_uclid5.py \
            --metamodel        "${METAMODEL}" \
            --tree             "${TREE_PATH}" \
            --contracts        "${CONTRACT_JSON}" \
            --output           "${UCL_PATH}" \
            --neural-var       "${NEURAL_VAR}" \
            --pos-x            "${POS_X}" \
            --pos-y            "${POS_Y}" \
            --domain           ${DOMAIN} \
            --bmc-steps        "${BMC_STEPS}" \
            --skip-grammar-check

        # Run uclid5 and save uclid5_output.txt + pipeline_report.json
        if command -v uclid &>/dev/null; then
            python3 ../../pipeline/symbolic/uclid5/run_uclid5_verification.py \
                --ucl     "${UCL_PATH}" \
                --out-dir "${OUTPUT}" \
                --bin     uclid
        else
            echo "  uclid binary not found in PATH — .ucl model generated at ${UCL_PATH}"
            echo "  Build UCLID5 (sbt assembly in the uclid/ repo) then run: uclid ${UCL_PATH}"
        fi
    fi

    echo ""
done

echo "All done. Reports in ${OUTPUT_BASE}/"
