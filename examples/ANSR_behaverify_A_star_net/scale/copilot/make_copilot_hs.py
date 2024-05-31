import os
import sys
def indent(n):
    return ' ' * (4 * n)
MAX_VAL = int(sys.argv[1])
NUMBER_OF_OBSTACLES = int(sys.argv[2])
OBSTACLE_FILE = sys.argv[3]
OUTPUT_LOCATION = sys.argv[4]
def create_obstacle_definition():
    obstacles = {}
    obstacle_sizes = {}
    with open(OBSTACLE_FILE, 'r', encoding = 'utf-8') as input_file:
        data = input_file.read()
        data = data.replace('condition {(eq, index_var,', '')
        data = data.replace(')} assign{result{', ', ')
        data = data.replace('}}', ';')
        (locations, sizes) = data.split('#', 1)
        locations = locations.replace('#', '')
        sizes = sizes.replace('#', '')
        for index_val in locations.split(';'):
            if index_val.strip() == '':
                continue
            (index, val) = index_val.split(',')
            index = int(index.strip())
            val = int(val.strip())
            obstacles[index] = val
        for index_val in sizes.split(';'):
            if index_val.strip() == '':
                continue
            (index, val) = index_val.split(',')
            index = int(index.strip())
            val = int(val.strip())
            obstacle_sizes[index] = val
    return (
        'obs :: Stream (Array ' + str(len(obstacles)) + ' Int32)' + os.linesep
        + 'obs = [array [' + ', '.join([str(obstacles[index]) for index in range(len(obstacles))]) + ']] ++ obs' + os.linesep
        + 'obs_size :: Stream (Array ' + str(len(obstacle_sizes)) + ' Int32)' + os.linesep
        + 'obs_size = [array [' + ', '.join([str(obstacle_sizes[index]) for index in range(len(obstacle_sizes))]) + ']] ++ obs_size' + os.linesep
    )
OBSTACLE_DEFINITION = create_obstacle_definition()
PREAMBLE = (
    '{-# LANGUAGE DataKinds        #-}' + os.linesep
    + '{-# LANGUAGE RebindableSyntax #-}' + os.linesep
    + os.linesep
    + 'module Main where' + os.linesep
    + 'import Language.Copilot' + os.linesep
    + 'import Copilot.Compile.C99' + os.linesep
)
SAFETY_POSTAMBLE = (
    os.linesep
    + OBSTACLE_DEFINITION + os.linesep
    + os.linesep
    + os.linesep
    + 'drone_x :: Stream Int32' + os.linesep
    + 'drone_x = extern "drone_x" Nothing' + os.linesep
    + 'drone_y :: Stream Int32' + os.linesep
    + 'drone_y = extern "drone_y" Nothing' + os.linesep
    + 'drone_speed :: Stream Int32' + os.linesep
    + 'drone_speed = extern "drone_speed" Nothing' + os.linesep
    + 'delta_x :: Stream Int32' + os.linesep
    + 'delta_x = extern "delta_x" Nothing' + os.linesep
    + 'delta_y :: Stream Int32' + os.linesep
    + 'delta_y = extern "delta_y" Nothing' + os.linesep
    + os.linesep
    + os.linesep
    + 'moveResult :: (Stream Int32, Stream Int32) -> (Stream Int32, Stream Int32) -> Stream Int32 -> (Stream Int32, Stream Int32)' + os.linesep
    + 'moveResult (x, y) (dx, dy) ds = (x + (ds * dx), y + (ds * dy))' + os.linesep
    + os.linesep
    + 'insideObs :: Stream Int32 -> Stream Int32 -> Stream Word32 -> Stream Bool' + os.linesep
    + 'insideObs x y i = (((obs .!! (2 * i)) - (obs_size .!! i)) <= x) && (x <= (obs .!! (2 * i))) && (((obs .!! ((2 * i) + 1)) - (obs_size .!! (i))) <= y) && (y <= (obs .!! ((2 * i) + 1)))' + os.linesep
    + os.linesep
    + os.linesep
    + 'dangerObs :: (Stream Int32, Stream Int32) -> (Stream Int32, Stream Int32) -> Stream Int32 -> Stream Bool' + os.linesep
    + 'dangerObs (x, y) (dx, dy) ds = (' + ' || '.join([('(insideObs nx ny (constant ' + str(index) + '))') for index in range(NUMBER_OF_OBSTACLES)]) + ')' + os.linesep
    + '  where' + os.linesep
    + '    (nx, ny) = moveResult (x, y) (dx, dy) ds' + os.linesep
    + os.linesep
    + 'spec = do' + os.linesep
    + '  trigger "go_slow" (dangerObs (drone_x, drone_y) (delta_x, delta_y) drone_speed) []' + os.linesep
    + os.linesep
    + '-- Compile the spec' + os.linesep
    + 'main = reify spec >>= compile "collision_monitor"' + os.linesep
)

LIVENESS_POSTAMBLE = (
    'import Copilot.Library.LTL' + os.linesep
    + os.linesep
    + 'current_action :: Stream Int32' + os.linesep
    + 'current_action = extern "current_action" Nothing' + os.linesep
    + os.linesep
    + 'pad :: Stream Int32 -> Int32 -> Stream Bool' + os.linesep
    + 'pad a c = [False, False] ++ (a == (constant c))' + os.linesep
    + os.linesep
    + 'opposingCardinality :: Stream Int32 -> Stream Bool' + os.linesep
    + 'opposingCardinality a = (((pad a 0) && (next (pad a 1))) || ((pad a 1) && (next (pad a 0))) || ((pad a 2) && (next (pad a 3))) || ((pad a 3) && (next (pad a 2))))' + os.linesep
    + os.linesep
    + os.linesep
    + 'spec = do' + os.linesep
    + '  trigger "go_slow" (opposingCardinality current_action) []' + os.linesep
    + os.linesep
    + '-- Compile the spec' + os.linesep
    + 'main = reify spec >>= compile "loop_monitor"' + os.linesep
)

with open(OUTPUT_LOCATION + 'CollisionMonitor.hs', 'w', encoding = 'utf-8') as output_file:
    output_file.write(PREAMBLE + SAFETY_POSTAMBLE)
with open(OUTPUT_LOCATION + 'LoopMonitor.hs', 'w', encoding = 'utf-8') as output_file:
    output_file.write(PREAMBLE + LIVENESS_POSTAMBLE)
