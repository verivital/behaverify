import random

state = {'x' : random.randint(0, 4),
         'y' : random.randint(0, 4),
         'target_x' :  random.randint(0, 4),
         'target_y' :  random.randint(0, 4),
         'missions_remaining' : random.randint(1, 10)}


def get_mission():
    if random.choice([True, False]):
        return (True, state['target_x'], state['target_y'])
    else:
        return (False, random.randint(0, 4), random.randint(0, 4))


def get_position():
    return (True, state['x'], state['y'])


def go_x(val):
    state['x'] = state['x'] + val
    check_completion()
    return


def go_y(val):
    state['y'] = state['y'] + val
    check_completion()
    return


def check_completion():
    if state['missions_remaining'] >= 0:
        if state['x'] == state['target_x'] and state['y'] == state['target_y']:
            state['missions_remaining'] = state['missions_remaining'] - 1
            state['target_x'] = random.randint(0, 4)
            state['target_y'] = random.randint(0, 4)
    return
