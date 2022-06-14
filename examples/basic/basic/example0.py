import py_trees


def create_root(print_pic=False):
    seq1 = py_trees.composites.Sequence('example_0_seq1')
    d1 = py_trees.behaviours.Dummy('node_2')
    d2 = py_trees.behaviours.Dummy('node_3')
    seq1.add_children([d1, d2])
    if print_pic:
        py_trees.display.render_dot_tree(seq1, target_directory = '../pictures')#works
    return seq1
