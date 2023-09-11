#!/bin/bash

if test -e ./bigger_fish_expanded/results; then 
    rm -r ./bigger_fish_expanded/results
fi
if test -e ./bigger_fish_expanded/smv; then 
    rm -r ./bigger_fish_expanded/smv
fi
if test -e ./bigger_fish_expanded/tree; then 
    rm -r ./bigger_fish_expanded/tree
fi
if test -e ./bigger_fish_expanded/processed_data; then 
    rm -r ./bigger_fish_expanded/processed_data
fi


if test -e ./blueROV_mod/results; then 
    rm -r ./blueROV_mod/results
fi
if test -e ./blueROV_mod/smv; then 
    rm -r ./blueROV_mod/smv
fi
if test -e ./blueROV_mod/tree; then 
    rm -r ./blueROV_mod/tree
fi
if test -e ./blueROV_mod/processed_data; then 
    rm -r ./blueROV_mod/processed_data
fi


if test -e ./light_controller_v3/results; then 
    rm -r ./light_controller_v3/results
fi
if test -e ./light_controller_v3/smv; then 
    rm -r ./light_controller_v3/smv
fi
if test -e ./light_controller_v3/tree; then 
    rm -r ./light_controller_v3/tree
fi
if test -e ./light_controller_v3/processed_data; then 
    rm -r ./light_controller_v3/processed_data
fi


if test -e ./differential_testing/array/results; then 
    rm -r ./differential_testing/array/results
fi
if test -e ./differential_testing/array/gen_files; then 
    rm -r ./differential_testing/array/gen_files
fi

if test -e ./differential_testing/integer_array/results; then 
    rm -r ./differential_testing/integer_array/results
fi
if test -e ./differential_testing/integer_array/gen_files; then 
    rm -r ./differential_testing/integer_array/gen_files
fi

if test -e ./differential_testing/moved; then 
    rm -r ./differential_testing/moved
fi


if test -e ./simple_robot/results; then 
    rm -r ./simple_robot/results
fi
if test -e ./simple_robot/smv; then 
    rm -r ./simple_robot/smv
fi
if test -e ./simple_robot/tree; then 
    rm -r ./simple_robot/tree
fi
if test -e ./simple_robot/processed_data; then 
    rm -r ./simple_robot/processed_data
fi


if test -e ./simplified_robot/results; then 
    rm -r ./simplified_robot/results
fi
if test -e ./simplified_robot/smv; then 
    rm -r ./simplified_robot/smv
fi
if test -e ./simplified_robot/tree; then 
    rm -r ./simplified_robot/tree
fi
if test -e ./simplified_robot/processed_data; then 
    rm -r ./simplified_robot/processed_data
fi
