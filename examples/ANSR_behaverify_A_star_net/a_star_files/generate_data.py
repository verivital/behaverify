import os
import sys
import itertools
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
                    iteration = iteration + 1
                    if (start_x, start_y, end_x, end_y) in seen_values:
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
                        no_action.add((start_x, start_y, end_x, end_y))
                        seen_values.add((start_x, start_y, end_x, end_y))
                    else:
                        for index in range(len(path) - 1):
                            if (path[index], path[-1]) in seen_values:
                                continue
                            seen_values.add((*path[index], *path[-1]))
                            if path[index][0] < path[index + 1][0] and path[index][1] == path[index + 1][1]:
                                right.add((path[index][0], path[index][1], end_x, end_y))
                            elif path[index][0] > path[index + 1][0] and path[index][1] == path[index + 1][1]:
                                left.add((path[index][0], path[index][1], end_x, end_y))
                            elif path[index][0] == path[index + 1][0] and path[index][1] < path[index + 1][1]:
                                up.add((path[index][0], path[index][1], end_x, end_y))
                            elif path[index][0] == path[index + 1][0] and path[index][1] > path[index + 1][1]:
                                down.add((path[index][0], path[index][1], end_x, end_y))
                            else:
                                print('unknown direction')
                                print('from: ' + path[index])
                                print('to: ' + path[index + 1])
                                print('adding to no_action')
                                no_action.add((path[index][0], path[index][1], end_x, end_y))
    return (left, right, up, down, no_action, grid) if return_grid else (left, right, up, down, no_action)

def check_all_points_in_region(cur_set, min_vals, max_vals):
    for s_x in range(min_vals[0], max_vals[0] + 1):
        for s_y in range(min_vals[1], max_vals[1] + 1):
            for e_x in range(min_vals[2], max_vals[2] + 1):
                for e_y in range(min_vals[3], max_vals[3] + 1):
                    if (s_x, s_y, e_x, e_y) not in cur_set:
                        return False
    return True

def remove_all_points_in_region(cur_set, min_vals, max_vals):
    for s_x in range(min_vals[0], max_vals[0] + 1):
        for s_y in range(min_vals[1], max_vals[1] + 1):
            for e_x in range(min_vals[2], max_vals[2] + 1):
                for e_y in range(min_vals[3], max_vals[3] + 1):
                    cur_set.remove((s_x, s_y, e_x, e_y))

def maximize_dimensions(cur_set, centered_at, dim_order = (0, 1, 2, 3)):
    (s_x, s_y, e_x, e_y) = centered_at
    default_vals = [s_x, s_y, e_x, e_y]
    min_vals = [None, None, None, None]
    max_vals = [None, None, None, None]
    for index in dim_order:
        cur_lb = []
        cur_ub = []
        for sub_index in range(4):
            cur_lb.append(default_vals[sub_index] if min_vals[sub_index] is None else min_vals[sub_index])
            cur_ub.append(default_vals[sub_index] if max_vals[sub_index] is None else max_vals[sub_index])
        cur_lb[index] -= 1
        cur_ub[index] -= 1
        while check_all_points_in_region(cur_set, cur_lb, cur_ub):
            cur_lb[index] -= 1
            cur_ub[index] -= 1
        min_val = cur_lb[index] + 1
        cur_lb = []
        cur_ub = []
        for sub_index in range(4):
            cur_lb.append(default_vals[sub_index] if min_vals[sub_index] is None else min_vals[sub_index])
            cur_ub.append(default_vals[sub_index] if max_vals[sub_index] is None else max_vals[sub_index])
        cur_lb[index] += 1
        cur_ub[index] += 1
        while check_all_points_in_region(cur_set, cur_lb, cur_ub):
            cur_lb[index] += 1
            cur_ub[index] += 1
        max_val = cur_ub[index] - 1
        min_vals[index] = min_val
        max_vals[index] = max_val
    return (tuple(min_vals), tuple(max_vals))

def calc_size(min_vals, max_vals):
    size = 1
    for index in range(len(min_vals)):
        size = size * (1 + max_vals[index] - min_vals[index])
    return size

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

