'''
Gridworld renderer for the NSBT city tracking mission (2026-07-02).

Adapted from REPRODUCIBILITY/2025_NEUS/examples/parse_nuxmv_output.py:
parses a nuXmv trace (simulation `show_traces -v` output or a CTL/LTL
counterexample) OR a JSON rollout (neural planner simulation), then renders
per-tick frames of the 25x25 city block grid showing BOTH the drone and the
moving target, with spec-status border coloring:

    amber  - specification obligation pending (F(found) not yet witnessed)
    green  - obligation met (target within sensor range at some tick)
    red    - obligation violated (deadline passed without found)

usage:
  python3 render_city_tracking.py <trace.txt|rollout.json> <meta.json> \
      <mode: sat|violation|neural> <output_prefix>

outputs: <prefix>.gif  <prefix>.mp4  <prefix>.png  (+ frames in <prefix>_frames/)
'''
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

CELL = 26
BORDER = 14
PAD = 6
CAPTION = 78

AMBER = (235, 165, 0)
GREEN = (0, 150, 60)
RED = (205, 30, 30)
OBSTACLE = (60, 64, 72)
FREE = (245, 245, 242)
GRID_LINE = (210, 210, 205)
DRONE = (25, 90, 220)
TARGET = (230, 90, 20)
DRONE_TRAIL = (140, 170, 240)
TARGET_TRAIL = (245, 180, 130)

SPEC_TEXT = {
    'sat': 'LTL F(found) / CTL (drone_safe -> AF found)   [verified SAT; witness trace]',
    'violation': 'LTL F[0,30](found) / CTL (drone_safe -> AF(found & step<=30))   [VIOLATED; counterexample]',
    'neural': 'retrained neural planner (2048x2 ONNX, greedy) -- SIMULATION ONLY, not verified',
}


def parse_nuxmv_trace(file_name):
    '''returns ordered list of {x, y, step} dicts (stage-0 values, forward-filled)'''
    states = []
    current = None
    loop_index = None
    var_re = re.compile(r'^\s*(?:system\.)?(\w+?)\s*=\s*(\S+)\s*$')
    with open(file_name, 'r', encoding='utf-8') as input_file:
        for line in input_file.readlines():
            if '-> State:' in line:
                if current is not None:
                    states.append(current)
                current = dict(states[-1]) if states else {}
            elif 'Loop starts here' in line and current is not None:
                loop_index = len(states) + 1
            elif current is not None:
                match = var_re.match(line)
                if match is None:
                    continue
                (name, value) = (match.group(1), match.group(2))
                for (key, var) in (('x', 'x_d_stage_0'), ('y', 'y_d_stage_0'), ('step', 'step_stage_0')):
                    if name == var:
                        current[key] = int(value)
    if current is not None:
        states.append(current)
    states = [s for s in states if 'x' in s and 'y' in s and 'step' in s]
    return (states, loop_index)


def load_states(input_path):
    if input_path.endswith('.json'):
        rollout = json.load(open(input_path, 'r', encoding='utf-8'))
        return ([{'x': s[0], 'y': s[1], 'step': s[2]} for s in rollout['states']], None)
    return parse_nuxmv_trace(input_path)


def get_font(size):
    for candidate in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                      '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def cell_box(x, y, n):
    '''grid coords -> pixel box; y axis points up (north)'''
    px = BORDER + PAD + x * CELL
    py = BORDER + PAD + (n - 1 - y) * CELL
    return (px, py, px + CELL, py + CELL)


