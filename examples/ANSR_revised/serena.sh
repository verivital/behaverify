#!/bin/bash


source /host/scripts/init.sh
source /host/ros2_ws/install/setup.bash

ros2 bag record \
    /adk_node/input/sparse_waypoints \
    /adk_node/SimpleFlight/collision_state \
    /adk_node/SimpleFlight/odom_local_ned \
    /adk_node/ground_truth/perception \
    /adk_node/vanderbilt/goal \
    /adk_node/vanderbilt/invalid_goal_event \
    /adk_node/vanderbilt/mission_spec \
    -o /output/results/`(date '+%Y_%m_%d_%H_%M_%S')`_eval.bag &


timeout 310s ros2 launch /host/ros2_ws/src/launch/vanderbilt.xml

source /host/scripts/bag_eval.sh
