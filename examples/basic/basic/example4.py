import py_trees



    
        

def create_root(print_pic=False):
    sel1 = py_trees.composites.Selector('example_4_sel1')
    d1 = py_trees.behaviours.Dummy('leaf_1')
    d2 = py_trees.behaviours.Dummy('leaf_2')
    d3 = py_trees.behaviours.Dummy('leaf_3')
    d4 = py_trees.behaviours.Dummy('leaf_4')
    d5 = py_trees.behaviours.Dummy('leaf_5')
    d6 = py_trees.behaviours.Dummy('leaf_6')
    d7 = py_trees.behaviours.Dummy('leaf_7')
    d8 = py_trees.behaviours.Dummy('leaf_8')
    sel1.add_children([d1, d2, d3, d4, d5, d6, d7, d8])
    if print_pic:
        py_trees.display.render_dot_tree(sel1, target_directory = '../pictures')#works
    return sel1