def simplify_set2(cur_set):
    print('original: ' + str(len(cur_set)))
    new_set = set()
    while len(cur_set) > 0:
        centered_at = cur_set.pop()
        cur_set.add(centered_at)
        biggest_size = 0
        best_min_vals = None
        best_max_vals = None
        for permutation in itertools.permutations((0, 1, 2, 3)):
            (min_vals, max_vals) = maximize_dimensions(cur_set, centered_at, dim_order = permutation)
            cur_size = calc_size(min_vals, max_vals)
            if cur_size > biggest_size:
                biggest_size = cur_size
                best_min_vals = min_vals
                best_max_vals = max_vals
        new_set.add((best_min_vals, best_max_vals))
        remove_all_points_in_region(cur_set, best_min_vals, best_max_vals)
    print('new: ' + str(len(new_set)))
    return new_set

def find_best_split(contiguous_set, split_index, min_vals, max_vals):
    totals_per_slice = {
        slice_index : {'in' : 0, 'out' : 0}
        for slice_index in range(min_vals[split_index], max_vals[split_index] + 1)
    }
    left_totals = {'in' : 0, 'out' : 0}
    right_totals = {'in' : 0, 'out' : 0}
    for s_x in range(min_vals[0], max_vals[0] + 1):
        for s_y in range(min_vals[1], max_vals[1] + 1):
            for e_x in range(min_vals[2], max_vals[2] + 1):
                for e_y in range(min_vals[3], max_vals[3] + 1):
                    slice_index = s_x if split_index == 0 else (s_y if split_index == 1 else (e_x if split_index == 2 else e_y))
                    if (s_x, s_y, e_x, e_y) in contiguous_set:
                        totals_per_slice[slice_index]['in'] += 1
                        right_totals['in'] += 1
                    else:
                        totals_per_slice[slice_index]['out'] += 1
                        right_totals['out'] += 1
    cur_max = None
    best_split_point = None
    for slice_index in range(min_vals[split_index], max_vals[split_index]): # intentionally leaves one out.
        left_totals['in'] += totals_per_slice[slice_index]['in']
        left_totals['out'] += totals_per_slice[slice_index]['out']
        right_totals['in'] -= totals_per_slice[slice_index]['in']
        right_totals['out'] -= totals_per_slice[slice_index]['out']
        split_score = abs(left_totals['in'] - right_totals['out']) + abs(left_totals['out'] - right_totals['in'])
        if cur_max is None or split_score < cur_max:
            cur_max = split_score
            best_split_point = slice_index
    return (cur_max, best_split_point)

def find_contiguous_region(cur_set, point):
    to_explore_from = {point}
    contiguous_set = {point}
    adj_vals = (-1, 0, 1)
    min_vals = [None, None, None, None]
    max_vals = [None, None, None, None]
    while len(to_explore_from) > 0:
        (s_x, s_y, e_x, e_y) = to_explore_from.pop()
        for m0 in adj_vals:
            for m1 in adj_vals:
                for m2 in adj_vals:
                    for m3 in adj_vals:
                        cur_point = (s_x + m0, s_y + m1, e_x + m2, e_y + m3)
                        if cur_point in cur_set and cur_point not in contiguous_set:
                            contiguous_set.add(cur_point)
                            to_explore_from.add(cur_point)
                            for index in range(4):
                                if min_vals[index] is None or cur_point[index] < min_vals[index]:
                                    min_vals[index] = cur_point[index]
                                if max_vals[index] is None or cur_point[index] > max_vals[index]:
                                    max_vals[index] = cur_point[index]
    return (contiguous_set, tuple(min_vals), tuple(max_vals))

def region_uniform(contiguous_set, min_vals, max_vals):
    all_in = True
    all_out = True
    for s_x in range(min_vals[0], max_vals[0] + 1):
        for s_y in range(min_vals[1], max_vals[1] + 1):
            for e_x in range(min_vals[2], max_vals[2] + 1):
                for e_y in range(min_vals[3], max_vals[3] + 1):
                    in_set = (s_x, s_y, e_x, e_y) in contiguous_set
                    all_in = all_in and in_set
                    all_out = all_out and (not in_set)
                    if (not all_in) and (not all_out):
                        return (all_in, all_out)
    return (all_in, all_out)

