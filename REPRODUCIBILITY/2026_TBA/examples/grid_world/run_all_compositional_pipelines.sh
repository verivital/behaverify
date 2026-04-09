#!/usr/bin/env bash
# run_all_compositional_pipelines.sh
#
# Run the compositional pipeline for every contract JSON in a given folder,
# using pre-computed contracts (--skip-contracts).
#
# Usage (from REPRODUCIBILITY/2026_TBA/examples/grid_world/):
#
#   ./run_all_compositional_pipelines.sh                                         # defaults to continuous_goals/enabled_pgd
#   ./run_all_compositional_pipelines.sh contracts/continuous_goals/disabled_pgd/
#   ./run_all_compositional_pipelines.sh contracts/continuous_goals/enabled_pgd/
#   ./run_all_compositional_pipelines.sh contracts/discrete_goals/
#
# Outputs go to:
#   results/compositional/<relative-path-under-contracts>/<network_stem>/pipeline_report.json
#
# The output path mirrors the contracts/ structure under results/compositional/:
#   contracts/continuous_goals/enabled_pgd/ -> results/compositional/continuous_goals/enabled_pgd/
#   contracts/discrete_goals/              -> results/compositional/discrete_goals/

set -euo pipefail

CONTRACTS_DIR="${1:-contracts/continuous_goals/enabled_pgd}"

# Strip leading "contracts/" to get the relative subfolder, then mirror under results/compositional/
RELATIVE="${CONTRACTS_DIR#contracts/}"
RELATIVE="${RELATIVE%/}"  # strip trailing slash if present
OUTPUT_BASE="results/compositional/${RELATIVE}"

echo "Contracts folder : ${CONTRACTS_DIR}"
echo "Output base      : ${OUTPUT_BASE}/"
echo ""

for CONTRACT_JSON in "${CONTRACTS_DIR}"/*.json; do
    STEM="$(basename "${CONTRACT_JSON}" .json)"
    ONNX=$(python3 -c "import json; print(json.load(open('${CONTRACT_JSON}'))['onnx_path'])")
    OUTPUT="${OUTPUT_BASE}/${STEM}"

    echo "========================================"
    echo "Network : ${STEM}"
    echo "ONNX    : ${ONNX}"
    echo "Output  : ${OUTPUT}"
    echo "========================================"

    python3 run_compositional_pipeline.py \
        --onnx       "${ONNX}" \
        --contracts  "${CONTRACT_JSON}" \
        --output     "${OUTPUT}" \
        --skip-contracts
    echo ""
done

echo "All done. Reports in ${OUTPUT_BASE}/"
