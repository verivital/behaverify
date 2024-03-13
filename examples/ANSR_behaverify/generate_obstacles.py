import sys
import random

def generate_obstacles(num_obstacles, min_val, max_val, max_size):
    for index in range(num_obstacles):
        x_val = random.randint(min_val, max_val)
        y_val = random.randint(min_val, max_val)
        while x_val == max_val and y_val == max_val:
            x_val = random.randint(min_val, max_val)
            y_val = random.randint(min_val, max_val)
        print('condition {(eq, index_var, ' + str(2 * index) + ')} assign{result{' + str(random.randint(min_val, max_val)) + '}}'
              + 'condition {(eq, index_var, ' + str((2 * index) + 1) + ')} assign{result{' + str(random.randint(min_val, max_val)) + '}}')
    print('##################################################################')
    for index in range(num_obstacles):
        print('condition {(eq, index_var, ' + str(index) + ')} assign{result{' + str(random.randint(0, max_size)) + '}}')

generate_obstacles(50, 0, 49, 3)
