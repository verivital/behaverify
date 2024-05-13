#include <stdio.h>

// Global variable
int cur_sum = 0;

// Function to add the input value to cur_sum and return the cumulative sum
int cum_sum(int value) {
    cur_sum += value;
    return cur_sum;
}
