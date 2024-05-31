#!/bin/bash


max_val=9
num_obs=2
max_size=1
mkdir './sparse_random'
for (( i==1; i<9; i++ )); do
    echo "generating obstacles"
    python3 ../a_star_files/generate_obstacles.py "${num_obs}" 0 "${max_val}" "${max_size}"
    echo "filling holes"
    python3 ../a_star_files/fill_holes.py "../a_star_files/ignore/obstacles_${max_val}_${num_obs}_${max_size}.txt"
    echo "computing new sizes"
    file=$(ls "../a_star_files/ignore" | grep "obstaclesFilled_${max_val}_[^_]*_[^.]*.txt")
    filename=$(basename $file)
    tail_end_with_ext=${filename#obstaclesFilled_}
    tail_end=${tail_end_with_ext%.txt}
    echo "----------------------------"
    echo $file
    echo $filename
    echo $tail_end_with_ext
    echo $tail_end
    echo "assembling tree"
    python3 ../a_star_files/assemble_tree_existing_obs.py "../a_star_files/ignore/obstaclesFilled_${tail_end}.txt"
    echo "setting up directory"
    mkdir "./sparse_random/${tail_end}/"
    echo "moving .tree"
    mv "../a_star_files/ignore/ANSRtFilled_${tail_end}.tree" "./sparse_random/${tail_end}/ANSRtFilled_${tail_end}.tree"
    mv "../a_star_files/ignore/obstaclesFilled_${tail_end}.txt" "./sparse_random/${tail_end}/obstaclesFilled_${tail_end}.txt"
    max_val=$((max_val + 5))
    num_obs=$((num_obs + 1))
    max_size=$((max_size + 1))
done


