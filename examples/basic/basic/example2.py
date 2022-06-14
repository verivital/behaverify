import py_trees


def create_root(print_pic=False):
    seq1 = py_trees.composites.Sequence('example_2_seq1')
    seq2 = py_trees.composites.Sequence('seq2')
    d1 = py_trees.behaviours.Dummy('node_z')
    d2 = py_trees.behaviours.Dummy('node_x')
    d3 = py_trees.behaviours.Dummy('node_y')
    d4 = py_trees.behaviours.Dummy('current_node')
    seq1.add_children([d1, seq2])
    seq2.add_children([d2, d3, d4])
    if print_pic:
        py_trees.display.render_dot_tree(seq1, target_directory = '../pictures')#works
    return seq1
