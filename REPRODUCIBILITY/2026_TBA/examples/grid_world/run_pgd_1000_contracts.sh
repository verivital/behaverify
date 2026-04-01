#!/usr/bin/env bash
# run_pgd_1000_contracts.sh
#
# Verify A/G contracts for all five 100%-accurate grid-world NNs using
# alpha-beta-CROWN with PGD attack enabled (pgd_order=before, 50 restarts)
# and a 60s BaB timeout.
#
# Results are saved to contracts/<name>_pgd60.json so original BaB-only
# results are preserved for comparison.
#
# Run from:  REPRODUCIBILITY/2026_TBA/examples/grid_world/

set -euo pipefail

NETWORKS=(
    "1000__6_18_0__0100_1"
    "1000__6_18_0__0150_1"
    "1000__6_18_0__0200_1"
    "1000__6_18_0__0250_1"
    "1000__6_18_0__0300_1"
)

for NAME in "${NETWORKS[@]}"; do
    echo "========================================"
    echo "Verifying ${NAME}"
    echo "========================================"
    python3 verify_contracts.py \
        --onnx   "./networks/${NAME}.onnx" \
        --output "./contracts/${NAME}_pgd60.json"
    echo ""
done

echo "All done. Results in contracts/*_pgd60.json"
