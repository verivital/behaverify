

def x(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable x expected value between 0 and 9 inclusive but received value ' + str(new_value))


def y(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable y expected value between 0 and 9 inclusive but received value ' + str(new_value))


def target_x(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable target_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable target_x expected value between 0 and 9 inclusive but received value ' + str(new_value))


def target_y(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable target_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable target_y expected value between 0 and 9 inclusive but received value ' + str(new_value))


def mission(new_value):
    if not isinstance(new_value, bool):
        raise Exception('variable mission expected type bool but received type ' + str(type(new_value)))
    return new_value


def x_goal(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable x_goal expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable x_goal expected value between 0 and 9 inclusive but received value ' + str(new_value))


def y_goal(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable y_goal expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable y_goal expected value between 0 and 9 inclusive but received value ' + str(new_value))


def x_true(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable x_true expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable x_true expected value between 0 and 9 inclusive but received value ' + str(new_value))


def y_true(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable y_true expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 9:
        return new_value
    else:
        raise Exception('variable y_true expected value between 0 and 9 inclusive but received value ' + str(new_value))


def remaining_goals(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable remaining_goals expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 3:
        return new_value
    else:
        raise Exception('variable remaining_goals expected value between 0 and 3 inclusive but received value ' + str(new_value))
