

def fairness_counter(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable fairness_counter expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 4:
        return new_value
    else:
        raise Exception('variable fairness_counter expected value between 0 and 4 inclusive but received value ' + str(new_value))


def direction(new_value):
    if not isinstance(new_value, str):
        raise Exception('variable direction expected type str but received type ' + str(type(new_value)))
    if new_value in ['east_to_west', 'west_to_east']:
        return new_value
    else:
        raise Exception("variable direction expected value in ['east_to_west', 'west_to_east'] but received value '" + new_value + "'")


def tunnel_state(new_value):
    if not isinstance(new_value, str):
        raise Exception('variable tunnel_state expected type str but received type ' + str(type(new_value)))
    if new_value in ['empty', 'east_to_west', 'west_to_east']:
        return new_value
    else:
        raise Exception("variable tunnel_state expected value in ['empty', 'east_to_west', 'west_to_east'] but received value '" + new_value + "'")


def east_cars(new_value):
    if not isinstance(new_value, bool):
        raise Exception('variable east_cars expected type bool but received type ' + str(type(new_value)))
    return new_value


def west_cars(new_value):
    if not isinstance(new_value, bool):
        raise Exception('variable west_cars expected type bool but received type ' + str(type(new_value)))
    return new_value


def west_light(new_value):
    if not isinstance(new_value, bool):
        raise Exception('variable west_light expected type bool but received type ' + str(type(new_value)))
    return new_value


def east_light(new_value):
    if not isinstance(new_value, bool):
        raise Exception('variable east_light expected type bool but received type ' + str(type(new_value)))
    return new_value
