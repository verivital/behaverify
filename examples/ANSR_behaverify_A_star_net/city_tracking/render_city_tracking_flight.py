'''
Gridworld renderer for a REAL tracking flight (2026-07-02) -- the flight twin
of render_city_tracking.py.

Instead of a nuXmv trace, this renders per-tick (default 0.5 s mission time)
frames of the 25x25 city block grid from ACTUAL bag telemetry:

    drone   - actual_pose_10hz (header stamps = sim/mission clock) CSV
              [t_log, t_header, x, y, z]
    target  - ground-truth trajectory CSV [x, y, heading, t_mission]
              (mission_briefing/trajectories/target-*.csv)

World -> block transform is identical to the abstraction (and to the audit):
b = (w + 500) // block on both axes. Visual style (colors, layout, zones,
legend) matches render_city_tracking.py exactly; the spec-status border is
driven by the REAL acquisition event (perception match time from the run log,
--found-t) against the LTL window [--window T0 T1]:

    amber - PENDING (window not yet satisfied)
    green - SAT (target acquired inside the window)
    red   - VIOLATED (window elapsed without acquisition)

usage:
  python3 render_city_tracking_flight.py <meta.json> <drone_pose.csv> \
      <target.csv> <frames_dir> [--tick 0.5] [--t0 0] [--t1 245] \
      [--found-t 14.829] [--window 5 111] [--modes modes.json]

outputs numbered frames <frames_dir>/frame_%05d.png (one per tick).
'''
import argparse
import json
import math
import os

from PIL import Image, ImageDraw

import render_city_tracking as base

AMBER = base.AMBER
GREEN = base.GREEN
RED = base.RED
LIGHT_BUILDING = (196, 202, 210)   # mid-height building, below the no-fly threshold

SPEC_LINE = ('Spec window [%g,%g]s: eventually acquire target  '
             '[BehaVerify/nuXmv model: SAT]')


def building_grid(elev_path, n, block, x_off, y_off, thresh):
    '''per-cell mid-height building mask (block-max ground elevation >= thresh) so
    the twin can show the real city buildings that fall below the verified no-fly
    height. Visualization only -- the verified obstacle set stays meta['grid'].'''
    import numpy as _np
    e = _np.fromfile(elev_path, dtype=_np.float32).reshape(1000, 1000)
    b = [[0] * n for _ in range(n)]
    for gx in range(n):
        ix = int(gx * block - x_off + 500)
        for gy in range(n):
            iy = int(gy * block - y_off + 500)
            blk = e[ix:ix + block, iy:iy + block]
            if blk.size and blk.max() >= thresh:
                b[gx][gy] = 1
    return b


def load_csv(path, cols):
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        header = None
        for line in f:
            parts = line.strip().split(',')
            if header is None and any(c.isalpha() for c in parts[0]):
                header = parts
                continue
            rows.append(tuple(float(parts[c]) for c in cols))
    rows.sort(key=lambda r: r[0])
    return rows


def interp(rows, t):
    '''rows sorted by rows[i][0]; linear interp of remaining cols, clamped.'''
    if t <= rows[0][0]:
        return rows[0][1:]
    if t >= rows[-1][0]:
        return rows[-1][1:]
    lo, hi = 0, len(rows) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if rows[mid][0] <= t:
            lo = mid
        else:
            hi = mid
    (ta, tb) = (rows[lo][0], rows[hi][0])
    w = 0.0 if tb == ta else (t - ta) / (tb - ta)
    return tuple(a + w * (b - a) for (a, b) in zip(rows[lo][1:], rows[hi][1:]))


