#!/usr/bin/env bash
# verify_all_continuous_contracts.sh
#
# Run CROWN verification for all 5 ACAS Xu NNs using continuous contracts
# (eps=1e-4, PGD-enabled). Outputs one results JSON per NN.
#
# Usage (from REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop/):
#   ./verify_all_continuous_contracts.sh
#   ./verify_all_continuous_contracts.sh --timeout 60   # pass extra args to verifier
#
# Results go to: contracts/continuous_goals/enabled_pgd/aprev_*_crown_results.json
# Run time estimate: ~2h per NN at 30s timeout (490 contracts each)

set -euo pipefail

EXTRA_ARGS=("$@")   # forward any extra args (e.g. --timeout 60) to each run

declare -A NN_MAP=(
    [1]="aprev_clear"
    [2]="aprev_weak_right"
    [3]="aprev_weak_left"
    [4]="aprev_strong_right"
    [5]="aprev_strong_left"
)

OUT_DIR="contracts/continuous_goals/enabled_pgd"

for IDX in 1 2 3 4 5; do
    NAME="${NN_MAP[$IDX]}"
    OUTPUT="${OUT_DIR}/${NAME}_crown_results.json"

    echo "========================================"
    echo "NN ${IDX}: ${NAME}"
    echo "Output : ${OUTPUT}"
    echo "========================================"

    python3 verify_acas_contracts.py \
        --network-idx "${IDX}" \
        --output      "${OUTPUT}" \
        "${EXTRA_ARGS[@]}"
    echo ""
done

echo "All 5 NNs verified. Results in ${OUT_DIR}/"
