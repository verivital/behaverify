def find_closest_unit(cur_seg, start, delta):
    can_return = False
    paran_count = 0
    index = start
    inside = False
    while (paran_count != 0) or (not(can_return)) or inside:
        if cur_seg[index] == ')':
            paran_count = paran_count - 1
        elif cur_seg[index] == '(':
            paran_count = paran_count + 1
        elif cur_seg[index] == 'p':
            can_return = True
        index = index + delta
        if delta > 0:
            while cur_seg[index] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                index = index + delta
    return index - delta
def replace_infix_symbol(guard_statement, symbol, replacement):
    while symbol in guard_statement:
        (left, right) = guard_statement.split(symbol, 1)
        left_index = find_closest_unit(left, len(left) - 1, -1)
        right_index = find_closest_unit(right, 0, 1)
        left_prefix = left[:left_index]
        left_group = left[left_index:]
        right_group = right[:(right_index + 1)]
        right_postfix = right[(right_index + 1):]
        guard_statement = left_prefix + '(' + replacement + ', ' + left_group.strip() + ', ' + right_group.strip() + ')' + right_postfix
    return guard_statement
def replace_prefix_symbol(guard_statement, symbol, replacement):
    while symbol in guard_statement:
        (left, right) = guard_statement.split(symbol, 1)
        right_index = find_closest_unit(right, 0, 1)
        right_group = right[:(right_index + 1)]
        right_postfix = right[(right_index + 1):]
        guard_statement = left + '(' + replacement + ', ' + right_group.strip() + ')' + right_postfix
    return guard_statement
def parse_guard(guard_statement):
    guard_statement = guard_statement.replace('!=', '_=')
    guard_statement = replace_prefix_symbol(guard_statement, '!', 'not')
    guard_statement = replace_infix_symbol(guard_statement, '==', 'eq')
    guard_statement = replace_infix_symbol(guard_statement, '_=', 'neq')
    guard_statement = replace_infix_symbol(guard_statement, '&&', 'and')
    guard_statement = replace_infix_symbol(guard_statement, '||', 'or')
    guard_statement = replace_infix_symbol(guard_statement, '->', 'implies')
    return guard_statement


print(parse_guard('(p1 && p3 && !p4 && !p6 && p7)'))
