import os
'''
[not_prime, prime]
'''
def check_prime(x):
    y = 0
    while True:
        if y * y == x:
            return '[1.0, 0.0]'
        if y * y > x:
            return '[0.0, 1.0]'
        y = y + 1
val = 20
with open(str(val) + 'prime_inputs.py', 'w') as f:
    lines = ['inputs = [' + os.linesep]
    for n in range(val):
        lines.append('    [' + str(n) + '.0],' + os.linesep)
    lines.append(']' + os.linesep)
    f.writelines(lines)
with open(str(val) + 'prime_targets.py', 'w') as f:
    lines = ['targets = [' + os.linesep]
    for n in range(val):
        lines.append('    ' + check_prime(n) + ',' + os.linesep)
    lines.append(']' + os.linesep)
    f.writelines(lines)
