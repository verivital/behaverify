

def a(new_values):
    def a__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise Exception('variable a expected type int but received type ' + str(type(new_value)))
        if new_value >= 0 and new_value <= 10:
            return new_value
        else:
            raise Exception('variable a expected value between 0 and 10 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing a: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise Exception('Index out of bounds when accessing a: ' + str(index))
        checked_value = a__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def b(new_values):
    def b__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise Exception('variable b expected type int but received type ' + str(type(new_value)))
        if new_value >= 0 and new_value <= 10:
            return new_value
        else:
            raise Exception('variable b expected value between 0 and 10 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing b: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise Exception('Index out of bounds when accessing b: ' + str(index))
        checked_value = b__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def c(new_values):
    def c__internal_type_check(new_value):
        if not isinstance(new_value, int):
            raise Exception('variable c expected type int but received type ' + str(type(new_value)))
        if new_value >= 0 and new_value <= 10:
            return new_value
        else:
            raise Exception('variable c expected value between 0 and 10 inclusive but received value ' + str(new_value))

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing c: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise Exception('Index out of bounds when accessing c: ' + str(index))
        checked_value = c__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def e(new_values):
    def e__internal_type_check(new_value):
        if not isinstance(new_value, bool):
            raise Exception('variable e expected type bool but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing e: ' + str(type(index)))
        if index < 0 or index >= 3:
            raise Exception('Index out of bounds when accessing e: ' + str(index))
        checked_value = e__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def f(new_values):
    def f__internal_type_check(new_value):
        if not isinstance(new_value, str):
            raise Exception('variable f expected type str but received type ' + str(type(new_value)))
        if new_value in ['hi', 'bye', 'die']:
            return new_value
        else:
            raise Exception("variable f expected value in ['hi', 'bye', 'die'] but received value '" + new_value + "'")

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if not isinstance(index, int):
            raise Exception('Index must be an int when accessing f: ' + str(type(index)))
        if index < 0 or index >= 4:
            raise Exception('Index out of bounds when accessing f: ' + str(index))
        checked_value = f__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


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
        if index < 0 or index >= 10:
            raise Exception('Index out of bounds when accessing test: ' + str(index))
        checked_value = test__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs
