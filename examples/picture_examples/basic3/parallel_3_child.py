import py_trees


def create_root(print_pic=False):
    par0 = py_trees.composites.Parallel('par0')
    d1 = py_trees.behaviours.Dummy('child1')
    d2 = py_trees.behaviours.Dummy('child2')
    d3 = py_trees.behaviours.Dummy('child3')
    par0.add_children([d1, d2, d3])
    if print_pic:
        py_trees.display.render_dot_tree(par0, target_directory = '../pictures')#works
    return par0

create_root(True)
