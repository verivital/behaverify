import os
from create_grid import create_grid
from mass_basic_a_star_2 import mass_a_star

def generate_sets(min_val, max_val, input_path, return_grid = False):
    grid = create_grid(input_path, min_val, max_val)
    left = set()
    right = set()
    up = set()
    down = set()
    no_action = set()
    seen_values = set()

    iteration = 0
    for start_x in range(min_val, max_val + 1):
        for start_y in range(min_val, max_val + 1):
            grid_cost = mass_a_star(grid, min_val, max_val, (start_x, start_y))
            print('Computed grid from ' + str((start_x, start_y)))
            for end_x in range(min_val, max_val + 1):
                for end_y in range(min_val, max_val + 1):
                    # if iteration % 5000 == 0:
                    #     print('iteration: ' + str(iteration))
                    iteration = iteration + 1
                    if ((start_x, start_y), (end_x, end_y)) in seen_values:
                        continue
                    if grid_cost[end_x][end_y]['cost'] == -1:
                        path = []
                    else:
                        path = [(end_x, end_y)]
                        try:
                            while path[-1][0] != start_x or path[-1][1] != start_y:
                                path.append(grid_cost[path[-1][0]][path[-1][1]]['from'])
                        except:
                            print(str((start_x, start_y)))
                            print(str((end_x, end_y)))
                            print(path)
                            raise Exception
                        path = list(reversed(path))
                    if len(path) < 2:
                        no_action.add(((start_x, start_y), (end_x, end_y)))
                        seen_values.add(((start_x, start_y), (end_x, end_y)))
                    else:
                        for index in range(len(path) - 1):
                            if (path[index], path[-1]) in seen_values:
                                continue
                            seen_values.add((path[index], path[-1]))
                            if path[index][0] < path[index + 1][0] and path[index][1] == path[index + 1][1]:
                                right.add(((path[index][0], path[index][1]), (end_x, end_y)))
                            elif path[index][0] > path[index + 1][0] and path[index][1] == path[index + 1][1]:
                                left.add(((path[index][0], path[index][1]), (end_x, end_y)))
                            elif path[index][0] == path[index + 1][0] and path[index][1] < path[index + 1][1]:
                                up.add(((path[index][0], path[index][1]), (end_x, end_y)))
                            elif path[index][0] == path[index + 1][0] and path[index][1] > path[index + 1][1]:
                                down.add(((path[index][0], path[index][1]), (end_x, end_y)))
                            else:
                                print('unknown direction')
                                print('from: ' + path[index])
                                print('to: ' + path[index + 1])
                                print('adding to no_action')
                                no_action.add(((path[index][0], path[index][1]), (end_x, end_y)))
    return (left, right, up, down, no_action, grid) if return_grid else (left, right, up, down, no_action)

def check_all_points_in_region(cur_set, min_s_x, max_s_x, min_s_y, max_s_y, min_e_x, max_e_x, min_e_y, max_e_y):
    for s_x in range(min_s_x, max_s_x + 1):
        for s_y in range(min_s_y, max_s_y + 1):
            for e_x in range(min_e_x, max_e_x + 1):
                for e_y in range(min_e_y, max_e_y + 1):
                    if ((s_x, s_y), (e_x, e_y)) not in cur_set:
                        return False
    return True

def remove_all_points_in_region(cur_set, min_vals, max_vals):
    for s_x in range(min_vals[0][0], max_vals[0][0] + 1):
        for s_y in range(min_vals[0][1], max_vals[0][1] + 1):
            for e_x in range(min_vals[1][0], max_vals[1][0] + 1):
                for e_y in range(min_vals[1][1], max_vals[1][1] + 1):
                    cur_set.remove(((s_x, s_y), (e_x, e_y)))

def maximize_dimensions(cur_set, centered_at):
    ((s_x, s_y), (e_x, e_y)) = centered_at
    min_vals = []
    max_vals = []
    ###s_x
    min_val = s_x
    while check_all_points_in_region(cur_set, min_val - 1, min_val - 1, s_y, s_y, e_x, e_x, e_y, e_y):
        min_val = min_val - 1
    max_val = s_x
    while check_all_points_in_region(cur_set, max_val + 1, max_val + 1, s_y, s_y, e_x, e_x, e_y, e_y):
        max_val = max_val + 1
    min_vals.append(min_val)
    max_vals.append(max_val)
    ###s_y
    min_val = s_y
    while check_all_points_in_region(cur_set, min_vals[0], max_vals[0], min_val - 1, min_val - 1, e_x, e_x, e_y, e_y):
        min_val = min_val - 1
    max_val = s_y
    while check_all_points_in_region(cur_set, min_vals[0], max_vals[0], max_val + 1, max_val + 1, e_x, e_x, e_y, e_y):
        max_val = max_val + 1
    min_vals.append(min_val)
    max_vals.append(max_val)
    ###e_x
    min_val = e_x
    while check_all_points_in_region(cur_set, min_vals[0], max_vals[0], min_vals[1], max_vals[1], min_val - 1, min_val - 1, e_y, e_y):
        min_val = min_val - 1
    max_val = e_x
    while check_all_points_in_region(cur_set, min_vals[0], max_vals[0], min_vals[1], max_vals[1], max_val + 1, max_val + 1, e_y, e_y):
        max_val = max_val + 1
    min_vals.append(min_val)
    max_vals.append(max_val)
    ###e_y
    min_val = e_y
    while check_all_points_in_region(cur_set, min_vals[0], max_vals[0], min_vals[1], max_vals[1], min_vals[2], max_vals[2], min_val - 1, min_val - 1):
        min_val = min_val - 1
    max_val = e_y
    while check_all_points_in_region(cur_set, min_vals[0], max_vals[0], min_vals[1], max_vals[1], min_vals[2], max_vals[2], max_val + 1, max_val + 1):
        max_val = max_val + 1
    min_vals.append(min_val)
    max_vals.append(max_val)
    return (
        ((min_vals[0], min_vals[1]), (min_vals[2], min_vals[3])),
        ((max_vals[0], max_vals[1]), (max_vals[2], max_vals[3]))
    )

