import random

battery = 10


def get_battery():
    global battery
    if random.choice((True, False)):
        battery = random.choice((battery, battery - 1))
        return (True, battery)
    else:
        return (False, battery)
