class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def value(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable value expected type int but received type ' + str(type(new_value)))
    return new_value
