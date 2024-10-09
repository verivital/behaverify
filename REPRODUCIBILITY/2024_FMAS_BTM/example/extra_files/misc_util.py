import os
def create_tail_end(max_val, fly_at, number_of_obstacles, max_size):
    return (
        '_' + str(max_val)
        + (
            ''
            if fly_at is None else
            (
                '_'
                + (
                    str(fly_at)
                    if fly_at >= 10 else
                    ('0' + str(fly_at))
                )
            )
        )
        + '_' + str(number_of_obstacles) + '_' + str(max_size)
    )

def extract_info(the_path):
    obstacle_path_split = the_path.split('/')[-1].split('.')[0].split('_')
    if len(obstacle_path_split) == 5:
        (_, max_val, fly_at, number_of_obstacles, max_size) = obstacle_path_split
        number_of_obstacles = int(number_of_obstacles)
        min_val = 0
        max_val = int(max_val)
        max_size = int(max_size)
        fly_at = int(fly_at)
    elif len(obstacle_path_split) == 4:
        (_, max_val, number_of_obstacles, max_size) = obstacle_path_split
        number_of_obstacles = int(number_of_obstacles)
        min_val = 0
        max_val = int(max_val)
        max_size = int(max_size)
        fly_at = None
    else:
        print(obstacle_path_split)
        raise ValueError('file is named in a weird way')
    return (min_val, max_val, fly_at, number_of_obstacles, max_size)

def handle_path(file_name_with_ext):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, file_name_with_ext)
