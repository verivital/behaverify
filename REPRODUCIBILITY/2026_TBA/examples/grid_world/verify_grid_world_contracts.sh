#!/usr/bin/env bash
# verify_grid_world_contracts.sh
#
# Unified A/G contract verification script for all grid-world NNs.
# Replaces verify_continuous_pgd_contracts.sh, verify_continuous_bab_contracts.sh,
# and verify_discrete_contracts.sh.
#
# Flags:
#   --neuro <verifier>   NN verifier name used as the contracts/ subfolder
#                        (default: crown). Abstracts over future verifiers (nnv, etc.).
#   --mode  <mode>       Verification mode (default: continuous-pgd):
#                          continuous-pgd   PGD-enabled BaB (recommended)
#                          continuous-bab   BaB-only, no PGD (baseline comparison)
#                          discrete         Integer goal points only (replicates 2025_NEUS)
#
# Output paths  (N = timeout_sec from grid_world_domain_config.yaml, default 60):
#   continuous-pgd  : contracts/<neuro>/continuous_goals/enabled_pgd/<name>_pgdN.json
#   continuous-bab  : contracts/<neuro>/continuous_goals/disabled_pgd/<name>.json
#   discrete        : contracts/<neuro>/discrete_goals/<name>_discrete.json
#
# Run from:  REPRODUCIBILITY/2026_TBA/examples/grid_world/

set -euo pipefail

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
NEURO="crown"
MODE="continuous-pgd"

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --neuro) NEURO="$2"; shift 2 ;;
        --mode)  MODE="$2";  shift 2 ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done

# ---------------------------------------------------------------------------
# Read timeout from domain config (used in continuous-pgd filename suffix)
# ---------------------------------------------------------------------------
TIMEOUT=$(python3 -c "import yaml; print(yaml.safe_load(open('grid_world_domain_config.yaml'))['verification']['timeout_sec'])")

# ---------------------------------------------------------------------------
# Mode → verifier flags, output subfolder, filename suffix, label
# ---------------------------------------------------------------------------
case "${MODE}" in
    continuous-pgd)
        VERIFY_FLAGS=()
        GOALS_DIR="continuous_goals/enabled_pgd"
        SUFFIX="_pgd${TIMEOUT}"
        MODE_LABEL="continuous, PGD-enabled (timeout=${TIMEOUT}s)"
        ;;
    continuous-bab)
        VERIFY_FLAGS=("--no-pgd")
        GOALS_DIR="continuous_goals/disabled_pgd"
        SUFFIX=""
        MODE_LABEL="continuous, BaB-only (no PGD)"
        ;;
    discrete)
        VERIFY_FLAGS=("--discrete")
        GOALS_DIR="discrete_goals"
        SUFFIX="_discrete"
        MODE_LABEL="discrete (integer goal points)"
        ;;
    *)
        echo "Unknown --mode '${MODE}'. Choose: continuous-pgd, continuous-bab, discrete." >&2
        exit 1
        ;;
esac

OUT_DIR="contracts/${NEURO}/${GOALS_DIR}"
mkdir -p "${OUT_DIR}"

# ---------------------------------------------------------------------------
# Networks
# ---------------------------------------------------------------------------
NETWORKS=(
    "1000__6_18_0__0100_1"
    "1000__6_18_0__0150_1"
    "1000__6_18_0__0200_1"
    "1000__6_18_0__0250_1"
    "1000__6_18_0__0300_1"
    "0996__6_18_0__200_1"
    "0995__6_18_0__200_1"
)

echo "Mode   : ${MODE_LABEL}"
echo "Neuro  : ${NEURO}"
echo "Output : ${OUT_DIR}/"
echo ""

for NAME in "${NETWORKS[@]}"; do
    echo "========================================"
    echo "Verifying ${NAME}  [${MODE_LABEL}]"
    echo "========================================"
    python3 verify_grid_world_contracts.py \
        "${VERIFY_FLAGS[@]}" \
        --onnx   "./networks/${NAME}.onnx" \
        --output "${OUT_DIR}/${NAME}${SUFFIX}.json"
    echo ""
done

echo "All done. Results in ${OUT_DIR}/*"