def describe_contiguous_region(contiguous_set, min_vals, max_vals):
    (all_in, all_out) = region_uniform(contiguous_set, min_vals, max_vals)
    if all_in:
        return {(min_vals, max_vals)}
    if all_out:
        return set()
    cur_max = None
    best_split_index = None
    best_split_point = None
    for split_index in range(len(min_vals)):
        if min_vals[split_index] == max_vals[split_index]:
            continue
        (split_score, split_point) = find_best_split(contiguous_set, split_index, min_vals, max_vals)
        if cur_max is None or cur_max < split_score:
            cur_max = split_score
            best_split_index = split_index
            best_split_point = split_point
    left_max_vals = [max_vals[index] for index in range(len(max_vals))]
    right_min_vals = [min_vals[index] for index in range(len(min_vals))]
    left_max_vals[best_split_index] = best_split_point
    right_min_vals[best_split_index] = best_split_point + 1
    left_set = describe_contiguous_region(contiguous_set, min_vals, tuple(left_max_vals))
    right_set = describe_contiguous_region(contiguous_set, tuple(right_min_vals), max_vals)
    return left_set.union(right_set)

def simplify_set_new(cur_set):
    print('original: ' + str(len(cur_set)))
    new_set = set()
    while len(cur_set) > 0:
        centered_at = cur_set.pop()
        cur_set.add(centered_at)
        (contiguous_set, min_vals, max_vals) = find_contiguous_region(cur_set, centered_at)
        cur_set.difference_update(contiguous_set)
        new_set.update(describe_contiguous_region(contiguous_set, min_vals, max_vals))
    print('new: ' + str(len(new_set)))
    return new_set


def simplify_sets_mid(original_sets, split_index, min_vals, max_vals):
    index = 0
    cur_set = set()
    for cur_set in original_sets: # this loop is used to set cur_set
        if ((min_vals[0], min_vals[1]), (min_vals[2], min_vals[3])) in cur_set:
            break
        index = index + 1
    if check_all_points_in_region(cur_set, min_vals, max_vals):
        # region is uniform! Done.
        new_sets = [set() for _ in range(5)]
        new_sets[index].add((min_vals, max_vals))
        return new_sets
    if min_vals[split_index] == max_vals[split_index]:
        return simplify_sets_mid(original_sets, (split_index + 1) % 4, min_vals, max_vals)
    # region is not uniform, and we can split on this dimension.
    split_point = (min_vals[split_index] + max_vals[split_index]) // 2
    left_max_vals = [max_vals[index] for index in range(len(max_vals))]
    right_min_vals = [min_vals[index] for index in range(len(min_vals))]
    left_max_vals[split_index] = split_point
    right_min_vals[split_index] = split_point + 1
    left_sets = simplify_sets_mid(original_sets, (split_index + 1) % 4, min_vals, tuple(left_max_vals))
    right_sets = simplify_sets_mid(original_sets, (split_index + 1) % 4, tuple(right_min_vals), max_vals)
    return [left_sets[index].union(right_sets[index]) for index in range(len(original_sets))]

