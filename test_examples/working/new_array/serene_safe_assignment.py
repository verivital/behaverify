

def test(new_values):
    def test__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise Exception('variable test expected type int but received type ' + str(type(new_value)))
        if new_value >= 0 and new_value <= 10:
            return new_value
        else:
            raise Exception('variable test expected value between 0 and 10 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing test: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise Exception('Index out of bounds when accessing test: ' + str(index))
        checked_value = test__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs
