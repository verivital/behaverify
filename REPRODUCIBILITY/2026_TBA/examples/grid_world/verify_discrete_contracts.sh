#!/usr/bin/env bash
# verify_discrete_contracts.sh
#
# Verify A/G contracts for all grid-world NNs (five 100%-accurate and two
# near-accurate: 99.6% and 99.5%) using alpha-beta-CROWN in DISCRETE mode
# (49 integer goal points per contract).
#
# Each contract is checked against every integer goal in {0,...,6}^2 rather
# than the full continuous range [0,6]^2. If all 38 contracts are SAT, the NN
# is safe for every integer goal -- consistent with the 2025_NEUS table approach.
#
# Both drone EPS and goal EPS are set to 0 (exact integer points), matching
# the 2025_NEUS table approach. CROWN may hit numerical issues in BaB
# (cut_ops.py divides by (upper-lower) without a zero-guard); if it crashes,
# fall back to EPS=1e-5.
#
# Results are saved to contracts/discrete_goals/<name>_discrete.json
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
    echo "Verifying ${NAME}  [discrete mode]"
    echo "========================================"
    python3 verify_grid_world_contracts.py \
        --discrete \
        --onnx   "./networks/${NAME}.onnx" \
        --output "./contracts/discrete_goals/${NAME}_discrete.json"
    echo ""
done

echo "All done. Results in contracts/discrete_goals/*"
