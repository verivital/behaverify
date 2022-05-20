#!/bin/bash

files=("example1" "example2" "example3" "example4" "example5" "example6" "example7" "example8")


for cur_file in ${files[@]}; do
    python3 behaverify_selector.py $cur_file create_root --root_args True --output_file ../models_selector_mixed/$cur_file.smv --selector_mode 0 --overwrite

    python3 behaverify_selector.py $cur_file create_root --output_file ../models_selector_parallel/$cur_file.smv --selector_mode 1 --overwrite

    python3 behaverify_selector.py $cur_file create_root --output_file ../models_selector_non_parallel/$cur_file.smv --selector_mode 2 --overwrite

    python3 behaverify_selector2.py $cur_file create_root --output_file ../models_selector_mixed2/$cur_file.smv --selector_mode 0 --overwrite

    python3 behaverify_selector2.py $cur_file create_root --output_file ../models_selector_parallel2/$cur_file.smv --selector_mode 1 --overwrite

    python3 behaverify_selector2.py $cur_file create_root --output_file ../models_selector_non_parallel2/$cur_file.smv --selector_mode 2 --overwrite

    python3 behaverify_sequence.py $cur_file create_root --output_file ../models_sequence/$cur_file.smv --overwrite

    python3 behaverify_sequence2.py $cur_file create_root --output_file ../models_sequence2/$cur_file.smv --overwrite

    python3 behaverify_ultimate.py $cur_file create_root --output_file ../models_ultimate/$cur_file.smv --overwrite
done

