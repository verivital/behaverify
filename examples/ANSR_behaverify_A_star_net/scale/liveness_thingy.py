import os
storage = {}
def state_convert(state):
    if 'init' in state:
        return 0
    return int(state.split('S', 1)[1]) - 1
with open('liveness_string.txt', 'r', encoding = 'utf-8') as input_file:
    definition = True
    from_state = None
    to_state = None
    for line in input_file.readlines():
        if definition:
            definition = False
            (_, from_state, _, to_state) = line.split('__')
            to_state = to_state.split('(')[0]
            from_state = state_convert(from_state)
            to_state = state_convert(to_state)
            if to_state not in storage:
                storage[to_state] = {}
            if from_state not in storage[to_state]:
                storage[to_state][from_state] = []
        else:
            definition = True
            if '(1)' in line:
                storage[to_state][from_state].append('True')
                continue
            line = line.split('return')[1]
            line = line.strip()
            line = line.replace('(', '')
            line = line.replace(')', '')
            for thing in line.split(' and '):
                predicate = 'liveness_' + thing.split('\'')[1]
                if 'not' in thing:
                    storage[to_state][from_state].append('(not, ' + predicate + ')')
                else:
                    storage[to_state][from_state].append(predicate)
to_write = (
    'variable_statement {' + os.linesep
    + 'liveness_states' + os.linesep
    + 'constant_index' + os.linesep
    + ''.join(
        [
            (
                'index_of{' + str(to_index) + '}' + os.linesep
                + 'assign{' + os.linesep
                + 'result{' + os.linesep
                + '(or,' + os.linesep
                + (',' + os.linesep).join(
                    [
                        (
                            '(and, (index, liveness_states, ' + str(from_index) + '), '
                            + ', '.join(storage[to_index][from_index])
                            + ')'
                        )
                        for from_index in range(len(storage))
                    ]
                )
                + ')' + os.linesep
                + '}' + os.linesep
                + '}' + os.linesep
            )
            for to_index in range(len(storage))
        ]
    )
    + '}' + os.linesep
)
with open('liveness_converted.txt', 'w', encoding = 'utf-8') as output_file:
    output_file.write(to_write)
