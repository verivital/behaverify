import sys
from create_grid import create_grid
from misc_util import create_tail_end, extract_info


def convert_table(file_name, max_val):
    action_map = {
        (sx, sy, ex, ey) : (0, 0)
        for sx in range(max_val + 1)
        for sy in range(max_val + 1)
        for ex in range(max_val + 1)
        for ey in range(max_val + 1)
    }
    convert_dir = {
        'left' : (-1, 0),
        'right' : (1, 0),
        'up' : (0, 1),
        'down' : (0, -1)
    }
    with open(file_name, 'r', encoding = 'utf-8') as table_file:
        for line in table_file:
            sx_min = None
            sx_max = None
            sy_min = None
            sy_max = None
            ex_min = None
            ex_max = None
            ey_min = None
            ey_max = None
            (info, result) = line.split('result')
            if info == '':
                continue
            info = info.split(',', 1)[1]
            info = info.replace('),', ')')
            while '(' in info:
                (cur_info, info) = info.split(')', 1)
                if 'eq' in cur_info:
                    val = int(cur_info.split(',')[-1].strip())
                    mode = 'eq'
                else:
                    try:
                        val = int(cur_info.split(',')[1].strip())
                        mode = 'min'
                    except:
                        val = int(cur_info.split(',')[-1].strip())
                        mode = 'max'
                if 'drone_x' in cur_info:
                    if mode == 'eq':
                        sx_min = val
                        sx_max = val
                    elif mode == 'min':
                        sx_min = val
                    elif mode == 'max':
                        sx_max = val
                if 'drone_y' in cur_info:
                    if mode == 'eq':
                        sy_min = val
                        sy_max = val
                    elif mode == 'min':
                        sy_min = val
                    elif mode == 'max':
                        sy_max = val
                if 'destination_x' in cur_info:
                    if mode == 'eq':
                        ex_min = val
                        ex_max = val
                    elif mode == 'min':
                        ex_min = val
                    elif mode == 'max':
                        ex_max = val
                if 'destination_y' in cur_info:
                    if mode == 'eq':
                        ey_min = val
                        ey_max = val
                    elif mode == 'min':
                        ey_min = val
                    elif mode == 'max':
                        ey_max = val
            result = convert_dir[result.split("'")[1]]
            for sx in range(sx_min, sx_max + 1):
                for sy in range(sy_min, sy_max + 1):
                    for ex in range(ex_min, ex_max + 1):
                        for ey in range(ey_min, ey_max + 1):
                            action_map[(sx, sy, ex, ey)] = result
    return action_map

def verify_table(table_file):
    (_, max_val, _, _, _) = extract_info(table_file)
    obstacle_file = table_file.replace('table', 'obstacles')
    grid = create_grid(obstacle_file, 0, max_val)
    action_map = convert_table(table_file, max_val)
    max_steps = 50
    print_mode = False
    for sx in range(max_val + 1):
        for sy in range(max_val + 1):
            if grid[sx][sy] == 1:
                continue
            for ex in range(max_val + 1):
                for ey in range(max_val + 1):
                    if grid[ex][ey] == 1 or (sx, sy) == (ex, ey):
                        if action_map[(sx, sy, ex, ey)] == (0, 0):
                            continue
                        else:
                            print('--------------------should be no action')
                            print((sx, sy, ex, ey))
                            print(action_map[(sx, sy, ex, ey)])
                        continue
                    print_mode = ((sx, sy, ex, ey) == (3, 9, 3, 1))
                    (cx, cy) = (sx, sy)
                    steps = 0
                    while (cx, cy) != (ex, ey):
                        (dx, dy) = action_map[(cx, cy, ex, ey)]
                        if print_mode:
                            print(str(steps) + ' : ' + str((cx, cy)) + ' -> ' + str((dx, dy)))
                        steps = steps + 1
                        if steps > max_steps:
                            print('--------------------TOO LONG')
                            print((sx, sy, ex, ey))
                            print((cx, cy))
                            print((dx, dy))
                            break
                        cx = cx + dx
                        cy = cy + dy
    
if __name__ == '__main__':
    verify_table(sys.argv[1])
