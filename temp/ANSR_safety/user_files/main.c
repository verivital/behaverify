#include <stdio.h>
#include "monitor_simplest.h"

int main() {
  int ptr = 1;

  int start_x = 2;
  int start_direction = right;
  monitor_simplest_input_t start_state;
  start_state.system_drone_x = start_x;
  start_state.system_current_action = start_direction;
  RV_value ini_res = monitor_simplest_scalar(&start_state, NULL, 1, &ptr);
  printf("initial %d\n", ini_res);
  printf("-----------------------------------------------\n");
  for (int i = 0; i <= 3; i++){
    RV_value result = monitor_simplest_scalar(&start_state, NULL, 1, &ptr); // Call monitor_ex function from monitor.h
    //printf("xs %d: %d\n", i+1, result);
    monitor_simplest_input_t new_state_x;
    new_state_x.system_drone_x = i;
    new_state_x.system_current_action = start_direction;
    result = monitor_simplest_scalar(&new_state_x, NULL, 0, &ptr); // Call monitor_ex function from monitor.h
    printf("xn %d: %d\n", i, result);
  }

  return 0;
}

/* int main() { */
/*   int ptr = 1; */

/*   int start_x = 0; */
/*   int start_y = 3; */
/*   int start_direction = up; */
/*   monitor_simpler_input_t start_state = {start_x, start_y, start_direction}; */
/*   start_state.system_drone_x = start_x; */
/*   start_state.system_drone_y = start_y; */
/*   start_state.system_current_action = start_direction; */
/*   for (int i = 0; i <= 4; i++){ */
/*     monitor_simpler_input_t new_state_x = {i, start_y, no_action}; */
/*     new_state_x.system_drone_x = i; */
/*     new_state_x.system_drone_y = start_y; */
/*     new_state_x.system_current_action = no_action; */
/*     RV_value result = monitor_simpler_scalar(&start_state, NULL, 1, &ptr); // Call monitor_ex function from monitor.h */
/*     //printf("xs %d: %d\n", i+1, result); */
/*     result = monitor_simpler_scalar(&new_state_x, NULL, 0, &ptr); // Call monitor_ex function from monitor.h */
/*     printf("xn %d: %d\n", i, result); */
/*   } */
/*   printf("-----------------------------------------------\n"); */
/*   for (int i = 0; i <= 4; i++){ */
/*     monitor_simpler_input_t new_state_y = {start_x, i, no_action}; */
/*     new_state_y.system_drone_x = start_x; */
/*     new_state_y.system_drone_y = i; */
/*     new_state_y.system_current_action = no_action; */
/*     RV_value result = monitor_simpler_scalar(&start_state, NULL, 1, &ptr); // Call monitor_ex function from monitor.h */
/*     //printf("ys %d: %d\n", i+1, result); */
/*     result = monitor_simpler_scalar(&new_state_y, NULL, 0, &ptr); // Call monitor_ex function from monitor.h */
/*     printf("yn %d: %d\n", i, result); */
/*   } */

/*   ptr = 1; */
/*   // Your loop that calls monitor_ex */
/*   monitor_simpler_input_t states[6] = { */
/*     {0, 6, right}, */
/*     {2, 6, down}, */
/*     {2, 4, down}, //crash inevitable */
/*     {2, 3, down}, //crash occurs */
/*     {2, 4, left}, // reset */
/*     {1, 4, up} */
/*   }; */
/*   RV_reset resets[6] = { */
/*     0, */
/*     0, */
/*     0, */
/*     0, */
/*     1, */
/*     0 */
/*   }; */
/*   printf("-----------------------------------------------\n"); */
/*   for (int i = 0; i < 6; i++) { */
/*     //RV_value result = monitor_simpler_ex(&states[i], NULL, resets[i], &ptr); // Call monitor_ex function from monitor.h */
/*     RV_value result = monitor_simpler_scalar(&states[i], NULL, resets[i], &ptr); // Call monitor_ex function from monitor.h */
/*     printf("Result of monitor_simpler_scalar call %d: %d\n", i+1, result); */
/*   } */
/*   return 0; */
/* } */

/* int main() { */
/*   int ptr = 1; */

/*   int sx = 6; */
/*   int sy = 6; */
/*   int speed = 1; */
/*   int dir = down; */
/*   monitor3_input_t start_state;// = {sx, sy, speed, dir}; */
/*   start_state.system_drone_x = sx; */
/*   start_state.system_drone_y = sy; */
/*   start_state.system_drone_speed = speed; */
/*   start_state.system_current_action = dir; */
/*   RV_value ini_res = monitor3_scalar(&start_state, NULL, 1, &ptr); // Call monitor_ex function from monitor.h */
/*   printf("initial %d\n", ini_res); */
/*   printf("-----------------------------------------------\n"); */
/*   for (int i = 0; i <= 6; i++){ */
/*     RV_value result = monitor3_scalar(&start_state, NULL, 1, &ptr); // Call monitor_ex function from monitor.h */
/*     //printf("xs %d: %d\n", i+1, result); */
/*     monitor3_input_t new_state_x;// = {i, sy, 1, no_action}; */
/*     new_state_x.system_drone_x = i; */
/*     new_state_x.system_drone_y = sy; */
/*     new_state_x.system_drone_speed = speed; */
/*     new_state_x.system_current_action = dir; */
/*     result = monitor3_scalar(&new_state_x, NULL, 0, &ptr); // Call monitor_ex function from monitor.h */
/*     printf("xn %d: %d\n", i, result); */
/*   } */
/*   printf("-----------------------------------------------\n"); */
/*   for (int i = 0; i <= 6; i++){ */
/*     RV_value result = monitor3_scalar(&start_state, NULL, 1, &ptr); // Call monitor_ex function from monitor.h */
/*     //printf("ys %d: %d\n", i+1, result); */
/*     monitor3_input_t new_state_y;// = {sx, i, 1, no_action}; */
/*     new_state_y.system_drone_x = sx; */
/*     new_state_y.system_drone_y = i; */
/*     new_state_y.system_drone_speed = speed; */
/*     new_state_y.system_current_action = dir; */
/*     result = monitor3_scalar(&new_state_y, NULL, 0, &ptr); // Call monitor_ex function from monitor.h */
/*     printf("yn %d: %d\n", i, result); */
/*   } */

/*   ptr = 1; */
/*   // Your loop that calls monitor_ex */
/*   monitor3_input_t states[6] = { */
/*     {0, 6, 2, right}, */
/*     {2, 6, 2, down}, */
/*     {2, 4, 1, down}, //crash inevitable */
/*     {2, 3, 1, down}, //crash occurs */
/*     {2, 4, 1, left}, // reset */
/*     {1, 4, 1, up} */
/*   }; */
/*   RV_reset resets[6] = { */
/*     0, */
/*     0, */
/*     0, */
/*     0, */
/*     1, */
/*     0 */
/*   }; */
/*   printf("-----------------------------------------------\n"); */
/*   for (int i = 0; i < 6; i++) { */
/*     //RV_value result = monitor3_ex(&states[i], NULL, resets[i], &ptr); // Call monitor_ex function from monitor.h */
/*     RV_value result = monitor3_scalar(&states[i], NULL, resets[i], &ptr); // Call monitor_ex function from monitor.h */
/*     printf("Result of monitor3_scalar call %d: %d\n", i+1, result); */
/*   } */
/*   return 0; */
/* } */
