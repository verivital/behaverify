#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "monitor_types.h"
#include "monitor.h"

static int32_t drone_x_cpy;
static int32_t delta_x_cpy;
static int32_t drone_y_cpy;
static int32_t delta_y_cpy;
static int32_t s0[(1)][(4)] = {{((int32_t)(3)), ((int32_t)(3)), ((int32_t)(0)), ((int32_t)(4))}};
static int32_t s1[(1)][(2)] = {{((int32_t)(1)), ((int32_t)(0))}};
static size_t s0_idx = (0);
static size_t s1_idx = (0);

int32_t * s0_get(size_t x) {
  return (s0)[((s0_idx) + (x)) % (1)];
}

int32_t * s1_get(size_t x) {
  return (s1)[((s1_idx) + (x)) % (1)];
}

void s0_gen(int32_t s0_output[(4)]) {
  (memcpy)((s0_output), ((s0_get)((0))), ((4) * (sizeof(int32_t))));
}

void s1_gen(int32_t s1_output[(2)]) {
  (memcpy)((s1_output), ((s1_get)((0))), ((2) * (sizeof(int32_t))));
}

bool go_slow_guard(void) {
  return ((((((s0_get)((0)))[(uint32_t)(0)]) - (((s1_get)((0)))[(uint32_t)(0)])) <= ((drone_x_cpy) + (delta_x_cpy))) && ((((drone_x_cpy) + (delta_x_cpy)) <= (((s0_get)((0)))[(uint32_t)(0)])) && ((((((s0_get)((0)))[(uint32_t)(1)]) - (((s1_get)((0)))[(uint32_t)(0)])) <= ((drone_y_cpy) + (delta_y_cpy))) && (((drone_y_cpy) + (delta_y_cpy)) <= (((s0_get)((0)))[(uint32_t)(1)]))))) || ((((((s0_get)((0)))[(uint32_t)(2)]) - (((s1_get)((0)))[(uint32_t)(1)])) <= ((drone_x_cpy) + (delta_x_cpy))) && ((((drone_x_cpy) + (delta_x_cpy)) <= (((s0_get)((0)))[(uint32_t)(2)])) && ((((((s0_get)((0)))[(uint32_t)(3)]) - (((s1_get)((0)))[(uint32_t)(1)])) <= ((drone_y_cpy) + (delta_y_cpy))) && (((drone_y_cpy) + (delta_y_cpy)) <= (((s0_get)((0)))[(uint32_t)(3)])))));
}

void step_model(void) {
  int32_t s0_tmp[(4)];
  int32_t s1_tmp[(2)];
  (drone_x_cpy) = (drone_x);
  (delta_x_cpy) = (delta_x);
  (drone_y_cpy) = (drone_y);
  (delta_y_cpy) = (delta_y);
  if ((go_slow_guard)()) {
    {(go_slow)();}
  };
  (s0_gen)((s0_tmp));
  (s1_gen)((s1_tmp));
  (memcpy)(((s0)[s0_idx]), (s0_tmp), ((4) * (sizeof(int32_t))));
  (memcpy)(((s1)[s1_idx]), (s1_tmp), ((2) * (sizeof(int32_t))));
  (s0_idx) = (((s0_idx) + (1)) % (1));
  (s1_idx) = (((s1_idx) + (1)) % (1));
}
//
#include <stdio.h>
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
  drone_x = x;
  drone_y = y;
  delta_x = dx;
  delta_y = dy;
  step_model();
  return slow_down;
}
