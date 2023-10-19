class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def foo(new_values):
    def foo__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise SereneAssignmentException('variable foo expected type int but received type ' + str(type(new_value)))
        if new_value >= 0 and new_value <= 10:
            return new_value
        else:
            raise SereneAssignmentException('variable foo expected value between 0 and 10 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise SereneAssignmentException('Index must be an int when accessing foo: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise SereneAssignmentException('Index out of bounds when accessing foo: ' + str(index))
        checked_value = foo__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def index_var(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable index_var expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 2:
        return new_value
    else:
        raise SereneAssignmentException('variable index_var expected value between 0 and 2 inclusive but received value ' + str(new_value))


def bar(new_values):
    def bar__internal_type_check(new_value):
        if not isinstance(new_value, str):
            raise SereneAssignmentException('variable bar expected type str but received type ' + str(type(new_value)))
        if new_value in ['increase', 'decrease', 'nope']:
            return new_value
        else:
            raise SereneAssignmentException("variable bar expected value in ['increase', 'decrease', 'nope'] but received value '" + new_value + "'")

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise SereneAssignmentException('Index must be an int when accessing bar: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise SereneAssignmentException('Index out of bounds when accessing bar: ' + str(index))
        checked_value = bar__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs
