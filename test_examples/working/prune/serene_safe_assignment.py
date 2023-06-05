

def test(new_value):
    if not isinstance(new_value, int):
        raise Exception('variable test expected type int but received type ' + str(type(new_value)))
    if new_value >= 0 and new_value <= 10:
        return new_value
    else:
        raise Exception('variable test expected value between 0 and 10 inclusive but received value ' + str(new_value))
