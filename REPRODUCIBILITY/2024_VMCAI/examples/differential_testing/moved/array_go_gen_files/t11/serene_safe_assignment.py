class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def blVAR0(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable blVAR0 expected type int but received type ' + str(type(new_value)))
    if new_value >= -5 and new_value <= -2:
        return new_value
    else:
        raise SereneAssignmentException('variable blVAR0 expected value between -5 and -2 inclusive but received value ' + str(new_value))


def envVAR1(new_values):
    def envVAR1__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise SereneAssignmentException('variable envVAR1 expected type int but received type ' + str(type(new_value)))
        if new_value >= 2 and new_value <= 5:
            return new_value
        else:
            raise SereneAssignmentException('variable envVAR1 expected value between 2 and 5 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise SereneAssignmentException('Index must be an int when accessing envVAR1: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise SereneAssignmentException('Index out of bounds when accessing envVAR1: ' + str(index))
        checked_value = envVAR1__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def blVAR2(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable blVAR2 expected type bool but received type ' + str(type(new_value)))
    return new_value
