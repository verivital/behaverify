import py_trees


def create_root(print_pic=False):
    sel0 = py_trees.composites.Selector('sel0')
    d1 = py_trees.behaviours.Dummy('child1')
    d2 = py_trees.behaviours.Dummy('child2')
    d3 = py_trees.behaviours.Dummy('child3')
    sel0.add_children([d1, d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(sel0, target_directory = '../pictures')#works
    return sel0

create_root(True)
