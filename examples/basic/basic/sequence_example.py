import py_trees



def create_root():
    root0 = py_trees.composites.Sequence('root0')
    c1 = py_trees.behaviours.SuccessEveryN('c1', 2)
    c2 = py_trees.behaviours.SuccessEveryN('c2', 3)
    
    root0.add_children([c1, c2])
    return root0



