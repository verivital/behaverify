'''
Basic A* algorithm. Allows for variable costs. Assumes all costs are non-negative.
Serena Serafina Serbinowska
'''
def a_star(function_obstacle_at_point, function_cost, flight_heights, start_location, end_location):
    '''
    function_obstacle_at_point will be used to determine if a point is safe (this should be created using partial function_obstacle_at_point(map_info, obstacle_map) )
    function_cost will compute the cost of moving from one cell to another (will not check for obstacles)
    flight_heights is a list of heights to try flying at
    start_location and end_location must be of form (x, y, z)
    '''
    if function_obstacle_at_point(start_location) or function_obstacle_at_point(end_location):
        # can't get anywhere. Return
        return []
    # grid_cost = {point : {'cost' : -1, 'from' : None} for point in grid}
    grid_cost = {}
    grid_cost[start_location] = {'cost' : 0, 'from' : {start_location}}
    smallest_cost = 0
    known_costs = {0 : -1} #each value points to the next smallest known cost. if something points to -1, it is the last value.
    frontier = {0 : [start_location]}
    #while len(frontier) > 0 and ((grid_cost[end_location]['cost'] == -1) or (smallest_cost < grid_cost[end_location]['cost'])):
    while len(frontier) > 0 and ((end_location not in grid_cost) or (smallest_cost < grid_cost[end_location]['cost'])):
        point = frontier[smallest_cost].pop() # we are going to explore from this point.
        if smallest_cost <= grid_cost[point]['cost']: # if the cost of getting to this location is not more expensive than the current known cost, explore (note that the default value of -1 is not relevant, because if we're exploring from this location than we must have reached this point so it has a non-negative cost)
            adj_cost = [
                ((point[0] + x_mod, point[1] + y_mod, z), function_cost(point, (point[0] + x_mod, point[1] + y_mod, z)))
                for x_mod in (-1, 0, 1)
                for y_mod in (-1, 0, 1)
                for z in flight_heights
                if (
                        (x_mod != 0 or y_mod !=0 or z != point[2]) and
                        (z == point[2] or (x_mod == 0 and y_mod == 0)) and
                        not function_obstacle_at_point((point[0] + x_mod, point[1] + y_mod, z))
                )
            ]
            for (n_p, n_c) in adj_cost:
                new_cost = grid_cost[point]['cost'] + n_c # calculate new cost of reaching the location from where we are.
                added = False
                if (n_p not in grid_cost) or grid_cost[n_p]['cost'] > new_cost: # if an update is required
                    grid_cost[n_p] = {'cost' : new_cost, 'from' : {point}} # set the new cost and location
                    added = True
                elif grid_cost[n_p]['cost'] == new_cost:
                    grid_cost[n_p]['from'].add(point)
                    added = True
                if added:
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
