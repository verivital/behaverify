class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def tiles(new_values):
    def tiles__internal_type_check(new_value):
        if not isinstance(new_value, str):
            raise SereneAssignmentException('variable tiles expected type str but received type ' + str(type(new_value)))
        if new_value in ['unknown', 'safe', 'hole', 'goal']:
            return new_value
        else:
            raise SereneAssignmentException("variable tiles expected value in ['unknown', 'safe', 'hole', 'goal'] but received value '" + new_value + "'")

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise SereneAssignmentException('Index must be an int when accessing tiles: ' + str(type(index)))
        if index < 0 or index >= 16:
            raise SereneAssignmentException('Index out of bounds when accessing tiles: ' + str(index))
        checked_value = tiles__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def action(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable action expected type int but received type ' + str(type(new_value)))
    if new_value in [-2, -1, 0, 1, 2, 3]:
        return new_value
    else:
        raise SereneAssignmentException("variable action expected value in [-2, -1, 0, 1, 2, 3] but received value '" + new_value + "'")


def sometimes(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable sometimes expected type bool but received type ' + str(type(new_value)))
    return new_value


def strategy(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable strategy expected type str but received type ' + str(type(new_value)))
    if new_value in ['x_first', 'y_first']:
        return new_value
    else:
        raise SereneAssignmentException("variable strategy expected value in ['x_first', 'y_first'] but received value '" + new_value + "'")


def subgoal(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable subgoal expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 15:
        return new_value
    else:
        raise SereneAssignmentException('variable subgoal expected value between 0 and 15 inclusive but received value ' + str(new_value))


def start_loc(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable start_loc expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 15:
        return new_value
    else:
        raise SereneAssignmentException('variable start_loc expected value between 0 and 15 inclusive but received value ' + str(new_value))


def goal_loc(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable goal_loc expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 15:
        return new_value
    else:
        raise SereneAssignmentException('variable goal_loc expected value between 0 and 15 inclusive but received value ' + str(new_value))


def loc(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable loc expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 15:
        return new_value
    else:
        raise SereneAssignmentException('variable loc expected value between 0 and 15 inclusive but received value ' + str(new_value))


def hole_loc(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable hole_loc expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 15:
        return new_value
    else:
        raise SereneAssignmentException('variable hole_loc expected value between 0 and 15 inclusive but received value ' + str(new_value))


def falls_remaining(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable falls_remaining expected type int but received type ' + str(type(new_value)))
    if new_value >= -1 and new_value <= 1:
        return new_value
    else:
        raise SereneAssignmentException('variable falls_remaining expected value between -1 and 1 inclusive but received value ' + str(new_value))
