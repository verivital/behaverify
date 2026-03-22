import math
import os

SPEED_OWN = 400
SPEED_INT = 600
MAX_DIST = 80000
DISTANCE_MODIFIER = 200

def indent(n):
    return (' ' * 4 * n)

def format_condition(cond, var_names):
    '''
    here value is just the
    '''
    if len(var_names) == 1:
        return '(eq, ' + var_names[0] + ', ' + str(cond[0]) + ')'
    return (
        '(and, ' + ', '.join(
            [
                ('(eq, ' + var_names[x] + ', ' + str(cond[x]) + ')')
                for x in range(len(var_names))
            ]
        )
        + ')'
    )

def format_if_old(indent_level, cond_values, var_names):
    if len(cond_values) == 0:
        raise ValueError
    if len(cond_values) == 1:
        return indent(indent_level) + str(cond_values[0][1]) + os.linesep
    (cond, value) = cond_values.pop()
    return(
        indent(indent_level) + '(if,\n'
        + indent(indent_level + 1) + format_condition(cond, var_names) + ',\n'
        + indent(indent_level + 1) + str(value) + ',\n'
        + format_if_old(indent_level + 1, cond_values, var_names) + '\n'
        + indent(indent_level) + ')\n'
    )


def format_if(indent_level, cond_values, var_names):
    pre_string = ''
    post_string = ''
    while len(cond_values) > 1:
        if len(cond_values) % 100 == 0:
            print(str(len(cond_values)) + ' left')
        (cond, value) = cond_values.pop()
        pre_string += (
            indent(indent_level) + '(if,\n'
            + indent(indent_level + 1) + format_condition(cond, var_names) + ',\n'
            + indent(indent_level + 1) + str(value) + ',\n'
        )
        post_string += indent(indent_level) + ')\n'
        indent_level = indent_level + 1
    (_, value) = cond_values.pop()
    return pre_string + indent(indent_level) + str(value) + '\n' + post_string

def format_all(cond_values, var_names):
    return 'result {\n' + format_if(4, cond_values, var_names) + indent(3) + '}\n'
# no indent at start because it's indented in the template already.

def handle_velocity(own, x_mode):
    print('handling velocity with: ' + str((own, x_mode)))
    velocities = [
        (
            (a, (SPEED_OWN if own else SPEED_INT)),
            int((math.cos(math.radians(a)) if x_mode else math.sin(math.radians(a))) * SPEED_OWN)
        )
        for a in range(360)
    ]
    return format_all(velocities, (('heading_own', 'speed_own') if own else ('heading_int', 'speed_int')))

def handle_distance():
    print('handling distance')
    print((-1 * MAX_DIST // DISTANCE_MODIFIER, 1 + (MAX_DIST // DISTANCE_MODIFIER)))
    distances = [
        (
            (x * DISTANCE_MODIFIER, y * DISTANCE_MODIFIER),
            int(math.sqrt(x*x + y*y)) * DISTANCE_MODIFIER
        )
        for x in range(-1 * MAX_DIST // DISTANCE_MODIFIER, 1 + (MAX_DIST // DISTANCE_MODIFIER))
        for y in range(-1 * MAX_DIST // DISTANCE_MODIFIER, 1 + (MAX_DIST // DISTANCE_MODIFIER))
    ]
    return format_all(distances, ('x', 'y'))

def handle_arctan(x_top):
    print('handling arctan with ' + str(x_top))
    arctans = [
        (
            (x * DISTANCE_MODIFIER, y * DISTANCE_MODIFIER),
            int(math.degrees(math.atan((x/y) if x_top else (y/x))))
        )
        for x in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
        for y in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
        if ((x_top and y != 0) or x != 0)
    ]
    return format_all(arctans, ('x', 'y'))
    
with open('acasxu_template_360.tree', 'r', encoding='utf-8') as input_file:
    content = input_file.read()

content = content.replace('REPLACE_VELOCITY_X_OWN', handle_velocity(True, True))
content = content.replace('REPLACE_VELOCITY_Y_OWN', handle_velocity(True, False))
content = content.replace('REPLACE_VELOCITY_X_INT', handle_velocity(False, True))
content = content.replace('REPLACE_VELOCITY_Y_INT', handle_velocity(False, False))
content = content.replace('REPLACE_DISTANCE', handle_distance())
content = content.replace('REPLACE_ARCTAN_XY', handle_arctan(True))
content = content.replace('REPLACE_ARCTAN_YX', handle_arctan(False))

with open('acasxu_replaced_360.tree', 'w', encoding = 'utf-8') as output_file:
    output_file.write(content)
