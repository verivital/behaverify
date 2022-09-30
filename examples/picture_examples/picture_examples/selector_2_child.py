import py_trees

def create_root():
    parent = py_trees.composites.Selector('selector', memory = False)
    d1 = py_trees.behaviours.Dummy('child1')
    d2 = py_trees.behaviours.Dummy('child2')
    parent.add_children([d1, d2])
    return parent




