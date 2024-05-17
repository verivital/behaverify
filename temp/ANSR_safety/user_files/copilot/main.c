#include <stdio.h>
#include <stdint.h>
#include "monitor.h"
int32_t drone_x;
int32_t drone_y;
int32_t delta_x;
int32_t delta_y;

int main() {
  // Your loop that calls monitor_ex
  int32_t states[6][5] = {
    {0, 6, 1, 0, 2},
    {2, 6, 0, -1, 2},
    {2, 4, 0, -1, 1}, //crash inevitable
    {2, 3, 0, -1, 1}, //crash occurs
    {2, 4, -1, 0, 1}, // reset
    {1, 4, 0, -1, 2}
  };
  printf("-----------------------------------------------\n");
  for (int i = 0; i < 6; i++) {
    //RV_value result = monitor_simpler_ex(&states[i], NULL, resets[i], &ptr); // Call monitor_ex function from monitor.h
    drone_x = states[i][0];
    drone_y = states[i][1];
    delta_x = states[i][2];
    delta_y = states[i][3];
    //speed = states[i][4];
    printf("%d\n", i);
    step();
  }
  return 0;
}

