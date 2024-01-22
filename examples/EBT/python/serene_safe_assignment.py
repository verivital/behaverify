def index_func(index, array_size):
    if type(index) is not int:
        raise TypeError('Array index must be an int')
    if index < 0 or index >= array_size:
        raise ValueError('Array index out of bounds')
    return index



def path_computed_bool(new_value):
    if type(new_value) is not bool:
        raise TypeError('variable path_computed_bool expected type bool but received type ' + str(type(new_value)))
    return new_value


def drone_location(new_values):
    def drone_location__internal_type_check(new_value):
        if type(new_value) not in {int, float}:
            raise TypeError('variable drone_location expected type int or float but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing drone_location: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing drone_location: ' + str(index))
        checked_value = drone_location__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def drone_velocity(new_values):
    def drone_velocity__internal_type_check(new_value):
        if type(new_value) not in {int, float}:
            raise TypeError('variable drone_velocity expected type int or float but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing drone_velocity: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing drone_velocity: ' + str(index))
        checked_value = drone_velocity__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def drone_action(new_values):
    def drone_action__internal_type_check(new_value):
        if type(new_value) not in {int, float}:
            raise TypeError('variable drone_action expected type int or float but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing drone_action: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing drone_action: ' + str(index))
        checked_value = drone_action__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def waypoint_location(new_values):
    def waypoint_location__internal_type_check(new_value):
        if type(new_value) not in {int, float}:
            raise TypeError('variable waypoint_location expected type int or float but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing waypoint_location: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing waypoint_location: ' + str(index))
        checked_value = waypoint_location__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def path_storage_x(new_values):
    def path_storage_x__internal_type_check(new_value):
        if type(new_value) not in {int, float}:
            raise TypeError('variable path_storage_x expected type int or float but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing path_storage_x: ' + str(type(index)))
        if index < 0 or index >= 25:
            raise ValueError('Index out of bounds when accessing path_storage_x: ' + str(index))
        checked_value = path_storage_x__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def path_storage_y(new_values):
    def path_storage_y__internal_type_check(new_value):
        if type(new_value) not in {int, float}:
            raise TypeError('variable path_storage_y expected type int or float but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing path_storage_y: ' + str(type(index)))
        if index < 0 or index >= 25:
            raise ValueError('Index out of bounds when accessing path_storage_y: ' + str(index))
        checked_value = path_storage_y__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs


def landmark_index(new_value):
    if type(new_value) is not int:
        raise TypeError('variable landmark_index expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 24:
        return new_value
    else:
        raise ValueError('variable landmark_index expected value between 0 and 24 inclusive but received value ' + str(new_value))


def subgoal(new_values):
    def subgoal__internal_type_check(new_value):
        if type(new_value) not in {int, float}:
            raise TypeError('variable subgoal expected type int or float but received type ' + str(type(new_value)))
        return new_value

    return_pairs = []
    seen_indices = set()
    for (index, new_value) in new_values:
        if type(index) is not int:
            raise ValueError('Index must be an int when accessing subgoal: ' + str(type(index)))
        if index < 0 or index >= 2:
            raise ValueError('Index out of bounds when accessing subgoal: ' + str(index))
        checked_value = subgoal__internal_type_check(new_value)
        if index not in seen_indices:
            seen_indices.add(index)
            return_pairs.append((index, checked_value))
    return return_pairs
