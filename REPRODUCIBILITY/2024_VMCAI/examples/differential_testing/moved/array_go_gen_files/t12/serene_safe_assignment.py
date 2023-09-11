class SereneAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)




def blVAR0(new_value):
    if not isinstance(new_value, bool):
        raise SereneAssignmentException('variable blVAR0 expected type bool but received type ' + str(type(new_value)))
    return new_value


def envVAR1(new_value):
    if not isinstance(new_value, int):
        raise SereneAssignmentException('variable envVAR1 expected type int but received type ' + str(type(new_value)))
    if new_value >= -5 and new_value <= -2:
        return new_value
    else:
        raise SereneAssignmentException('variable envVAR1 expected value between -5 and -2 inclusive but received value ' + str(new_value))


def envVAR2(new_value):
    if not isinstance(new_value, str):
        raise SereneAssignmentException('variable envVAR2 expected type str but received type ' + str(type(new_value)))
    if new_value in ['yes', 'no', 'both']:
        return new_value
    else:
        raise SereneAssignmentException("variable envVAR2 expected value in ['yes', 'no', 'both'] but received value '" + new_value + "'")
