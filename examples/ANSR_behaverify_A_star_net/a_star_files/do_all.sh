#!/bin/bash

smv_prefix="ANSRt"
for obstacle_file_name in ignore/obstacles*; do
    echo $obstacle_file_name
    python3 fill_holes.py "${obstacle_file_name}"
done
echo "done with filling--------"
for obstacle_file_name in ignore/obstaclesFilled*; do
    echo $obstacle_file_name 
    base_file_name="${obstacle_file_name%.txt}"
    numbers="${base_file_name#ignore/obstacles}"
    echo "${numbers}"
    python3 assemble_tree_existing_obs.py "${obstacle_file_name}"
    python3 table_to_training.py "ignore/table${numbers}.txt"
    python3 obstacle_to_training.py "${obstacle_file_name}"
    python3 ../draw_obstacles.py "${obstacle_file_name}"
    python3 /home/serene/git_repos/behaverify/src/dsl_to_nuxmv.py /home/serene/git_repos/behaverify/metamodel/behaverify.tx "ignore/${smv_prefix}${numbers}.tree" "ignore/${smv_prefix}${numbers}.smv" --recursion_limit 5000
done
