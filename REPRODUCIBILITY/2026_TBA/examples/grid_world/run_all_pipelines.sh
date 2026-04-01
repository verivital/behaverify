#!/usr/bin/env bash
# run_all_pipelines.sh
#
# Run the compositional pipeline for every contract JSON in a given folder,
# using pre-computed contracts (--skip-contracts).
#
# Usage (from REPRODUCIBILITY/2026_TBA/examples/grid_world/):
#
#   ./run_all_pipelines.sh                            # defaults to contracts/enabled_pgd/
#   ./run_all_pipelines.sh contracts/disabled_pgd/
#   ./run_all_pipelines.sh contracts/enabled_pgd/
#
# Outputs go to:
#   results/compositional/<folder_basename>/<network_stem>/pipeline_report.json

set -euo pipefail

CONTRACTS_DIR="${1:-contracts/enabled_pgd}"
FOLDER_NAME="$(basename "${CONTRACTS_DIR}")"

echo "Contracts folder : ${CONTRACTS_DIR}"
echo "Output subfolder : results/compositional/${FOLDER_NAME}/"
echo ""

for CONTRACT_JSON in "${CONTRACTS_DIR}"/*.json; do
    STEM="$(basename "${CONTRACT_JSON}" .json)"
    ONNX=$(python3 -c "import json; print(json.load(open('${CONTRACT_JSON}'))['onnx_path'])")
    OUTPUT="results/compositional/${FOLDER_NAME}/${STEM}"

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

echo "All done. Reports in results/compositional/${FOLDER_NAME}/"
