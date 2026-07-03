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
CAPTION = 148

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
STREET_PATH = (200, 120, 40)
ZONE_BELIEF_FILL = (255, 244, 180)
ZONE_BELIEF_EDGE = (200, 160, 0)
ZONE_GOAL_FILL = (200, 240, 200)
ZONE_GOAL_EDGE = (0, 130, 60)
KOZ_EDGE = (205, 30, 30)
STAY_WITHIN_EDGE = (0, 160, 200)

def spec_text(mode, deadline):
    return {
        'sat': 'CTL (drone_safe -> AF found) + zone-consistency   [verified SAT; witness trace]',
        'violation': 'CTL (drone_safe -> AF(found & step<=%d))   [VIOLATED; counterexample]' % deadline,
        'neural': 'retrained neural planner (2048x2 ONNX, greedy) -- SIMULATION ONLY, not verified',
    }[mode]


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


def render(input_path, meta_path, mode, prefix, plain=False):
    meta = json.load(open(meta_path, 'r', encoding='utf-8'))
    episode_label = meta.get('episode_label', 'episode-000 track')
    grid = meta['grid']
    n = len(grid)
    tpw = meta['ticks_per_waypoint']
    path = meta['path']
    deadline = meta['deadline']
    sensor = meta['sensor_range']
    block = meta.get('block', 40)
    fly_at = meta.get('fly_at', 80)
    zones = meta.get('zones', [])
    inventory = meta.get('zone_inventory', {})
    polyline = meta.get('target_world_polyline', [])

    def world_to_px(wx, wy):
        '''continuous world coords -> pixel coords (same +500 // block
        transform as the abstraction, kept continuous for the street path)'''
        bx = (wx + 500.0) / block
        by = (wy + 500.0) / block
        return (BORDER + PAD + bx * CELL, BORDER + PAD + (n - by) * CELL)

    def zone_style(zone):
        if zone['kind'] == 'keep_out':
            return (None, KOZ_EDGE)
        if zone['kind'] == 'stay_within':
            return (None, STAY_WITHIN_EDGE)
        if zone['label'].startswith('goal'):
            return (ZONE_GOAL_FILL, ZONE_GOAL_EDGE)
        return (ZONE_BELIEF_FILL, ZONE_BELIEF_EDGE)

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
    height = 2 * (BORDER + PAD) + n * CELL + (0 if plain else CAPTION)
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

        image = Image.new('RGB', (width, height), GRID_LINE if plain else status[1])
        draw = ImageDraw.Draw(image)
        draw.rectangle([BORDER, BORDER, width - BORDER,
                        height - BORDER - (0 if plain else CAPTION - PAD)], fill=FREE)
        # cells
        for gx in range(n):
            for gy in range(n):
                box = cell_box(gx, gy, n)
                if grid[gx][gy] == 1:
                    draw.rectangle(box, fill=OBSTACLE)
                else:
                    draw.rectangle(box, outline=GRID_LINE)
        # mission zones (episode description.json, projected to blocks):
        # free cells inside a zone are tinted; zone boundary drawn on top,
        # thick while the zone's step window is active
        for zone in zones:
            (fill, edge) = zone_style(zone)
            (bx0, by0, bx1, by1) = zone['block_rect']
            if fill is not None:
                for gx in range(bx0, bx1 + 1):
                    for gy in range(by0, by1 + 1):
                        if grid[gx][gy] == 0:
                            box = cell_box(gx, gy, n)
                            draw.rectangle(box, fill=fill, outline=GRID_LINE)
            lo = cell_box(bx0, by1, n)
            hi = cell_box(bx1, by0, n)
            window = zone.get('step_window')
            active = window is not None and window[0] <= step <= window[1]
            if zone['kind'] == 'keep_out':
                # hatch the keep-out interior (drone-forbidden)
                for off in range(0, (hi[2] - lo[0]) + (hi[3] - lo[1]), 10):
                    draw.line([(lo[0] + off, lo[1]), (lo[0], lo[1] + off)],
                              fill=edge, width=1)
            draw.rectangle([lo[0], lo[1], hi[2], hi[3]], outline=edge,
                           width=4 if active else 2)
        # actual (world-coordinate) target street trajectory from the episode
        # CSV: the ground vehicle drives streets THROUGH drone no-fly blocks
        if polyline:
            draw.line([world_to_px(wx, wy) for (wx, wy) in polyline],
                      fill=STREET_PATH, width=2)
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
        if not plain:
            draw.text((box[0] + 8, box[1] + 5), 'T', fill='white', font=font_small)
        # drone
        box = cell_box(dx, dy, n)
        draw.ellipse([box[0] + 2, box[1] + 2, box[2] - 2, box[3] - 2], fill=DRONE, outline='white')
        if not plain:
            draw.text((box[0] + 8, box[1] + 5), 'D', fill='white', font=font_small)
        if plain:
            frame_path = os.path.join(frames_dir, 'frame_%03d.png' % tick)
            image.save(frame_path)
            frames.append(image)
            continue
        # caption
        cap_y = height - CAPTION - BORDER + 2 * PAD
        draw.rectangle([BORDER, height - CAPTION - BORDER + PAD, width - BORDER, height - BORDER], fill=(25, 28, 32))
        draw.text((BORDER + PAD, cap_y),
                  'NSBT city tracking - %dx%d ADK city (block=%dm, fly_at=%dm) - %s'
                  % (n, n, block, fly_at, episode_label), fill='white', font=font_small)
        draw.text((BORDER + PAD, cap_y + 17), spec_text(mode, deadline), fill=(200, 200, 200), font=font_small)
        draw.text((BORDER + PAD, cap_y + 36),
                  'tick %3d   drone=(%d,%d)  target=(%d,%d)  dist=%d   %s' % (step, dx, dy, tx, ty, dist, status[0]),
                  fill=status[1] if status[1] != AMBER else (255, 200, 90), font=font_big)
        # legend
        leg_y = cap_y + 58
        draw.ellipse([BORDER + PAD, leg_y, BORDER + PAD + 12, leg_y + 12], fill=DRONE)
        draw.text((BORDER + PAD + 17, leg_y - 1), 'drone (verified NSBT)', fill=(200, 200, 200), font=font_small)
        draw.rectangle([BORDER + 190, leg_y, BORDER + 202, leg_y + 12], fill=TARGET)
        draw.text((BORDER + 207, leg_y - 1), 'target (ground vehicle)', fill=(200, 200, 200), font=font_small)
        draw.rectangle([BORDER + 390, leg_y, BORDER + 402, leg_y + 12], fill=OBSTACLE)
        draw.text((BORDER + 407, leg_y - 1), 'drone no-fly block (>=%dm structure)' % fly_at,
                  fill=(200, 200, 200), font=font_small)
        leg_y += 19
        draw.line([BORDER + PAD, leg_y + 6, BORDER + PAD + 12, leg_y + 6], fill=STREET_PATH, width=2)
        draw.text((BORDER + PAD + 17, leg_y - 1), 'actual street trajectory (target drives BELOW the no-fly blocks)',
                  fill=(200, 200, 200), font=font_small)
        leg_y += 19
        leg_x = BORDER + PAD
        for zone in zones:
            (fill, edge) = zone_style(zone)
            draw.rectangle([leg_x, leg_y, leg_x + 12, leg_y + 12],
                           fill=fill, outline=edge)
            text = '%s t=[%g,%g]s' % (zone['label'], zone['window_s'][0], zone['window_s'][1])
            draw.text((leg_x + 17, leg_y - 1), text, fill=(200, 200, 200), font=font_small)
            leg_x += 17 + 8 * len(text) + 20
        leg_y += 19
        koz_text = ('keep-out: none in episode' if not inventory.get('keep_out_zones')
                    else 'keep-out zones: %d (hatched red)' % inventory['keep_out_zones'])
        sw_text = ('stay-within: none (full map reachable)' if not inventory.get('stay_within_zones')
                   else 'stay-within zones: %d (cyan)' % inventory['stay_within_zones'])
        draw.text((BORDER + PAD, leg_y - 1), koz_text + '   ' + sw_text,
                  fill=(200, 200, 200), font=font_small)
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
    plain_flag = '--plain' in sys.argv
    argv = [a for a in sys.argv if a != '--plain']
    render(argv[1], argv[2], argv[3], argv[4], plain=plain_flag)