def render(input_path, meta_path, mode, prefix):
    meta = json.load(open(meta_path, 'r', encoding='utf-8'))
    grid = meta['grid']
    n = len(grid)
    tpw = meta['ticks_per_waypoint']
    path = meta['path']
    deadline = meta['deadline']
    sensor = meta['sensor_range']

    (states, loop_index) = load_states(input_path)
    if not states:
        raise RuntimeError('no states parsed from ' + input_path)
    print('parsed %d states from %s (loop at %s)' % (len(states), input_path, loop_index))

    def target_of(step):
        return tuple(path[min(len(path) - 1, step // tpw)])

    # trim the static tail (both agents parked / lasso self-loop): keep 4 settle frames
    signature = [(s['x'], s['y']) + target_of(s['step']) for s in states]
    last_change = max((i for i in range(1, len(signature)) if signature[i] != signature[i - 1]), default=0)
    states = states[:last_change + 4]
    print('rendering %d frames after static-tail trim' % len(states))

    width = 2 * (BORDER + PAD) + n * CELL
    height = 2 * (BORDER + PAD) + n * CELL + CAPTION
    font_big = get_font(15)
    font_small = get_font(12)

    frames_dir = prefix + '_frames'
    os.makedirs(frames_dir, exist_ok=True)
    frames = []
    found_ever = False
    violated = False
    drone_trail = []
    target_trail = []

    for (tick, state) in enumerate(states):
        (dx, dy, step) = (state['x'], state['y'], state['step'])
        (tx, ty) = target_of(step)
        dist = abs(dx - tx) + abs(dy - ty)
        found_now = dist <= sensor
        if found_now:
            found_ever = True
        if mode == 'violation' and step > deadline and not found_ever:
            violated = True

        if found_ever:
            status = ('FOUND: obligation met', GREEN)
        elif mode == 'violation':
            status = ('pending: %d ticks to deadline' % max(0, deadline - step), AMBER)
        else:
            status = ('pending: searching for target', AMBER)
        if mode == 'violation' and violated:
            status = ('VIOLATED: missed deadline', RED)

        image = Image.new('RGB', (width, height), status[1])
        draw = ImageDraw.Draw(image)
        draw.rectangle([BORDER, BORDER, width - BORDER, height - BORDER - CAPTION + PAD], fill=FREE)
        # cells
        for gx in range(n):
            for gy in range(n):
                box = cell_box(gx, gy, n)
                if grid[gx][gy] == 1:
                    draw.rectangle(box, fill=OBSTACLE)
                else:
                    draw.rectangle(box, outline=GRID_LINE)
        # trails
        drone_trail.append((dx, dy))
        target_trail.append((tx, ty))
        for (px, py) in target_trail[:-1]:
            box = cell_box(px, py, n)
            draw.rectangle([box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8], fill=TARGET_TRAIL)
        for (px, py) in drone_trail[:-1]:
            box = cell_box(px, py, n)
            draw.ellipse([box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8], fill=DRONE_TRAIL)
        # sensor footprint (manhattan radius) around drone
        for (ox, oy) in [(a, b) for a in range(-sensor, sensor + 1) for b in range(-sensor, sensor + 1) if abs(a) + abs(b) <= sensor]:
            (sx, sy) = (dx + ox, dy + oy)
            if 0 <= sx < n and 0 <= sy < n and (ox, oy) != (0, 0):
                box = cell_box(sx, sy, n)
                draw.rectangle(box, outline=(GREEN if found_now else DRONE), width=2)
        # target
        box = cell_box(tx, ty, n)
        draw.rectangle([box[0] + 3, box[1] + 3, box[2] - 3, box[3] - 3], fill=TARGET)
        draw.text((box[0] + 8, box[1] + 5), 'T', fill='white', font=font_small)
        # drone
        box = cell_box(dx, dy, n)
        draw.ellipse([box[0] + 2, box[1] + 2, box[2] - 2, box[3] - 2], fill=DRONE, outline='white')
        draw.text((box[0] + 8, box[1] + 5), 'D', fill='white', font=font_small)
        # caption
        cap_y = height - CAPTION - BORDER + 2 * PAD
        draw.rectangle([BORDER, height - CAPTION - BORDER + PAD, width - BORDER, height - BORDER], fill=(25, 28, 32))
        draw.text((BORDER + PAD, cap_y), 'NSBT city tracking - 25x25 ADK city map (block=40m, fly_at=80m)', fill='white', font=font_small)
        draw.text((BORDER + PAD, cap_y + 17), SPEC_TEXT[mode], fill=(200, 200, 200), font=font_small)
        draw.text((BORDER + PAD, cap_y + 36),
                  'tick %3d   drone=(%d,%d)  target=(%d,%d)  dist=%d   %s' % (step, dx, dy, tx, ty, dist, status[0]),
                  fill=status[1] if status[1] != AMBER else (255, 200, 90), font=font_big)
        frame_path = os.path.join(frames_dir, 'frame_%03d.png' % tick)
        image.save(frame_path)
        frames.append(image)

    # animated gif (hold last frame)
    frames_out = frames + [frames[-1]] * 8
    frames_out[0].save(prefix + '.gif', save_all=True, append_images=frames_out[1:],
                       duration=180, loop=0)
    # mp4
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '6',
                    '-i', os.path.join(frames_dir, 'frame_%03d.png'),
                    '-vf', 'tpad=stop_mode=clone:stop_duration=2',
                    '-pix_fmt', 'yuv420p', '-movflags', 'faststart', prefix + '.mp4'],
                   check=True)
    # still png: final frame (full trails + verdict)
    frames[-1].save(prefix + '.png')
    print('wrote %s.{gif,mp4,png} (%d frames)' % (prefix, len(frames)))


if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
