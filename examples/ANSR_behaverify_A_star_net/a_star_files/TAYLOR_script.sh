#!/bin/bash
set -euo pipefail
# Overnight fixes (2026-07-02): fail fast on any stage error (previously a
# mid-pipeline crash still ran every later stage and could exit 0), validate
# the argument count (previously a 5/6-arg invocation silently produced
# garbage), and actually honor the fill_holes flag (previously declared but
# ignored -- holes were always filled).

if [ "$#" -ne 7 ]; then
    echo "usage: $0 <python> <obs.npz> <block_size> <fly_at> <x_len> <y_len> <fill_holes 0|1>" >&2
    echo "example: $0 ~/taylor_venv/bin/python3 ./city_1000_1000.npz 40 80 1000 1000 1" >&2
    exit 1
fi

my_python=$1 # this should point to whatever python is.
obs_file=$2 # points to your obstacle map (city_1000_1000.npz, probably)
block_size=$3 # how big each block should be. Bigger number means fewer grids. E.g., if I have 1000 x 1000, and block size is 50, will have a 20x20 map. If block size is 4, will have 250 x 250 map
fly_at=$4 # height to fly at. If height is say, 12, then we can ignore any obstacles that are 11 or shorter.
x_len=$5 # size of map x dimension
y_len=$6 # size of map y dimension
fill_holes=$7 # if 0, don't fill holes. If 1, fill holes.

if [ "${fill_holes}" != "0" ] && [ "${fill_holes}" != "1" ]; then
    echo "fill_holes must be 0 or 1, got: ${fill_holes}" >&2
    exit 1
fi

mkdir -p ./ignore

"${my_python}" convert_npz.py "${obs_file}" "${block_size}" "${fly_at}" "${x_len}" "${y_len}"
# this will convert the .npz file to a useable file for my tool chain

new_obs=$(cat "map_${block_size}_${fly_at}.txt")
# get the new name of the file

mv "map_${block_size}_${fly_at}.txt" "./ignore/map_${block_size}_${fly_at}.txt"
mv "${new_obs}" "./ignore/${new_obs}"
# move the files so we don't clog the repo.

new_obs="./ignore/${new_obs}"

if [ "${fill_holes}" == "1" ]; then
    "${my_python}" fill_holes.py "${new_obs}"
    # we fill holes (there are likely regions of the map that are unreachable from the starting location. We are removing them.
    filled_map="${new_obs//obstacles/mapFilled}"
    filled_obs=$(cat "${filled_map}")
else
    filled_obs="${new_obs}"
fi

"${my_python}" assemble_tree_SIMPLE_existing_obs.py "${filled_obs}"
#"${my_python}" generate_data.py "${filled_obs}"
table="${filled_obs//obstacles/table}"
"${my_python}" SIMPLE_table_to_training.py "${table}"

"${my_python}" ../draw_obstacles.py "${filled_obs}"

echo "DONE: obstacles=${filled_obs} table=${table}"
