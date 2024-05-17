#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include "monitor.h"

int32_t drone_x;
int32_t delta_x;
int32_t drone_y;
int32_t delta_y;
_Bool slow_down;
void go_slow(void) {
  printf("SLOW DOWN\n");
  slow_down = true;
}

_Bool driver(int32_t x, int32_t y, int32_t dx, int32_t dy) {
  printf("hello\n");
  drone_x = x;
  drone_y = y;
  delta_x = dx;
  delta_y = dy;
  printf("hello\n");
  step();
  return slow_down;
}
