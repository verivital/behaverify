class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def blVAR0(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable blVAR0 expected type int but received type ' + str(type(new_value)))
    if new_value >= 2 and new_value <= 5:
        return new_value
    else:
        raise SereneAssignmentException('variable blVAR0 expected value between 2 and 5 inclusive but received value ' + str(new_value))


def envVAR1(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable envVAR1 expected type bool but received type ' + str(type(new_value)))
    return new_value


def envVAR2(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable envVAR2 expected type str but received type ' + str(type(new_value)))
    if new_value in ['yes', 'no', 'both']:
        return new_value
    else:
        raise SereneAssignmentException("variable envVAR2 expected value in ['yes', 'no', 'both'] but received value '" + new_value + "'")


def blVAR3(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable blVAR3 expected type int but received type ' + str(type(new_value)))
    if new_value >= 2 and new_value <= 5:
        return new_value
    else:
        raise SereneAssignmentException('variable blVAR3 expected value between 2 and 5 inclusive but received value ' + str(new_value))


def localVAR4(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable localVAR4 expected type bool but received type ' + str(type(new_value)))
    return new_value


def envFROZENVAR5(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable envFROZENVAR5 expected type int but received type ' + str(type(new_value)))
    if new_value >= 2 and new_value <= 5:
        return new_value
    else:
        raise SereneAssignmentException('variable envFROZENVAR5 expected value between 2 and 5 inclusive but received value ' + str(new_value))


def envFROZENVAR6(new_values):
    def envFROZENVAR6__internal_type_check(new_value):
        if not isinstance(new_value, bool):
            raise SereneAssignmentException('variable envFROZENVAR6 expected type bool but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise SereneAssignmentException('Index must be an int when accessing envFROZENVAR6: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise SereneAssignmentException('Index out of bounds when accessing envFROZENVAR6: ' + str(index))
        checked_value = envFROZENVAR6__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs
