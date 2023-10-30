def index_func(index, array_size):
    if type(index) is not int:
        raise TypeError('Array index must be an int')
    if index < 0 or index >= array_size:
        raise ValueError('Array index out of bounds')
    return index



def blVAR0(new_value):
    if type(new_value) is not bool:
        raise TypeError('variable blVAR0 expected type bool but received type ' + str(type(new_value)))
    return new_value


def envVAR1(new_value):
    if type(new_value) is not int:
        raise TypeError('variable envVAR1 expected type int but received type ' + str(type(new_value)))
    if new_value >= -5 and new_value <= -2:
        return new_value
    else:
        raise ValueError('variable envVAR1 expected value between -5 and -2 inclusive but received value ' + str(new_value))


def blVAR2(new_values):
    def blVAR2__internal_type_check(new_value):
        if type(new_value) is not str:
            raise TypeError('variable blVAR2 expected type str but received type ' + str(type(new_value)))
        if new_value in ['yes', 'no', 'both']:
            return new_value
        else:
            raise ValueError("variable blVAR2 expected value in ['yes', 'no', 'both'] but received value " + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing blVAR2: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing blVAR2: ' + str(index))
        checked_value = blVAR2__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def blVAR3(new_values):
    def blVAR3__internal_type_check(new_value):
        if type(new_value) is not bool:
            raise TypeError('variable blVAR3 expected type bool but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing blVAR3: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing blVAR3: ' + str(index))
        checked_value = blVAR3__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs
