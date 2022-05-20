import py_trees



def create_root():
    root0 = py_trees.composites.Sequence('root0')
    selector1 = py_trees.composites.Selector('selector1')
    selector2 = py_trees.composites.Selector('selector2')
    check3 = py_trees.behaviours.CheckBlackboardVariableExists('first_var', 'check3')
    set4 = py_trees.behaviours.SetBlackboardVariable('first_var', 3, False, 'set4')
    unset5  = py_trees.behaviours.UnsetBlackboardVariable('first_var', 'unset5')
    
    root0.add_children([selector1, selector2])
    selector1.add_children([check3, set4])
    selector2.add_children([unset5])
    return root0



