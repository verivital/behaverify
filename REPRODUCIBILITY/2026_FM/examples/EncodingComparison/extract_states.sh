#!/bin/bash
cd /home/BehaVerify_2026_FM/behaverify/REPRODUCIBILITY/2026_FM/examples/EncodingComparison

rm -f States-Fastforwarding-Concise States-Naive-Concise

for i in 1 2 3 4 5 6 7 8 9 10; do
  val=$(grep reachable results/STATES_FF_binary_tree_$i.txt 2>/dev/null | sed 's/.*states: //' | sed 's/ .*//')
  if [ -n "$val" ]; then
    echo "$val" >> States-Fastforwarding-Concise
  else
    echo "TIMEOUT" >> States-Fastforwarding-Concise
  fi

  val=$(grep reachable results/STATES_NAIVE_binary_tree_$i.txt 2>/dev/null | sed 's/.*states: //' | sed 's/ .*//')
  if [ -n "$val" ]; then
    echo "$val" >> States-Naive-Concise
  else
    echo "TIMEOUT" >> States-Naive-Concise
  fi
done

echo "Fastforwarding states:"
cat States-Fastforwarding-Concise
echo ""
echo "Naive states:"
cat States-Naive-Concise
