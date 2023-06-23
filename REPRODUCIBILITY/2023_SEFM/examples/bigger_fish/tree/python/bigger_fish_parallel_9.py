import biggest_fish_is0_file
import biggest_fish_is1_file
import biggest_fish_is2_file
import biggest_fish_is3_file
import biggest_fish_is4_file
import biggest_fish_is5_file
import biggest_fish_is6_file
import biggest_fish_is7_file
import biggest_fish_is8_file
import biggest_fish_is9_file
import bigger_fish_file
import py_trees
import serene_safe_assignment


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'biggest_fish', access = py_trees.common.Access.WRITE)
    blackboard_reader.biggest_fish = serene_safe_assignment.biggest_fish(0)
    return blackboard_reader


def create_tree(environment):
    biggest_fish_is6 = biggest_fish_is6_file.biggest_fish_is6('biggest_fish_is6')
    decorator6 = py_trees.decorators.FailureIsRunning(name = 'decorator6', child = biggest_fish_is6)
    biggest_fish_is7 = biggest_fish_is7_file.biggest_fish_is7('biggest_fish_is7')
    decorator7 = py_trees.decorators.FailureIsRunning(name = 'decorator7', child = biggest_fish_is7)
    biggest_fish_is8 = biggest_fish_is8_file.biggest_fish_is8('biggest_fish_is8')
    decorator8 = py_trees.decorators.FailureIsRunning(name = 'decorator8', child = biggest_fish_is8)
    biggest_fish_is9 = biggest_fish_is9_file.biggest_fish_is9('biggest_fish_is9')
    decorator9 = py_trees.decorators.FailureIsRunning(name = 'decorator9', child = biggest_fish_is9)
    biggest_fish_is2 = biggest_fish_is2_file.biggest_fish_is2('biggest_fish_is2')
    decorator2 = py_trees.decorators.FailureIsRunning(name = 'decorator2', child = biggest_fish_is2)
    biggest_fish_is3 = biggest_fish_is3_file.biggest_fish_is3('biggest_fish_is3')
    decorator3 = py_trees.decorators.FailureIsRunning(name = 'decorator3', child = biggest_fish_is3)
    biggest_fish_is4 = biggest_fish_is4_file.biggest_fish_is4('biggest_fish_is4')
    decorator4 = py_trees.decorators.FailureIsRunning(name = 'decorator4', child = biggest_fish_is4)
    biggest_fish_is5 = biggest_fish_is5_file.biggest_fish_is5('biggest_fish_is5')
    decorator5 = py_trees.decorators.FailureIsRunning(name = 'decorator5', child = biggest_fish_is5)
    biggest_fish_is0 = biggest_fish_is0_file.biggest_fish_is0('biggest_fish_is0')
    decorator0 = py_trees.decorators.FailureIsRunning(name = 'decorator0', child = biggest_fish_is0)
    biggest_fish_is1 = biggest_fish_is1_file.biggest_fish_is1('biggest_fish_is1')
    decorator1 = py_trees.decorators.FailureIsRunning(name = 'decorator1', child = biggest_fish_is1)
    parallel1 = py_trees.composites.Parallel(name = 'parallel1', policy = py_trees.common.ParallelPolicy.SuccessOnOne(), children = [decorator0, decorator1])
    parallel5 = py_trees.composites.Parallel(name = 'parallel5', policy = py_trees.common.ParallelPolicy.SuccessOnOne(), children = [decorator2, decorator3, decorator4, decorator5, parallel1])
    parallel9 = py_trees.composites.Parallel(name = 'parallel9', policy = py_trees.common.ParallelPolicy.SuccessOnOne(), children = [decorator6, decorator7, decorator8, decorator9, parallel5])
    special_decorator = py_trees.decorators.RunningIsFailure(name = 'special_decorator', child = parallel9)
    bigger_fish = bigger_fish_file.bigger_fish('bigger_fish', environment)
    biggest_fish_sequence = py_trees.composites.Sequence(name = 'biggest_fish_sequence', memory = False, children = [special_decorator, bigger_fish])
    return biggest_fish_sequence
