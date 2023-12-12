def index_func(index, array_size):
    if type(index) is not int:
        raise TypeError('Array index must be an int')
    if index < 0 or index >= array_size:
        raise ValueError('Array index out of bounds')
    return index



def cur_x(new_value):
    if type(new_value) is not int:
        raise TypeError('variable cur_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable cur_x expected value between 0 and 10 inclusive but received value ' + str(new_value))


def cur_y(new_value):
    if type(new_value) is not int:
        raise TypeError('variable cur_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable cur_y expected value between 0 and 10 inclusive but received value ' + str(new_value))


def dest_x(new_value):
    if type(new_value) is not int:
        raise TypeError('variable dest_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable dest_x expected value between 0 and 10 inclusive but received value ' + str(new_value))


def dest_y(new_value):
    if type(new_value) is not int:
        raise TypeError('variable dest_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable dest_y expected value between 0 and 10 inclusive but received value ' + str(new_value))


def x_mode(new_value):
    if type(new_value) is not bool:
        raise TypeError('variable x_mode expected type bool but received type ' + str(type(new_value)))
    return new_value


def y_dir(new_value):
    if type(new_value) is not int:
        raise TypeError('variable y_dir expected type int but received type ' + str(type(new_value)))
    if new_value in [(-1), 1]:
        return new_value
    else:
        raise ValueError("variable y_dir expected value in [(-1), 1] but received value " + str(new_value))


def victory(new_value):
    if type(new_value) is not bool:
        raise TypeError('variable victory expected type bool but received type ' + str(type(new_value)))
    return new_value


def tar_x(new_value):
    if type(new_value) is not int:
        raise TypeError('variable tar_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable tar_x expected value between 0 and 10 inclusive but received value ' + str(new_value))


def tar_y(new_value):
    if type(new_value) is not int:
        raise TypeError('variable tar_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable tar_y expected value between 0 and 10 inclusive but received value ' + str(new_value))


def timer(new_value):
    if type(new_value) is not int:
        raise TypeError('variable timer expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise ValueError('variable timer expected value between 0 and 10 inclusive but received value ' + str(new_value))
