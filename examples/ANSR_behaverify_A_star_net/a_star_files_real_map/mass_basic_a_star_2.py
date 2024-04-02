#grid shoult be a dictionary of dictionaries such that grid[x][y] == 1 -> there is an obstacle at (x, y)
def mass_a_star(grid, min_val, max_val, start_location):
    (s_x, s_y) = start_location
    if grid[s_x][s_y] == 1:
        return { x : {y : {'cost' : -1, 'from' : ()} for y in range(len(grid[min_val]))} for x in range(len(grid))}
    # (e_x, e_y) = end_location
    # if grid[e_x][e_y] == 1: return []
    def get_adjacent(c_x, c_y):
        return [
            (a_x, a_y) for a_x in (c_x - 1, c_x, c_x + 1) for a_y in (c_y - 1, c_y, c_y + 1)
            if (
                    ((abs(a_x - c_x) + abs(a_y - c_y)) == 1) and
                    (min_val <= a_x and a_x <= max_val) and
                    (min_val <= a_y and a_y <= max_val) and
                    (grid[a_x][a_y] != 1)
            )
        ]
    direction_convert = {
        (-1, 0) : 'left',
        (1, 0) : 'right',
        (0, -1) : 'down',
        (0, 1) : 'up'
    }
    def prefer_direction(point_source_a, point_source_b, point_end):
        dir_a = direction_convert[((point_end[0] - point_source_a[0]), (point_end[1] - point_source_a[1]))]
        dir_b = direction_convert[((point_end[0] - point_source_b[0]), (point_end[1] - point_source_b[1]))]
        if dir_a == 'left':
            return False
        if dir_b == 'left':
            return True
        if dir_a == 'right':
            return False
        if dir_b == 'right':
            return True
        if dir_a == 'up':
            return False
        if dir_b == 'up':
            return True
        return False

    grid_cost = { x : {y : {'cost' : -1, 'from' : ()} for y in range(len(grid[min_val]))} for x in range(len(grid))}
    grid_cost[s_x][s_y] = {'cost' : 0, 'from' : (s_x, s_y)}
    smallest_cost = 0
    known_costs = {0 : -1} #each value points to the next smallest known cost. if something points to -1, it is the last value.
    frontier = {0 : {(s_x, s_y)}}
    #while len(frontier) > 0 and ((grid_cost[e_x][e_y]['cost'] == -1) or (smallest_cost < grid_cost[e_x][e_y]['cost'])):
    while len(frontier) > 0:
        (x, y) = frontier[smallest_cost].pop()
        if smallest_cost <= grid_cost[x][y]['cost']:
            adj = [
                (n_x, n_y) for (n_x, n_y) in get_adjacent(x, y)  # add each adjacent member that satisfies the conditions below
                if (
                        (grid_cost[n_x][n_y]['cost'] == -1) or  # we've never been here before
                        (grid_cost[n_x][n_y]['cost'] > (smallest_cost + 1)) or  # we've found a more efficient path to here.
                        (
                            grid_cost[n_x][n_y]['cost'] == (smallest_cost + 1) and
                            prefer_direction(grid_cost[n_x][n_y]['from'], (x, y), (n_x, n_y))
                        )
                )
            ]
            if len(adj) > 0:
                # we need to make some updates because at least one path thing changed
                if (smallest_cost + 1) not in known_costs: # make sure we know that there is an explore option at this cost.
                    prev = smallest_cost
                    while True: # this updates our linked list.
                        if (known_costs[prev] == -1) or (known_costs[prev] > (smallest_cost + 1)):
                            known_costs[smallest_cost + 1] = known_costs[prev]
                            known_costs[prev] = smallest_cost + 1
                            break
                if (smallest_cost + 1) not in frontier: # make sure we can track our frontier
                    frontier[smallest_cost + 1] = set()
                for (n_x, n_y) in adj:
                    grid_cost[n_x][n_y] = {'cost' : smallest_cost + 1, 'from' : (x, y)}
                    frontier[smallest_cost + 1].add((n_x, n_y)) # update our frontier
        if len(frontier[smallest_cost]) == 0: # if this was the last value at this cost, update the smallest known cost.
            frontier.pop(smallest_cost)
            smallest_cost = known_costs.pop(smallest_cost) # get the next smallest cost, and also remove our current smallest cost from the lsit.
    return grid_cost
    # if grid_cost[e_x][e_y]['cost'] == -1:
    #     return []
    # path = [(e_x, e_y)]
    # try:
    #     while path[-1][0] != s_x or path[-1][1] != s_y:
    #         path.append(grid_cost[path[-1][0]][path[-1][1]]['from'])
    # except:
    #     print(start_location)
    #     print(end_location)
    #     print(path)
    #     print(grid_cost[0][0])
    #     raise Exception
    # return list(reversed(path))
