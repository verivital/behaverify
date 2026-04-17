#!/usr/bin/env bash
# verify_continuous_bab_contracts.sh
#
# Verify A/G contracts for all grid-world NNs (five 100%-accurate and two
# near-accurate: 99.6% and 99.5%) using alpha-beta-CROWN with PGD attack
# DISABLED (BaB only, timeout=60s).
#
# This is the baseline comparison for verify_continuous_pgd_contracts.sh.
# Both use timeout_sec=60; the only variable is PGD enabled/disabled.
#
# Results are saved to contracts/continuous_goals/disabled_pgd/<name>.json
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
    echo "Verifying ${NAME}  [BaB only, no PGD]"
    echo "========================================"
    python3 verify_grid_world_contracts.py \
        --no-pgd \
        --onnx   "./networks/${NAME}.onnx" \
        --output "./contracts/continuous_goals/disabled_pgd/${NAME}.json"
    echo ""
done

echo "All done. Results in contracts/continuous_goals/disabled_pgd/*"
