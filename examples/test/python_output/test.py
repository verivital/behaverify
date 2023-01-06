import guard_file
import action_file
import py_trees


def create_tree():
    root = py_trees.composites.Parallel('root', py_trees.common.ParallelPolicy.SuccessOnAll(False))
    sel = py_trees.composites.Selector('sel', False)
    guard = guard_file.guard('guard')
    dec = py_trees.decorators.RunningIsSuccess(guard, 'dec')
    action = action_file.action('action')
    sel.add_children([dec, action])
    seq = py_trees.composites.Sequence('seq', False)
    guard_1 = guard_file.guard('guard_1')
    action_1 = action_file.action('action_1')
    seq.add_children([guard_1, action_1])
    root.add_children([sel, seq])
    return root
