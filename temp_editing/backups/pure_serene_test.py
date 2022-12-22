import py_trees

root = py_trees.composites.Parallel(name = 'root')
sel = py_trees.composites.Selector(name = 'sel', memory = False)
seq = py_trees.composites.Sequence(name = 'seq', memory = False)
guard = py_trees.behaviours.Dummy(name = 'guard')
guard1 = py_trees.behaviours.Dummy(name = 'guard1')
action = py_trees.behaviours.Dummy(name = 'action')
action1 = py_trees.behaviours.Dummy(name = 'action1')

dec = py_trees.decorators.RunningIsSuccess(guard, name = 'dec')

root.add_children([sel, seq])
sel.add_children([dec, action])
seq.add_children([guard1, action1])

py_trees.display.render_dot_tree(root)
