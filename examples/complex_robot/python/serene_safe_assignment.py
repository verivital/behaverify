class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def zone(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable zone expected type str but received type ' + str(type(new_value)))
    if new_value in ['home', 'maze', 'target']:
        return new_value
    else:
        raise SereneAssignmentException("variable zone expected value in ['home', 'maze', 'target'] but received value '" + new_value + "'")


def side(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable side expected type int but received type ' + str(type(new_value)))
    if new_value in [-1, 1]:
        return new_value
    else:
        raise SereneAssignmentException("variable side expected value in [-1, 1] but received value '" + new_value + "'")


def have_flag(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable have_flag expected type bool but received type ' + str(type(new_value)))
    return new_value


def need_side_reached(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable need_side_reached expected type bool but received type ' + str(type(new_value)))
    return new_value


def tile_searched(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable tile_searched expected type bool but received type ' + str(type(new_value)))
    return new_value


def will_collide(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable will_collide expected type bool but received type ' + str(type(new_value)))
    return new_value


def x(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 18:
        return new_value
    else:
        raise SereneAssignmentException('variable x expected value between 0 and 18 inclusive but received value ' + str(new_value))


def y(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable y expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_1(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_1 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_1 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_2(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_2 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_2 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_3(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_3 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_3 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_4(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_4 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_4 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_5(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_5 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_5 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_6(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_6 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_6 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_7(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_7 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_7 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_8(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_8 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_8 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def hole_9(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_9 expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_9 expected value between 0 and 2 inclusive but received value ' + str(new_value))


def flag_x(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable flag_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 15 and new_value <= 18:
        return new_value
    else:
        raise SereneAssignmentException('variable flag_x expected value between 15 and 18 inclusive but received value ' + str(new_value))


def flag_y(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable flag_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable flag_y expected value between 0 and 2 inclusive but received value ' + str(new_value))


def tile_progress(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable tile_progress expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable tile_progress expected value between 0 and 2 inclusive but received value ' + str(new_value))


def tile_tracker(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable tile_tracker expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable tile_tracker expected value between 0 and 2 inclusive but received value ' + str(new_value))
