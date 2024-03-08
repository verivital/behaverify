import os
from create_grid import create_grid
from basic_a_star import a_star

def generate_sets(min_val, max_val):
    grid = create_grid('ignore/obstacles.txt', min_val, max_val)
    left = set()
    right = set()
    up = set()
    down = set()
    no_action = set()
    seen_values = set()

    iteration = 0
    for start_x in range(min_val, max_val + 1):
        for start_y in range(min_val, max_val + 1):
            for end_x in range(min_val, max_val + 1):
                for end_y in range(min_val, max_val + 1):
                    if iteration % 100 == 0:
                        print('iteration: ' + str(iteration))
                    iteration = iteration + 1
                    if ((start_x, start_y), (end_x, end_y)) in seen_values:
                        continue
                    path = a_star(grid, min_val, max_val, (start_x, start_y), (end_x, end_y))
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
    return (left, right, up, down, no_action)


def generate_table(min_val, max_val):
    (left, right, up, down, no_action) = generate_sets(min_val, max_val)
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
    with open('ignore/table.txt', 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(lines)


if __name__ == '__main__':
    (left_, right_, up_, down_, no_action_) = generate_sets(0, 19)
    with open('ignore/left.txt', 'w', encoding = 'utf-8') as output_file_:
        output_file_.write(str(left_))
    with open('ignore/right.txt', 'w', encoding = 'utf-8') as output_file_:
        output_file_.write(str(right_))
    with open('ignore/up.txt', 'w', encoding = 'utf-8') as output_file_:
        output_file_.write(str(up_))
    with open('ignore/down.txt', 'w', encoding = 'utf-8') as output_file_:
        output_file_.write(str(down_))
    with open('ignore/no_action.txt', 'w', encoding = 'utf-8') as output_file_:
        output_file_.write(str(no_action_))
