#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "monitor_types.h"
#include "monitor.h"

static int32_t current_action_cpy;
static int32_t s0[(2)] = {((int32_t)(4)), ((int32_t)(4))};
static size_t s0_idx = (0);

int32_t s0_get(size_t x) {
  return (s0)[((s0_idx) + (x)) % (2)];
}

int32_t s0_gen(void) {
  return current_action_cpy;
}

bool go_slow_guard(void) {
  return ((((s0_get)((1))) == ((int32_t)(0))) && (((s0_get)((0))) == ((int32_t)(1)))) || (((((s0_get)((1))) == ((int32_t)(1))) && (((s0_get)((0))) == ((int32_t)(0)))) || (((((s0_get)((1))) == ((int32_t)(2))) && (((s0_get)((0))) == ((int32_t)(3)))) || ((((s0_get)((1))) == ((int32_t)(3))) && (((s0_get)((0))) == ((int32_t)(2))))));
}

void step(void) {
  int32_t s0_tmp;
  (current_action_cpy) = (current_action);
  if ((go_slow_guard)()) {
    {(go_slow)();}
  };
  (s0_tmp) = ((s0_gen)());
  ((s0)[s0_idx]) = (s0_tmp);
  (s0_idx) = (((s0_idx) + (1)) % (2));
}
