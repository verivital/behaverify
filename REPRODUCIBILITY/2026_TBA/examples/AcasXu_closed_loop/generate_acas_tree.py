"""
generate_acas_tree.py

Instantiate acas_template_360.tree by filling in pre-computed lookup-table
expressions for the closed-loop ACAS Xu behavior tree model.

The template contains seven REPLACE_* placeholders, each replaced by a BehaVerify
DSL `result { (if, ...) }` expression covering all integer (x_mag, y_mag) pairs
in [0, MAX_DIST / DISTANCE_MODIFIER]²:

  REPLACE_VELOCITY_X_OWN  — ownship x-velocity:  round(cos(heading_own) * SPEED_OWN)
  REPLACE_VELOCITY_Y_OWN  — ownship y-velocity:  round(sin(heading_own) * SPEED_OWN)
  REPLACE_VELOCITY_X_INT  — intruder x-velocity: round(cos(heading_int) * SPEED_INT)
  REPLACE_VELOCITY_Y_INT  — intruder y-velocity: round(sin(heading_int) * SPEED_INT)
  REPLACE_DISTANCE        — Euclidean distance:  round(sqrt(x_mag² + y_mag²)) * 100
  REPLACE_ARCTAN_XY       — Rounded arctan(x_mag / y_mag) in degrees
  REPLACE_ARCTAN_YX       — Rounded arctan(y_mag / x_mag) in degrees

Input:  acas_template_360.tree
Output: tree/acas_360.tree  (tree/ directory must exist before running)

Usage:
    python3 generate_acas_tree.py
"""

import math
import os
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Model parameters (single source of truth: acas_model_params.yaml)
# ---------------------------------------------------------------------------

def _load_params() -> dict:
    path = Path(__file__).parent / "acas_model_params.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

_P = _load_params()

SPEED_OWN         = _P["physics"]["speed_own"]
SPEED_INT         = _P["physics"]["speed_int"]
MAX_DIST          = _P["physics"]["max_dist"]
DISTANCE_MODIFIER = _P["physics"]["distance_modifier"]

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
    print("hello!")
    pre_string = ''
    post_string = indent(indent_level)
    while len(cond_values) > 1:
        if len(cond_values) % 1000 == 0:
            print(str(len(cond_values)) + ' left')
        (cond, value) = cond_values.pop()
        pre_string += (
            indent(indent_level) + '(if, ' + format_condition(cond, var_names) + ',\n'
            + indent(indent_level + 1) + str(value) + ',\n'
        )
        post_string += ')'
        # indent_level = indent_level + 1
    (_, value) = cond_values.pop()
    return pre_string + indent(indent_level) + str(value) + '\n' + post_string + '\n'


def format_all(cond_values, var_names):
    return 'result {\n' + format_if(4, cond_values, var_names) + indent(3) + '}\n'
# no indent at start because it's indented in the template already.

def create_bounding_boxes(conds):
    if not conds:
        return []
    conds = sorted(conds)  # Sort to process in order
    result = []
    while conds:
        a, c = conds[0]  # Start a new bounding box
        b, d = a, c
        # Expand horizontally
        to_remove = []
        for i, j in conds:
            if i == b + 1 and c <= j <= d:
                b = i
                to_remove.append((i, j))
            elif a <= i <= b and (j == d + 1 or j == c - 1):
                d = max(d, j)
                c = min(c, j)
                to_remove.append((i, j))
        # Remove used conds
        for item in to_remove:
            conds.remove(item)
        conds.remove((a, c))
        result.append((a, b, c, d))
    return result

def better_cond_values(cond_values):
    temp = {}
    for (cond, value) in cond_values:
        if value in temp:
            temp[value].append(cond)
        else:
            temp[value] = [cond]
    new_cond_values = []
    for value in temp:
        for cond in create_bounding_boxes(temp[value]):
            new_cond_values.append((cond, value))
    return new_cond_values

def format_condition_v2(cond, var_names):
    return (
        '(and, ' + ', '.join(
            [
                ('(le, ' + str(cond[x]) + ', ' + var_names[x] + '), (ge, ' + var_names[x] + ', ' + str(cond[x + 1]) + ')')
                for x in range(len(var_names))
            ]
        )
        + ')'
    )


