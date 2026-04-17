#!/usr/bin/env bash
#
# verify_all_discrete_contracts.sh
#
# Run discrete CROWN verification for all 5 ACAS Xu NNs.
# Each dangerous (x_mag, y_mag) state is verified individually via one CROWN
# call with lower=upper=exact NN inputs (EPS=0). Contracts short-circuit on
# the first UNSAT found. Bridges to the 2025_NEUS table approach.
#
# Usage (from REPRODUCIBILITY/2026_TBA/examples/AcasXu_closed_loop/):
#   ./verify_all_discrete_contracts.sh
#   ./verify_all_discrete_contracts.sh --discrete-timeout 10   # override per-state timeout
#
# Results go to: contracts/crown/discrete_goals/aprev_*_crown_results.json

set -euo pipefail

EXTRA_ARGS=("$@")   # forward any extra args (e.g. --discrete-timeout 10) to each run

declare -A NN_MAP=(
    [1]="aprev_clear"
    [2]="aprev_weak_right"
    [3]="aprev_weak_left"
    [4]="aprev_strong_right"
    [5]="aprev_strong_left"
)

OUT_DIR="contracts/crown/discrete_goals"

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
        --discrete \
        "${EXTRA_ARGS[@]}"
    echo ""
done

echo "All 5 NNs verified (discrete). Results in ${OUT_DIR}/"
