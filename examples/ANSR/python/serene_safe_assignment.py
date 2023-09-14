class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def prev_dest_x(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable prev_dest_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable prev_dest_x expected value between 0 and 10 inclusive but received value ' + str(new_value))


def prev_dest_y(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable prev_dest_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable prev_dest_y expected value between 0 and 10 inclusive but received value ' + str(new_value))


def cur_x(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable cur_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable cur_x expected value between 0 and 10 inclusive but received value ' + str(new_value))


def cur_y(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable cur_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable cur_y expected value between 0 and 10 inclusive but received value ' + str(new_value))


def dest_x(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable dest_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable dest_x expected value between 0 and 10 inclusive but received value ' + str(new_value))


def dest_y(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable dest_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable dest_y expected value between 0 and 10 inclusive but received value ' + str(new_value))


def dir(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable dir expected type int but received type ' + str(type(new_value)))
    if new_value in [-1, 1]:
        return new_value
    else:
        raise SereneAssignmentException("variable dir expected value in [-1, 1] but received value '" + new_value + "'")


def victory(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable victory expected type bool but received type ' + str(type(new_value)))
    return new_value


def tree_x(new_values):
    def tree_x__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise SereneAssignmentException('variable tree_x expected type int but received type ' + str(type(new_value)))
        if new_value >= 0 and new_value <= 10:
            return new_value
        else:
            raise SereneAssignmentException('variable tree_x expected value between 0 and 10 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise SereneAssignmentException('Index must be an int when accessing tree_x: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise SereneAssignmentException('Index out of bounds when accessing tree_x: ' + str(index))
        checked_value = tree_x__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def tree_y(new_values):
    def tree_y__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise SereneAssignmentException('variable tree_y expected type int but received type ' + str(type(new_value)))
        if new_value >= 0 and new_value <= 10:
            return new_value
        else:
            raise SereneAssignmentException('variable tree_y expected value between 0 and 10 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise SereneAssignmentException('Index must be an int when accessing tree_y: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise SereneAssignmentException('Index out of bounds when accessing tree_y: ' + str(index))
        checked_value = tree_y__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def tar_x(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable tar_x expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable tar_x expected value between 0 and 10 inclusive but received value ' + str(new_value))


def tar_y(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable tar_y expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise SereneAssignmentException('variable tar_y expected value between 0 and 10 inclusive but received value ' + str(new_value))


def timer(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable timer expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 5:
        return new_value
    else:
        raise SereneAssignmentException('variable timer expected value between 0 and 5 inclusive but received value ' + str(new_value))
