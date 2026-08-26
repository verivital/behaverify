'''
NSBT city tracking mission generator (overnight assurance run, 2026-07-02).

Builds verifiable BehaVerify .tree models of a drone-tracks-moving-target
mission on the 25x25 block-downsampled ADK city map
(a_star_files/ignore/obstaclesFilled_24_80_61_2.txt, from city_1000_1000.npz
via convert_npz block_size=40 fly_at=80).

The drone is the NSBT A*-table planner (the exact "fake network" table baked
by assemble_tree_SIMPLE_existing_obs.py); the moving target replays the
block-downsampled target trajectory of ansr_benchmark tracking episode-000
(target CSV world coords -> npz cell = world+500 -> block = cell//40,
orientation world x -> data axis 0, empirically validated: 0.0%% of vehicle
trajectory points land on height>=80 cells under this mapping and only this
mapping).

Emits three trees into a_star_files/ignore/:
  city_track_verify.tree    - drone start nondeterministic over ALL cells;
                              LTLSPEC (implies drone_safe (F found))       [expect TRUE]
                              LTLSPEC (implies drone_safe (G drone_safe))  [expect TRUE]
  city_track_violation.tree - same model;
                              LTLSPEC (implies drone_safe (F[0,deadline] found)) [expect FALSE]
  city_track_sim.tree       - fixed drone start (for the deterministic
                              witness trace rendered as the SAT animation)

Mission-zone incorporation (fidelity-audit update, 2026-07-02): ALL zone
information of the ACTUAL adapted episode
(release_installer/scenarios/GENERATED/track-episode-000-vu/description.json)
is parsed and projected into grid cells (world rect -> block rect via
block = (world + 500) // BLOCK on both axes, same transform as the target
trajectory).  For THIS episode: keep_out_zones = [], stay_within_zones = [],
areas_of_interest = [], routes_of_interest = [] (all empty -> the drone's
reachable set is the full grid and no KOZ cells exist); the only spatial
mission information is the target location_belief_map: two time-bounded
polygons (initial belief / search-start zone, active t in [5,20] s, and the
late-window "goal zone", active t in [92,111] s, probability 1.0).  The time
bounds are mapped to step-counter windows through the target-waypoint
schedule (waypoint k <-> steps [k*tpw, (k+1)*tpw - 1]; block-entry wall
times taken from the episode CSV) and encoded as step-dependent CTL
consistency specs:  AG (step in window -> target inside zone cells).
Non-empty keep_out_zones would be unioned into the obstacle set (drone-
forbidden; the target is a ground vehicle and is NOT constrained by drone
obstacles); non-empty stay_within_zones would bound the drone's grid.  Both
paths abort loudly if such zones appear until the table is re-baked.

usage: python3 gen_city_tracking.py [deadline=30] [ticks_per_waypoint=2]
           [--map-id Filled_24_80_61_2] [--block 40] [--max-val 24]
           [--fly-at 80] [--ignore-dir DIR] [--prefix city_track]
           [--allow-pursuit-failure]
'''
import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A_STAR = os.path.join(HERE, '..', 'a_star_files')
IGNORE = os.path.join(A_STAR, 'ignore')
TARGET_CSV = ('/home/johnsott/ansr-final/github/ansr_benchmark/benchmark_gen/'
              'scratch/output-track/episode-000/trajectories/target-ojcfBtS.csv')
EPISODE_DESC = ('/home/johnsott/ansr-final/gitlab/release_installer/scenarios/'
                'GENERATED/track-episode-000-vu/description.json')

MIN_VAL = 0
MAX_VAL = 24
BLOCK = 40
HALF_WORLD = 500  # npz cell = world coord + 500 (center [0,0], resolution 1)
# per-axis world->block origin offset: block = (w + OFF) // BLOCK. For the full
# 1000x1000 map OFF = HALF_WORLD = 500 on both axes (origin at world -500). For
# a cropped ROI (finer block over the region the drone/target actually traverse)
# OFF = -world_min of the ROI on that axis, so block 0 is the ROI's min corner.
X_OFF = 500
Y_OFF = 500


