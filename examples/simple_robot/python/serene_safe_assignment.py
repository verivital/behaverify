def index_func(index, array_size):
    if type(index) is not int:
        raise TypeError('Array index must be an int')
    if index < 0 or index >= array_size:
        raise ValueError('Array index out of bounds')
    return index



def x_true(new_value):
    if type(new_value) is not int:
        raise TypeError('variable x_true expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable x_true expected value between 0 and 10 inclusive but received value ' + str(new_value))


def y_true(new_value):
    if type(new_value) is not int:
        raise TypeError('variable y_true expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable y_true expected value between 0 and 10 inclusive but received value ' + str(new_value))


def x_goal(new_value):
    if type(new_value) is not int:
        raise TypeError('variable x_goal expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable x_goal expected value between 0 and 10 inclusive but received value ' + str(new_value))


def y_goal(new_value):
    if type(new_value) is not int:
        raise TypeError('variable y_goal expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable y_goal expected value between 0 and 10 inclusive but received value ' + str(new_value))


def remaining_goals(new_value):
    if type(new_value) is not int:
        raise TypeError('variable remaining_goals expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 3:
        return new_value
    else:
        raise ValueError('variable remaining_goals expected value between 0 and 3 inclusive but received value ' + str(new_value))


def goal_reached(new_value):
    if type(new_value) is not bool:
        raise TypeError('variable goal_reached expected type bool but received type ' + str(type(new_value)))
    return new_value
