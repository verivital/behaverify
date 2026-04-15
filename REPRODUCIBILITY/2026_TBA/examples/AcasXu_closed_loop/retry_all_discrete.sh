#!/usr/bin/env bash
# Retry TIMEOUT contracts from all 5 discrete NN results via PGD.
# Uses temp YAML configs per NN since the parallel script reads network_idx/output_path from YAML.

set -euo pipefail

declare -A NN_MAP=(
    [1]="aprev_clear"
    [2]="aprev_weak_right"
    [3]="aprev_weak_left"
    [4]="aprev_strong_right"
    [5]="aprev_strong_left"
)

BASE_CFG="verify_acas_contracts_config.yaml"
OUT_DIR="contracts/discrete_goals"

for IDX in 1 2 3 4 5; do
    NAME="${NN_MAP[$IDX]}"
    OUTPUT="${OUT_DIR}/${NAME}_crown_results.json"
    TMP_CFG="verify_acas_contracts_config_nn${IDX}.yaml"

    echo "========================================"
    echo "Retry NN ${IDX}: ${NAME}"
    echo "========================================"

    # Create per-NN YAML by overriding network_idx and output_path
    python3 -c "
import yaml
with open('${BASE_CFG}') as f: c = yaml.safe_load(f)
c['network_idx'] = ${IDX}
c['output_path'] = '${OUTPUT}'
with open('${TMP_CFG}', 'w') as f: yaml.dump(c, f)
"

    python3 verify_acas_contracts_parallel.py \
        --config      "${TMP_CFG}" \
        --retry-from  "${OUTPUT}" \
        --timeout     3600 \
        --discrete \
        --discrete-timeout 60 \
        --device      cuda \
        --workers     8

    rm -f "${TMP_CFG}"
    echo ""
done

echo "All NN retries complete."
