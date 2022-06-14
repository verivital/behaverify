import py_trees



    
        

def create_root(print_pic=False):
    sel1 = py_trees.composites.Selector('example_3_sel1')
    seq1 = py_trees.composites.Sequence('seq1')
    d1 = py_trees.behaviours.Dummy('node_z')
    d2 = py_trees.behaviours.Dummy('node_x')
    d3 = py_trees.behaviours.Dummy('node_y')
    d4 = py_trees.behaviours.Dummy('current_node')
    sel1.add_children([d1, seq1])
    seq1.add_children([d2, d3, d4])
    if print_pic:
        py_trees.display.render_dot_tree(sel1, target_directory = '../pictures')#works
    return sel1