def simplify_sets_find(original_sets, split_index, min_vals, max_vals):
    # print((min_vals, max_vals))
    index = 0
    cur_set = set()
    for cur_set in original_sets: # this loop is used to set cur_set
        if ((min_vals[0], min_vals[1]), (min_vals[2], min_vals[3])) in cur_set:
            break
        index = index + 1
    if check_all_points_in_region(cur_set, min_vals, max_vals):
        # region is uniform! Done.
        new_sets = [set() for _ in range(5)]
        new_sets[index].add((min_vals, max_vals))
        # print('terminated!')
        return new_sets
    if min_vals[split_index] == max_vals[split_index]:
        fixed_issue = False
        for shift_by in range(len(min_vals)):
            if min_vals[(split_index + shift_by) % 4] != max_vals[(split_index + shift_by) % 4]:
                split_index = (split_index + shift_by) % 4
                fixed_issue = True
                break
        if not fixed_issue:
            raise RuntimeError('a single point is somehow not within its own region')
    # region is not uniform, and we can split on this dimension.
    cur_point = [min_vals[index] for index in range(len(min_vals))]
    split_point = min_vals[split_index]
    while ((cur_point[0], cur_point[1]), (cur_point[2], cur_point[3])) in cur_set:
        split_point = split_point + 1
        if split_point >= max_vals[split_index]:
            # print('forced split')
            split_point = ((min_vals[split_index] + max_vals[split_index]) // 2) + 1
            break
        cur_point[split_index] = split_point
    left_max_vals = [max_vals[index] for index in range(len(max_vals))]
    right_min_vals = [min_vals[index] for index in range(len(min_vals))]
    left_max_vals[split_index] = split_point - 1
    right_min_vals[split_index] = split_point
    left_sets = simplify_sets_find(original_sets, (split_index + 1) % 4, min_vals, tuple(left_max_vals))
    right_sets = simplify_sets_find(original_sets, (split_index + 1) % 4, tuple(right_min_vals), max_vals)
    return [left_sets[index].union(right_sets[index]) for index in range(len(original_sets))]

def eval_split(original_sets, min_vals, left_max_vals, right_min_vals, max_vals):
    set_pairs = ((original_sets[0], 'left'), (original_sets[1], 'right'), (original_sets[2], 'up'), (original_sets[3], 'down'), (original_sets[4], 'no_action'))
    left_totals = {'left' : 0, 'right' : 0, 'up' : 0, 'down' : 0, 'no_action' : 0}
    for s_x in range(min_vals[0], left_max_vals[0] + 1):
        for s_y in range(min_vals[1], left_max_vals[1] + 1):
            for e_x in range(min_vals[2], left_max_vals[2] + 1):
                for e_y in range(min_vals[3], left_max_vals[3] + 1):
                    for (cur_set, cur_key) in set_pairs:
                        if (s_x, s_y ,e_x, e_y) in cur_set:
                            left_totals[cur_key] += 1
                            break
    right_totals = {'left' : 0, 'right' : 0, 'up' : 0, 'down' : 0, 'no_action' : 0}
    for s_x in range(right_min_vals[0], max_vals[0] + 1):
        for s_y in range(right_min_vals[1], max_vals[1] + 1):
            for e_x in range(right_min_vals[2], max_vals[2] + 1):
                for e_y in range(right_min_vals[3], max_vals[3] + 1):
                    for (cur_set, cur_key) in set_pairs:
                        if (s_x, s_y, e_x, e_y) in cur_set:
                            right_totals[cur_key] += 1
                            break
    split_score = 0
    for cur_key in left_totals:
        split_score += left_totals[cur_key] * right_totals[cur_key]
    return split_score

def find_best_split_for_index(original_sets, split_index, min_vals, max_vals):
    set_pairs = ((original_sets[0], 'left'), (original_sets[1], 'right'), (original_sets[2], 'up'), (original_sets[3], 'down'), (original_sets[4], 'no_action'))
    totals_per_slice = {
        slice_index : {'left' : 0, 'right' : 0, 'up' : 0, 'down' : 0, 'no_action' : 0}
        for slice_index in range(min_vals[split_index], max_vals[split_index] + 1)
    }
    left_totals = {'left' : 0, 'right' : 0, 'up' : 0, 'down' : 0, 'no_action' : 0}
    right_totals = {'left' : 0, 'right' : 0, 'up' : 0, 'down' : 0, 'no_action' : 0}
    for s_x in range(min_vals[0], max_vals[0] + 1):
        for s_y in range(min_vals[1], max_vals[1] + 1):
            for e_x in range(min_vals[2], max_vals[2] + 1):
                for e_y in range(min_vals[3], max_vals[3] + 1):
                    slice_index = s_x if split_index == 0 else (s_y if split_index == 1 else (e_x if split_index == 2 else e_y))
                    for (cur_set, cur_key) in set_pairs:
                        if (s_x, s_y, e_x, e_y) in cur_set:
                            totals_per_slice[slice_index][cur_key] += 1
                            right_totals[cur_key] += 1
                            break
    # totals = {}
    # for cur_key in right_totals:
    #     totals[cur_key] = right_totals[cur_key]
    cur_max = None
    best_split_point = None
    mid_point = (min_vals[split_index] + max_vals[split_index]) // 2
    for slice_index in range(min_vals[split_index], max_vals[split_index]): # intentionally leaves one out.
        split_score = 0
        # split_score = None
        for cur_key in left_totals:
            # if totals[cur_key] == 0:
            #     continue
            left_totals[cur_key] += totals_per_slice[slice_index][cur_key]
            right_totals[cur_key] -= totals_per_slice[slice_index][cur_key]
            split_score += abs(left_totals[cur_key] - right_totals[cur_key])
            # cur_score = left_totals[cur_key] * right_totals[cur_key]
            # if split_score is None or cur_score < split_score:
            #     split_score = cur_score
        if cur_max is None or split_score < cur_max or (split_score == cur_max and (abs(mid_point - slice_index) < abs(mid_point - slice_index))):
            cur_max = split_score
            best_split_point = slice_index
    return (cur_max, best_split_point)

def simplify_sets_optimal(original_sets, min_vals, max_vals):
    print((min_vals, max_vals))
    index = 0
    cur_set = set()
    for cur_set in original_sets: # this loop is used to set cur_set
        if (min_vals[0], min_vals[1], min_vals[2], min_vals[3]) in cur_set:
            break
        index = index + 1
    if check_all_points_in_region(cur_set, min_vals, max_vals):
        # region is uniform! Done.
        new_sets = [set() for _ in range(5)]
        new_sets[index].add((min_vals, max_vals))
        # print('terminated!')
        return new_sets
    cur_max = None
    best_split_index = None
    best_split_point = None
    for split_index in range(len(min_vals)):
        if min_vals[split_index] == max_vals[split_index]:
            continue
        (split_score, split_point) = find_best_split_for_index(original_sets, split_index, min_vals, max_vals)
        if cur_max is None or cur_max < split_score :
            cur_max = split_score
            best_split_index = split_index
            best_split_point = split_point
    # for split_index in range(len(min_vals)):
    #     if min_vals[split_index] == max_vals[split_index]:
    #         continue
    #     left_max_vals = [max_vals[index] for index in range(len(max_vals))]
    #     right_min_vals = [min_vals[index] for index in range(len(min_vals))]
    #     for split_point in range(min_vals[split_index], max_vals[split_index]):
    #         left_max_vals[split_index] = split_point
    #         right_min_vals[split_index] = split_point + 1
    #         split_score = eval_split(original_sets, min_vals, left_max_vals, right_min_vals, max_vals)
    #         if best_split_point is None:
    #             cur_min = split_score
    #             best_split_point = split_point
    #             best_split_index = split_index
    #         elif split_score < cur_min:
    #             cur_min = split_score
    #             best_split_point = split_point
    #             best_split_index = split_index
    left_max_vals = [max_vals[index] for index in range(len(max_vals))]
    right_min_vals = [min_vals[index] for index in range(len(min_vals))]
    left_max_vals[best_split_index] = best_split_point
    right_min_vals[best_split_index] = best_split_point + 1
    left_sets = simplify_sets_optimal(original_sets, min_vals, tuple(left_max_vals))
    right_sets = simplify_sets_optimal(original_sets, tuple(right_min_vals), max_vals)
    return [left_sets[index].union(right_sets[index]) for index in range(len(original_sets))]


def generate_table_new(min_val, max_val, input_path, output_path):
    (left, right, up, down, no_action) = generate_sets(min_val, max_val, input_path)
    print('--------------------')
    print(len(left))
    print(len(right))
    print(len(up))
    print(len(down))
    print(len(no_action))
    #(left, right, up, down, no_action) = simplify_sets_find((left, right, up, down, no_action), 0, tuple([min_val]*4), tuple([max_val]*4))
    (left, right, up, down, no_action) = simplify_sets_optimal((left, right, up, down, no_action), tuple([min_val]*4), tuple([max_val]*4))
    print('--------------------')
    print(len(left))
    print(len(right))
    print(len(up))
    print(len(down))
    print(len(no_action))
    lines = []
    #for (cur_set, direction) in ((left, 'left'), (right, 'right'), (up, 'up'), (down, 'down'), (no_action, 'no_action')):
    for (cur_set, direction) in ((left, 'left'), (right, 'right'), (up, 'up'), (down, 'down')):
        for ((min_s_x, min_s_y, min_e_x, min_e_y), (max_s_x, max_s_y, max_e_x, max_e_y)) in cur_set:
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
        for ((min_s_x, min_s_y, min_e_x, min_e_y), (max_s_x, max_s_y, max_e_x, max_e_y)) in new_set:
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
        for (s_x, s_y, e_x, e_y) in cur_set:
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
    # sys.setrecursionlimit(100000)
    generate_table(0, 29, 'ignore/obstacles_29_30_2.txt', 'ignore/curTable_29_30_2.txt')
    # generate_table_new(0, 29, 'ignore/obstacles_29_30_2.txt', 'ignore/newTable_29_30_2.txt')