def render(args):
    meta = json.load(open(args.meta, 'r', encoding='utf-8'))
    grid = meta['grid']
    n = len(grid)
    sensor = meta['sensor_range']
    block = meta.get('block', 40)
    fly_at = meta.get('fly_at', 80)
    x_off = meta.get('x_off', 500)
    y_off = meta.get('y_off', 500)
    zones = meta.get('zones', [])
    inventory = meta.get('zone_inventory', {})
    polyline = meta.get('target_world_polyline', [])

    buildings = None
    if args.elev and os.path.exists(args.elev):
        buildings = building_grid(args.elev, n, block, x_off, y_off, args.build_thresh)

    drone = load_csv(args.drone_csv, (1, 2, 3, 4))     # t_header, x, y, z
    target = load_csv(args.target_csv, (3, 0, 1))      # t, x, y
    modes = []
    if args.modes:
        modes = sorted(json.loads(open(args.modes).read()), key=lambda m: m[0])

    short_modes = {'AREA_SEARCH_FIRST_TARGET': 'SEARCH',
                   'TRACKING': 'TRACK',
                   'AREA_SEARCH_TARGET_LOST': 'SEARCH-LOST'}

    def mode_at(mt):
        cur = ''
        for (mtime, label) in modes:
            if mtime <= mt:
                cur = label
        return short_modes.get(cur, cur)

    def to_block(wx, wy):
        return (max(0, min(n - 1, int((wx + x_off) // block))),
                max(0, min(n - 1, int((wy + y_off) // block))))

    def world_to_px(wx, wy):
        bx = (wx + x_off) / block
        by = (wy + y_off) / block
        return (base.BORDER + base.PAD + bx * base.CELL,
                base.BORDER + base.PAD + (n - by) * base.CELL)

    width = 2 * (base.BORDER + base.PAD) + n * base.CELL
    height = (2 * (base.BORDER + base.PAD) + n * base.CELL
              + (0 if args.plain else base.CAPTION))
    font_big = base.get_font(15)
    font_small = base.get_font(12)
    os.makedirs(args.frames_dir, exist_ok=True)

    (w0, w1) = args.window
    n_frames = int(round((args.t1 - args.t0) / args.tick)) + 1
    drone_trail = []          # block trail (draw style of the model renderer)
    target_trail = []
    drone_world = []          # continuous world path (provenance overlay)
    print('rendering %d gridworld frames (t %g..%g s, tick %g s)'
          % (n_frames, args.t0, args.t1, args.tick))

    for k in range(n_frames):
        mt = args.t0 + k * args.tick
        (dxw, dyw, dzw) = interp(drone, mt)
        (txw, tyw) = interp(target, mt)
        (dx, dy) = to_block(dxw, dyw)
        (tx, ty) = to_block(txw, tyw)
        dist = abs(dx - tx) + abs(dy - ty)
        dist_m = math.hypot(dxw - txw, dyw - tyw)
        found_ever = mt >= args.found_t and args.found_t <= w1
        violated = (not found_ever) and mt > w1

        if found_ever:
            status = ('SAT: FOUND t=%.1fs' % args.found_t, GREEN)
        elif violated:
            status = ('VIOLATED: window elapsed', RED)
        elif mt < w0:
            status = ('PENDING: opens in %.0fs' % (w0 - mt), AMBER)
        else:
            status = ('PENDING: %.0fs left' % (w1 - mt), AMBER)

        image = Image.new('RGB', (width, height),
                          base.GRID_LINE if args.plain else status[1])
        draw = ImageDraw.Draw(image)
        draw.rectangle([base.BORDER, base.BORDER, width - base.BORDER,
                        height - base.BORDER
                        - (0 if args.plain else base.CAPTION - base.PAD)],
                       fill=base.FREE)
        for gx in range(n):
            for gy in range(n):
                box = base.cell_box(gx, gy, n)
                if grid[gx][gy] == 1:
                    draw.rectangle(box, fill=base.OBSTACLE)
                elif buildings is not None and buildings[gx][gy]:
                    draw.rectangle(box, fill=LIGHT_BUILDING, outline=base.GRID_LINE)
                else:
                    draw.rectangle(box, outline=base.GRID_LINE)
        # mission zones: tint free cells, boundary thick while window active
        for zone in zones:
            (fill, edge) = (base.ZONE_GOAL_FILL, base.ZONE_GOAL_EDGE) \
                if zone['label'].startswith('goal') \
                else (base.ZONE_BELIEF_FILL, base.ZONE_BELIEF_EDGE)
            if zone['kind'] == 'keep_out':
                (fill, edge) = (None, base.KOZ_EDGE)
            elif zone['kind'] == 'stay_within':
                (fill, edge) = (None, base.STAY_WITHIN_EDGE)
            (bx0, by0, bx1, by1) = zone['block_rect']
            if fill is not None:
                for gx in range(bx0, bx1 + 1):
                    for gy in range(by0, by1 + 1):
                        if grid[gx][gy] == 0:
                            draw.rectangle(base.cell_box(gx, gy, n),
                                           fill=fill, outline=base.GRID_LINE)
            lo = base.cell_box(bx0, by1, n)
            hi = base.cell_box(bx1, by0, n)
            (z0, z1) = zone['window_s']
            active = z0 <= mt <= z1
            if zone['kind'] == 'keep_out':
                for off in range(0, (hi[2] - lo[0]) + (hi[3] - lo[1]), 10):
                    draw.line([(lo[0] + off, lo[1]), (lo[0], lo[1] + off)],
                              fill=edge, width=1)
            draw.rectangle([lo[0], lo[1], hi[2], hi[3]], outline=edge,
                           width=4 if active else 2)
        # actual target street trajectory (episode CSV, world coords)
        if polyline:
            draw.line([world_to_px(wx, wy) for (wx, wy) in polyline],
                      fill=base.STREET_PATH, width=2)
        # continuous world flight path of the REAL drone (provenance)
        drone_world.append(world_to_px(dxw, dyw))
        if len(drone_world) > 1:
            draw.line(drone_world, fill=base.DRONE_TRAIL, width=2)
        # block trails (same style as the model renderer)
        if not drone_trail or drone_trail[-1] != (dx, dy):
            drone_trail.append((dx, dy))
        if not target_trail or target_trail[-1] != (tx, ty):
            target_trail.append((tx, ty))
        for (px, py) in target_trail[:-1]:
            box = base.cell_box(px, py, n)
            draw.rectangle([box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8],
                           fill=base.TARGET_TRAIL)
        for (px, py) in drone_trail[:-1]:
            box = base.cell_box(px, py, n)
            draw.ellipse([box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8],
                         fill=base.DRONE_TRAIL)
        # sensor footprint
        ring = GREEN if (found_ever and dist <= sensor) else base.DRONE
        for ox in range(-sensor, sensor + 1):
            for oy in range(-sensor, sensor + 1):
                if 0 < abs(ox) + abs(oy) <= sensor:
                    (sx, sy) = (dx + ox, dy + oy)
                    if 0 <= sx < n and 0 <= sy < n:
                        draw.rectangle(base.cell_box(sx, sy, n),
                                       outline=ring, width=2)
        # target
        box = base.cell_box(tx, ty, n)
        draw.rectangle([box[0] + 3, box[1] + 3, box[2] - 3, box[3] - 3],
                       fill=base.TARGET)
        if not args.plain:
            draw.text((box[0] + 8, box[1] + 5), 'T', fill='white',
                      font=font_small)
        # drone
        box = base.cell_box(dx, dy, n)
        draw.ellipse([box[0] + 2, box[1] + 2, box[2] - 2, box[3] - 2],
                     fill=base.DRONE, outline='white')
        if args.plain:
            image.save(os.path.join(args.frames_dir, 'frame_%05d.png' % k))
            continue
        draw.text((box[0] + 8, box[1] + 5), 'D', fill='white',
                  font=font_small)
        # caption
        cap_y = height - base.CAPTION - base.BORDER + 2 * base.PAD
        draw.rectangle([base.BORDER,
                        height - base.CAPTION - base.BORDER + base.PAD,
                        width - base.BORDER, height - base.BORDER],
                       fill=(25, 28, 32))
        draw.text((base.BORDER + base.PAD, cap_y),
                  'GRIDWORLD TWIN %s - %dx%d (block %dm, fly_at %dm)'
                  % (args.run_label, n, n, block, fly_at),
                  fill='white', font=font_small)
        draw.text((base.BORDER + base.PAD, cap_y + 17),
                  SPEC_LINE % (w0, w1), fill=(200, 200, 200),
                  font=font_small)
        mode = mode_at(mt)
        draw.text((base.BORDER + base.PAD, cap_y + 36),
                  't=%6.1fs %s D=(%d,%d) T=(%d,%d) dist=%d blk (%.0f m)  %s'
                  % (mt, ('[%s]' % mode) if mode else '', dx, dy, tx, ty,
                     dist, dist_m, status[0]),
                  fill=status[1] if status[1] != AMBER else (255, 200, 90),
                  font=font_big)
        leg_y = cap_y + 58
        draw.ellipse([base.BORDER + base.PAD, leg_y,
                      base.BORDER + base.PAD + 12, leg_y + 12],
                     fill=base.DRONE)
        draw.text((base.BORDER + base.PAD + 17, leg_y - 1),
                  'drone (bag telemetry)', fill=(200, 200, 200),
                  font=font_small)
        draw.rectangle([base.BORDER + 230, leg_y, base.BORDER + 242,
                        leg_y + 12], fill=base.TARGET)
        draw.text((base.BORDER + 247, leg_y - 1),
                  'target (ground vehicle, GT)', fill=(200, 200, 200),
                  font=font_small)
        draw.rectangle([base.BORDER + 440, leg_y, base.BORDER + 452,
                        leg_y + 12], fill=base.OBSTACLE)
        draw.text((base.BORDER + 457, leg_y - 1),
                  'no-fly (>=%dm)' % fly_at, fill=(200, 200, 200), font=font_small)
        if buildings is not None:
            draw.rectangle([base.BORDER + 560, leg_y, base.BORDER + 572,
                            leg_y + 12], fill=LIGHT_BUILDING)
            draw.text((base.BORDER + 577, leg_y - 1), 'building (<no-fly)',
                      fill=(200, 200, 200), font=font_small)
        leg_y += 19
        leg_x = base.BORDER + base.PAD
        for zone in zones:
            (fill, edge) = (base.ZONE_GOAL_FILL, base.ZONE_GOAL_EDGE) \
                if zone['label'].startswith('goal') \
                else (base.ZONE_BELIEF_FILL, base.ZONE_BELIEF_EDGE)
            draw.rectangle([leg_x, leg_y, leg_x + 12, leg_y + 12],
                           fill=fill, outline=edge)
            text = '%s t=[%g,%g]s' % (zone['label'], zone['window_s'][0],
                                      zone['window_s'][1])
            draw.text((leg_x + 17, leg_y - 1), text, fill=(200, 200, 200),
                      font=font_small)
            leg_x += 17 + 8 * len(text) + 20
        leg_y += 19
        koz_text = ('keep-out: none in episode'
                    if not inventory.get('keep_out_zones')
                    else 'keep-out zones: %d (hatched red)'
                    % inventory['keep_out_zones'])
        sw_text = ('stay-within: none (full map reachable)'
                   if not inventory.get('stay_within_zones')
                   else 'stay-within zones: %d (cyan)'
                   % inventory['stay_within_zones'])
        draw.text((base.BORDER + base.PAD, leg_y - 1),
                  koz_text + '   ' + sw_text, fill=(200, 200, 200),
                  font=font_small)
        image.save(os.path.join(args.frames_dir, 'frame_%05d.png' % k))
    print('wrote %d frames to %s' % (n_frames, args.frames_dir))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('meta')
    ap.add_argument('drone_csv')
    ap.add_argument('target_csv')
    ap.add_argument('frames_dir')
    ap.add_argument('--tick', type=float, default=0.5)
    ap.add_argument('--t0', type=float, default=0.0)
    ap.add_argument('--t1', type=float, default=245.0)
    ap.add_argument('--found-t', type=float, default=14.829)
    ap.add_argument('--window', nargs=2, type=float, default=[5.0, 111.0])
    ap.add_argument('--modes', default=None)
    ap.add_argument('--run-label', default='trackrun_2026_07_02__09_27_14')
    ap.add_argument('--plain', action='store_true',
                    help='grid+markers+trails only: no caption, no border '
                         'status, no text')
    ap.add_argument('--elev', default=None,
                    help='city_elev.f32 (1000x1000): draw mid-height buildings '
                         '(below the no-fly height) as a light tier so the twin '
                         'matches the overhead city (visualization only)')
    ap.add_argument('--build-thresh', type=float, default=10.0,
                    help='min ground elevation (m) to show as a building tier')
    render(ap.parse_args())
