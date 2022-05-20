import py_trees



def create_root():
    root0 = py_trees.composites.Sequence('root0')
    default1 = py_trees.behaviours.Count('default1')
    selector2 = py_trees.composites.Selector('selector2')
    selector3 = py_trees.composites.Selector('selector3')
    default4 = py_trees.behaviours.Count('default4')
    sequence5 = py_trees.composites.Sequence('sequence5')
    sequence6 = py_trees.composites.Sequence('sequence6')
    default7 = py_trees.behaviours.Count('default7')
    default8 = py_trees.behaviours.Count('default8')
    default9 = py_trees.behaviours.Count('default9')
    default10 = py_trees.behaviours.Count('default10')
    default11 = py_trees.behaviours.Count('default11')
    default12 = py_trees.behaviours.Count('default12')
    default13 = py_trees.behaviours.Count('default13')
    default14 = py_trees.behaviours.Count('default14')
    default15 = py_trees.behaviours.Count('default15')
    
    root0.add_children([default1, selector2, selector3, default4])
    selector2.add_children([sequence5, sequence6])
    selector3.add_children([default7, default8, default9])
    sequence5.add_children([default10, default11, default12])
    sequence6.add_children([default13, default14, default15])
    return root0




