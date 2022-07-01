import py_trees




def create_root(print_pic=False):
    sel1 = py_trees.composites.Selector('wideSel')
    d1 = py_trees.behaviours.Dummy('child1')
    d2 = py_trees.behaviours.Dummy('child2')
    d3 = py_trees.behaviours.Dummy('child3')
    d4 = py_trees.behaviours.Dummy('child4')
    d5 = py_trees.behaviours.Dummy('child5')
    d6 = py_trees.behaviours.Dummy('child6')
    d7 = py_trees.behaviours.Dummy('child7')
    d8 = py_trees.behaviours.Dummy('child8')
    sel1.add_children([d1, d2, d3, d4, d5, d6, d7, d8])
    if print_pic:
        py_trees.display.render_dot_tree(sel1, target_directory = '../pictures')#works
    return sel1


create_root(True)
