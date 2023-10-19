class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def x_goal(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable x_goal expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 7:
        return new_value
    else:
        raise SereneAssignmentException('variable x_goal expected value between 0 and 7 inclusive but received value ' + str(new_value))


def y_goal(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable y_goal expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 7:
        return new_value
    else:
        raise SereneAssignmentException('variable y_goal expected value between 0 and 7 inclusive but received value ' + str(new_value))


def x_true(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable x_true expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 7:
        return new_value
    else:
        raise SereneAssignmentException('variable x_true expected value between 0 and 7 inclusive but received value ' + str(new_value))


def y_true(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable y_true expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 7:
        return new_value
    else:
        raise SereneAssignmentException('variable y_true expected value between 0 and 7 inclusive but received value ' + str(new_value))


def remaining_goals(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable remaining_goals expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 3:
        return new_value
    else:
        raise SereneAssignmentException('variable remaining_goals expected value between 0 and 3 inclusive but received value ' + str(new_value))
