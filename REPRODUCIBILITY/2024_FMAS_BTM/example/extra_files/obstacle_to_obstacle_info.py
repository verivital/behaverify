import os
import sys
from misc_util import extract_info

def convert_obstacles_to_obstacle_info(input_path):
    (_, _, fly_at, number_of_obstacles, _) = extract_info(input_path)
    obstacles = {}
    obstacle_sizes = {}
    with open(input_path, 'r', encoding = 'utf-8') as input_file:
        data = input_file.read()
        data = data.replace('condition {(eq, index_var,', '')
        data = data.replace(')} assign{result{', ', ')
        data = data.replace('}}', ';')
        (locations, sizes) = data.split('#', 1)
        locations = locations.replace('#', '')
        sizes = sizes.replace('#', '')
        for index_val in locations.split(';'):
            if index_val.strip() == '':
                continue
            (index, val) = index_val.split(',')
            index = int(index.strip())
            val = int(val.strip())
            obstacles[index] = val
        for index_val in sizes.split(';'):
            if index_val.strip() == '':
                continue
            (index, val) = index_val.split(',')
            index = int(index.strip())
            val = int(val.strip())
            obstacle_sizes[index] = val
    obstacles_lines = (
        ['    obstacles = [None for _ in range(' + str(2 * number_of_obstacles) + ')]' + os.linesep]
        + [('    obstacles[' + str(index) + '] = ' + str(obstacles[index])) for index in obstacles]
    )
    obstacle_sizes_lines = (
        ['    obstacle_sizes = [None for _ in range(' + str(number_of_obstacles) + ')]' + os.linesep]
        + [('    obstacle_sizes[' + str(index) + '] = ' + str(obstacle_sizes[index])) for index in obstacle_sizes]
    )
    input_lines = ['def obs_info_' + str(fly_at) + '():' + os.linesep] + obstacles_lines + obstacle_sizes_lines + ['    return (obstacles, obstacle_sizes)' + os.linesep]
    output_path_input = input_path.replace('obstacles', 'obs_info').replace('.txt', '.py')
    with open(output_path_input, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(input_lines)

if __name__ == '__main__':
    convert_obstacles_to_obstacle_info(sys.argv[1])
