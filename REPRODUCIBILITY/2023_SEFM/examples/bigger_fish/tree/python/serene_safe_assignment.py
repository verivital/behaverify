class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def biggest_fish(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable biggest_fish expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 199:
        return new_value
    else:
        raise SereneAssignmentException('variable biggest_fish expected value between 0 and 199 inclusive but received value ' + str(new_value))
