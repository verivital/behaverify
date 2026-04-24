#!/usr/bin/env python3
"""Visualize the 2DLivelock counterexample trace from nuXmv output.

Usage:
    python3 visualize_livelock.py [nuxmv_output_file]
    python3 visualize_livelock.py output/nuxmv/2DLivelock_output.txt
"""
import sys
import re

MAX_X, MAX_Y = 3, 1
GOAL1 = (MAX_X, MAX_Y)   # R1 goal: (3, 1)
GOAL2 = (0,    MAX_Y)    # R2 goal: (0, 1)


def parse_first_trace(path):
    """Extract per-state variable values from the first counterexample in the file."""
    states = []
    loop_at = None
    in_trace = False
    current = {}

    with open(path) as f:
        for line in f:
            s = line.strip()

            if '-- specification' in s and 'is false' in s:
                in_trace = True
                continue
            if not in_trace:
                continue
            if '-- specification' in s:   # next spec result -- stop
                break
            if '-- Loop starts here' in s:
                loop_at = len(states)      # next appended state starts the loop
                continue
            if s.startswith('-> State:'):
                if current:
                    states.append(current.copy())
                current = {}
                continue

            m = re.match(r'system\.(\w+)_stage_(\d+)\s*=\s*(-?\w+)', s)
            if m:
                var, stage, val = m.group(1), int(m.group(2)), m.group(3)
                if var in ('x_d1', 'y_d1', 'x_d2', 'y_d2'):
                    current[(var, stage)] = int(val)

    if current:
        states.append(current.copy())
    return states, loop_at


def resolve(raw_states):
    """Carry forward stage_1 values; fall back to stage_0 for initial state."""
    resolved = []
    last = {}
    for raw in raw_states:
        pos = dict(last)
        for var in ('x_d1', 'y_d1', 'x_d2', 'y_d2'):
            if (var, 1) in raw:
                pos[var] = raw[(var, 1)]
            elif (var, 0) in raw and var not in pos:
                pos[var] = raw[(var, 0)]
        last = pos
        resolved.append(pos)
    return resolved


def draw(pos):
    r1 = (pos.get('x_d1'), pos.get('y_d1'))
    r2 = (pos.get('x_d2'), pos.get('y_d2'))

    cells = {GOAL1: 'G1', GOAL2: 'G2'}
    if None not in r1 and None not in r2:
        if r1 == r2:
            cells[r1] = 'XX'
        else:
            cells[r1] = 'R1'
            cells[r2] = 'R2'

    for y in range(MAX_Y, -1, -1):
        row = f'  y={y} '
        for x in range(MAX_X + 1):
            row += '[{:2}]'.format(cells.get((x, y), '  '))
        print(row)
    print('       ' + '    '.join(f'x={x}' for x in range(MAX_X + 1)))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'output/nuxmv/2DLivelock_output.txt'
    raw_states, loop_at = parse_first_trace(path)
    states = resolve(raw_states)

    if not states:
        print(f'No counterexample found in {path}')
        return

    print('2D Livelock Trace Visualization')
    print(f'R1: (1,1) -> goal G1={GOAL1}   R2: (2,1) -> goal G2={GOAL2}')
    print('Legend: R1/R2=robots  G1/G2=goals  XX=collision  (blank)=empty\n')

    for i, pos in enumerate(states):
        if loop_at is not None and i == loop_at:
            print('  *** LOOP STARTS HERE -- livelock cycle ***\n')
        r1 = (pos.get('x_d1'), pos.get('y_d1'))
        r2 = (pos.get('x_d2'), pos.get('y_d2'))
        print(f'State {i + 1}:  R1={r1}  R2={r2}')
        draw(pos)
        print()


if __name__ == '__main__':
    main()
