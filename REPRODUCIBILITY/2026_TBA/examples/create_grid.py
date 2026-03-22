def create_grid(file_name, min_val, max_val):
    grid = {x : {y : 0 for y in range(min_val, max_val + 1)} for x in range(min_val, max_val + 1)}
    obstacles = {}
    obstacle_sizes = {}
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
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
    for index in range(len(obstacle_sizes)):
        obs_x = obstacles[2 * index]
        obs_y = obstacles[(2 * index) + 1]
        obs_size = obstacle_sizes[index]
        for x_mod in range(obs_size + 1):
            for y_mod in range(obs_size + 1):
                grid[max(min_val, obs_x - x_mod)][max(min_val, obs_y - y_mod)] = 1
    return grid


if __name__ == '__main__':
    import sys
    grid = create_grid(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    for cur_x in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        for cur_y in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            if grid[cur_x][cur_y] == 0:
                print((cur_x, cur_y))
    # print(grid[49][49])
