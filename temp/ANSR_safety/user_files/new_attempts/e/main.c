#include <stdio.h>
#include "monitor.h"





int main() {
  int max_x = 1;
  int max_y = 1;
  int dirs[5] = {left, right, up, down, no_action};
  char dir_names[] = {"lrudn"};
  for (int sx = 0; sx <= max_x; sx++){
    for (int sy = 0; sy <= max_y; sy++){
      for (int ex = 0; ex <= max_x; ex++){
	for (int ey = 0; ey <= max_y; ey++){
	  for (int dir_loc = 0; dir_loc < 5; dir_loc++){
	    for (int speed = 1; speed <= 1; speed++){
	      int ptr = 1;
	      monitor_input_t start_state;
	      start_state.system_drone_x = sx;
	      start_state.system_drone_y = sy;
	      //start_state.system_drone_speed = speed;
	      start_state.system_current_action = dirs[dir_loc];
	      monitor_input_t end_state;
	      end_state.system_drone_x = ex;
	      end_state.system_drone_y = ey;
	      //end_state.system_drone_speed = speed;
	      end_state.system_current_action = dirs[dir_loc];
	      RV_value result_start = monitor_scalar(&start_state, NULL, 1, &ptr);
	      RV_value result_end = monitor_scalar(&end_state, NULL, 0, &ptr);
	      if (result_end != 3){
		printf("from (%d, %d) to (%d, %d) via (%c, %d) -> (%d, %d)\n", sx, sy, ex, ey, dir_names[dir_loc], speed, result_start, result_end);
	      }
	    }
	  }
	}
      }
    }
  }
  return 0;
}
