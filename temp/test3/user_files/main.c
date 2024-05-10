#include <stdio.h>
#include "monitor.h" // Assuming monitor.h is in the same directory as your source file

int main() {
  int ptr = 1;

  // Your loop that calls monitor_ex
  long state = 0;
  for (int i = 0; i < 10; i++) {
    RV_value result = monitor_ex(&state, 1, 0, &ptr); // Call monitor_ex function from monitor.h
    printf("Result of monitor_ex call %d: %d\n", i+1, result);
    state++;
  }  
  return 0;
}