def simplify_set(cur_set):
    print('original: ' + str(len(cur_set)))
    new_set = set()
    while len(cur_set) > 0:
        centered_at = cur_set.pop()
        cur_set.add(centered_at)
        (min_vals, max_vals) = maximize_dimensions(cur_set, centered_at)
        new_set.add((min_vals, max_vals))
        remove_all_points_in_region(cur_set, min_vals, max_vals)
    print('new: ' + str(len(new_set)))
    return new_set

def generate_table(min_val, max_val, input_path, output_path):
    (left, right, up, down, no_action) = generate_sets(min_val, max_val, input_path)
    print('--------------------')
    print('no_action')
    print(len(no_action))
    lines = []
    #for (cur_set, direction) in ((left, 'left'), (right, 'right'), (up, 'up'), (down, 'down'), (no_action, 'no_action')):
    for (cur_set, direction) in ((left, 'left'), (right, 'right'), (up, 'up'), (down, 'down')):
        print('--------------------')
        print(direction)
        new_set = simplify_set(cur_set)
        for (((min_s_x, min_s_y), (min_e_x, min_e_y)), ((max_s_x, max_s_y), (max_e_x, max_e_y))) in new_set:
            lines.append(
                (
                    'case{(and, '
                    + (
                        ('(eq, drone_x, ' + str(min_s_x) + '), ')
                        if min_s_x == max_s_x else
                        ('(lte,' + str(min_s_x) + ', drone_x), (lte, drone_x, ' + str(max_s_x) + '), ')
                    )
                    + (
                        ('(eq, drone_y, ' + str(min_s_y) + '), ')
                        if min_s_y == max_s_y else
                        ('(lte,' + str(min_s_y) + ', drone_y), (lte, drone_y, ' + str(max_s_y) + '), ')
                    )
                    + (
                        ('(eq, destination_x, ' + str(min_e_x) + '), ')
                        if min_e_x == max_e_x else
                        ('(lte,' + str(min_e_x) + ', destination_x), (lte, destination_x, ' + str(max_e_x) + '), ')
                    )
                    + (
                        ('(eq, destination_y, ' + str(min_e_y) + ')')
                        if min_e_y == max_e_y else
                        ('(lte,' + str(min_e_y) + ', destination_y), (lte, destination_y, ' + str(max_e_y) + ')')
                    )
                    + ')} '
                    + 'result{\'' + direction + '\'}'
                    + os.linesep
                )
            )
    lines.append('result{\'no_action\'}' + os.linesep)
    with open(output_path, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(lines)

def generate_table_original(min_val, max_val, input_path, output_path):
    (left, right, up, down, no_action) = generate_sets(min_val, max_val, input_path)
    lines = []
    #for (cur_set, direction) in ((left, 'left'), (right, 'right'), (up, 'up'), (down, 'down'), (no_action, 'no_action')):
    for (cur_set, direction) in ((left, 'left'), (right, 'right'), (up, 'up'), (down, 'down')):
        for ((s_x, s_y), (e_x, e_y)) in cur_set:
            lines.append(
                (
                    'case{(and, '
                    + '(eq, drone_x, ' + str(s_x) + '), '
                    + '(eq, drone_y, ' + str(s_y) + '), '
                    + '(eq, destination_x, ' + str(e_x) + '), '
                    + '(eq, destination_y, ' + str(e_y) + '))}'
                    + 'result{\'' + direction + '\'}'
                    + os.linesep
                )
            )
    lines.append('result{\'no_action\'}' + os.linesep)
    with open(output_path, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(lines)


if __name__ == '__main__':
    (left_, right_, up_, down_, no_action_) = generate_sets(0, 19, 'ignore/obstacles_10_0_19_3.txt')
    print('left')
    simplify_set(left_)
    print('right')
    simplify_set(right_)
    print('up')
    simplify_set(up_)
    print('down')
    simplify_set(down_)
    # with open('ignore/left.txt', 'w', encoding = 'utf-8') as output_file_:
    #     output_file_.write(str(left_))
    # with open('ignore/right.txt', 'w', encoding = 'utf-8') as output_file_:
    #     output_file_.write(str(right_))
    # with open('ignore/up.txt', 'w', encoding = 'utf-8') as output_file_:
    #     output_file_.write(str(up_))
    # with open('ignore/down.txt', 'w', encoding = 'utf-8') as output_file_:
    #     output_file_.write(str(down_))
    # with open('ignore/no_action.txt', 'w', encoding = 'utf-8') as output_file_:
    #     output_file_.write(str(no_action_))
