#!/bin/bash

meta_dim=2
max_size=0
iterations=$1

for (( i==1; i<iterations; i++ )); do
    echo "generating obstacles"
    echo "${meta_dim}"
    python3 ./extra_files/generate_obstacles.py "${meta_dim}"
    max_val=$((meta_dim * 5 - 1))
    num_obs=$((8 * meta_dim * meta_dim))
    echo "filling holes"
    python3 ./extra_files/fill_holes.py "./extra_files/ignore/obstacles_${max_val}_${num_obs}_${max_size}.txt"
    echo "computing new sizes"
    file=$(ls "./extra_files/ignore" | grep "obstaclesFilled_${max_val}_[^_]*_[^.]*.txt")
    filename=$(basename $file)
    tail_end_with_ext=${filename#obstaclesFilled_}
    tail_end=${tail_end_with_ext%.txt}
    echo "----------------------------"
    echo $file
    echo $filename
    echo $tail_end_with_ext
    echo $tail_end
    echo "assembling tree"
    python3 ./extra_files/assemble_tree_existing_obs.py "./extra_files/ignore/obstaclesFilled_${tail_end}.txt"
    echo "setting up directory"
    mkdir "./dense_fixed/${tail_end}/"
    echo "moving .tree"
    mv "./extra_files/ignore/ANSRtFilled_${tail_end}.tree" "./dense_fixed/${tail_end}/ANSRtFilled_${tail_end}.tree"
    mv "./extra_files/ignore/obstaclesFilled_${tail_end}.txt" "./dense_fixed/${tail_end}/obstaclesFilled_${tail_end}.txt"
    meta_dim=$((meta_dim + 1))
done


