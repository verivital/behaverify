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

usage: python3 gen_city_tracking.py [deadline=30] [ticks_per_waypoint=2]
'''
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A_STAR = os.path.join(HERE, '..', 'a_star_files')
IGNORE = os.path.join(A_STAR, 'ignore')
OBSTACLES = os.path.join(IGNORE, 'obstaclesFilled_24_80_61_2.txt')
TABLE = os.path.join(IGNORE, 'tableFilled_24_80_61_2.txt')
TARGET_CSV = ('/home/johnsott/ansr-final/github/ansr_benchmark/benchmark_gen/'
              'scratch/output-track/episode-000/trajectories/target-ojcfBtS.csv')

MIN_VAL = 0
MAX_VAL = 24
BLOCK = 40
HALF_WORLD = 500  # npz cell = world coord + 500 (center [0,0], resolution 1)


def world_to_block(w):
    return min(MAX_VAL, max(MIN_VAL, int((w + HALF_WORLD) // BLOCK)))


def load_target_path():
    '''downscale the episode target trajectory to a deduped block waypoint list'''
    blocks = []
    with open(TARGET_CSV, 'r', encoding='utf-8') as csv_file:
        for row in csv.reader(csv_file):
            block = (world_to_block(float(row[0])), world_to_block(float(row[1])))
            if not blocks or block != blocks[-1]:
                blocks.append(block)
    return blocks


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
    deadline = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    ticks_per_waypoint = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    path = load_target_path()
    (grid, number_of_obstacles) = load_obstacle_grid()
    cases = load_table_cases()
    net = make_net(cases)
    print('target waypoints (blocks):', path)
    print('final target block free:', grid[path[-1][0]][path[-1][1]] == 0)

    # rollout from every free cell: sanity for the SAT spec + sizing for step_max/deadline
    free_cells = [(x, y) for x in range(MAX_VAL + 1) for y in range(MAX_VAL + 1) if grid[x][y] == 0]
    catch_times = {}
    for start in free_cells:
        (caught, _) = rollout(net, path, ticks_per_waypoint, start)
        assert caught is not None, ('pursuit failed from free start', start)
        catch_times[start] = caught
    max_catch = max(catch_times.values())
    print('free cells:', len(free_cells), '| catch ticks: min',
          min(catch_times.values()), 'max', max_catch,
          '| worst start:', max(catch_times, key=catch_times.get))
    assert deadline < max_catch, 'deadline must be violable'
    step_max = ticks_per_waypoint * len(path) + 60
    print('step_max:', step_max, '| deadline:', deadline)

    # pick the sim start: catch time in [16, 24], farthest from the target start
    candidates = [s for (s, t) in catch_times.items() if 16 <= t <= 24]
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
        out = os.path.join(IGNORE, name)
        with open(out, 'w', encoding='utf-8') as output_file:
            output_file.write(text)
        print('wrote', out)

    emit('city_track_verify.tree', NONDET_INIT, NONDET_INIT, SPEC_SAT)
    emit('city_track_violation.tree', NONDET_INIT, NONDET_INIT, SPEC_VIOLATION)
    emit('city_track_sim.tree', str(sim_start[0]), str(sim_start[1]), SPEC_SAT)

    # persist the scenario metadata for the renderer
    import json
    meta = {
        'path': path, 'ticks_per_waypoint': ticks_per_waypoint,
        'step_max': step_max, 'deadline': deadline, 'sensor_range': 1,
        'sim_start': list(sim_start), 'sim_catch_tick': catch_times[sim_start],
        'max_catch_tick': max_catch,
        'worst_start': list(max(catch_times, key=catch_times.get)),
        'grid': grid,
    }
    with open(os.path.join(IGNORE, 'city_track_meta.json'), 'w', encoding='utf-8') as meta_file:
        json.dump(meta, meta_file)
    print('wrote', os.path.join(IGNORE, 'city_track_meta.json'))


if __name__ == '__main__':
    main()
