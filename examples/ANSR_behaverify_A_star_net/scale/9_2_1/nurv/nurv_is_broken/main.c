#include <stdio.h>
#include "monitor.h"

int main() {
  int ptr = 1;
  monitor_input_t state;
  state.system_drone_x = 0;
  state.system_drone_y = 8;
  state.system_drone_speed = 2;
  state.system_delta_x = 1;
  state.system_delta_y = 0;
  RV_value result = monitor_scalar(&state, NULL, 0, &ptr);
  printf("-------------------------------------------------\n");
  printf("%d\n", result);
  printf("-------------------------------------------------\n");
  state.system_drone_x = 1;
  state.system_drone_y = 8;
  state.system_drone_speed = 2;
  state.system_delta_x = 1;
  state.system_delta_y = 0;
  result = monitor_scalar(&state, NULL, 0, &ptr);
  printf("-------------------------------------------------\n");
  printf("%d\n", result);
  printf("-------------------------------------------------\n");

  return 0;
}
