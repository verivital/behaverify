#!/usr/bin/env bash
# Single-script entry point that runs the entire BehaVerify vs BT2Fiacre vs
# BT2BIP comparison pipeline and prints the Table 2, Table 3 and Section 4.3
# results in one go.
#
# All intermediates land in $OUT (default /out) so they survive a `docker
# cp` or volume mount. The final formatted tables go to both stdout and
# $OUT/results.txt.

set -euo pipefail

OUT="${OUT_DIR:-/out}"
mkdir -p "${OUT}"

echo "[run_all] Output dir: ${OUT}"
echo "[run_all] Started at $(date -u)"
echo

bash /home/bv/run_table2.sh    "${OUT}"
echo

bash /home/bv/run_table3.sh    "${OUT}"
echo

bash /home/bv/run_section43.sh "${OUT}"
echo

python3 /home/bv/format_results.py "${OUT}"
echo
echo "[run_all] Done. Tables in ${OUT}/results.txt"
