import math
network_decimal_bits = 5
network_total_bit = 8
def weird_fixed_binary(value):
    '''
    Convert a value to a fixed binary representation
    '''
    negative = value < 0
    value = value * -1 if negative else value
    dec_val = value % 1
    binary_string = ''
    reached_zero = False
    while len(binary_string) < network_decimal_bits:
        if dec_val == 0.0:
            binary_string = binary_string + ('0' * (network_decimal_bits - len(binary_string)))
            reached_zero = True
            break
        cur_val = 2**(-1 * (len(binary_string) + 1))
        if cur_val > dec_val:
            binary_string = binary_string + '0'
        else:
            dec_val = dec_val - cur_val
            binary_string = binary_string + '1'
    if not reached_zero:
        print('WARNING: at least one network value lost precision due to insufficient decimal points (fractional part, potentially safe)')
    print(binary_string)
    int_val = int(value)
    print(int_val)
    int_string = ''
    if int_val > 0:
        starting_point = int(math.log2(int_val))
        while starting_point >= 0:
            cur_val = 2**(starting_point)
            if cur_val < int_val:
                int_string = int_string + '1'
                value = value - cur_val
            else:
                int_string = int_string + '0'
            starting_point = starting_point - 1
    binary_string = int_string + binary_string
    # binary_string = ('0' * (int(network_total_bits) - len(binary_string))) + binary_string
    return (negative, binary_string)

print(weird_fixed_binary(3.75))
