'''
Basic A* algorithm. Allows for variable costs. Assumes all costs are non-negative.
Serena Serafina Serbinowska
'''
def a_star(grid, start_location, end_location):
    '''
    points should be ordered tuples. (x, y), (x, y, z), (x, y, z, w), w/e. Ordered pairs need not be the same length.
    grid should be a dictionary of dictionaries of lists such that grid[point] = [(point0, c0), (point1, c1), ...] where cI is the cost to go from point0 to point1
    '''
    if (start_location not in grid) or (len(grid[start_location]) == 0):
        # can't get anywhere. Return
        return []
    # grid_cost = {point : {'cost' : -1, 'from' : None} for point in grid}
    grid_cost = {}
    grid_cost[start_location] = {'cost' : 0, 'from' : start_location}
    smallest_cost = 0
    known_costs = {0 : -1} #each value points to the next smallest known cost. if something points to -1, it is the last value.
    frontier = {0 : [start_location]}
    #while len(frontier) > 0 and ((grid_cost[end_location]['cost'] == -1) or (smallest_cost < grid_cost[end_location]['cost'])):
    while len(frontier) > 0 and ((end_location not in grid_cost) or (smallest_cost < grid_cost[end_location]['cost'])):
        point = frontier[smallest_cost].pop() # we are going to explore from this point.
        if smallest_cost <= grid_cost[point]['cost']: # if the cost of getting to this location is not more expensive than the current known cost, explore (note that the default value of -1 is not relevant, because if we're exploring from this location than we must have reached this point so it has a non-negative cost)
            if point in grid:
                adj_cost = grid[point] # adjacent locations
                for (n_p, n_c) in adj_cost:
                    new_cost = grid_cost[point]['cost'] + n_c # calculate new cost of reaching the location from where we are.
                    if (n_p not in grid_cost) or grid_cost[n_p]['cost'] > new_cost: # if an update is required
                        grid_cost[n_p] = {'cost' : new_cost, 'from' : point} # set the new cost and location
                        if new_cost in known_costs: # if we've already got the cost, then just add it to the frontier
                            frontier[new_cost].append(n_p)
                            continue
                        # we don't have this cost. insert it and create a new frontier
                        prev = smallest_cost
                        while True:
                            if (known_costs[prev] == -1) or (known_costs[prev] > new_cost):
                                known_costs[new_cost] = known_costs[prev]
                                known_costs[prev] = new_cost
                                break
                            prev = known_costs[prev]
                        frontier[new_cost] = [n_p]
        if len(frontier[smallest_cost]) == 0: # clear our smallest cost if appropriate.
            frontier.pop(smallest_cost)
            smallest_cost = known_costs.pop(smallest_cost)
    if end_location not in grid_cost:
        return []
    path = [end_location]
    try:
        while path[-1] != start_location:
            path.append(grid_cost[path[-1]]['from'])
    except Exception as exc:
        print(start_location)
        print(end_location)
        print(path)
        raise exc
    return list(reversed(path))