def world_to_block(w, off=None):
    return min(MAX_VAL, max(MIN_VAL, int((w + (HALF_WORLD if off is None else off)) // BLOCK)))


def load_target_path(target_csv):
    '''downscale the episode target trajectory to a deduped block waypoint
    list; also return the block-entry wall time (s) of every waypoint and a
    decimated world polyline (for the renderer street-path overlay)'''
    blocks = []
    entry_times = []
    polyline = []
    with open(target_csv, 'r', encoding='utf-8') as csv_file:
        for (i, row) in enumerate(csv.reader(csv_file)):
            block = (world_to_block(float(row[0]), X_OFF),
                     world_to_block(float(row[1]), Y_OFF))
            if not blocks or block != blocks[-1]:
                blocks.append(block)
                entry_times.append(float(row[3]))
            if i % 20 == 0:
                polyline.append((float(row[0]), float(row[1])))
    return (blocks, entry_times, polyline)


def rect_of_polygon(poly):
    '''episode zone polygons are closed axis-aligned rectangles; reduce to a
    world bbox and assert nothing is lost'''
    xs = sorted({v[0] for v in poly})
    ys = sorted({v[1] for v in poly})
    assert len(xs) == 2 and len(ys) == 2, ('non-rectangular zone polygon', poly)
    return (xs[0], ys[0], xs[1], ys[1])


def rect_to_block_rect(rect):
    '''world bbox -> inclusive block index ranges of every intersected block'''
    (x0, y0, x1, y1) = rect
    bx0 = max(MIN_VAL, int((x0 + X_OFF) // BLOCK))
    by0 = max(MIN_VAL, int((y0 + Y_OFF) // BLOCK))
    # subtract an epsilon so a boundary exactly on a block edge does not
    # drag in the next (untouched) block
    bx1 = min(MAX_VAL, int((x1 + X_OFF - 1e-9) // BLOCK))
    by1 = min(MAX_VAL, int((y1 + Y_OFF - 1e-9) // BLOCK))
    return (bx0, by0, bx1, by1)


def window_to_steps(window, entry_times, ticks_per_waypoint, step_max):
    '''[t_lo, t_hi] seconds -> inclusive step window: steps of every waypoint
    whose block-occupancy time span intersects the window (last waypoint is
    parked forever)'''
    (t_lo, t_hi) = window
    spans = [(entry_times[k],
              entry_times[k + 1] if k + 1 < len(entry_times) else float('inf'))
             for k in range(len(entry_times))]
    ks = [k for (k, (a, b)) in enumerate(spans) if a <= t_hi and b > t_lo]
    if not ks:
        return None
    lo = ticks_per_waypoint * min(ks)
    hi = (step_max if max(ks) == len(entry_times) - 1
          else ticks_per_waypoint * (max(ks) + 1) - 1)
    return (lo, hi)


def load_zones(episode_desc, entry_times, ticks_per_waypoint, step_max):
    '''parse ALL zone/constraint types of the adapted episode description;
    project each into block space; map time bounds to step windows'''
    desc = json.load(open(episode_desc, 'r', encoding='utf-8'))
    spatial = desc.get('scenario_constraints', {}).get('spatial_constraints', {})
    koz = spatial.get('keep_out_zones', [])
    swz = spatial.get('stay_within_zones', [])
    objective = desc.get('scenario_objective', {})
    aoi = objective.get('areas_of_interest', [])
    roi = objective.get('routes_of_interest', [])
    assert not koz, ('episode has keep_out_zones: union them into the obstacle '
                     'set and re-bake the A* table before generating', koz)
    assert not swz, ('episode has stay_within_zones: clamp the drone grid '
                     'bounds before generating', swz)
    zones = []
    for entity in objective.get('entities_of_interest', []):
        for belief in entity.get('entity_priors', {}).get('location_belief_map', []):
            polys = belief.get('polygon_vertices', [])
            earliest = belief.get('no_earlier_than', [])
            latest = belief.get('no_later_than', [])
            for (i, poly) in enumerate(polys):
                rect = rect_of_polygon(poly)
                window = (earliest[i] if i < len(earliest) else 0.0,
                          latest[i] if i < len(latest) else float('inf'))
                steps = window_to_steps(window, entry_times,
                                        ticks_per_waypoint, step_max)
                # episode-adapter convention: the LAST belief polygon is the
                # goal zone; the first is the initial belief / search start
                label = ('goal zone' if len(polys) > 1 and i == len(polys) - 1
                         else 'initial belief (search start)')
                zones.append({
                    'kind': 'belief', 'label': label,
                    'entity_id': entity.get('entity_id'),
                    'probability': belief.get('probability'),
                    'world_rect': rect, 'window_s': list(window),
                    'block_rect': rect_to_block_rect(rect),
                    'step_window': list(steps) if steps else None,
                })
    inventory = {
        'keep_out_zones': len(koz), 'stay_within_zones': len(swz),
        'areas_of_interest': len(aoi), 'routes_of_interest': len(roi),
        'belief_polygons': len(zones),
    }
    return (zones, inventory)


def zone_exprs(zone):
    (bx0, by0, bx1, by1) = zone['block_rect']
    (s_lo, s_hi) = zone['step_window']
    inside = ('(and, (gte, tar_x, %d), (lte, tar_x, %d), '
              '(gte, tar_y, %d), (lte, tar_y, %d))' % (bx0, bx1, by0, by1))
    when = ('(and, (gte, step, %d), (lte, step, %d))' % (s_lo, s_hi))
    return (when, inside)


def zone_spec(zone):
    '''step-counter-dependent CTL consistency spec: whenever the step counter
    is inside the zone's active window, the scripted target is inside the
    zone's block rectangle (containment semantics: park/goal-style beliefs)'''
    (when, inside) = zone_exprs(zone)
    return ('    CTLSPEC { (always_globally, (implies, %s, %s)) }'
            % (when, inside))


def zone_visit_spec(zone):
    '''step-counter-dependent CTL consistency spec, VISIT semantics (looping
    routes): on every path the scripted target is eventually inside the
    zone's block rectangle at some step of the zone's active window'''
    (when, inside) = zone_exprs(zone)
    return ('    CTLSPEC { (always_finally, (and, %s, %s)) }'
            % (when, inside))


def load_obstacle_grid():
    text = open(OBSTACLES, 'r', encoding='utf-8').read()
    (obs_part, size_part) = text.split('#', 1)
    size_part = size_part.replace('#', '')
    pair_re = re.compile(r'\(eq, index_var, (\d+)\)\} assign\{result\{(-?\d+)\}\}')
    coords = {int(i): int(v) for (i, v) in pair_re.findall(obs_part)}
    sizes = {int(i): int(v) for (i, v) in pair_re.findall(size_part)}
    grid = [[0] * (MAX_VAL + 1) for _ in range(MAX_VAL + 1)]
    for k in range(len(sizes)):
        (x, y, s) = (coords[2 * k], coords[2 * k + 1], sizes[k])
        for gx in range(max(0, x - s), x + 1):
            for gy in range(max(0, y - s), y + 1):
                grid[gx][gy] = 1
    return (grid, len(sizes))


def load_table_cases():
    '''ordered (interval-dict, move) list of the exact A* table'''
    text = open(TABLE, 'r', encoding='utf-8').read()
    case_re = re.compile(r"case\{\(and,([^}]*)\)\}\s*result\{'(\w\w)'\}")
    cases = []
    for match in case_re.finditer(text):
        (conds, move) = (match.group(1), match.group(2))
        intervals = {}
        for vm in re.finditer(r'\(eq, (x_d|y_d|x_g|y_g), (\d+)\)', conds):
            intervals[vm.group(1)] = (int(vm.group(2)), int(vm.group(2)))
        for vm in re.finditer(r'\(lte,\s*(\d+), (x_d|y_d|x_g|y_g)\), \(lte, \2, (\d+)\)', conds):
            intervals[vm.group(2)] = (int(vm.group(1)), int(vm.group(3)))
        assert set(intervals) == {'x_d', 'y_d', 'x_g', 'y_g'}
        cases.append((intervals, move))
    return cases


def make_net(cases):
    cache = {}

    def net(xd, yd, xg, yg):
        key = (xd, yd, xg, yg)
        if key not in cache:
            result = 'XX'
            for (iv, move) in cases:
                if (iv['x_d'][0] <= xd <= iv['x_d'][1] and iv['y_d'][0] <= yd <= iv['y_d'][1]
                        and iv['x_g'][0] <= xg <= iv['x_g'][1] and iv['y_g'][0] <= yg <= iv['y_g'][1]):
                    result = move
                    break
            cache[key] = result
        return cache[key]
    return net


DELTA = {'We': (-1, 0), 'Ea': (1, 0), 'No': (0, 1), 'So': (0, -1), 'XX': (0, 0)}


def rollout(net, path, ticks_per_waypoint, start, max_ticks=400):
    '''mirror of the .tree semantics: state t = (drone, target(step=t));
    tick computes act from state t; env update moves drone and increments step.
    returns (catch_tick_or_None, states)'''
    def target(step):
        return path[min(len(path) - 1, step // ticks_per_waypoint)]
    (x, y) = start
    states = []
    caught = None
    for tick in range(max_ticks):
        (tx, ty) = target(tick)
        found = abs(x - tx) + abs(y - ty) <= 1
        states.append((x, y, tx, ty, found))
        if found and caught is None:
            caught = tick
            break
        (dx, dy) = DELTA[net(x, y, tx, ty)]
        x = max(MIN_VAL, min(MAX_VAL, x + dx))
        y = max(MIN_VAL, min(MAX_VAL, y + dy))
    return (caught, states)


TEMPLATE = '''configuration {} enumerations {'We', 'Ea', 'No', 'So', 'XX'}
constants {REPLACE_CONSTANTS}
variables {
    variable { bl act VAR {'We', 'Ea', 'No', 'So', 'XX'} assign{result{'XX'}}}
    variable { env x_d VAR [min_val, max_val] assign{result{REPLACE_INIT_X}}}
    variable { env y_d VAR [min_val, max_val] assign{result{REPLACE_INIT_Y}}}
    variable { env step VAR [0, step_max] assign{result{0}}}
    variable { env tar_x DEFINE INT assign{
REPLACE_TAR_X_CASES
	    result{REPLACE_TAR_X_LAST}}}
    variable { env tar_y DEFINE INT assign{
REPLACE_TAR_Y_CASES
	    result{REPLACE_TAR_Y_LAST}}}
    variable { env x_g DEFINE INT assign{result{tar_x}}}
    variable { env y_g DEFINE INT assign{result{tar_y}}}
    variable { env found DEFINE BOOLEAN assign{result{
	(lte, (add, (abs, (sub, x_d, tar_x)), (abs, (sub, y_d, tar_y))), sensor_range)}}}
    variable { env net DEFINE ENUM assign{
	    REPLACE_FAKE_NETWORK
	}
    }
    variable { env obstacles DEFINE INT static array (mult, number_of_obstacles, 2) iterative_assign, index_var
	REPLACE_OBSTACLES
	assign{result{0}}
    }
    variable { env obstacle_sizes DEFINE INT static array number_of_obstacles iterative_assign, index_var
	REPLACE_OBSTACLE_SIZES
	assign{result{0}}
    }
    variable { env drone_safe DEFINE BOOLEAN assign{result{
	(not,
	    (or,
		(loop, loop_var, [0, (sub, number_of_obstacles, 1)] such_that True,
		    (and,
			(lte, x_d, (index, obstacles, constant_index (mult, loop_var, 2))),
			(gte, x_d, (sub, (index, obstacles, constant_index (mult, loop_var, 2)), (index, obstacle_sizes, constant_index loop_var))),
			(lte, y_d, (index, obstacles, constant_index (add, (mult, loop_var, 2), 1))),
			(gte, y_d, (sub, (index, obstacles, constant_index (add, (mult, loop_var, 2), 1)), (index, obstacle_sizes, constant_index loop_var)))
		    )
		)
	    )
	)}}}
} environment_update {
    variable_statement {x_d
	assign {
	    case {(eq, act, 'We')} result { (max, min_val, (sub, x_d, 1))}
	    case {(eq, act, 'Ea')} result { (min, max_val, (add, x_d, 1))}
	    result {x_d}}}
    variable_statement {y_d
	assign {
	    case {(eq, act, 'So')} result { (max, min_val, (sub, y_d, 1))}
	    case {(eq, act, 'No')} result { (min, max_val, (add, y_d, 1))}
	    result {y_d}}}
    variable_statement {step
	assign {
	    case {(lt, step, step_max)} result {(add, step, 1)}
	    result {step}}}
} checks {}
environment_checks {
    environment_check { TargetFound
	arguments {} read_variables { x_d, y_d, act}
	condition {found}}
} actions {
    action { Hover
	arguments{} local_variables {}read_variables {} write_variables {act}
	initial_values {}
	update {
	    variable_statement { act assign{result{'XX'}}}
	    return_statement {result {success}}
	}
    } action {NextAct
	arguments{} local_variables {}read_variables {} write_variables {act}
	initial_values {}
	update {
	    read_environment {
		read_net
		condition{True}
		variable_statement {act assign {result{net}}}
	    }
	    return_statement {result { success}}
	}
    }
} sub_trees {}
tree {
    composite {Drone selector children {
	    composite { FoundSeq sequence children { TargetFound {} Hover {}}}
	    NextAct {}
	}
    }
}
tick_prerequisite {(True)}
specifications {
REPLACE_SPECS
}
'''

#{ primary engine: CTL (check_ctlspec, the engine used for all prior ANSRt
#  table models, see a_star_files/RESULTS_*.txt); the LTL twins of the same
#  properties are kept in the model for check_ltlspec if runtime allows. }
SPEC_SAT = '''    CTLSPEC { (implies, drone_safe, (always_finally, found)) }
    CTLSPEC { (implies, drone_safe, (always_globally, drone_safe)) }
    LTLSPEC { (implies, drone_safe, (finally, found)) }
    LTLSPEC { (implies, drone_safe, (globally, drone_safe)) }'''
SPEC_VIOLATION = '''    CTLSPEC { (implies, drone_safe, (always_finally, (and, found, (lte, step, deadline)))) }
    LTLSPEC { (implies, drone_safe, (finally_bounded, [0, deadline], found)) }'''
NONDET_INIT = '(loop, loop_var, [min_val, max_val] such_that True, loop_var)'


def main():
    global MAX_VAL, BLOCK, OBSTACLES, TABLE, X_OFF, Y_OFF
    parser = argparse.ArgumentParser()
    parser.add_argument('deadline', nargs='?', type=int, default=30)
    parser.add_argument('ticks_per_waypoint', nargs='?', type=int, default=2)
    parser.add_argument('--map-id', default='Filled_24_80_61_2')
    parser.add_argument('--block', type=int, default=40)
    parser.add_argument('--max-val', type=int, default=24)
    parser.add_argument('--fly-at', type=int, default=80)
    parser.add_argument('--x-off', type=float, default=None,
                        help='world->block x origin offset: bx=(wx+x_off)//block '
                             '(ROI crop; default HALF_WORLD=500 = full-map origin)')
    parser.add_argument('--y-off', type=float, default=None,
                        help='world->block y origin offset (default 500)')
    parser.add_argument('--ignore-dir', default=IGNORE)
    parser.add_argument('--prefix', default='city_track')
    parser.add_argument('--allow-pursuit-failure', action='store_true')
    parser.add_argument('--target-csv', default=TARGET_CSV,
                        help='episode target trajectory CSV [x,y,heading,t]')
    parser.add_argument('--episode-desc', default=EPISODE_DESC,
                        help='adapted episode description.json')
    parser.add_argument('--episode-label', default='episode-000 track',
                        help='human label stored in meta for the renderers')
    args = parser.parse_args()
    (deadline, ticks_per_waypoint) = (args.deadline, args.ticks_per_waypoint)
    (MAX_VAL, BLOCK) = (args.max_val, args.block)
    X_OFF = HALF_WORLD if args.x_off is None else args.x_off
    Y_OFF = HALF_WORLD if args.y_off is None else args.y_off
    out_dir = args.ignore_dir
    OBSTACLES = os.path.join(out_dir, 'obstacles%s.txt' % args.map_id)
    TABLE = os.path.join(out_dir, 'table%s.txt' % args.map_id)

    (path, entry_times, polyline) = load_target_path(args.target_csv)
    (grid, number_of_obstacles) = load_obstacle_grid()
    cases = load_table_cases()
    net = make_net(cases)
    print('target waypoints (blocks):', path)
    print('final target block free:', grid[path[-1][0]][path[-1][1]] == 0)
    print('waypoints inside drone-obstacle blocks (target is a ground '
          'vehicle, unconstrained):',
          sum(1 for (x, y) in path if grid[x][y] == 1), '/', len(path))

    # rollout from every free cell: sanity for the SAT spec + sizing for step_max/deadline
    free_cells = [(x, y) for x in range(MAX_VAL + 1) for y in range(MAX_VAL + 1) if grid[x][y] == 0]
    catch_times = {}
    failed_starts = []
    for start in free_cells:
        (caught, _) = rollout(net, path, ticks_per_waypoint, start)
        if caught is None:
            failed_starts.append(start)
            assert args.allow_pursuit_failure, ('pursuit failed from free start', start)
        else:
            catch_times[start] = caught
    max_catch = max(catch_times.values())
    print('free cells:', len(free_cells), '| pursuit failures:', len(failed_starts),
          '| catch ticks: min', min(catch_times.values()), 'max', max_catch,
          '| worst start:', max(catch_times, key=catch_times.get))
    if failed_starts:
        print('WARNING: F(found) is expected FALSE at this abstraction; '
              'failing starts (first 10):', failed_starts[:10])
    assert deadline < max_catch, 'deadline must be violable'
    step_max = ticks_per_waypoint * len(path) + 60
    print('step_max:', step_max, '| deadline:', deadline)

    # mission zones of the ACTUAL adapted episode
    (zones, inventory) = load_zones(args.episode_desc, entry_times,
                                    ticks_per_waypoint, step_max)
    print('zone inventory of', args.episode_desc, '->', inventory)
    zone_specs = []
    for zone in zones:
        print('  zone [%s] world_rect=%s window_s=%s -> blocks=%s steps=%s'
              % (zone['label'], zone['world_rect'], zone['window_s'],
                 zone['block_rect'], zone['step_window']))
        if zone['step_window'] is None:
            print('    (window precedes/follows the scripted path: no spec)')
            continue
        # python-mirror consistency check picks the belief semantics:
        #   containment (AG window -> in zone) if the scripted target never
        #   leaves the zone inside its window (park/goal-style episodes);
        #   otherwise visit (AF (window & in zone)) for looping routes that
        #   pass through the belief zone during the window.
        (bx0, by0, bx1, by1) = zone['block_rect']
        (s_lo, s_hi) = zone['step_window']
        in_zone_steps = []
        for step in range(s_lo, min(s_hi, step_max) + 1):
            (tx, ty) = path[min(len(path) - 1, step // ticks_per_waypoint)]
            if bx0 <= tx <= bx1 and by0 <= ty <= by1:
                in_zone_steps.append(step)
        window_steps = min(s_hi, step_max) - s_lo + 1
        assert in_zone_steps, \
            ('scripted target NEVER inside zone during its window '
             '(belief map inconsistent with trajectory)', zone)
        if len(in_zone_steps) == window_steps:
            zone['spec_kind'] = 'containment (AG window -> in zone)'
            zone_specs.append(zone_spec(zone))
        else:
            zone['spec_kind'] = 'visit (AF (window & in zone))'
            zone_specs.append(zone_visit_spec(zone))
        print('    in-zone steps %d/%d -> %s'
              % (len(in_zone_steps), window_steps, zone['spec_kind']))
    zone_spec_text = ('\n' + '\n'.join(zone_specs)) if zone_specs else ''

    # pick the sim start: catch time in [16, 24], farthest from the target start
    candidates = [s for (s, t) in catch_times.items() if 16 <= t <= 24]
    if not candidates:
        candidates = list(catch_times)
    sim_start = max(candidates, key=lambda s: (s[0] - path[0][0]) ** 2 + (s[1] - path[0][1]) ** 2)
    print('sim start:', sim_start, 'catch tick:', catch_times[sim_start])

    # target script case chains over step
    def chain(axis):
        lines = []
        for (k, wp) in enumerate(path[:-1]):
            hi = ticks_per_waypoint * (k + 1) - 1
            lines.append('\t    case {(lte, step, %d)} result {%d}' % (hi, wp[axis]))
        return '\n'.join(lines)

    constants = ', '.join([
        'min_val := %d' % MIN_VAL, 'max_val := %d' % MAX_VAL,
        'number_of_obstacles := %d' % number_of_obstacles,
        'max_obstacle_size := 2',
        'step_max := %d' % step_max, 'deadline := %d' % deadline,
        'sensor_range := 1'])
    fake_network = open(TABLE, 'r', encoding='utf-8').read()
    data = open(OBSTACLES, 'r', encoding='utf-8').read()
    (obstacles, obstacle_sizes) = data.split('#', 1)
    obstacles = obstacles.replace('#', '')
    obstacle_sizes = obstacle_sizes.replace('#', '')

    def emit(name, init_x, init_y, specs):
        text = (TEMPLATE
                .replace('REPLACE_CONSTANTS', constants)
                .replace('REPLACE_INIT_X', init_x)
                .replace('REPLACE_INIT_Y', init_y)
                .replace('REPLACE_TAR_X_CASES', chain(0))
                .replace('REPLACE_TAR_X_LAST', str(path[-1][0]))
                .replace('REPLACE_TAR_Y_CASES', chain(1))
                .replace('REPLACE_TAR_Y_LAST', str(path[-1][1]))
                .replace('REPLACE_FAKE_NETWORK', fake_network)
                .replace('REPLACE_OBSTACLES', obstacles)
                .replace('REPLACE_OBSTACLE_SIZES', obstacle_sizes)
                .replace('REPLACE_SPECS', specs))
        out = os.path.join(out_dir, name)
        with open(out, 'w', encoding='utf-8') as output_file:
            output_file.write(text)
        print('wrote', out)

    emit('%s_verify.tree' % args.prefix, NONDET_INIT, NONDET_INIT,
         SPEC_SAT + zone_spec_text)
    emit('%s_violation.tree' % args.prefix, NONDET_INIT, NONDET_INIT,
         SPEC_VIOLATION)
    emit('%s_sim.tree' % args.prefix, str(sim_start[0]), str(sim_start[1]),
         SPEC_SAT + zone_spec_text)

    # persist the scenario metadata for the renderer
    meta = {
        'path': path, 'ticks_per_waypoint': ticks_per_waypoint,
        'step_max': step_max, 'deadline': deadline, 'sensor_range': 1,
        'sim_start': list(sim_start), 'sim_catch_tick': catch_times[sim_start],
        'max_catch_tick': max_catch,
        'worst_start': list(max(catch_times, key=catch_times.get)),
        'grid': grid,
        'block': BLOCK, 'fly_at': args.fly_at, 'map_id': args.map_id,
        'x_off': X_OFF, 'y_off': Y_OFF,
        'zones': zones, 'zone_inventory': inventory,
        'pursuit_failures': failed_starts,
        'target_world_polyline': polyline,
        'episode_label': args.episode_label,
        'target_csv': args.target_csv, 'episode_desc': args.episode_desc,
    }
    meta_path = os.path.join(out_dir, '%s_meta.json' % args.prefix)
    with open(meta_path, 'w', encoding='utf-8') as meta_file:
        json.dump(meta, meta_file)
    print('wrote', meta_path)


if __name__ == '__main__':
    main()
