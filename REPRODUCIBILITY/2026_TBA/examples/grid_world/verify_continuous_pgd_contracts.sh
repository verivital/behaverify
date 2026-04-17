#!/usr/bin/env bash
# verify_continuous_pgd_contracts.sh
#
# Verify A/G contracts for all grid-world NNs (five 100%-accurate and two
# near-accurate: 99.6% and 99.5%) using alpha-beta-CROWN with PGD attack
# enabled (pgd_order=before, 50 restarts) and a 60s BaB timeout.
#
# Results are saved to contracts/continuous_goals/enabled_pgd/<name>_pgd60.json so original
# BaB-only results in contracts/continuous_goals/disabled_pgd/ are preserved for comparison.
#
# Run from:  REPRODUCIBILITY/2026_TBA/examples/grid_world/

set -euo pipefail

NETWORKS=(
    "1000__6_18_0__0100_1"
    "1000__6_18_0__0150_1"
    "1000__6_18_0__0200_1"
    "1000__6_18_0__0250_1"
    "1000__6_18_0__0300_1"
    "0996__6_18_0__200_1"
    "0995__6_18_0__200_1"
)

for NAME in "${NETWORKS[@]}"; do
    echo "========================================"
    echo "Verifying ${NAME}"
    echo "========================================"
    python3 verify_grid_world_contracts.py \
        --onnx   "./networks/${NAME}.onnx" \
        --output "./contracts/continuous_goals/enabled_pgd/${NAME}_pgd60.json"
    echo ""
done

echo "All done. Results in contracts/continuous_goals/enabled_pgd/*_pgd60.json"