def format_if_v2(indent_level, cond_values, var_names):
    pre_string = ''
    post_string = indent(indent_level)
    while len(cond_values) > 1:
        if len(cond_values) % 1000 == 0:
            print(str(len(cond_values)) + ' left')
        (cond, value) = cond_values.pop()
        pre_string += (
            indent(indent_level) + '(if, ' + format_condition_v2(cond, var_names) + ',\n'
            + indent(indent_level + 1) + str(value) + ',\n'
        )
        post_string += ')'
        # indent_level = indent_level + 1
    (_, value) = cond_values.pop()
    return pre_string + indent(indent_level) + str(value) + '\n' + post_string


def format_all_v2(cond_values, var_names):
    print(len(cond_values))
    print(len(better_cond_values(cond_values)))
    return 'result {\n' + format_if_v2(4, better_cond_values(cond_values), var_names) + indent(3) + '}\n'
# no indent at start because it's indented in the template already.


def handle_velocity(own, x_mode):
    print('handling velocity with: ' + str((own, x_mode)))
    velocities = [
        (
            (a, (SPEED_OWN if own else SPEED_INT)),
            round((math.cos(math.radians(a)) if x_mode else math.sin(math.radians(a))) * (SPEED_OWN if own else SPEED_INT))
        )
        for a in range(360)
    ]
    return format_all(velocities, (('heading_own', 'speed_own') if own else ('heading_int', 'speed_int')))

def handle_distance():
    print('handling distance')
    print(1 + (MAX_DIST // DISTANCE_MODIFIER))
    distances = [
        (
            (x * DISTANCE_MODIFIER, y * DISTANCE_MODIFIER),
            round(math.sqrt(x*x + y*y)) * DISTANCE_MODIFIER
        )
        for x in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
        for y in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
    ]
    return format_all(distances, ('x', 'y'))

def handle_arctan(x_top):
    print('handling arctan with ' + str(x_top))
    arctans = [
        (
            (x * DISTANCE_MODIFIER, y * DISTANCE_MODIFIER),
            (
                (
                    0
                    if y == 0 else
                    round(math.degrees(math.atan((x/y))))
                )
                if x_top else
                (
                    0
                    if x == 0 else
                    round(math.degrees(math.atan((y/x))))
                )
            )
        )
        for x in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
        for y in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
    ]
    return format_all(arctans, ('x', 'y'))


def handle_distance_v2():
    print('handling distance')
    print(1 + (MAX_DIST // DISTANCE_MODIFIER))
    distances = [
        (
            (x, y),
            round(math.sqrt(x*x + y*y)) * DISTANCE_MODIFIER
        )
        for x in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
        for y in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
    ]
    return format_all(distances, ('x_mag', 'y_mag'))

def handle_arctan_v2(x_top):
    print('handling arctan with ' + str(x_top))
    arctans = [
        (
            (x, y),
            (
                (
                    0
                    if y == 0 else
                    round(math.degrees(math.atan((x/y))))
                )
                if x_top else
                (
                    0
                    if x == 0 else
                    round(math.degrees(math.atan((y/x))))
                )
            )
        )
        for x in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
        for y in range(0, 1 + (MAX_DIST // DISTANCE_MODIFIER))
    ]
    return format_all(arctans, ('x_mag', 'y_mag'))

with open('acas_template_360.tree', 'r', encoding='utf-8') as input_file:
    content = input_file.read()
 
content = content.replace('REPLACE_VELOCITY_X_OWN', handle_velocity(True, True))
content = content.replace('REPLACE_VELOCITY_Y_OWN', handle_velocity(True, False))
content = content.replace('REPLACE_VELOCITY_X_INT', handle_velocity(False, True))
content = content.replace('REPLACE_VELOCITY_Y_INT', handle_velocity(False, False))
content = content.replace('REPLACE_DISTANCE', handle_distance_v2())
content = content.replace('REPLACE_ARCTAN_XY', handle_arctan_v2(True))
content = content.replace('REPLACE_ARCTAN_YX', handle_arctan_v2(False))

with open('./tree/acas_360.tree', 'w', encoding = 'utf-8') as output_file:
    output_file.write(content)
