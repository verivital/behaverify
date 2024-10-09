#include <stdlib.h>
#include <time.h>
#include "collision_monitor.h"
#include "loop_monitor.h"
#include "obstacle_file.h"

int main(int argc, char *argv[]){
  srand(time(0));
  int iterations = atoi(argv[1]);
  int grid_size = atoi(argv[2]);
  int x = 0;
  int y = 0;
  int dx;
  int dy;
  int speed;
  int action;

  _Bool collision_states_initial[1] = {1};
  _Bool loop_states_initial[16] = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  _Bool collision_states_fake[1] = {1};
  

  _Bool *collision_states = collision_states_initial;
  _Bool *collision_states_next = collision_states_fake;
  _Bool *loop_states = loop_states_initial;
  _Bool *loop_states_next;
  int monitor_var;
  char* cur_act;
  for (int count = 0; count < iterations; count++){
    speed = 2;
    action = rand() % 5;
    if (action == 0){dx = -1;dy = 0;cur_act = "left";}
    else{
      if (action == 1){dx = 1;dy = 0; cur_act = "right";}
      else{
	if (action == 2){dx = 0;dy = 1; cur_act = "up";}
	else{
	  if (action == 3){dx = 0;dy = -1; cur_act = "down";}
	  else{dx = 0; dy = 0; cur_act = "no_action";}
	}
      }
    }
    if (((x + dx) >= grid_size) || ((x + dx) < 0) || ((y + dy) >= grid_size) || ((y + dy) < 0) || OBSTACLE_QUERY[x + dx][y + dy]){action = 5; dx = 0; dy = 0; cur_act = "no_action";}
    monitor_var = collision_monitor_transition(collision_states, collision_states_next, dx, dy, x, y, OBSTACLE_SIZES, OBSTACLES);
    if (monitor_var == 2){speed = 1;}
    _Bool loop_states_fake[16] = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    loop_states_next = loop_states_fake;
    monitor_var = loop_monitor_transition(loop_states, loop_states_next, cur_act);
    if (monitor_var == 2){speed = 1; loop_monitor_reset(loop_states);}
    else {loop_states = loop_states_next;}
    x = x + (dx * speed);
    y = y + (dy * speed);
    x = (grid_size < x) ? grid_size : x;
    x = (x < 0) ? 0 : x;
    y = (grid_size < y) ? grid_size : y;
    y = (y < 0) ? 0 : y;
  }
}
