#!/bin/bash

path_name=$1
file_name=$2
use_haskell=$3  # 0 means no, 1 means yes
use_nuxmv=$4


if ! test -d "${path_name}/gen_files"; then
    if test -e "${path_name}/gen_files"; then
	rm -r "${path_name}/gen_files"
    fi
    mkdir "${path_name}/gen_files"
fi
if test -e "${path_name}/gen_files/${file_name}"; then
    rm -r "${path_name}/gen_files/${file_name}"
fi
mkdir "${path_name}/gen_files/${file_name}"


if [[ $use_haskell == 1 ]]; then
    cur_loc=$(pwd)
    cd "${path_name}/gen_files/${file_name}"
    #cabal init --non-interactive
    mkdir ./app
    cd $cur_loc
    ./fix_haskell.sh "${path_name}/gen_files/${file_name}" $file_name
    python3 ../../src/dsl_to_haskell.py ../../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree $path_name/gen_files/$file_name/ $file_name --max_iter 10
fi


if [[ $use_nuxmv == 1 ]]; then
    python3 ../../src/dsl_to_behaverify.py ../../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree --output_file $path_name/gen_files/$file_name/$file_name.smv --do_not_trim --keep_last_stage
    python3 ../../src/dsl_to_behaverify.py ../../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree --output_file $path_name/gen_files/$file_name/OPT_$file_name.smv
elif [[ $use_nuxmv == 2 ]]; then
    python3 ../../src/dsl_to_behaverify_old_index.py ../../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree --output_file $path_name/gen_files/$file_name/$file_name.smv --do_not_trim --keep_last_stage
    python3 ../../src/dsl_to_behaverify_old_index.py ../../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree --output_file $path_name/gen_files/$file_name/OPT_$file_name.smv
fi
python3 ../../src/dsl_to_pytree.py ../../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree $path_name/gen_files/$file_name/ $file_name --max_iter 10 --serene_print

