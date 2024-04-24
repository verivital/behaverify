#!/bin/bash

if test -e ./ANSR_no_net/results; then 
    rm -r ./ANSR_no_net/results
fi
if test -e ./ANSR_no_net/smv; then 
    rm -r ./ANSR_no_net/smv
fi
if test -e ./ANSR_no_net/tree; then 
    rm -r ./ANSR_no_net/tree
fi
if test -e ./ANSR_no_net/processed_data; then 
    rm -r ./ANSR_no_net/processed_data
fi


if test -e ./bigger_fish_selector/results; then 
    rm -r ./bigger_fish_selector/results
fi
if test -e ./bigger_fish_selector/smv; then 
    rm -r ./bigger_fish_selector/smv
fi
if test -e ./bigger_fish_selector/tree; then 
    rm -r ./bigger_fish_selector/tree
fi
if test -e ./bigger_fish_selector/processed_data; then 
    rm -r ./bigger_fish_selector/processed_data
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
