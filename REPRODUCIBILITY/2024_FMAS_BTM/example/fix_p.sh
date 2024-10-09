#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
mon_types=("behaverify")

for category in "${categories[@]}"; do
    echo $category
    for folder in "${category}"/*; do
	if [ -f "${folder}" ]; then
	    continue
	fi
	echo "----------------------------"
	echo $folder
	tail_end=$(basename "${folder}")
	echo $tail_end
	max_val=$(echo $tail_end | cut -d'_' -f1)
	echo $max_val
	for mon_type in "${mon_types[@]}"; do
	    sed -i 's|static static _Bool|static _Bool p|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static static _Bool|static _Bool p|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    
	    sed -i 's|static _Bool0_func|static _Bool p0_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool1_func|static _Bool p1_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool2_func|static _Bool p2_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool3_func|static _Bool p3_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool4_func|static _Bool p4_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool5_func|static _Bool p5_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool6_func|static _Bool p6_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool7_func|static _Bool p7_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool8_func|static _Bool p8_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    sed -i 's|static _Bool9_func|static _Bool p9_func|' "${category}/${tail_end}/${mon_type}/python/collision_monitor.c"
	    
	    sed -i 's|static _Bool0_func|static _Bool p0_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool1_func|static _Bool p1_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool2_func|static _Bool p2_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool3_func|static _Bool p3_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool4_func|static _Bool p4_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool5_func|static _Bool p5_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool6_func|static _Bool p6_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool7_func|static _Bool p7_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool8_func|static _Bool p8_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    sed -i 's|static _Bool9_func|static _Bool p9_func|' "${category}/${tail_end}/${mon_type}/python/loop_monitor.c"
	    
	done
    done
done
