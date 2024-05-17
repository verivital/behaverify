#include <stdint.h>
#include <stdio.h>
#include "monitor.h"
#include "user_code.h"


int main(){
  int32_t states[6][5] = {
    {0, 6, 1, 0, 2},
    {2, 6, 0, -1, 2},
    {2, 4, 0, -1, 1}, //crash inevitable
    {2, 3, 0, -1, 1}, //crash occurs
    {2, 4, -1, 0, 1}, // reset
    {1, 4, 0, -1, 2}
  };
  for (int i = 0; i < 6; i++) {
    printf("%d\n", i);
    driver(states[i][0], states[i][1], states[i][2], states[i][3]);
  }
  return 0;
  
}
