#!/bin/bash

location=$1
sed -i 's|#include "monitor.h"|#include "collision_monitor.h"|' "${location}/collision_monitor.c"
sed -i 's|#include "monitor.h"|#include "loop_monitor.h"|' "${location}/loop_monitor.c"

echo 'int user_interface(int drone_x, int drone_y, int drone_speed, int delta_x, int delta_y);' >> "${location}/collision_monitor.h"
echo 'int location = 1;' >> "${location}/collision_monitor.c"
echo 'int user_interface(int drone_x, int drone_y, int drone_speed, int delta_x, int delta_y){' >> "${location}/collision_monitor.c"
echo '  monitor_input_t input;' >> "${location}/collision_monitor.c"
echo '  input.system_drone_x = drone_x;' >> "${location}/collision_monitor.c"
echo '  input.system_drone_x = drone_y;' >> "${location}/collision_monitor.c"
echo '  input.system_drone_speed = drone_speed;' >> "${location}/collision_monitor.c"
echo '  input.system_delta_x = delta_x;' >> "${location}/collision_monitor.c"
echo '  input.system_delta_y = delta_y;' >> "${location}/collision_monitor.c"
echo '  return monitor_scalar(&input, NULL, 1, &location); ' >> "${location}/collision_monitor.c"
echo '}' >> "${location}/collision_monitor.c"

echo 'int user_interface(int current_action, _Bool use_reset);' >> "${location}/loop_monitor.h"
echo 'int location = 1;' >> "${location}/loop_monitor.c"
echo 'int user_interface(int current_action, _Bool use_reset){' >> "${location}/loop_monitor.c"
echo '  monitor_input_t input;' >> "${location}/loop_monitor.c"
echo '  input.system_current_action = current_action;' >> "${location}/loop_monitor.c"
echo '  RV_reset reset_now = NO_RESET;' >> "${location}/loop_monitor.c"
echo '  if (use_reset) { reset_now = HARD_RESET;}'  >> "${location}/loop_monitor.c"
echo '  return monitor_scalar(&input, NULL, reset_now, &location); ' >> "${location}/loop_monitor.c"
echo '}' >> "${location}/loop_monitor.c"
