import sys
import random
import os

def generate_obstacles(number_of_obstacles, min_val, max_val, max_size):
    lines = []
    for index in range(number_of_obstacles):
        x_val = random.randint(min_val, max_val)
        y_val = random.randint(min_val, max_val)
        while x_val == max_val and y_val == max_val:
            x_val = random.randint(min_val, max_val)
            y_val = random.randint(min_val, max_val)
        lines.append('condition {(eq, index_var, ' + str(2 * index) + ')} assign{result{' + str(random.randint(min_val, max_val)) + '}}'
                     + 'condition {(eq, index_var, ' + str((2 * index) + 1) + ')} assign{result{' + str(random.randint(min_val, max_val)) + '}}' + os.linesep)
    lines.append('##################################################################' + os.linesep)
    for index in range(number_of_obstacles):
        lines.append('condition {(eq, index_var, ' + str(index) + ')} assign{result{' + str(random.randint(0, max_size)) + '}}' + os.linesep)
    with open('ignore/obstacles_' + str(number_of_obstacles) + '_' + str(min_val) + '_' + str(max_val) + '_' + str(max_size) + '.txt', 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(lines)

if __name__ == '__main__':
    #generate_obstacles(50, 0, 49, 3)
    #generate_obstacles(10, 0, 19, 3)
    generate_obstacles(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
